"""Módulo de ingesta de datos — carga de fuentes externas hacia el pipeline."""

from pathlib import Path

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


_ARCHIVOS_OLIST = {
    "orders": "olist_orders_dataset.csv",
    "items": "olist_order_items_dataset.csv",
    "customers": "olist_customers_dataset.csv",
    "payments": "olist_order_payments_dataset.csv",
    "reviews": "olist_order_reviews_dataset.csv",
}

_FECHAS_OLIST = {
    "orders": [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ],
    "reviews": ["review_creation_date", "review_answer_timestamp"],
}


def cargar_olist(data_dir: str) -> dict[str, pd.DataFrame]:
    """Carga las 5 tablas principales de Olist desde data_dir.

    Registra con print() la forma (filas × columnas) de cada tabla al cargarla.
    Las columnas de fecha se cargan como datetime64, no como object.

    Args:
        data_dir: ruta al directorio que contiene los archivos CSV de Olist.

    Returns:
        Dict con keys 'orders', 'items', 'customers', 'payments', 'reviews',
        cada uno mapeado a su DataFrame correspondiente.

    Raises:
        FileNotFoundError: si alguno de los 5 archivos no existe en data_dir.
    """
    tablas: dict[str, pd.DataFrame] = {}
    for nombre, archivo in _ARCHIVOS_OLIST.items():
        ruta = Path(data_dir) / archivo
        # read_csv ya lanza FileNotFoundError si el archivo no existe.
        df = pd.read_csv(ruta, parse_dates=_FECHAS_OLIST.get(nombre, []))
        print(f"  {nombre}: {df.shape[0]:,} filas × {df.shape[1]} columnas")
        tablas[nombre] = df
    return tablas


def join_verificado(
    df_left: pd.DataFrame,
    df_right: pd.DataFrame,
    on: str | list[str],
    how: str = "left",
    nombre: str = "join",
) -> pd.DataFrame:
    """Realiza un merge y verifica que el resultado no multiplique filas.

    Un join que multiplica filas indica que la tabla derecha tiene duplicados
    en la columna clave — error silencioso sin esta verificación.

    Args:
        df_left: DataFrame izquierdo (el que define el número de filas esperado).
        df_right: DataFrame derecho.
        on: columna(s) clave del join.
        how: tipo de join ('left', 'inner', 'outer', 'right').
        nombre: nombre descriptivo para el mensaje de error.

    Returns:
        DataFrame resultante del merge.

    Raises:
        AssertionError: si el resultado tiene más filas que df_left.
    """
    resultado = df_left.merge(df_right, on=on, how=how)
    assert len(resultado) <= len(df_left), (
        f"{nombre}: el join multiplicó las filas "
        f"({len(df_left)} → {len(resultado)} filas); "
        "revisa duplicados en la clave de la tabla derecha."
    )
    return resultado


def construir_dataset_base(tablas: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Combina las tablas de Olist en un único DataFrame analítico.

    Estrategia de joins (todos verificados con join_verificado):
        - orders × customers → left join on customer_id
        - + items_agg → left join on order_id (items se agrega primero)

    Items se agrega antes del join: n_items (count), precio_total (sum de price)
    y flete_total (sum de freight_value) por order_id. Las columnas resultantes
    coinciden con las que esperan los Labs 03-06.

    Args:
        tablas: dict retornado por cargar_olist().

    Returns:
        DataFrame con una fila por pedido (99,441 filas si los datos son completos).
    """
    items_agg = (
        tablas["items"]
        .groupby("order_id")
        .agg(
            n_items=("order_item_id", "count"),
            precio_total=("price", "sum"),
            flete_total=("freight_value", "sum"),
        )
        .reset_index()
    )
    clientes = tablas["customers"][
        [
            "customer_id",
            "customer_unique_id",
            "customer_zip_code_prefix",
            "customer_city",
            "customer_state",
        ]
    ]

    df = join_verificado(tablas["orders"], clientes, on="customer_id", nombre="orders×customers")
    df = join_verificado(df, items_agg, on="order_id", nombre="orders×items")
    return df
