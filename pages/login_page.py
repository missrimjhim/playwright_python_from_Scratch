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
        self.log_in_link = page.locator("a.ico-login")
        self.remember_me_checkbox = page.locator("input#RememberMe")

    def register_first_time(self, firstname, lastname, password, email):

        try:
            ExecutionLogger.log("Click Register link")
            self.register_link.click()

            ExecutionLogger.log(f"Entering firstname: {firstname}")
            self.firstname_input.fill(firstname)

            ExecutionLogger.log(f"Entering lastname: {lastname}")
            self.lastname_input.fill(lastname)

            ExecutionLogger.log(f"Entering email: {email}")
            self.email_input.fill(email)

            ExecutionLogger.log("Entering password")
            self.password_input.fill(password)

            ExecutionLogger.log("Entering confirmed password")
            self.confirmed_password_input.fill(password)

            ExecutionLogger.log("Click Register button")
            self.login_button.click()

        except Exception as e:
            ExecutionLogger.error("Registration failed – expected elements not found")
            raise e

    def validate_registration(self):
        try:
            ExecutionLogger.verify("Verify registration success message")
            expect(self.page.locator("div.result")).to_contain_text(
                "Your registration completed"
            )

            ExecutionLogger.log("Click Continue button")
            self.continue_button.click()

            ExecutionLogger.verify("Verify home page title")
            expect(self.page).to_have_title("Demo Web Shop")

            ExecutionLogger.verify("Verify user email is displayed")
            expect(
                self.page.locator("a.account", has_text="@gmail.com")
            ).to_be_visible()

        except Exception as e:
            ExecutionLogger.error("Registration failed – expected elements not found")
            raise e

    def click_on_log_in_link(self):
        try:
            ExecutionLogger.log("Click Log In button")
            self.log_in_link.click()
            expect(self.page.locator("div.page-title", has_text="Welcome, Please Sign In!")).to_be_visible()
        except Exception as e:
            ExecutionLogger.error("login failed – to click")
            raise e

    def enter_valid_login_credentials(self, email_id, password):
        try:
            ExecutionLogger.log("Enter email id")
            self.email_input.fill(email_id)
            ExecutionLogger.log("Enter Password")
            self.password_input.fill(password)
            ExecutionLogger.log("Check Checkbox")
            self.remember_me_checkbox.check()
            ExecutionLogger.log("Click the log in button")
            self.page.locator("input.button-1.login-button", has_text="Log in").click()

        except Exception as e:
            ExecutionLogger.error("Registration failed – expected elements not found")
            raise e

    def validate_login_existing_user(self):
        try:
            ExecutionLogger.verify("Verify home page title")
            expect(self.page).to_have_title("Demo Web Shop")

            ExecutionLogger.verify("Verify user email is displayed")
            expect(self.page.locator("a.account", has_text="@gmail.com")
            ).to_be_visible()

        except Exception as e:
            ExecutionLogger.error("Registration failed – expected elements not found")
            raise e

    def validate_incorrect_login(self):
        try:
            ExecutionLogger.log("Incorrect message displayed?")
            expect(self.page.locator("div.message-error", has_text="Login was unsuccessful")).to_contain_text("Login was unsuccessful")
            ExecutionLogger.verify("Yes Incorrect Login message displayed")

        except Exception as e:
            ExecutionLogger.error("Registration failed – expected elements not found")
            raise e

