import json
from pathlib import Path

import pytest

from croatian_locator.exceptions import InvalidLocationDataError
from croatian_locator.models import City, County, Region
from croatian_locator.repository import JsonLocationRepository


@pytest.fixture
def valid_location_data() -> list[dict[str, object]]:
    return [
        {
            "name": "Čakovec",
            "county": "Međimurje County",
            "broad_region": "Central Croatia",
            "traditional_regions": [
                {
                    "name": "Međimurje",
                    "category": "traditional",
                }
            ],
        }
    ]


def write_json_file(
    file_path: Path,
    data: object,
) -> None:
    file_path.write_text(
        json.dumps(
            data,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )


def test_load_cities_successfully(
    tmp_path: Path,
    valid_location_data: list[dict[str, object]],
) -> None:
    file_path = tmp_path / "locations.json"
    write_json_file(file_path, valid_location_data)

    repository = JsonLocationRepository(file_path)

    cities = repository.load_cities()

    expected_city = City(
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

    assert cities == [expected_city]


def test_load_cities_when_file_does_not_exist(
    tmp_path: Path,
) -> None:
    missing_file = tmp_path / "missing_locations.json"
    repository = JsonLocationRepository(missing_file)

    with pytest.raises(
        InvalidLocationDataError,
        match="not found",
    ):
        repository.load_cities()


def test_load_cities_from_malformed_json(
    tmp_path: Path,
) -> None:
    file_path = tmp_path / "locations.json"
    file_path.write_text(
        '{"name": "Čakovec",',
        encoding="utf-8",
    )

    repository = JsonLocationRepository(file_path)

    with pytest.raises(
        InvalidLocationDataError,
        match="invalid JSON",
    ):
        repository.load_cities()


def test_load_cities_rejects_wrong_top_level_type(
    tmp_path: Path,
) -> None:
    file_path = tmp_path / "locations.json"

    write_json_file(
        file_path,
        {
            "name": "Čakovec",
        },
    )

    repository = JsonLocationRepository(file_path)

    with pytest.raises(
        InvalidLocationDataError,
        match="top-level JSON value must be a list",
    ):
        repository.load_cities()


def test_load_cities_rejects_missing_required_field(
    tmp_path: Path,
) -> None:
    file_path = tmp_path / "locations.json"

    invalid_data = [
        {
            "name": "Čakovec",
            "broad_region": "Central Croatia",
            "traditional_regions": [
                {
                    "name": "Međimurje",
                    "category": "traditional",
                }
            ],
        }
    ]

    write_json_file(file_path, invalid_data)

    repository = JsonLocationRepository(file_path)

    with pytest.raises(
        InvalidLocationDataError,
        match="county",
    ):
        repository.load_cities()


def test_load_city_with_multiple_traditional_regions(
    tmp_path: Path,
) -> None:
    file_path = tmp_path / "locations.json"

    location_data = [
        {
            "name": "Vinkovci",
            "county": "Vukovar-Syrmia County",
            "broad_region": "Eastern Croatia",
            "traditional_regions": [
                {
                    "name": "Slavonia",
                    "category": "traditional",
                },
                {
                    "name": "Syrmia",
                    "category": "historical",
                },
            ],
        }
    ]

    write_json_file(file_path, location_data)

    repository = JsonLocationRepository(file_path)

    cities = repository.load_cities()

    assert cities[0].traditional_regions == (
        Region(
            name="Slavonia",
            category="traditional",
        ),
        Region(
            name="Syrmia",
            category="historical",
       ),
    )