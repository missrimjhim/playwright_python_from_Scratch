import os
import platform
from pathlib import Path
import pytest
import allure
from playwright.sync_api import sync_playwright
from utils.execution_logger import ExecutionLogger


# -------------------------------
# Register pytest.ini keys
# -------------------------------
def pytest_addoption(parser):
    parser.addini("env", "Test environment")
    parser.addini("browser", "Browser name")
    parser.addini("base_url", "Application URL")


# -------------------------------
# Test start – initialize logger
# -------------------------------
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_call(item):
    config = item.config

    ExecutionLogger.start(
        item.name,
        config.getini("env"),
        config.getini("browser"),
        config.getini("base_url")
    )
    yield


# -------------------------------
# Test end – capture status
# -------------------------------
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    result = outcome.get_result()

    if result.when == "call":
        status = "PASS" if result.passed else "FAIL"
        ExecutionLogger.end(status)

        # Screenshot on failure
        if result.failed:
            page = item.funcargs.get("page")
            if page:
                screenshot = page.screenshot()
                allure.attach(
                    screenshot,
                    name="Failure Screenshot",
                    attachment_type=allure.attachment_type.PNG
                )


# -------------------------------
# Playwright Browser Fixture
# -------------------------------
@pytest.fixture(scope="function")
def browser_context(request):
    config = request.config

    with sync_playwright() as p:
        browser_name = config.getini("browser").lower()

        if browser_name == "chromium":
            browser = p.chromium.launch(headless=False)
        elif browser_name == "firefox":
            browser = p.firefox.launch(headless=False)
        elif browser_name == "webkit":
            browser = p.webkit.launch(headless=False)
        else:
            raise ValueError(f"Invalid browser in pytest.ini: {browser_name}")

        context = browser.new_context(record_video_dir="allure-results/videos")
        yield context

        context.close()
        browser.close()


# -------------------------------
# Page Fixture
# -------------------------------
@pytest.fixture
def page(browser_context, request):
    config = request.config
    page = browser_context.new_page()

    base_url = config.getini("base_url")
    page.goto(base_url)

    yield page

    page.close()


def pytest_sessionstart(session):
    results_dir = session.config.option.allure_report_dir
    if results_dir:
        os.makedirs(results_dir, exist_ok=True)

    with open(os.path.join(results_dir, "environment.properties"), "w") as f:
        f.write(f"Environment={session.config.getini('env')}\n")
        f.write(f"Browser={session.config.getini('browser')}\n")
        f.write(f"BaseURL={session.config.getini('base_url')}\n")
        f.write(f"OS={platform.system()} {platform.release()}\n")
        f.write(f"Python={platform.python_version()}\n")