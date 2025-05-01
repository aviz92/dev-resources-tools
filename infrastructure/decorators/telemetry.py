import json
import logging
import time
import functools
import datetime
from typing import Callable, Any

logger = logging.getLogger(__name__)


def report_telemetry(
    func: Callable[..., Any],
    start_time: datetime.datetime,
    end_time: datetime.datetime,
    *args: Any,
    **kwargs: Any
) -> None:
    data = {
        "function_name": func.__name__,
        "args": args,
        "kwargs": kwargs,
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "timestamp": time.time(),
    }
    logger.info(f"Sending telemetry data with the following data: {json.dumps(data, indent=4, sort_keys=False, default=str)}")


def report_func_telemetry(func: Callable[..., Any]) -> Callable[..., Any]:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        # print(f"Calling function: {func.__name__}, with arguments: {args} and keyword arguments: {kwargs}")
        # return func(*args, **kwargs)
        logger.info(f"calling {report_telemetry.__name__} to report the telemetry of {func.__name__}")
        start_time = datetime.datetime.now(datetime.UTC)
        result = func(*args, **kwargs)
        end_time = datetime.datetime.now(datetime.UTC)
        report_telemetry(func=func, start_time=start_time, end_time=end_time, *args, **kwargs)
        return result

    return wrapper


@report_func_telemetry
def main():
    from infrastructure.logger_infrastructure.logger import get_logger

    _logger = get_logger(
        project_name='Telemetry Decorator Project Test',
        log_level=logging.DEBUG,
        # extra={'user': 'test_user'}
    )
    time.sleep(2)
    _logger.info("Doing some work...")


if __name__ == "__main__":
    logger.info("Running main...")
    main()

    logger.info("Done.")
