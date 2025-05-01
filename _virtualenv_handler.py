import sys
import os


class VenvHandler:
    def __init__(self):
        self.sys_executable = sys.executable
        self.sys_version = sys.version
        self.virtual_env = os.getenv("VIRTUAL_ENV")

    def get_venv_handler_details(self):
        print(
            f'\nPython executable path: {self.sys_executable}'
            f'\nPython version: {self.sys_version}'
            f'\nVirtualenv path: {self.virtual_env}'
        )


if __name__ == '__main__':
    venv_handler = VenvHandler()
    venv_handler.get_venv_handler_details()
