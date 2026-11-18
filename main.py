"""Ejecutar desde la raíz: python main.py"""
import matplotlib.pyplot as plt
from src.netflix_analisis.config import Config
from src.netflix_analisis.repository import CsvNetflixRepository
from src.netflix_analisis.cleaning import NetflixCleaner
from src.netflix_analisis.analysis import NetflixAnalyzer
from src.netflix_analisis.visualization import NetflixPlotter


def main() -> None:
    config = Config()
    raw = CsvNetflixRepository().load(config.csv_path)
    clean = NetflixCleaner(config).clean(raw)
    analyzer = NetflixAnalyzer(clean, config.missing_label)
    plotter = NetflixPlotter()

    print('Datos originales:', raw.shape)
    print('Nulos antes:', raw.isna().sum().to_string())
    print('Duplicados:', int(raw.duplicated().sum()))
    print('Tipos después:', clean.dtypes.to_string())
    print('Top países:\n', analyzer.top_countries())
    print('Top géneros:\n', analyzer.genre_counts().head(10))
    print('Top directores:\n', analyzer.director_counts().head(5))
    director, works = analyzer.top_director_works()
    print('Director más frecuente:', director or 'Ninguno')
    print(works.to_string(index=False))
    print('Duración media por país:\n', analyzer.movie_duration_by_country())

    plotter.countries(analyzer.top_countries())
    plotter.genres(analyzer.genre_counts())
    movies, countries = analyzer.boxplot_data()
    plotter.movie_durations(movies, countries)
    plt.show()


if __name__ == '__main__':
    main()
