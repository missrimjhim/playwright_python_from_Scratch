import pytest
import pytest_html.extras
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="function")
def browser_context():
    with (sync_playwright() as p):
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://demowebshop.tricentis.com/")
        yield page
        context.close()
        browser.close()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Let pytest and other hooks run, and get the report
    outcome = yield
    result = outcome.get_result()

    page = None
    screenshot_path = None

    # Only act on failures in the 'call' phase (the actual test body)
    if result.failed and result.when == call:
        page = item.funcargs.get("page", None)

        if page:
            screenshot_path = f"screenshots/{item.name}.png"
            page.screenshot(path=screenshot_path)

    # Attach screenshot to HTML report if available
    if screenshot_path and hasattr(item, "extra"):
        item.extra.append(pytest_html.extras.image(screenshot_path))

