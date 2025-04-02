from pydantic import BaseModel, Field


class MovieCatalogBase(BaseModel):
    title: str
    description: str
    year_released: int
    rating: float


class MovieCatalogCreate(MovieCatalogBase):
    """
    Модель для создания фильмов
    """

    title: str = Field(
        ...,
        min_length=3,
        max_length=50,
        title="Movie title",
    )
    description: str = Field(
        ...,
        title="Movie description",
        min_length=20,
        max_length=500,
    )
    year_released: int = Field(
        1900,
        ge=0,
        le=9999,
        title="Year released",
    )
    rating: float = Field(
        1.0,
        ge=0.0,
        le=10.0,
        title="Movie rating",
    )


class MovieCatalog(MovieCatalogBase):
    """
    Модель каталога фильмов
    """

    id: int = Field(
        ge=1,
    )
