from pydantic import BaseModel


class MovieCatalogBase(BaseModel):
    id: int
    title: str
    description: str
    year_released: int
    rating: float


class MovieCatalog(MovieCatalogBase):
    pass
