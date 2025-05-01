import os
import shutil
from pathlib import Path

IGNORED_DIRS = ['.venv']


def delete_pycache_folder(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if any(ignored_dir in dirpath for ignored_dir in IGNORED_DIRS):
            continue

        if '__pycache__' in dirnames:
            pycache_dir = os.path.join(dirpath, '__pycache__')
            print(f"cleaning: {pycache_dir}")
            try:
                shutil.rmtree(pycache_dir)
                print(f"delete: {pycache_dir}")
            except Exception as e:
                print(f"cant find {pycache_dir}: {e}")


def main():
    root_dir = Path(__file__).parent
    delete_pycache_folder(root_dir=root_dir)


if __name__ == "__main__":
    main()
