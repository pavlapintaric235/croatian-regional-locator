from pathlib import Path

from croatian_locator.exceptions import (
    CityNotFoundError,
    InvalidLocationDataError,
)
from croatian_locator.models import City
from croatian_locator.repository import JsonLocationRepository
from croatian_locator.service import CroatianLocationService


def create_location_service() -> CroatianLocationService:
    """Load the location data and create the search service."""
    project_directory = Path(__file__).resolve().parent
    data_file = project_directory / "data" / "locations.json"

    repository = JsonLocationRepository(data_file)
    cities = repository.load_cities()

    return CroatianLocationService(cities)


def display_city(city: City) -> None:
    """Display a city and its geographical information."""
    traditional_region_names = ", ".join(
        region.name
        for region in city.traditional_regions
    )

    print()
    print(f"City: {city.name}")
    print(f"County: {city.county.name}")
    print(f"Broad region: {city.broad_region.name}")
    print(f"Traditional regions: {traditional_region_names}")
    print()


def main() -> None:
    """Run the Croatian Regional Locator command-line interface."""
    print("CROATIAN REGIONAL LOCATOR")
    print()

    try:
        service = create_location_service()
    except InvalidLocationDataError as error:
        print(f"Unable to start the application: {error}")
        return

    while True:
        city_name = input(
            "Enter a Croatian city, or enter 0 to exit: "
        ).strip()

        if city_name == "0":
            print("Goodbye!")
            break

        if not city_name:
            print("Please enter a city name or 0 to exit.")
            print()
            continue

        try:
            city = service.find_city(city_name)
        except CityNotFoundError as error:
            print()
            print(error)
            print()
            continue

        display_city(city)


if __name__ == "__main__":
    main()