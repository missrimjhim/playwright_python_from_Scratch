from pages.login_page import LoginPage


def test_TC_01_User_registration(browser_context):
    login_page = LoginPage(browser_context)
    login_page.register_first_time("abcde", "efgd","asdfgh","543eashgfgdyudd@gmail.com")
    login_page.validate_registration()





