import json
import logging

logger = logging.getLogger(__name__)


def print_in_format(data: any, log_level: int = logging.INFO) -> None:
    formatted_data = json.dumps(data, indent=4, sort_keys=True, default=str)

    level_name = logging.getLevelName(log_level).lower()
    log_method = getattr(logger, level_name, logger.debug)

    log_method("\n%s", formatted_data)
