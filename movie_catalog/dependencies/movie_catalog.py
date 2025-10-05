from typing import Annotated

from fastapi import Depends, Request
from storage.movie_catalog import MovieCatalogStorage


def get_movie_catalog_storage(
    request: Request,
) -> MovieCatalogStorage:
    return request.app.state.movie_catalog_storage


GetMovieCatalogStorage = Annotated[
    MovieCatalogStorage,
    Depends(get_movie_catalog_storage),
]
