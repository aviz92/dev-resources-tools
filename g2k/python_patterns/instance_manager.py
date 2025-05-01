# instance_manager.py

class SomeInstance:
    def __init__(self, add_to_instance_manager: bool = False):
        if add_to_instance_manager:
            instance_manager.add(self)

    @property
    def __class_name__(self):
        return self.__class__.__name__

    def __enter__(self):
        print(f"Entering {self.__class_name__}")
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        print(f"Exiting {self.__class_name__}")
        # Handle any cleanup here
        if exc_type:
            print(f"Exception: {exc_value}")
        return True


class InstanceManager:
    def __init__(self):
        self._instances = []

    def add(self, instance):
        self._instances.append(instance)

    def close_all(self):
        for instance in reversed(self._instances):
            _instance_name = instance.__class__.__name__
            try:
                if hasattr(instance, 'close'):
                    instance.close()
                else:  # hasattr(instance, '__exit__'):
                    instance.__exit__(None, None, None)
                print(f"Instance: {_instance_name} closed successfully.")
            except Exception as e:
                print(f"Failed to close instance {instance}: {e}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close_all()


def main():
    SomeInstance(add_to_instance_manager=True)

    resource1 = open('file1.txt', 'w')
    resource2 = open('file2.txt', 'w')

    instance_manager.add(resource1)
    instance_manager.add(resource2)

    # do stuff...

    instance_manager.close_all()  # or, if inside `with manager:`, it will happen automatically


if __name__ == "__main__":
    instance_manager = InstanceManager()

    main()
