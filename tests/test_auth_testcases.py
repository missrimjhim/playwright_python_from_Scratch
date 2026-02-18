from pages.login_page import LoginPage


def test_TC_01_User_registration(page):
    login_page = LoginPage(page)
    login_page.register_first_time("abcde", "efgd","asdfgh","5a79swagrirratatam@gmail.com")
    login_page.validate_registration()






