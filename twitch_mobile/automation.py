import time
import os
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class TwitchMobileAutomation:
    """Core automation framework for Twitch mobile web"""

    def __init__(self, driver):
        self.driver = driver
        self.screenshots_dir = "screenshots"
        os.makedirs(self.screenshots_dir, exist_ok=True)

    def navigate_to_homepage(self):
        """Navigate to Twitch homepage"""
        self.driver.get("https://www.twitch.tv")
        self.wait_for_page_load()

    def search_for_game(self, game_name):
        """Search for a game on Twitch"""
        try:
            # Click browse button
            browse_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[text()='瀏覽']"))
            )
            browse_button.click()

            # Click search box
            search_box = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='search']"))
            )
            search_box.clear()
            search_box.send_keys(game_name)
        
            # Wait for search suggestions to appear
            time.sleep(2)
            
            # Click the first search result (StarCraft II category)
            first_result = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "ul li:first-child a.tw-link"))
            )
            first_result.click()

            # Wait for page to load
            self.wait_for_page_load()

        except (TimeoutException, NoSuchElementException) as e:
            self.take_screenshot(suffix="search_failed")
            print(f"Search failed: {e}")
            raise

    def scroll_page(self, times=2):
        """Scroll page specified number of times"""
        for i in range(times):
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )
            time.sleep(2)  # Wait for content to load

    def select_random_streamer(self):
        """Select a random streamer from search results"""
        try:
            # Find all streamer elements
            streamers = self.driver.find_elements(
                By.CSS_SELECTOR, "div[role='list'] > div"
            )
            if not streamers:
                raise NoSuchElementException("No streamers found")

            # Pick random one
            import random
            streamer = random.choice(streamers)
            self.driver.execute_script("arguments[0].scrollIntoView();", streamer)
            time.sleep(1)

            # Try clicking title first, then preview if that fails
            try:
                title_link = streamer.find_element(By.CSS_SELECTOR, "button.tw-link")
                self.driver.execute_script("arguments[0].click();", title_link)
            except NoSuchElementException:
                preview = streamer.find_element(By.CSS_SELECTOR, "div[role='img']")
                self.driver.execute_script("arguments[0].click();", preview)

        except Exception as e:
            self.take_screenshot(suffix="streamer_select_failed")
            print(f"Streamer selection failed: {e}")
            raise

    def wait_for_page_load(self, timeout=10):
        """Wait for page to load completely"""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script("return document.readyState")
                == "complete"
            )
        except TimeoutException:
            print("Page load timeout")

    def is_video_player_visible(self, timeout=10):
        """Check if video player is visible on page"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "video"))
            )
            return True
        except TimeoutException:
            return False

    def take_screenshot(self, suffix=""):
        """Take screenshot with timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{suffix}.png" if suffix else f"{timestamp}.png"
        filepath = os.path.join(self.screenshots_dir, filename)
        self.driver.save_screenshot(filepath)
        print(f"Screenshot saved: {filepath}")
        return filepath

    def wait_for_streamer_page_load(self, timeout=20):
        """Wait for streamer page to load completely including video stream"""
        try:
            # Wait for basic page to be ready
            self.wait_for_page_load(timeout=10)
            
            # Wait for video element to be present
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "video"))
            )
            
            # Check if video is loading/playing
            WebDriverWait(self.driver, 15).until(
                lambda driver: driver.execute_script("""
                    var video = document.querySelector('video');
                    if (!video) return false;
                    return video.readyState >= 2 || 
                           video.currentTime > 0 || 
                           !video.paused ||
                           video.videoWidth > 0;
                """)
            )
            
            # Wait for chat (optional)
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "[data-a-target='chat-input']"))
                )
            except TimeoutException:
                pass  # Mobile might not have chat visible
            
            # Additional wait for stream to stabilize
            time.sleep(2)
            
            return True
        except TimeoutException:
            # Continue even if video not fully ready, page might still be valid
            print("Stream page might not be fully loaded, but continuing")
            return False 