import pandas as pd
from .config import Config


class NetflixCleaner:
    """Normaliza una copia; nunca modifica el DataFrame original."""

    def __init__(self, config: Config):
        self.config = config

    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        missing = set(self.config.required_columns) - set(df.columns)
        if missing:
            raise ValueError(f'Faltan columnas requeridas: {sorted(missing)}')

        result = df.copy(deep=True)
        result[list(self.config.text_columns)] = result[
            list(self.config.text_columns)
        ].fillna(self.config.missing_label)

        # dtype anulable evita fallos ante años ausentes o valores inválidos.
        result['release_year'] = pd.to_numeric(
            result['release_year'], errors='coerce'
        ).astype('Int64')
        result['date_added'] = pd.to_datetime(
            result['date_added'], format='mixed', errors='coerce'
        )
        # Las temporadas de TV no son minutos: esas filas quedan como NaN.
        result['duration_minutes'] = pd.to_numeric(
            result['duration'].astype('string').str.extract(
                r'^\s*(\d+)\s*min\s*$', expand=False, flags=0
            ), errors='coerce'
        )
        return result
