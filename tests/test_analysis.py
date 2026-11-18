import pandas as pd
from src.netflix_analisis.analysis import NetflixAnalyzer
from src.netflix_analisis.cleaning import NetflixCleaner
from src.netflix_analisis.config import Config


def sample():
    return pd.DataFrame([
        dict(show_id='1', title='A', type='Movie', release_year='2018', date_added='Jan 1, 2020', duration='90 min', listed_in='Drama, Comedy', director='Ana, Luis', cast=None, country='RD', rating=None),
        dict(show_id='2', title='B', type='TV Show', release_year='2005', date_added='bad', duration='2 Seasons', listed_in='Drama', director=None, cast=None, country=None, rating=None),
        dict(show_id='3', title='C', type='Movie', release_year='2022', date_added='Feb 2, 2021', duration='120 min', listed_in='Comedy', director='Ana', cast=None, country='RD', rating=None),
    ])


def test_clean_does_not_mutate_input():
    original = sample()
    cleaned = NetflixCleaner(Config()).clean(original)
    assert pd.isna(original.loc[1, 'director'])
    assert cleaned.loc[1, 'director'] == 'Desconocido'
    assert cleaned['release_year'].dtype.name == 'Int64'
    assert pd.isna(cleaned.loc[1, 'duration_minutes'])
    assert cleaned.loc[0, 'duration_minutes'] == 90
    assert pd.isna(cleaned.loc[1, 'date_added'])


def test_analysis():
    analyzer = NetflixAnalyzer(NetflixCleaner(Config()).clean(sample()))
    assert len(analyzer.titles_after(2010)) == 2
    assert analyzer.top_countries().loc['RD'] == 2
    assert analyzer.genre_counts().loc['Comedy'] == 2
    assert analyzer.director_counts().loc['Ana'] == 2
    director, works = analyzer.top_director_works()
    assert director == 'Ana' and len(works) == 2
    assert analyzer.movie_duration_by_country().loc['RD', 'promedio'] == 105
    movies, countries = analyzer.boxplot_data(min_movies=2)
    assert countries == ['RD'] and len(movies) == 2


def test_no_directors():
    cleaned = NetflixCleaner(Config()).clean(sample().assign(director=None))
    director, works = NetflixAnalyzer(cleaned).top_director_works()
    assert director is None and works.empty
