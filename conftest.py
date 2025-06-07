import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import os
import platform


@pytest.fixture(scope="session")
def mobile_driver():
    """Setup Chrome mobile emulator driver"""
    chrome_options = Options()
    
    # Mobile device emulation
    mobile_emulation = {"deviceName": "iPhone 12 Pro"}
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    
    # Chrome options for better compatibility
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Special handling for M1/M2 Macs
    if platform.system() == "Darwin" and platform.machine() == "arm64":
        chrome_options.add_argument("--disable-features=VizDisplayCompositor")
    
    # ChromeDriver setup
    chromedriver_path = "./chromedriver-mac-arm64/chromedriver"
    if os.path.exists(chromedriver_path):
        print(f"Using local ChromeDriver: {chromedriver_path}")
        service = Service(chromedriver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
    else:
        print("Local ChromeDriver not found, using system default")
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