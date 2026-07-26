from dataclasses import dataclass


@dataclass(frozen=True)
class County:
    """Represent an official Croatian county."""

    name: str


@dataclass(frozen=True)
class Region:
    """Represent a geographical, traditional, or historical region."""

    name: str
    category: str


@dataclass(frozen=True)
class City:
    """Represent a Croatian city and its regional relationships."""

    name: str
    county: County
    broad_region: Region
    traditional_regions: tuple[Region, ...]