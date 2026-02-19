# pages/page_manager.py
from pages.login_page import LoginPage
from utils.excel_reader import ExcelReader


class PageManager:
    def __init__(self, page):
        self.login = LoginPage(page)
        self.testdata = ExcelReader()
