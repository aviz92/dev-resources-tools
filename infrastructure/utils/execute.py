from collections.abc import Callable
from time import sleep, time
from typing import Any

from tqdm import tqdm


def _timed_execution(
    func: Callable[[], Any],
    timeout: int = 60,
    interval: int = 1,
    expect_true: bool = True,
    pb_description: str = "Executing",
    return_result: bool = False,
) -> Any | bool | None:
    pbar = tqdm(total=timeout, desc=pb_description, unit="s", ncols=100)
    start_time = time()

    while time() - start_time < timeout:
        res = func()
        if (expect_true and res) or (not expect_true and not res):
            pbar.close()
            return res if return_result else True
        pbar.update(interval)
        sleep(interval)

    pbar.close()
    return None if return_result else False


def timed_execution_bool(
    func: Callable[[], Any],
    timeout: int = 60,
    interval: int = 1,
    expect_true: bool = True,
    pb_description: str = "Executing",
) -> bool:
    return _timed_execution(
        func=func,
        timeout=timeout,
        interval=interval,
        expect_true=expect_true,
        pb_description=pb_description,
        return_result=False,
    )


def timed_execution_result(
    func: Callable[[], Any],
    timeout: int = 60,
    interval: int = 1,
    expect_true: bool = True,
    pb_description: str = "Executing",
) -> Any:
    return _timed_execution(
        func=func,
        timeout=timeout,
        interval=interval,
        expect_true=expect_true,
        pb_description=pb_description,
        return_result=True,
    )
