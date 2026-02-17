from playwright.sync_api import Page, expect
from utils.html_logger import HTMLLogger



class LoginPage:
    def __init__(self, page : Page, logger: HTMLLogger):
        self.page = page
        self.logger = logger
        # Locators
        self.register_link = page.get_by_role("link", name="Register")
        self.firstname_input = page.locator("input#FirstName")
        self.lastname_input = page.locator("input#LastName")
        self.password_input = page.locator("input#Password")
        self.confirmed_password_input = page.locator("input#ConfirmPassword")
        self.email_input = page.locator("input#Email")
        self.login_button = page.get_by_role("button", name="Register")
        self.continue_button = page.get_by_role("button", name="Continue")

    def register_first_time(self, firstname, lastname, password, email):
        self.register_link.click()
        self.logger.step(f"Entering firstname: {firstname}")
        self.firstname_input.fill(firstname)
        self.logger.step(f"Entering lastname: {lastname}")
        self.lastname_input.fill(lastname)
        self.logger.step(f"Entering email: {email}")
        self.email_input.fill(email)
        self.logger.step("Entering password:")
        self.password_input.fill(password)
        self.logger.step("Entering confirmed password:")
        self.confirmed_password_input.fill(password)
        self.logger.step("Click the login button")
        self.login_button.click()

    def validate_registration(self):
        try:
            expect(self.page.locator("div.result")).to_contain_text("Your registration completed")
            self.logger.verify("Login successful — dashboard visible")
            self.continue_button.click()
            expect(self.page).to_have_title("Demo Web Shop")
            expect(self.page.locator("a.account", has_text=".com")).to_contain_text(".com")
        except Exception:
            self.logger.error("Login failed — dashboard not found")
            raise


