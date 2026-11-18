from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Config:
    csv_path: Path = Path('data/netflix_titles_ficticio (2).csv')
    missing_label: str = 'Desconocido'
    text_columns: tuple[str, ...] = ('director', 'cast', 'country', 'rating')
    required_columns: tuple[str, ...] = (
        'show_id', 'title', 'type', 'release_year', 'date_added',
        'duration', 'listed_in', 'director', 'cast', 'country', 'rating'
    )
