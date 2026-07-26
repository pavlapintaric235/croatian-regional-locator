from dataclasses import FrozenInstanceError

import pytest

from croatian_locator.models import City, County, Region


def test_county_stores_name():
    county = County(name="Međimurje County")

    assert county.name == "Međimurje County"


def test_region_stores_name_and_category():
    region = Region(
        name="Central Croatia",
        category="broad",
    )

    assert region.name == "Central Croatia"
    assert region.category == "broad"


def test_city_uses_composition():
    county = County(name="Međimurje County")

    broad_region = Region(
        name="Central Croatia",
        category="broad",
    )

    traditional_region = Region(
        name="Međimurje",
        category="traditional",
    )

    city = City(
        name="Čakovec",
        county=county,
        broad_region=broad_region,
        traditional_regions=(traditional_region,),
    )

    assert city.name == "Čakovec"
    assert city.county is county
    assert city.broad_region is broad_region
    assert city.traditional_regions == (traditional_region,)


def test_city_can_have_multiple_traditional_regions():
    county = County(name="Vukovar-Syrmia County")

    broad_region = Region(
        name="Eastern Croatia",
        category="broad",
    )

    slavonia = Region(
        name="Slavonia",
        category="traditional",
    )

    syrmia = Region(
        name="Syrmia",
        category="historical",
    )

    city = City(
        name="Vukovar",
        county=county,
        broad_region=broad_region,
        traditional_regions=(slavonia, syrmia),
    )

    assert city.traditional_regions == (slavonia, syrmia)
    assert len(city.traditional_regions) == 2


def test_dataclass_objects_compare_by_value():
    first_county = County(name="Istria County")
    second_county = County(name="Istria County")

    assert first_county == second_county
    """the test proves that the dataclass compares County objects by their stored attribute values, not whether both variables point to the exact same object"""

def test_county_is_frozen():
    county = County(name="Istria County")

    with pytest.raises(FrozenInstanceError):
        county.name = "Međimurje County"