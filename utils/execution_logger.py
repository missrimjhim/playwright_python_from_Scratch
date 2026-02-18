from datetime import datetime
from utils.html_logger import HTMLLogger


class ExecutionLogger:
    html_logger = None
    start_time = None
    pytest_config = None
    steps = []
    @staticmethod
    def init():
        """
        Must be called once per test run.
        Creates the HTML logger file.
        """
        ExecutionLogger.html_logger = HTMLLogger(ExecutionLogger.pytest_config)

    @staticmethod
    def start(test_name, env, browser, url):
        ExecutionLogger.steps = []  # reset per test
        ExecutionLogger.start_time = datetime.now()

        ExecutionLogger.html_logger.banner("TEST STARTED")
        ExecutionLogger.html_logger.info(f"Test Name   : {test_name}")
        ExecutionLogger.html_logger.info(f"Environment : {env}")
        ExecutionLogger.html_logger.info(f"Browser     : {browser}")
        ExecutionLogger.html_logger.info(f"URL         : {url}")
        ExecutionLogger.html_logger.info(
            f"Start Time  : {ExecutionLogger.start_time.strftime('%d-%m-%Y %H:%M:%S')}"
        )
        ExecutionLogger.html_logger.info("-----------------------------------")

    @staticmethod
    def log(step):
        ExecutionLogger.steps.append(step)
        ExecutionLogger.html_logger.info(step)

    @staticmethod
    def end(status):
        end_time = datetime.now()

        ExecutionLogger.html_logger.info("-----------------------------------")
        ExecutionLogger.html_logger.banner("TEST ENDED")
        ExecutionLogger.html_logger.info(
            f"End Time : {end_time.strftime('%d-%m-%Y %H:%M:%S')}"
        )
        ExecutionLogger.html_logger.info(f"Status   : {status}")

    @staticmethod
    def save():
        ExecutionLogger.html_logger.save()
