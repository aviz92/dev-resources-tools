# metaclass.py

# 📌 Principle:
# A Metaclass is a class of a class. It defines how classes themselves are constructed. By using a metaclass, you can modify or extend the behavior of classes at the time of their creation.
# In this example:
# MyMeta is a metaclass that adds an extra method (extra_method) to the class.
# MyClass uses MyMeta as its metaclass, which means MyClass automatically gets this new method.
# Metaclasses are typically used for controlling class behavior, validation, or enforcing patterns.

# Metaclass definition
class MyMeta(type):
    def __new__(cls, name, bases, dct):
        # Add an extra method to the class
        dct['extra_method'] = lambda self: "This is an extra method"
        return super().__new__(cls, name, bases, dct)


# Class using the metaclass
class MyClass(metaclass=MyMeta):
    def __init__(self, name):
        self.name = name


def main():
    obj = MyClass("Test")
    print(f"Name: {obj.name}")
    print(f"Extra method output: {obj.extra_method()}")


if __name__ == "__main__":
    main()
