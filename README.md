# analytics-project

Proyecto del semestre — **Analítica de Datos**. Pipeline reproducible sobre el
dataset [Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce),
construido lab a lab con entorno gestionado por `uv`, calidad automatizada con
`ruff` y CI en GitHub Actions.

## Requisitos

- Python 3.12.x
- [uv](https://docs.astral.sh/uv/) 0.1.x o superior
- git 2.x o superior

## Puesta en marcha

```bash
uv sync --all-groups     # instala dependencias (runtime + dev)
uv run pytest            # corre la suite de tests
uv run ruff check .      # lint
uv run ruff format --check .   # verificación de formato
```

## Estructura

```
analytics-project/
├── src/analytics/       # código del paquete (src layout)
│   └── extract.py       # ingesta de datos (Lab 01: cargar_csv)
├── tests/               # suite de pytest
├── data/raw/            # CSVs de Olist (no versionados — ver .gitignore)
└── .github/workflows/   # CI: ruff + pytest en cada push
```

## Dataset

Los 9 CSV de Olist se colocan en `data/raw/` y **no se versionan**. Se descargan
del campus virtual. Los tests usan CSVs de prueba pequeños generados en tiempo de
ejecución, no el dataset real.

## Progreso del semestre

| Lab | Módulo | Estado |
|-----|--------|--------|
| 01  | setup + `extract.py` (`cargar_csv`) | 🔨 en construcción |
| 02  | `extract.py` completo + `quality.py` | pendiente |
| 03  | `transform.py` + `eda.py` | pendiente |
