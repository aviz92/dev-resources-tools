# lru_cache.py

import requests
import functools
from functools import lru_cache
from typing import Any, Callable


def authenticate(func: Callable[..., Any]) -> Callable[..., Any]:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print("Authenticating user.")
        return func(*args, **kwargs)

    return wrapper


@lru_cache
@authenticate
def fetch_user(user_id: int) -> dict[str, int | str]:
    print("Fetching user from the database.")
    return {"id": user_id, "name": "Alice"}


@lru_cache(maxsize=10)  # Cache up to 10 API responses
def fetch_dad_joke(joke_id=None):
    headers = {"Accept": "application/json"}
    if joke_id:
        url = f"https://icanhazdadjoke.com/j/{joke_id}"
    else:
        url = "https://icanhazdadjoke.com/"
    print(f"Fetching joke from {url}...")
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()  # Return the joke as JSON


def main() -> None:
    user = fetch_user(1)
    print(user)

    # Calling again with the same user_id
    user = fetch_user(1)  # Should authenticate again, but it doesn't!
    print(user)

    user = fetch_user(2)
    print(user)


def main2() -> None:
    print("Fetch joke by ID:")
    print(fetch_dad_joke("08xHQCdx5Ed"))
    print("Repeat same ID joke:")
    print(fetch_dad_joke("08xHQCdx5Ed"))

    # Display cache info
    print("\nCache Info:")
    print(fetch_dad_joke.cache_info())


if __name__ == "__main__":
    main()
    print("\n" + "-" * 40 + "\n")
    main2()
