from pydantic import BaseModel, Field


class MovieBase(BaseModel):
    title: str
    description: str
    year_released: int
    rating: float


class MovieCreate(MovieBase):
    """
    Модель для создания фильмов
    """

    slug: str = Field(
        ...,
        min_length=3,
        max_length=50,
        title="Movie slug",
    )
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


class MovieUpdate(MovieBase):
    """
    Модель для обновления фильма
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


class MoviePartialUpdate(MovieBase):
    title: str | None = Field(
        None,
        min_length=3,
        max_length=50,
        title="Movie title",
    )
    description: str | None = Field(
        None,
        title="Movie description",
        min_length=20,
        max_length=500,
    )
    year_released: int | None = Field(
        None,
        ge=0,
        le=9999,
        title="Year released",
    )
    rating: float | None = Field(
        None,
        ge=0.0,
        le=10.0,
        title="Movie rating",
    )


class Movie(MovieBase):
    """
    Модель фильма
    """

    slug: str
