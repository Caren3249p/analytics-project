"""Módulo de ingesta de datos — carga de fuentes externas hacia el pipeline."""

import pandas as pd


def cargar_csv(ruta: str) -> pd.DataFrame:
    """Carga un archivo CSV y verifica que contenga al menos una fila de datos.

    Args:
        ruta: ruta al archivo CSV a cargar.

    Returns:
        DataFrame con los datos cargados.

    Raises:
        FileNotFoundError: si el archivo no existe en la ruta indicada.
        ValueError: si el archivo existe pero no contiene filas de datos.
    """
    # pd.read_csv() ya lanza FileNotFoundError por sí mismo si la ruta no existe,
    # por lo que no hace falta comprobar la existencia del archivo manualmente.
    df = pd.read_csv(ruta)

    # Un CSV con solo encabezados produce un DataFrame sin filas: df.empty es True.
    if df.empty:
        raise ValueError(f"El archivo '{ruta}' no contiene filas de datos.")

    return df
