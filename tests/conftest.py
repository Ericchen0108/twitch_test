import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import os
import platform


@pytest.fixture(scope="session")
def mobile_driver():
    """Chrome mobile emulator setup"""
    chrome_options = Options()
    
    # Mobile emulation
    mobile_emulation = {"deviceName": "iPhone 12 Pro"}
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    
    # Chrome settings
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    
    # Check for local ChromeDriver
    system = platform.system()
    if system == "Darwin":  # macOS
        chromedriver_path = "./drivers/chromedriver-mac-arm64/chromedriver"
    elif system == "Linux":
        chromedriver_path = "./drivers/chromedriver-linux64/chromedriver"
        chrome_options.add_argument("--headless")  # Linux headless mode
    else:
        chromedriver_path = "./drivers/chromedriver-win32/chromedriver.exe"
    
    # Start browser
    if os.path.exists(chromedriver_path):
        service = Service(chromedriver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
    else:
        print("Using ChromeDriver from system PATH")
        driver = webdriver.Chrome(options=chrome_options)
    
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


@pytest.fixture(scope="session", autouse=True)
def setup_screenshots_dir():
    """Create screenshots directory"""
    screenshots_dir = "screenshots"
    os.makedirs(screenshots_dir, exist_ok=True)
    return screenshots_dir


def pytest_configure(config):
    """pytest configuration"""
    os.makedirs("reports", exist_ok=True)


def pytest_html_report_title(report):
    """设置HTML报告标题"""
    report.title = "Twitch移动端自动化测试报告" 