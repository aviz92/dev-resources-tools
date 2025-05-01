# asyncio_task_group.py

import asyncio
import random


async def multiply(number: int, multiplier: int = 10, timeout: int = 10) -> int:
    timeout = random.randint(1, timeout)
    print(f"Task {number} started")
    await asyncio.sleep(timeout)
    print(f"Task {number} completed")
    return number * multiplier


async def main():
    tasks = []
    # Using TaskGroup to manage multiple tasks
    async with asyncio.TaskGroup() as task_group:
        for i in range(5):
            _task = task_group.create_task(multiply(number=i))
            tasks.append(_task)

    # Once the async with block ends, all tasks are completed.
    print("All tasks are completed.")

    results = [_task.result() for _task in tasks]
    print("Results:", results)


if __name__ == '__main__':
    # Running the event loop
    asyncio.run(main())
