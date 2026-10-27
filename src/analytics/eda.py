"""Análisis exploratorio reproducible: funciones que retornan, no imprimen — Lab 03."""

import pandas as pd
from pandas.api import types as pdt


def perfil_columna(df: pd.DataFrame, columna: str) -> dict:
    """Genera un perfil estadístico de una columna. No imprime — retorna un dict.

    Claves siempre presentes: 'columna', 'tipo', 'n_total', 'n_nulos',
    'pct_nulos', 'n_unicos'.

    Si la columna es numérica, agrega además: 'media', 'mediana', 'std',
    'min', 'max' (todos redondeados a 2 decimales, excepto min/max).

    Si la columna NO es numérica, agrega además: 'valor_mas_frecuente'
    (None si la columna está completamente vacía) y
    'freq_valor_mas_frecuente' (int, 0 si está completamente vacía).

    Args:
        df: DataFrame que contiene la columna.
        columna: nombre de la columna a perfilar.

    Returns:
        Diccionario con el perfil de la columna.
    """
    serie = df[columna]
    n_total = len(serie)
    n_nulos = int(serie.isna().sum())
    perfil = {
        "columna": columna,
        "tipo": str(serie.dtype),
        "n_total": n_total,
        "n_nulos": n_nulos,
        "pct_nulos": round(n_nulos / n_total * 100, 2) if n_total else 0.0,
        "n_unicos": int(serie.nunique()),
    }
    if pdt.is_numeric_dtype(serie) and not pdt.is_bool_dtype(serie):
        perfil.update(
            {
                "media": round(float(serie.mean()), 2),
                "mediana": round(float(serie.median()), 2),
                "std": round(float(serie.std()), 2),
                "min": float(serie.min()),
                "max": float(serie.max()),
            }
        )
    else:
        conteos = serie.value_counts()
        if conteos.empty:
            perfil["valor_mas_frecuente"] = None
            perfil["freq_valor_mas_frecuente"] = 0
        else:
            perfil["valor_mas_frecuente"] = conteos.index[0]
            perfil["freq_valor_mas_frecuente"] = int(conteos.iloc[0])
    return perfil


def distribucion_categorica(df: pd.DataFrame, columna: str) -> pd.DataFrame:
    """Retorna el conteo y porcentaje de cada categoría, ordenado descendente.

    Args:
        df: DataFrame que contiene la columna.
        columna: nombre de la columna categórica.

    Returns:
        DataFrame indexado por categoría, con columnas 'conteo' (int) y
        'porcentaje' (float, redondeado a 2 decimales, suma ≈ 100).
    """
    conteo = df[columna].value_counts()  # ya viene ordenado de mayor a menor
    resultado = pd.DataFrame({"conteo": conteo})
    resultado["porcentaje"] = (conteo / conteo.sum() * 100).round(2)
    resultado.index.name = columna
    return resultado


def matriz_correlacion(df: pd.DataFrame, columnas: list[str]) -> pd.DataFrame:
    """Retorna la matriz de correlación de Pearson para las columnas dadas.

    Args:
        df: DataFrame que contiene las columnas.
        columnas: lista de nombres de columnas numéricas a correlacionar.

    Returns:
        DataFrame cuadrado (len(columnas) x len(columnas)) con los
        coeficientes de correlación de Pearson. La diagonal es siempre 1.0.
    """
    # numeric_only=True evita un error si por accidente entra una columna de texto.
    return df[columnas].corr(method="pearson", numeric_only=True)
