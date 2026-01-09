"""
============================================================
 conftest.py — Project FLAIR
============================================================

PURPOSE
-------
Central test configuration for Project FLAIR UI automation.

This file is responsible for:
- Creating and closing the Selenium WebDriver
- Handling browser configuration (headless / downloads)
- Providing shared fixtures used by all tests
- Capturing screenshots on test failure
- Generating HTML test reports

IMPORTANT RULES
---------------
- DO NOT create WebDriver instances inside test files
- DO NOT hardcode URLs in tests
- ALWAYS use the `driver` fixture
"""

from __future__ import annotations

import os
import pytest
from datetime import datetime
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from config.settings import (
    DEFAULT_BASE_URL,
    DEFAULT_HEADLESS,
)

# ============================================================
# PROJECT FOLDERS
# ============================================================

PROJECT_ROOT = Path.cwd()
DOWNLOADS_DIR = PROJECT_ROOT / "downloads"
SCREENSHOTS_DIR = PROJECT_ROOT / "screenshots"
REPORTS_DIR = PROJECT_ROOT / "reports"

DOWNLOADS_DIR.mkdir(exist_ok=True)
SCREENSHOTS_DIR.mkdir(exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)

# ============================================================
# FIXTURES
# ============================================================

@pytest.fixture(scope="session")
def base_url() -> str:
    """
    Base URL for Project FLAIR.

    Tests must NEVER hardcode URLs.
    """
    if not DEFAULT_BASE_URL:
        raise ValueError("BASE_URL is not set in config/settings.py")
    return DEFAULT_BASE_URL


@pytest.fixture(scope="function")
def driver() -> webdriver.Chrome:
    """
    Selenium WebDriver fixture (Chrome).

    - Fresh browser per test
    - Prevents state leakage between FLAIR tests
    - Automatically closes after test
    """

    options = Options()

    if DEFAULT_HEADLESS:
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")

    # Auto-download configuration (needed for Export POS, reports, etc.)
    prefs = {
        "download.default_directory": str(DOWNLOADS_DIR),
        "download.prompt_for_download": False,
        "safebrowsing.enabled": True,
    }
    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=options)
    driver.maximize_window()

    yield driver

    driver.quit()


@pytest.fixture(scope="session")
def download_dir() -> str:
    """
    Expose download directory to tests.
    """
    return str(DOWNLOADS_DIR)

# ============================================================
# SCREENSHOT ON FAILURE (QA EVIDENCE)
# ============================================================

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Capture screenshot automatically when a test FAILS.

    Screenshots are saved to:
    /screenshots/<testname>_<timestamp>.png
    """
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver")
        if not driver:
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{item.name}_{timestamp}.png"
        filepath = SCREENSHOTS_DIR / filename

        driver.save_screenshot(str(filepath))

# ============================================================
# HTML REPORT CONFIGURATION
# ============================================================

def pytest_configure(config):
    """
    Configure HTML report output for each test run.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = REPORTS_DIR / f"flair_test_report_{timestamp}.html"
    config.option.htmlpath = str(report_file)
