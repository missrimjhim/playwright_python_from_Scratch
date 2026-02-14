from playwright.sync_api import sync_playwright
def test_open_google():
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=False)

        # open browser
        page=browser.new_page()
        # open url
        page.goto("https://google.com")
        # assert
        assert "Google" in page.title()
        browser.close()