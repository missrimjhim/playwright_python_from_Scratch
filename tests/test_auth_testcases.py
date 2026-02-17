from pages.login_page import LoginPage
from utils.html_logger import HTMLLogger

def test_TC_01_User_registration(browser_context):
    logger = HTMLLogger()
    login_page = LoginPage(browser_context,logger)
    login_page.register_first_time("abcde", "efgd","asdfgh","54389y@gmail.com")
    login_page.validate_registration()
    logger.save()





