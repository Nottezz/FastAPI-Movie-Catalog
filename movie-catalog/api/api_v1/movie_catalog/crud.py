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

    def get(self) -> list[Movie]:
        return list(self.movie_catalog.values())

    def get_by_slug(self, slug: str) -> Movie | None:
        return self.movie_catalog.get(slug, None)

    def create(self, create_movie: MovieCreate) -> Movie:
        movie = Movie(
            **create_movie.model_dump(),
        )
        self.movie_catalog[create_movie.slug] = movie
        self.save_storage()
        return movie

    def delete_by_slug(self, slug: str) -> None:
        self.movie_catalog.pop(slug, None)
        self.save_storage()

    def delete(self, movie: Movie) -> None:
        self.delete_by_slug(movie.slug)

    def update(self, movie: Movie, updated_movie: MovieUpdate) -> Movie:
        for field, value in updated_movie:
            setattr(movie, field, value)
        self.save_storage()
        return movie

    def partial_update(self, movie: Movie, updated_movie: MoviePartialUpdate) -> Movie:
        for field, value in updated_movie.model_dump(exclude_unset=True).items():
            setattr(movie, field, value)
        self.save_storage()
        return movie


try:
    storage = MovieCatalogStorage.load_storage()
    logger.warning("Movie catalog storage loaded from file.")
except ValidationError:
    storage = MovieCatalogStorage()
    storage.save_storage()
    logger.warning("Movie catalog storage validation failed! File has been rewritten.")
