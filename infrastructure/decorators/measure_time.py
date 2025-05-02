# measure_time.py

import time


def measure_time(func) -> callable:
    def wrapper(*args, **kwargs) -> callable:
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f'execution_time: {execution_time}')
        return result

    return wrapper


@measure_time
def some_function():
    for _ in range(3):
        time.sleep(1)


if __name__ == '__main__':
    some_function()
