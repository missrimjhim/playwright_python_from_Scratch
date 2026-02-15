from playwright.sync_api import Page, expect
import pytest_html


class LoginPage:
    def __init__(self, page : Page):
        self.page = page
        # Locators
        self.register_link = page.get_by_role("link", name="Register")
        self.firstname_input = page.locator("input#FirstName")
        self.lastname_input = page.locator("input#LastName")
        self.password_input = page.locator("input#Password")
        self.confirmed_password_input = page.locator("input#ConfirmPassword")
        self.email_input = page.locator("input#Email")
        self.login_button = page.get_by_role("button", name="Register")
        self.continue_button = page.get_by_role("button", name="Continue")

    def register_first_time(self, firstname, lastname, password, email,extra):
        self.register_link.click()
        self.firstname_input.fill(firstname)
        self.lastname_input.fill(lastname)
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.confirmed_password_input.fill(password)
        self.login_button.click()

    def validate_registration(self):
        expect(self.page.locator("div.result")).to_contain_text("Your registration completed")
        self.continue_button.click()
        expect(self.page).to_have_title("Demo Web Shop")
        expect(self.page.locator("a.account", has_text=".com")).to_contain_text(".com")


