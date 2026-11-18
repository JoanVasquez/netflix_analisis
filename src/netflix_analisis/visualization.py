import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


class NetflixPlotter:
    """Solo recibe resultados; no carga ni modifica datos."""

    @staticmethod
    def countries(top_countries: pd.Series):
        fig, ax = plt.subplots(figsize=(10, 6))
        top_countries.plot(kind='bar', ax=ax, color='blue')
        ax.set(title='Los 10 países con más títulos después de 2010',
               xlabel='País', ylabel='Cantidad de títulos')
        ax.tick_params(axis='x', labelrotation=45)
        for label in ax.get_xticklabels():
            label.set_ha('right')
        fig.tight_layout()
        return fig

    @staticmethod
    def genres(counts: pd.Series):
        fig, ax = plt.subplots(figsize=(8, 8))
        values = counts.head(5).copy()
        others = counts.iloc[5:].sum()
        if others > 0:
            values.loc['Otros'] = others
        if not values.empty and values.sum() > 0:
            ax.pie(values.to_numpy(), labels=values.index,
                   autopct='%1.1f%%', startangle=90)
        else:
            ax.text(0.5, 0.5, 'No hay datos de géneros', ha='center', va='center')
        ax.set_title('Distribución de los géneros más comunes')
        fig.tight_layout()
        return fig

    @staticmethod
    def movie_durations(movies: pd.DataFrame, country_order: list[str]):
        fig, ax = plt.subplots(figsize=(12, 6))
        if not movies.empty and country_order:
            sns.boxplot(data=movies, x='country', y='duration_minutes',
                        order=country_order, ax=ax)
        else:
            ax.text(0.5, 0.5, 'No hay países con suficientes películas',
                    ha='center', va='center', transform=ax.transAxes)
        ax.set(title='Distribución de la duración de películas por país',
               xlabel='País', ylabel='Duración en minutos')
        ax.tick_params(axis='x', labelrotation=45)
        for label in ax.get_xticklabels():
            label.set_ha('right')
        fig.tight_layout()
        return fig
