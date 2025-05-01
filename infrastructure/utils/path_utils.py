from pathlib import Path


def get_project_path(project_name: str) -> str:
    current_path = Path(__file__).parent
    while current_path != current_path.parent:
        if str(current_path).endswith(f'/{project_name}'):
            return str(current_path)
        current_path = current_path.parent
    raise FileNotFoundError(
        f'Project "{project_name}" not found in any parent directories.\n'
        f'Current path: {Path(__file__)}',
    )
