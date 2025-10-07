import logging
from typing import cast

from pydantic import BaseModel
from redis import Redis

from movie_catalog.config import settings
from movie_catalog.exceptions import MovieAlreadyExists
from movie_catalog.schemas.movie_catalog import (
    Movie,
    MovieCreate,
    MoviePartialUpdate,
    MovieUpdate,
)

logger = logging.getLogger(__name__)

redis = Redis(
    host=settings.redis.connection.host,
    port=settings.redis.connection.port,
    db=settings.redis.db.movie_catalog,
    decode_responses=True,
)


class MovieCatalogStorage(BaseModel):
    hast_name: str

    def save_data(self, movie: Movie) -> None:
        redis.hset(
            name=self.hast_name,
            key=movie.slug,
            value=movie.model_dump_json(),
        )
        logger.debug("Finish saving data to redis.")

    def get(self) -> list[Movie]:
        return [
            Movie.model_validate_json(value)
            for value in cast(set[str], redis.hvals(name=self.hast_name))
        ]

    def get_by_slug(self, slug: str) -> Movie | None:
        if data := redis.hget(name=self.hast_name, key=slug):
            return Movie.model_validate_json(data)
        return None

    def exists(self, slug: str) -> bool:
        return bool(redis.hexists(name=self.hast_name, key=slug))

    def create(self, create_movie: MovieCreate) -> Movie:
        movie = Movie(
            **create_movie.model_dump(),
        )
        self.save_data(movie)
        logger.debug("Add movie <%s> to catalog.", create_movie.slug)
        return movie

    def create_or_rise_if_exists(self, create_movie: MovieCreate) -> Movie:
        if not self.exists(create_movie.slug):
            return self.create(create_movie)

        logger.error("Movie with slug <%s> already exists.", create_movie.slug)
        raise MovieAlreadyExists(create_movie.slug)

    def delete_by_slug(self, slug: str) -> None:
        redis.hdel(self.hast_name, slug)
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


storage = MovieCatalogStorage(hast_name=settings.redis.collections.movie_catalog_hash)
