import pytest

from croatian_locator.exceptions import CityNotFoundError
from croatian_locator.models import City, County, Region
from croatian_locator.service import CroatianLocationService


@pytest.fixture
def cakovec() -> City:
    return City(
        name="Čakovec",
        county=County(
            name="Međimurje County",
        ),
        broad_region=Region(
            name="Central Croatia",
            category="broad",
        ),
        traditional_regions=(
            Region(
                name="Međimurje",
                category="traditional",
            ),
        ),
    )


@pytest.fixture
def service(cakovec: City) -> CroatianLocationService:
    cities = [
        cakovec,
        City(
            name="Šibenik",
            county=County(
                name="Šibenik-Knin County",
            ),
            broad_region=Region(
                name="Dalmatia",
                category="broad",
            ),
            traditional_regions=(
                Region(
                    name="Dalmatia",
                    category="traditional",
                ),
            ),
        ),
        City(
            name="Đakovo",
            county=County(
                name="Osijek-Baranja County",
            ),
            broad_region=Region(
                name="Eastern Croatia",
                category="broad",
            ),
            traditional_regions=(
                Region(
                    name="Slavonia",
                    category="traditional",
                ),
            ),
        ),
    ]

    return CroatianLocationService(cities)


def test_find_city_with_exact_name(service: CroatianLocationService, cakovec: City):
    city = service.find_city("Čakovec")

    assert city is cakovec


def test_find_city_with_lowercase_name(service: CroatianLocationService):
    city = service.find_city("čakovec")

    assert city.name == "Čakovec"


def test_find_city_with_uppercase_name(service: CroatianLocationService):
    city = service.find_city("ČAKOVEC")

    assert city.name == "Čakovec"


def test_find_city_without_diacritics(service: CroatianLocationService):
    cakovec = service.find_city("Cakovec")
    sibenik = service.find_city("Sibenik")
    dakovo = service.find_city("Dakovo")

    assert cakovec.name == "Čakovec"
    assert sibenik.name == "Šibenik"
    assert dakovo.name == "Đakovo"


def test_find_city_ignores_surrounding_whitespace(service: CroatianLocationService):
    city = service.find_city("  Cakovec  ")

    assert city.name == "Čakovec"


def test_find_unknown_city_raises_error(service: CroatianLocationService):
    with pytest.raises(CityNotFoundError) as exception_info:
        service.find_city("London")

    assert exception_info.value.city_name == "London"
    assert str(exception_info.value) == (
        'No Croatian city was found for "London".'
    )


def test_find_city_preserves_original_spelling(service: CroatianLocationService):
    city = service.find_city("DAKOVO")

    assert city.name == "Đakovo"