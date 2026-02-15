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

        browser = p.chromium.launch(headless=False, slow_mo=1000)

        page = browser.new_page()

        page.goto("https://demowebshop.tricentis.com/")

        page.get_by_role("link", name="Register").click()

        expect(page.locator(".page-title")).to_have_text("Register")

        page.get_by_label("Female").check()

        page.locator("input#FirstName").fill("Arpitaa")

        page.locator("input#LastName").fill("Chowdhuryy")

        page.locator("input#Email").fill("abc@gmail9.com")

        page.locator("input#Password").fill("Abc@12349")

        page.locator("input#ConfirmPassword").fill("Abc@12349")

        page.get_by_role("button", name="Register").click()

        expect(page.locator("div.result")).to_contain_text("Your registration completed")

        page.get_by_role("button", name="Continue").click()