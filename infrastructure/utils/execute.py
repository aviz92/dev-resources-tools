from collections.abc import Callable
from time import sleep, time

from tqdm import tqdm


def timed_execution(
    func: Callable[[], bool],
    timeout: int = 60,
    interval: int = 1,
    expect_true: bool = True,
    pb_description: str = "Executing",
) -> bool:
    pbar = tqdm(total=timeout, desc=pb_description, unit="s", ncols=100)
    start_time = time()
    while time() - start_time < timeout:
        ret = func()
        if (expect_true and ret) or (not expect_true and not ret):
            pbar.close()
            return True
        pbar.update(interval)
        sleep(interval)
    pbar.close()
    return False
