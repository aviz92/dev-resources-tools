import logging
import time
import functools
from typing import Callable, Any

logger = logging.getLogger(__name__)


class Timer:
    def __enter__(self):
        self.start_time = time.perf_counter()
        logger.info("Timer started.")
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        # logger.info(exc_type, exc_value, exc_traceback)
        self.end_time = time.perf_counter()
        self.elapsed_time = self.end_time - self.start_time
        logger.info(f"Timer stopped. Elapsed time: {self.elapsed_time:.2f} seconds.")


def timer(func: Callable[..., Any]) -> Callable[..., Any]:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        with Timer():
            return func(*args, **kwargs)

    return wrapper


@timer
def main2():
    from infrastructure.logger_infrastructure.logger import get_logger

    _logger = get_logger(
        project_name='Timer Decorator Project Test',
        log_level=logging.DEBUG,
        # extra={'user': 'test_user'}
    )

    time.sleep(2)
    _logger.info("Doing some work...")


def main():
    from infrastructure.logger_infrastructure.logger import get_logger

    _logger = get_logger(
        project_name='Timer Decorator Project Test',
        log_level=logging.DEBUG,
        # extra={'user': 'test_user'}
    )

    with Timer() as t:
        x = 0 / 0
        # Simulate some work
        time.sleep(2)
        _logger.info("Doing some work...")


if __name__ == "__main__":
    # logger.info("Running main...")
    # main()

    logger.info("Running main2...")
    main2()

    logger.info("Done.")
