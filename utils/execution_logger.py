# utils/execution_logger.py
from datetime import datetime
import allure


class ExecutionLogger:
    start_time = None
    test_name = None
    env = None
    browser = None
    url = None

    @staticmethod
    def start(test_name, env, browser, url):
        ExecutionLogger.test_name = test_name
        ExecutionLogger.env = env
        ExecutionLogger.browser = browser
        ExecutionLogger.url = url
        ExecutionLogger.start_time = datetime.now()
        # Set test title
        allure.dynamic.title(test_name)

        # Add labels (shown nicely in Allure UI)
        allure.dynamic.label("env", env)
        allure.dynamic.label("browser", browser)

        # Add description
        allure.dynamic.description(
            f"""
                    **Environment:** {env}  
                    **Browser:** {browser}  
                    **Base URL:** {url}  
                    **Start Time:** {ExecutionLogger.start_time.strftime("%d-%m-%Y %H:%M:%S")}
                    """
        )

        # Add environment details to Allure
        allure.attach(env, "Environment", allure.attachment_type.TEXT)
        allure.attach(browser, "Browser", allure.attachment_type.TEXT)
        allure.attach(url, "Base URL", allure.attachment_type.TEXT)
        allure.attach(
            ExecutionLogger.start_time.strftime("%d-%m-%Y %H:%M:%S"),
            "Start Time",
            allure.attachment_type.TEXT
        )

        with allure.step("TEST STARTED"):
            pass

    @staticmethod
    def log(step):
        with allure.step(step):
            pass

    @staticmethod
    def verify(message):
        with allure.step(f"VERIFY: {message}"):
            pass

    @staticmethod
    def error(message):
        allure.attach(
            message,
            "ERROR",
            allure.attachment_type.TEXT
        )

    @staticmethod
    def end(status):
        end_time = datetime.now()

        allure.attach(
            end_time.strftime("%d-%m-%Y %H:%M:%S"),
            "End Time",
            allure.attachment_type.TEXT
        )
        allure.attach(status, "Test Status", allure.attachment_type.TEXT)

        with allure.step("TEST ENDED"):
            pass
