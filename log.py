import logging
import os

if not os.path.exists("logs"):
    os.mkdir("logs")
with open("logs/application.log", "w") as f:
    pass

# Create a common file handler for all loggers
common_file_handler = logging.FileHandler("logs/application.log")
common_file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
common_file_handler.setFormatter(formatter)


class MyLogger:
    def __init__(self, logger_name):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(common_file_handler)
        self.encoding = "utf-8"

    def log_info(self, message: str):
        # ensure that the message is encoded in utf-8
        self.logger.info(message.encode(self.encoding))

    def log_debug(self, message: str):
        self.logger.debug(message.encode(self.encoding))

    def log_warning(self, message: str):
        self.logger.warning(message.encode(self.encoding))

    def log_error(self, message: str):
        self.logger.error(message.encode(self.encoding))

    def log_critical(self, message: str):
        self.logger.critical(message.encode(self.encoding))

    def log_exception(self, message: str):
        self.logger.exception(message)


# Usage example:
if __name__ == "__main__":
    logger1 = MyLogger("Logger1")
    logger2 = MyLogger("Logger2")

    logger1.log_info("This is an info message from Logger1")
    logger1.log_debug("This is a debug message from Logger1")
    logger1.log_warning("This is a warning message from Logger1")
    logger1.log_error("This is an error message from Logger1")
    logger1.log_critical("This is a critical message from Logger1")

    logger2.log_info("This is an info message from Logger2")
    logger2.log_debug("This is a debug message from Logger2")
    logger2.log_warning("This is a warning message from Logger2")
    logger2.log_error("This is an error message from Logger2")
    logger2.log_critical("This is a critical message from Logger2")

    try:
        # Simulate an exception
        raise Exception("An exception occurred")
    except Exception as e:
        logger1.log_exception("An exception occurred in Logger1")
        logger2.log_exception("An exception occurred in Logger2")
