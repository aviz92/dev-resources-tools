from typing import NamedTuple


class PythonCommands(NamedTuple):
    PYTHON_PIP_INSTALL: str = 'python{python_version} -m pip install {module}'
    PYTHON_EXECUTE: str = 'python{python_version} {python_script_path}'
    DNF_INSTALL_PYTHON_VERSION: str = 'sudo dnf install python{python_version} -y'
    DOWNLOAD_PIP: str = 'wget https://bootstrap.pypa.io/get-pip.py'
    INSTALL_PIP: str = 'python{python_version} get-pip.py'
