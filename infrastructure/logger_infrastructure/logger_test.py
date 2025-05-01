import logging


class LoggerTest:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def main(self):
        self.logger.info('Hello World')
        self.logger.debug('Hello World')


def main():
    from infrastructure.logger_infrastructure.logger import get_logger

    logger = get_logger(
        project_name='Logger Project Test',
        log_level=logging.DEBUG,
        # extra={'user': 'test_user'}
    )

    logger.debug("This is a debug message.")
    logger.info("This is an info message.")
    logger.step("This is a step message.")
    logger.warning("This is a warning message.")

    try:
        _ = 1 / 0
    except ZeroDivisionError:
        logger.exception("This is an exception message.")

    logger.critical("This is a critical message.")

    logger_test = LoggerTest()
    logger_test.main()

if __name__ == '__main__':
    main()
