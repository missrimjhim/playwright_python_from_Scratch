from pages.login_page import LoginPage


def test_TC_01_User_registration(pages):
    pages.login.register_first_time("abcde", "efgd","asdfgh","5navidm@gmail.com")
    pages.login.validate_registration()








