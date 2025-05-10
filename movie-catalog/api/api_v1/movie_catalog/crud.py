import logging
import json
from redis import Redis
from pydantic import BaseModel, ValidationError

from config import (
    STORAGE_PATH,
    REDIS_HOST,
    REDIS_PORT,
    REDIS_DB_MOVIE_CATALOG,
    REDIS_MOVIE_CATALOG_HASH_NAME,
)
from schemas.movie_catalog import Movie, MovieCreate, MovieUpdate, MoviePartialUpdate

logger = logging.getLogger(__name__)
redis = Redis(
    host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB_MOVIE_CATALOG, decode_responses=True
)


class MovieCatalogStorage(BaseModel):
    movie_catalog: dict[str, Movie] = {}

    def save_storage(self) -> None:
        STORAGE_PATH.write_text(self.model_dump_json(indent=2), encoding="utf-8")
        logger.info("Finish saving movie catalog.")

    def save_data(self, movie: Movie) -> None:
        redis.hset(
            name=REDIS_MOVIE_CATALOG_HASH_NAME,
            key=movie.slug,
            value=movie.model_dump_json(),
        )
        logger.debug("Finish saving data to redis.")

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
        return [
            Movie.model_validate_json(value)
            for value in redis.hvals(name=REDIS_MOVIE_CATALOG_HASH_NAME)
        ]

    def get_by_slug(self, slug: str) -> Movie | None:
        if data := redis.hget(name=REDIS_MOVIE_CATALOG_HASH_NAME, key=slug):
            return Movie.model_validate_json(data)
        return None

    def create(self, create_movie: MovieCreate) -> Movie:
        movie = Movie(
            **create_movie.model_dump(),
        )
        self.save_data(movie)
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
        self.save_data(movie)
        logger.debug("Update movie <%s>.", movie.slug)
        return movie

    def partial_update(self, movie: Movie, updated_movie: MoviePartialUpdate) -> Movie:
        for field, value in updated_movie.model_dump(exclude_unset=True).items():
            setattr(movie, field, value)
        self.save_data(movie)
        logger.debug("Partial update movie <%s>.", movie.slug)
        return movie


storage = MovieCatalogStorage()
