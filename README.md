# Twitch Mobile Test Automation

This is a Selenium automation project that tests Twitch's mobile website. It searches for StarCraft II streams, picks a random streamer, and takes a screenshot.

## Project Structure

```
twitch_test/
├── twitch_mobile/
│   ├── __init__.py
│   └── automation.py        # Main automation logic
├── tests/
│   ├── conftest.py         # pytest fixtures and config
│   └── test_twitch_mobile.py
├── drivers/                # Put ChromeDriver here
├── screenshots/            # Screenshots end up here
├── reports/                # HTML reports
└── requirements.txt
```

## Requirements

You'll need:

- Python 3.9+
- Chrome browser
- ChromeDriver (matching your Chrome version)

Check your Python version first:

```bash
python3 --version
```

## Setup

Clone the repo and set up a virtual environment:

```bash
git clone <your-repo-url>
cd twitch_test

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip3 install -r requirements.txt
```

### ChromeDriver Setup

You have two options:

**Option 1 (recommended):** Download ChromeDriver manually

1. Check your Chrome version (Chrome → Help → About Google Chrome)
2. Download matching version from https://chromedriver.chromium.org/downloads
3. Extract it to the `drivers/` folder:
   - macOS: `drivers/chromedriver-mac-arm64/chromedriver`
   - Linux: `drivers/chromedriver-linux64/chromedriver`
   - Windows: `drivers/chromedriver-win32/chromedriver.exe`

**Option 2:** Let webdriver-manager handle it automatically (already included in requirements.txt)

## Running the Test

```bash
python3 -m pytest tests/test_twitch_mobile.py -v
```

For HTML reports:

```bash
python3 -m pytest tests/test_twitch_mobile.py -v --html=reports/report.html --self-contained-html
```

## What it does

The test workflow:

1. Goes to Twitch homepage
2. Searches for "StarCraft II"
3. Scrolls down twice to load more streams
4. Randomly picks a streamer
5. Waits for the stream page to load
6. Takes a screenshot (saved to `screenshots/` folder)

## Notes

- Uses iPhone 12 Pro mobile emulation
- Sometimes Twitch takes a while to load - the waits should handle this
- If no streamers are found, try running when more people are streaming
- The test is designed to be reasonably robust, but web scraping can be flaky due to network issues or site changes

If you get permission errors on macOS/Linux, make the driver executable:

```bash
chmod +x drivers/chromedriver-mac-arm64/chromedriver
```

## Dependencies

- `selenium` - browser automation
- `pytest` - test framework
- `pytest-html` - generates nice HTML reports
- `webdriver-manager` - backup ChromeDriver management
