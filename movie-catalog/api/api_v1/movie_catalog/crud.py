from pydantic import BaseModel

from schemas.movie_catalog import Movie, MovieCreate


class MovieCatalogStorage(BaseModel):
    movie_catalog: dict[str, Movie] = {}

    def get(self) -> list[Movie]:
        return list(self.movie_catalog.values())

    def get_by_slug(self, slug: str) -> Movie | None:
        return self.movie_catalog.get(slug, None)

    def create(self, create_movie: MovieCreate) -> Movie:
        movie = Movie(
            **create_movie.model_dump(),
        )
        self.movie_catalog[create_movie.slug] = movie
        return movie

    def delete_by_slug(self, slug: str) -> None:
        self.movie_catalog.pop(slug, None)

    def delete(self, movie: Movie) -> None:
        self.delete_by_slug(movie.slug)


storage = MovieCatalogStorage()

storage.create(
    MovieCreate(
        slug="udivitelnoe-puteshestvie-doktora-dulittla",
        title="Удивительное путешествие доктора Дулиттла",
        description="Семь лет назад доктор Дулиттл, прославленный врач-ветеринар, живущий в викторианской Англии, потерял свою жену. Теперь он ведет затворнический образ жизни, скрывшись за высокими стенами своего поместья. Экзотические животные из его коллекции – его единственная компания.",
        year_released=2020,
        rating=6.4,
    )
)

storage.create(
    MovieCreate(
        slug="sdelano-v-amerike",
        title="Сделано в Америке",
        description="Он был самым юным пилотом Боинга 747 в США, а уже через несколько лет стал одним из богатейших людей в Америке. Его стиль жизни был столь же экстремальным, как и его бизнес. Закрытые приемы, роскошные блондинки, крутые тачки и рисковые сделки. Он обладал талантом делать деньги из воздуха.",
        year_released=2017,
        rating=7.3,
    )
)

storage.create(
    MovieCreate(
        slug="linkoln",
        title="Линкольн",
        description="1865 год. Шестнадцатый президент США Авраам Линкольн находится на пике популярности. Но перед ним стоят серьёзные задачи: провести запрещающую рабство поправку к Конституции через Палату представителей и завершить Гражданскую войну.",
        year_released=2012,
        rating=6.9,
    )
)
