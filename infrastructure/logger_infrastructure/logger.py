import logging
import os
import sys
import time
from logging import LoggerAdapter, Logger
from typing import Optional, Any
from colorlog import ColoredFormatter

from infrastructure.consts.global_const import PROJECT_NAME
from infrastructure.utils.path_utils import get_project_path


def print_before_logger(project_name: str) -> None:
    main_string = f'Start "{project_name}" Process'

    number_of_ladder = "#" * len(f"### {main_string} ###")
    print(f"\n{number_of_ladder}")
    print(f"### {main_string} ###")
    print(f"{number_of_ladder}\n")
    time.sleep(0.3)


class CustomLoggerAdapter(logging.LoggerAdapter):
    def exception(self, msg: str, *args, **kwargs):
        level_no = 45
        logging.addLevelName(level_no, "EXCEPTION")
        self.log(level_no, msg, *args, exc_info=True, **kwargs)

    def step(self, msg: str, *args, **kwargs):
        level_no = 25
        logging.addLevelName(level_no, "STEP")
        self.log(level_no, msg, *args, exc_info=False, **kwargs)


def configure_logging(
    log_format: str,
    log_level: int = logging.INFO,
    log_file: Optional[str] = None,
    console_output: bool = True
) -> None:
    """
    Configure global logging settings.

    Args:
        log_level: Logging level (default: INFO)
        log_format: Format string for log messages
        log_file: Path to log file (if None, no file logging)
        console_output: Whether to output logs to console
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Clear existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Add file handler if specified
    if log_file is not None:
        log_file_formatter = logging.Formatter(log_format)

        # Create directory if it doesn't exist
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

        file_handler = logging.FileHandler(log_file)

        file_handler.setFormatter(log_file_formatter)
        root_logger.addHandler(file_handler)

    # Add console handler if specified
    if console_output:
        # log_console_formatter = logging.Formatter('%(log_color)s ' + log_format)
        log_console_formatter = ColoredFormatter(
            '%(log_color)s ' + log_format,
            log_colors={
                'DEBUG': 'white',
                'INFO': 'green',
                'WARNING': 'yellow',
                'STEP': 'blue',
                'ERROR': 'red,bold',
                'EXCEPTION': 'light_red,bold',
                'CRITICAL': 'red,bg_white',
            }
        )

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_console_formatter)
        root_logger.addHandler(console_handler)


def get_logger(
    project_name: str,
    extra: Optional[dict[str, Any]] = None,
    log_format: str = "%(asctime)s | %(levelname)-10s(l.%(levelno)s) | %(filename)s:%(lineno)d | %(message)s",
    log_level: int = logging.INFO,
    log_file: str = None,
    console_output: bool = True,

) -> CustomLoggerAdapter[Logger | LoggerAdapter[Any] | Any] | Logger:
    """
    Get a named logger with optional extra context.

    Args:
        project_name: Name of the project
        log_level: Optional specific log level
        extra: Optional dictionary of extra context values
        log_format: Format string for log messages
        log_file: Path to log file (if None, no file logging)
        console_output: Whether to output logs to console

    Returns:
        Configured logger
    """
    if not log_file:
        file_name_executable = os.path.basename(sys.argv[0]).split('.')[0]
        log_file = get_project_path(PROJECT_NAME) + f"/logs/{file_name_executable}.log"
    print_before_logger(project_name=project_name)

    configure_logging(
        log_level=logging.DEBUG,
        log_format=log_format,
        log_file=log_file,
        console_output=console_output,
    )

    logger = logging.getLogger()

    if log_level is not None:
        logger.setLevel(log_level)

    return CustomLoggerAdapter(logger, extra)
