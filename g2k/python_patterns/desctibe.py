# describe.py

from functools import singledispatch


def describe_old_version(obj):
    if isinstance(obj, int):
        print(f"This is an integer: {obj}")
    elif isinstance(obj, str):
        print(f"This is a string: {obj}")
    elif isinstance(obj, list):
        print(f"This is a list with {len(obj)} elements: {obj}")
    elif isinstance(obj, dict):
        print(f"This is a dictionary with {len(obj)} keys: {obj}")
    else:
        # print(f"This is an object of type {type(obj)}: {obj}")
        raise NotImplementedError("cannot describe this object of type {type(obj)}")


@singledispatch
def describe(obj):
    raise NotImplementedError(f"cannot describe this object of type {type(obj)}")


@describe.register
def _(obj: int):
    print(f"This is an integer: {obj}")


@describe.register
def _(obj: str):
    print(f"This is a string: {obj}")


@describe.register
def _(obj: list):
    print(f"This is a list with {len(obj)} elements: {obj}")


@describe.register
def _(obj: dict):
    print(f"This is a dictionary with {len(obj)} keys: {obj}")


def main():
    describe(42)
    describe("Hello, World!")
    describe([1, 2, 3])
    describe({"name": "Alice", "age": 30})


def main_old_version():
    describe_old_version(42)
    describe_old_version("Hello, World!")
    describe_old_version([1, 2, 3])
    describe_old_version({"name": "Alice", "age": 30})


if __name__ == '__main__':
    main()
    print("\n" + "-" * 40 + "\n")
    main_old_version()
