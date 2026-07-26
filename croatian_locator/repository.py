import json
from json import JSONDecodeError
from pathlib import Path

from croatian_locator.exceptions import InvalidLocationDataError
from croatian_locator.models import City, County, Region


class JsonLocationRepository:
    """Load and convert Croatian location data from a JSON file."""

    def __init__(self, file_path: str | Path):
        self._file_path = Path(file_path)

    def load_cities(self):
        """Load, validate, and return all cities from the JSON file."""
        raw_data = self._read_json()

        if not isinstance(raw_data, list):
            raise InvalidLocationDataError(
                "The top-level JSON value must be a list."
            )

        return [
            self._build_city(city_data, index)
            for index, city_data in enumerate(raw_data)
        ]

    def _read_json(self) -> object:
        """Read and decode the configured JSON file."""
        try:
            with self._file_path.open(
                mode="r",
                encoding="utf-8",
            ) as file:
                return json.load(file)

        except FileNotFoundError as error:
            raise InvalidLocationDataError(
                f'Location data file not found: "{self._file_path}".'
            ) from error

        except JSONDecodeError as error:
            raise InvalidLocationDataError(
                f'Location data file contains invalid JSON: '
                f'"{self._file_path}".'
            ) from error

        except OSError as error:
            raise InvalidLocationDataError(
                f'Location data file could not be read: '
                f'"{self._file_path}".'
            ) from error

    def _build_city(
        self,
        city_data: object,
        index: int,
    ) -> City:
        """Validate one city dictionary and convert it into a City object."""
        if not isinstance(city_data, dict):
            raise InvalidLocationDataError(
                f"City entry at index {index} must be a JSON object."
            )

        required_fields = (
            "name",
            "county",
            "broad_region",
            "traditional_regions",
        )

        missing_fields = [
            field
            for field in required_fields
            if field not in city_data
        ]

        if missing_fields:
            missing_fields_text = ", ".join(missing_fields)

            raise InvalidLocationDataError(
                f"City entry at index {index} is missing required "
                f"field(s): {missing_fields_text}."
            )

        name = city_data["name"]
        county_name = city_data["county"]
        broad_region_name = city_data["broad_region"]
        traditional_regions_data = city_data["traditional_regions"]

        if not isinstance(name, str) or not name.strip():
            raise InvalidLocationDataError(
                f'Field "name" in city entry at index {index} '
                f"must be a non-empty string."
            )

        if not isinstance(county_name, str) or not county_name.strip():
            raise InvalidLocationDataError(
                f'Field "county" in city entry at index {index} '
                f"must be a non-empty string."
            )

        if (
            not isinstance(broad_region_name, str)
            or not broad_region_name.strip()
        ):
            raise InvalidLocationDataError(
                f'Field "broad_region" in city entry at index {index} '
                f"must be a non-empty string."
            )

        if (
            not isinstance(traditional_regions_data, list)
            or not traditional_regions_data
        ):
            raise InvalidLocationDataError(
                f'Field "traditional_regions" in city entry at index '
                f"{index} must be a non-empty list."
            )

        traditional_regions = tuple(
            self._build_region(
                region_data,
                city_index=index,
                region_index=region_index,
            )
            for region_index, region_data in enumerate(
                traditional_regions_data
            )
        )

        county = County(name=county_name)

        broad_region = Region(
            name=broad_region_name,
            category="broad",
        )

        return City(
            name=name,
            county=county,
            broad_region=broad_region,
            traditional_regions=traditional_regions,
        )

    def _build_region(
        self,
        region_data: object,
        city_index: int,
        region_index: int,
    ) -> Region:
        """Validate one region dictionary and convert it into a Region object."""
        if not isinstance(region_data, dict):
            raise InvalidLocationDataError(
                f"Traditional region at index {region_index} in city "
                f"entry {city_index} must be a JSON object."
            )

        required_fields = (
            "name",
            "category",
        )

        missing_fields = [
            field
            for field in required_fields
            if field not in region_data
        ]

        if missing_fields:
            missing_fields_text = ", ".join(missing_fields)

            raise InvalidLocationDataError(
                f"Traditional region at index {region_index} in city "
                f"entry {city_index} is missing required field(s): "
                f"{missing_fields_text}."
            )

        name = region_data["name"]
        category = region_data["category"]

        if not isinstance(name, str) or not name.strip():
            raise InvalidLocationDataError(
                f'Field "name" in traditional region at index '
                f"{region_index} in city entry {city_index} must be "
                f"a non-empty string."
            )

        if not isinstance(category, str) or not category.strip():
            raise InvalidLocationDataError(
                f'Field "category" in traditional region at index '
                f"{region_index} in city entry {city_index} must be "
                f"a non-empty string."
            )

        return Region(
            name=name,
            category=category,
        )