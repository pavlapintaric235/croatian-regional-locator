from croatian_locator.exceptions import CityNotFoundError
from croatian_locator.models import City
from croatian_locator.normalization import normalize_text


class CroatianLocationService:
    """Find Croatian cities using normalized city names."""

    def __init__(self, cities: list[City]):
        self._cities_by_name = {
            normalize_text(city.name): city
            for city in cities
        }

    def find_city(self, city_name: str) -> City:
        """Return the city matching the supplied name."""
        normalized_name = normalize_text(city_name)

        if normalized_name not in self._cities_by_name:
            raise CityNotFoundError(city_name)

        return self._cities_by_name[normalized_name]
        