"""
test_git_hygiene.py — Validación de higiene de Git en proyectos de Ciencia de Datos.

Verifica que los datasets pesados o datos crudos en data/raw/ NO estén siendo
rastreados por Git, preservando la inmutabilidad y la limpieza del repositorio.
"""

import subprocess
from pathlib import Path


def test_no_raw_data_tracked_in_git():
    """
    Verifica mediante 'git ls-files' que solo archivos permitidos (como .gitkeep)
    estén bajo control de versiones en data/raw/.
    """
    project_root = Path(__file__).resolve().parent.parent
    data_raw_dir = project_root / "data" / "raw"

    if not data_raw_dir.exists():
        return

    try:
        result = subprocess.run(
            ["git", "ls-files", str(data_raw_dir)],
            capture_output=True,
            text=True,
            check=True
        )
        tracked_files = result.stdout.strip().splitlines()

        for file_path in tracked_files:
            file_name = Path(file_path).name
            assert file_name == ".gitkeep", (
                f"Violación de higiene: El archivo '{file_path}' está siendo rastreado en Git. "
                f"Los datos crudos deben ser ignorados por .gitignore."
            )
    except FileNotFoundError:
        # Si git no está disponible en el entorno de testing, omitir
        pass
