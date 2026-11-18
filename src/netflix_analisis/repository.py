from pathlib import Path
import pandas as pd


class CsvNetflixRepository:
    """Única responsabilidad: leer el dataset CSV."""

    def load(self, path: Path) -> pd.DataFrame:
        if not path.is_file():
            raise FileNotFoundError(f'No se encontró el CSV: {path.resolve()}')
        return pd.read_csv(path)
