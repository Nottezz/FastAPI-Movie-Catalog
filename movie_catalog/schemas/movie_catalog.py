from pydantic import AnyHttpUrl, BaseModel, Field

DESCRIPTION_MAX_LENGTH = 500
DESCRIPTION_MIN_LENGTH = 20


class MovieBase(BaseModel):
    title: str
    description: str
    year_released: int
    rating: float
    original_link: AnyHttpUrl | None = None


class MovieCreate(MovieBase):
    """
    Модель для создания фильмов
    """

    slug: str = Field(
        ...,
        min_length=3,
        max_length=50,
        title="Slug",
    )
    title: str = Field(
        ...,
        min_length=3,
        max_length=50,
        title="Title",
    )
    description: str = Field(
        ...,
        title="Description",
        min_length=DESCRIPTION_MIN_LENGTH,
        max_length=DESCRIPTION_MAX_LENGTH,
    )
    year_released: int = Field(
        1900,
        ge=1900,
        le=9999,
        title="Year released",
    )
    rating: float = Field(
        1.0,
        ge=0.0,
        le=10.0,
        title="Rating",
    )
    original_link: AnyHttpUrl | None = None


class MovieUpdate(MovieBase):
    """
    Модель для обновления фильма
    """

    title: str = Field(
        ...,
        min_length=3,
        max_length=50,
        title="Title",
    )
    description: str = Field(
        ...,
        title="Description",
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
        title="Rating",
    )


class MovieUpdateForm(MovieBase):
    """
    Модель для обновления фильма в форме
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
    rating: float | None = Field(
        None,
        ge=0.0,
        le=10.0,
        title="Movie rating",
    )


class MoviePartialUpdate(BaseModel):
    """
    Модель для частичного редактирования полей
    """

    title: str | None = Field(
        None,
        min_length=3,
        max_length=50,
        title="Movie title",
    )
    description: str | None = Field(
        None,
        min_length=20,
        max_length=500,
        title="Movie description",
    )
    year_released: int | None = Field(
        None,
        ge=1900,
        le=9999,
        title="Year released",
    )
    rating: float | None = Field(
        None,
        ge=0.0,
        le=10.0,
        title="Movie rating",
    )
    original_link: AnyHttpUrl | None = None


class MovieRead(MovieBase):
    """
    Модель для чтения фильма
    """

    slug: str


class Movie(MovieBase):
    """
    Модель фильма
    """

    slug: str
    note: str = ""
