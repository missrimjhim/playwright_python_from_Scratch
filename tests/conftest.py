import base64
from pathlib import Path
import pytest
from playwright.sync_api import sync_playwright
from utils.execution_logger import ExecutionLogger


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    if config.pluginmanager.hasplugin("html"):
        config._html = config.pluginmanager.getplugin("html")
    else:
        config._html = None


# -------------------------------
# Register pytest.ini keys
# -------------------------------
def pytest_addoption(parser):
    parser.addini("env", "Test environment")
    parser.addini("browser", "Browser name")
    parser.addini("base_url", "Application URL")


# -------------------------------
# Execution Logger
# -------------------------------
def pytest_sessionstart(session):
    ExecutionLogger.pytest_config = session.config
    ExecutionLogger.init()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call(item):
    config = item.config
    ExecutionLogger.start(
        item.name,
        config.getini("env"),
        config.getini("browser"),
        config.getini("base_url")
    )
    yield


def pytest_runtest_makereport(item, call):
    if call.when == "call":
        status = "PASS" if call.excinfo is None else "FAIL"
        ExecutionLogger.end(status)


def pytest_sessionfinish(session, exitstatus):
    ExecutionLogger.save()


# -------------------------------
# Playwright browser
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

        context = browser.new_context()
        yield context
        context.close()
        browser.close()


# -------------------------------
# Page fixture
# -------------------------------
@pytest.fixture
def page(browser_context, request):
    config = request.config
    page = browser_context.new_page()
    page.goto(config.getini("base_url"))
    yield page
    page.close()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    result = outcome.get_result()
    if result.when == "call":
        pytest_html = item.config._html
        if pytest_html:
            steps_html = "<br>".join(ExecutionLogger.steps)

            html = f"""
                    <div style="font-family: monospace;">
                        <b>Execution Log</b><br>
                        {steps_html}
                    </div>
                    """

            extra = getattr(result, "extra", [])
            extra.append(pytest_html.extras.html(html))
            result.extra = extra

        status = "PASS" if call.excinfo is None else "FAIL"
        ExecutionLogger.end(status)

    if result.when == "call" and result.failed:
        page = item.funcargs.get("page")

        if page:
            project_root = Path(__file__).parent.parent
            screenshots_dir = project_root / "screenshots"
            screenshots_dir.mkdir(exist_ok=True)

            screenshot_path = screenshots_dir / f"{item.name}.png"
            page.screenshot(path=str(screenshot_path))

            # Convert to base64 for pytest-html
            with open(screenshot_path, "rb") as img:
                encoded = base64.b64encode(img.read()).decode("utf-8")

            html = f'''
                        <a href="data:image/png;base64,{encoded}" target="_blank">
                            <img src="data:image/png;base64,{encoded}" 
                                 style="width:300px; border:1px solid #ccc"/>
                        </a>
                        '''

            pytest_html = item.config._html
            if pytest_html:
                steps_html = "<br>".join(ExecutionLogger.steps)

                html_1 = f"""
                            <div style="font-family: monospace;">
                                <b>Execution Log</b><br>
                                {steps_html}
                            </div>
                            """
                extra = getattr(result, "extra", [])
                extra.append(pytest_html.extras.html(html_1))
                extra.append(pytest_html.extras.html(html))
                result.extra = extra
