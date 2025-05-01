# plugin_metadata.py

class PluginMeta(type):
    registry = {}

    def __new__(cls, name, bases, attrs):
        new_class = super().__new__(cls, name, bases, attrs)

        # Avoid registering the base class itself
        if bases != ():
            PluginMeta.registry[name] = new_class
            print(f"Registered plugin: {name}")
        return new_class


class Plugin(metaclass=PluginMeta):
    def run(self):
        raise NotImplementedError("Subclasses must implement this method.")


class PluginA(Plugin):
    def run(self):
        print("Running Plugin A")


class PluginB(Plugin):
    def run(self):
        print("Running Plugin B")


def main():
    print(f"Available plugins: {PluginMeta.registry.keys()}")

    for plugin_name, plugin_class in PluginMeta.registry.items():
        print(f"Instantiating plugin: {plugin_name}...")

        # Example of running a plugin
        plugin = plugin_class()
        plugin.run()


if __name__ == '__main__':
    main()
