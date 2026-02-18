from playwright.sync_api import Page, expect
from utils.execution_logger import ExecutionLogger



class LoginPage:
    def __init__(self, page: Page):
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

    def register_first_time(self, firstname, lastname, password, email):
        self.register_link.click()
        ExecutionLogger.log(f"Entering firstname: {firstname}")
        self.firstname_input.fill(firstname)
        ExecutionLogger.log(f"Entering lastname: {lastname}")
        self.lastname_input.fill(lastname)
        ExecutionLogger.log(f"Entering email: {email}")
        self.email_input.fill(email)
        ExecutionLogger.log("Entering password:")
        self.password_input.fill(password)
        ExecutionLogger.log("Entering confirmed password:")
        self.confirmed_password_input.fill(password)
        ExecutionLogger.log("Click the login button")
        self.login_button.click()

    def validate_registration(self):
        try:
            expect(self.page.locator("div.result")).to_contain_text("Your registration completed")
            ExecutionLogger.html_logger.verify("Login successful — dashboard visible")
            self.continue_button.click()
            expect(self.page).to_have_title("Demo Web Shop")
            expect(self.page.locator("a.account", has_text=".com")).to_contain_text(".com")
        except Exception:
            ExecutionLogger.html_logger.error("Login failed — dashboard not found")
            raise


