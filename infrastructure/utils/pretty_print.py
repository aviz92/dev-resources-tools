import json
import logging

logger = logging.getLogger(__name__)


def print_in_format(
    data: any,
    log_level: int = logging.INFO,
    indent: int = 4,
    sort_keys: bool = True,
    default: callable = None
) -> None:
    formatted_data = json.dumps(data, indent=indent, sort_keys=sort_keys, default=default)

    level_name = logging.getLevelName(log_level).lower()
    log_method = getattr(logger, level_name, logger.debug)

    log_method("\n%s", formatted_data)
