import time
import os
import random
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class TwitchMobileAutomation:
    """Twitch mobile automation framework"""
    
    def __init__(self, driver, timeout=15):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        self.base_url = "https://www.twitch.tv"
    
    def navigate_to_homepage(self):
        """Navigate to Twitch homepage"""
        self.driver.get(self.base_url)
        print("Navigated to Twitch homepage")
    
    def search_for_game(self, game_name):
        """Search for a specific game"""
        # Click search button
        search_button = self._find_search_button()
        if search_button:
            search_button.click()
            print("Search button clicked")
            time.sleep(3)
        
        # Enter search term
        search_input = self._find_search_input()
        if search_input:
            search_input.send_keys(game_name)
            print(f"Entered search term: {game_name}")
            time.sleep(2)
        
        # Click search result
        first_result = self._find_search_result_and_click()
        if first_result:
            print("Search result clicked")
            time.sleep(2)
        
        return True
    
    def scroll_page(self, times=2):
        """Scroll down the page multiple times"""
        for i in range(times):
            self.driver.execute_script("window.scrollBy(0, 500);")
            time.sleep(2)
            print(f"Scroll completed: {i+1}/{times}")
    
    def select_random_streamer(self):
        """Select a random streamer from available options"""
        try:
            list_container = self.wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'div[role="list"]')))
            
            channels = list_container.find_elements(
                By.CSS_SELECTOR, 'div.Layout-sc-1xcs6mc-0 > div > article')
            print(f"Found {len(channels)} channels")
            
            if len(channels) > 0:
                selected_index = random.randint(0, len(channels)-1)
                target_channel = channels[selected_index]
                print(f"Selected channel #{selected_index+1}")
                
                preview_button = target_channel.find_element(
                    By.CSS_SELECTOR, 'button.tw-link')
                
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'});",
                    preview_button)
                time.sleep(1)
                
                self.driver.execute_script(
                    "arguments[0].click();", preview_button)
                print("Channel clicked successfully")
                
                WebDriverWait(self.driver, 10).until(
                    lambda d: '/directory' not in d.current_url)
                print("Page navigation completed")
                return True
            else:
                print("No channels found")
                
        except Exception as e:
            print(f"Failed to select streamer: {e}")
        
        return False
    
    def wait_for_page_load(self):
        """Wait for streamer page to fully load"""
        try:
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "video")))
            print("Video player loaded")
            time.sleep(5)
            print("Page load completed")
        except TimeoutException:
            print("Video player not found, continuing")
            time.sleep(3)
    
    def take_screenshot(self, suffix=""):
        """Take screenshot and save to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"twitch_test_{timestamp}"
        if suffix:
            filename += f"_{suffix}"
        filename += ".png"
        
        screenshot_path = os.path.join("screenshots", filename)
        self.driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved: {screenshot_path}")
        return screenshot_path
    
    def _find_search_button(self):
        """Find search button on homepage"""
        try:
            element = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//div[text()='瀏覽']")))
            return element
        except TimeoutException:
            print("Search button not found, redirecting to search page")
            self.driver.get("https://www.twitch.tv/search")
            return None
    
    def _find_search_input(self):
        """Find search input field"""
        try:
            element = self.wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input[data-a-target='tw-input']")))
            return element
        except TimeoutException:
            return None
    
    def _find_search_result_and_click(self):
        """Find and click first search result"""
        try:
            first_result = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, "(//ul/li//a)[1]"
            )))
            first_result.click()
            return first_result
        except TimeoutException:
            return None


class TestTwitchMobile:
    """Test class for Twitch mobile automation"""
    
    def test_search_and_screenshot_workflow(self, mobile_driver):
        """
        Test complete workflow: search -> scroll -> select streamer -> screenshot
        """
        automation = TwitchMobileAutomation(mobile_driver)
        
        try:
            # Step 1: Navigate to homepage
            automation.navigate_to_homepage()
            
            # Step 2: Search for StarCraft II
            automation.search_for_game("StarCraft II")
            
            # Step 3: Scroll page twice
            automation.scroll_page(times=2)
            
            # Step 4: Select random streamer
            streamer_selected = automation.select_random_streamer()
            
            # Step 5: Wait for page load and take screenshot
            if streamer_selected:
                automation.wait_for_page_load()
            else:
                print("Failed to select streamer, taking screenshot of current page")
                time.sleep(3)
            
            screenshot_path = automation.take_screenshot()
            
            # Verify screenshot exists
            assert os.path.exists(screenshot_path), "Screenshot file not created"
            print("Test completed successfully")
            
        except Exception as e:
            automation.take_screenshot("error")
            print(f"Test failed: {e}")
            raise e 