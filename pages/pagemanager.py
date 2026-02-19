# pages/page_manager.py
from pages.login_page import LoginPage


class PageManager:
    def __init__(self, page):
        self.login = LoginPage(page)

