import pandas as pd


class NetflixAnalyzer:
    """Consultas independientes: no mutan el DataFrame recibido."""

    def __init__(self, df: pd.DataFrame, missing_label: str = 'Desconocido'):
        self._df = df
        self._missing_label = missing_label

    def overview(self) -> dict:
        df = self._df
        return {
            'shape': df.shape,
            'nulls': df.isna().sum(),
            'dtypes': df.dtypes,
            'statistics': df.describe(),
            'duplicates': int(df.duplicated().sum()),
        }

    def titles_after(self, year: int = 2010) -> pd.DataFrame:
        return self._df.loc[self._df['release_year'] > year].copy()

    def top_countries(self, year: int = 2010, limit: int = 10) -> pd.Series:
        titles = self.titles_after(year)
        return (titles.groupby('country')['show_id']
                .count().sort_values(ascending=False).head(limit))

    def genre_counts(self, year: int = 2010) -> pd.Series:
        genres = (self.titles_after(year)['listed_in']
                  .dropna().str.split(',').explode().str.strip())
        return genres.loc[genres.ne('')].value_counts()

    def director_counts(self) -> pd.Series:
        directors = self._df.loc[
            self._df['director'].notna()
            & self._df['director'].ne(self._missing_label), 'director'
        ].astype('string').str.split(',').explode().str.strip()
        return directors.loc[directors.ne('')].value_counts()

    def top_director_works(self) -> tuple[str | None, pd.DataFrame]:
        counts = self.director_counts()
        columns = ['title', 'type', 'release_year']
        if counts.empty:
            return None, self._df.iloc[0:0][columns].copy()
        name = str(counts.index[0])
        # Evita coincidencias parciales entre nombres de directores.
        mask = self._df['director'].fillna('').astype('string').str.split(',').apply(
            lambda names: name in [part.strip() for part in names]
        )
        return name, self._df.loc[mask, columns].copy()

    def movies_with_country(self) -> pd.DataFrame:
        return self._df.loc[
            self._df['type'].eq('Movie')
            & self._df['country'].notna()
            & self._df['country'].ne(self._missing_label)
        ].copy()

    def movie_duration_by_country(self) -> pd.DataFrame:
        return (self.movies_with_country().groupby('country')['duration_minutes']
                .agg(cantidad='count', promedio='mean')
                .sort_values('promedio', ascending=False).round(2))

    def boxplot_data(self, min_movies: int = 5) -> tuple[pd.DataFrame, list[str]]:
        summary = self.movie_duration_by_country()
        country_labels = summary.index.astype(str)
        valid = summary.loc[
            summary['cantidad'].ge(min_movies)
            & ~country_labels.str.contains(',', regex=False)
        ].index.tolist()
        movies = self.movies_with_country()
        filtered = movies.loc[
            movies['country'].isin(valid) & movies['duration_minutes'].notna()
        ].copy()
        return filtered, valid
