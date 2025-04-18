import logging

from pydantic import BaseModel, ValidationError

from config import STORAGE_PATH
from schemas.movie_catalog import Movie, MovieCreate, MovieUpdate, MoviePartialUpdate

logger = logging.getLogger(__name__)


class MovieCatalogStorage(BaseModel):
    movie_catalog: dict[str, Movie] = {}

    def save_storage(self) -> None:
        STORAGE_PATH.write_text(self.model_dump_json(indent=2), encoding="utf-8")
        logger.info("Finish saving movie catalog.")

    @classmethod
    def load_storage(cls) -> "MovieCatalogStorage":
        if not STORAGE_PATH.exists():
            logger.warning("Movie catalog storage does not exist.")
            return MovieCatalogStorage()
        return cls.model_validate_json(STORAGE_PATH.read_text())

    def init_storage_from_state(self) -> None:
        try:
            data = MovieCatalogStorage.load_storage()
        except ValidationError:
            self.save_storage()
            logger.warning(
                "Movie catalog storage validation failed! File has been rewritten."
            )
            return
        self.movie_catalog.update(data.movie_catalog)
        logger.warning("Recovered data from storage file.")

    def get(self) -> list[Movie]:
        return list(self.movie_catalog.values())

    def get_by_slug(self, slug: str) -> Movie | None:
        return self.movie_catalog.get(slug, None)

    def create(self, create_movie: MovieCreate) -> Movie:
        movie = Movie(
            **create_movie.model_dump(),
        )
        self.movie_catalog[create_movie.slug] = movie
        logger.debug("Add movie <%s> to catalog.", create_movie.slug)
        return movie

    def delete_by_slug(self, slug: str) -> None:
        self.movie_catalog.pop(slug, None)
        logger.debug("Remove movie <%s> from catalog.", slug)

    def delete(self, movie: Movie) -> None:
        self.delete_by_slug(movie.slug)

    def update(self, movie: Movie, updated_movie: MovieUpdate) -> Movie:
        for field, value in updated_movie:
            setattr(movie, field, value)
        logger.debug("Update movie <%s>.", movie.slug)
        return movie

    def partial_update(self, movie: Movie, updated_movie: MoviePartialUpdate) -> Movie:
        for field, value in updated_movie.model_dump(exclude_unset=True).items():
            setattr(movie, field, value)
        logger.debug("Partial update movie <%s>.", movie.slug)
        return movie


storage = MovieCatalogStorage()
