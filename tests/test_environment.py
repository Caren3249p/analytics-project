"""Tests de infraestructura — verifican que el entorno y la estructura del proyecto
estén correctamente configurados antes de construir funcionalidad.
"""

import importlib
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent


def test_dependencias_principales():
    """Las dependencias principales del proyecto deben estar instaladas e importables."""
    for paquete in ("pandas", "pytest"):
        assert importlib.import_module(paquete) is not None


def test_estructura_del_proyecto():
    """El proyecto debe seguir el src layout esperado por el curso."""
    assert (RAIZ / "pyproject.toml").is_file()
    assert (RAIZ / "src" / "analytics").is_dir()
    assert (RAIZ / "src" / "analytics" / "__init__.py").is_file()
    assert (RAIZ / "tests").is_dir()


def test_paquete_importable():
    """El paquete analytics debe poder importarse desde el src layout."""
    analytics = importlib.import_module("analytics")
    assert analytics.__version__
