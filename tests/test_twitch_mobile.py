from twitch_mobile.automation import TwitchMobileAutomation


class TestTwitchMobile:
    
    def test_twitch_mobile_workflow(self, mobile_driver):
        """
        Complete test workflow:
        1. Navigate to Twitch homepage
        2. Search for StarCraft II
        3. Scroll page twice
        4. Randomly select a streamer
        5. Wait for stream page to load
        6. Take screenshot
        """
        twitch = TwitchMobileAutomation(mobile_driver)
        
        # Go to homepage
        twitch.navigate_to_homepage()
        
        # Search for game
        twitch.search_for_game("StarCraft II")
        
        # Scroll to load more content
        twitch.scroll_page(times=2)
        
        # Select streamer
        twitch.select_random_streamer()
        
        # Wait for page to load
        twitch.wait_for_streamer_page_load()
        
        # Take final screenshot
        twitch.take_screenshot()
        
        print("Test completed!") 