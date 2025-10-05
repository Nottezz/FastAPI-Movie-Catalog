class MovieCatalogBaseError(Exception):
    """
    Base exception class for Movie Catalog
    """


class MovieAlreadyExists(MovieCatalogBaseError):
    """
    Exception raised when a movie already exists
    """
