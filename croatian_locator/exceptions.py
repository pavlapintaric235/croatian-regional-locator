class LocationError(Exception):
    """Base exception for errors raised by Croatian Regional Locator."""


class CityNotFoundError(LocationError):
    """Raised when a requested Croatian city cannot be found."""

    def __init__(self, city_name: str):
        self.city_name = city_name
        message = f'No Croatian city was found for "{city_name}".'
        super().__init__(message)


class InvalidLocationDataError(LocationError):
    """Raised when location data cannot be loaded or validated."""