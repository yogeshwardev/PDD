"""
conftest.py – Shared fixtures for all Selenium E2E tests
Smart Admission Web App (GitHub Pages)
"""

import os
import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait

# ─── Environment ─────────────────────────────────────────────────────────────
BASE_URL = os.environ.get(
    "BASE_URL", "https://dinesh-2005d.github.io/Smart_Admission/"
).rstrip("/") + "/"

HEADLESS = os.environ.get("HEADLESS", "true").lower() == "true"
SCREENSHOTS_DIR = os.environ.get("SCREENSHOTS_DIR", "../Test Results/Screenshots")
IMPLICIT_WAIT = int(os.environ.get("IMPLICIT_WAIT", "10"))
PAGE_LOAD_TIMEOUT = int(os.environ.get("PAGE_LOAD_TIMEOUT", "30"))


# ─── Chrome Options ───────────────────────────────────────────────────────────
def get_chrome_options():
    opts = Options()
    if HEADLESS:
        opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--window-size=1366,768")
    opts.add_argument("--disable-extensions")
    opts.add_argument("--disable-infobars")
    opts.add_argument("--disable-notifications")
    opts.add_argument("--log-level=3")
    opts.add_argument("--remote-debugging-port=9222")
    # Stable User-Agent for React Native Web
    opts.add_argument(
        "--user-agent=Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
    return opts


# ─── Fixtures ─────────────────────────────────────────────────────────────────
@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture(scope="function")
def driver(request):
    """Create a Chrome WebDriver instance for each test."""
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

    opts = get_chrome_options()
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        service = Service(ChromeDriverManager().install())
        drv = webdriver.Chrome(service=service, options=opts)
    except Exception:
        # Fallback: let Selenium manage chromedriver automatically
        drv = webdriver.Chrome(options=opts)

    drv.implicitly_wait(IMPLICIT_WAIT)
    drv.set_page_load_timeout(PAGE_LOAD_TIMEOUT)

    yield drv

    # Take screenshot on failure
    if request.node.rep_call.failed if hasattr(request.node, "rep_call") else False:
        _capture_failure_screenshot(drv, request.node.name)

    drv.quit()


@pytest.fixture(scope="function")
def wait(driver):
    return WebDriverWait(driver, 20)


@pytest.fixture(scope="function")
def app(driver, base_url):
    """Navigate to the app and wait for it to load."""
    driver.get(base_url)
    time.sleep(5)  # Allow React Native Web to hydrate (needs more time on CI)
    return driver


# ─── Hooks ────────────────────────────────────────────────────────────────────
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)

    if rep.when == "call" and rep.failed:
        driver_fixture = item.funcargs.get("driver")
        if driver_fixture:
            _capture_failure_screenshot(driver_fixture, item.name)


def _capture_failure_screenshot(driver, test_name):
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    ts = time.strftime("%Y%m%d_%H%M%S")
    safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in test_name)
    path = os.path.join(SCREENSHOTS_DIR, f"FAIL_{safe_name}_{ts}.png")
    try:
        driver.save_screenshot(path)
        print(f"\n📸 Screenshot saved: {path}")
    except Exception as e:
        print(f"\n⚠️  Could not save screenshot: {e}")


# ─── CLI option for base_url ──────────────────────────────────────────────────
def pytest_addoption(parser):
    parser.addoption(
        "--base-url",
        action="store",
        default=BASE_URL,
        help="Base URL of the deployed app",
    )


def pytest_configure(config):
    global BASE_URL
    try:
        url = config.getoption("--base-url")
        if url:
            BASE_URL = url.rstrip("/") + "/"
    except (ValueError, AttributeError):
        pass
