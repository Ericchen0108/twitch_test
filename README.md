# Twitch Mobile Automation Framework

A scalable and maintainable automation framework for testing Twitch mobile web application using Selenium and pytest.

## Features

- Mobile device emulation (iPhone 12 Pro)
- Framework-based design for scalability
- Automated screenshot capture
- Cross-platform compatibility
- Clean test reporting

## Prerequisites

- Python 3.9+
- Chrome browser
- ChromeDriver (included for macOS ARM64)

## Setup

1. Clone the repository:

```bash
git clone <repository-url>
cd opennet
```

2. Create virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running Tests

### Basic Test Execution

```bash
# Run all tests
python -m pytest test_twitch_mobile.py -v

# Run with live output
python -m pytest test_twitch_mobile.py -v -s

# Generate HTML report
python -m pytest test_twitch_mobile.py -v --html=reports/report.html --self-contained-html
```

### Test Workflow

The test performs the following actions:

1. Navigate to Twitch homepage
2. Search for "StarCraft II"
3. Scroll page twice to load content
4. Randomly select a streamer
5. Wait for page to load completely
6. Take screenshot

## Framework Structure

```
opennet/
├── test_twitch_mobile.py      # Main test file with framework
├── conftest.py                # pytest configuration and fixtures
├── requirements.txt           # Python dependencies
├── screenshots/               # Test screenshots (auto-generated)
├── reports/                   # Test reports (auto-generated)
└── chromedriver-mac-arm64/    # ChromeDriver for macOS ARM64
```

## Framework Design

### TwitchMobileAutomation Class

Core automation framework with reusable methods:

- `navigate_to_homepage()` - Navigate to Twitch
- `search_for_game(game_name)` - Search functionality
- `scroll_page(times)` - Page scrolling
- `select_random_streamer()` - Random streamer selection
- `wait_for_page_load()` - Page load waiting
- `take_screenshot(suffix)` - Screenshot capture

### TestTwitchMobile Class

Test implementation using the framework:

- `test_search_and_screenshot_workflow()` - Complete test workflow

## Configuration

### Mobile Device Emulation

Configured in `conftest.py` to emulate iPhone 12 Pro.

### Screenshot Storage

Screenshots are automatically saved to `screenshots/` directory with timestamp.

### Test Reports

HTML reports are generated in `reports/` directory when using `--html` option.

## Troubleshooting

### ChromeDriver Issues

- For macOS ARM64: ChromeDriver is included in the project
- For other platforms: Ensure ChromeDriver is in PATH or update `conftest.py`

### Test Failures

- Check `screenshots/` for error screenshots
- Review test reports in `reports/` directory
- Ensure stable internet connection

## Contributing

1. Follow the framework pattern for new tests
2. Keep methods focused and reusable
3. Add appropriate error handling
4. Include screenshot capture on failures

## License

MIT License - see LICENSE file for details.
