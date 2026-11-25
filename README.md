# Croatian Regional Locator

Croatian Regional Locator is a Python command-line application that identifies the official Croatian county, broad geographical region, and one or more traditional, historical, or geographical regions associated with a Croatian city.
**Demo Video** - https://lnkd.in/p/dyP297Hp
The project contains 128 Croatian city-level entries and supports searches both with and without Croatian diacritics.

## Features

* Search for a Croatian city by name
* Case-insensitive search
* Diacritic-insensitive search
* Support for Croatian letters such as `č`, `ć`, `đ`, `š`, and `ž`
* Display the city’s official county in English
* Display its broad geographical region
* Display one or more traditional, historical, or geographical regions
* Continue searching until the user chooses to exit
* Load all location data from JSON
* Raise readable custom exceptions
* Automated testing with pytest
* Object-oriented architecture using composition

Examples of equivalent searches:

```text
Čakovec
čakovec
ČAKOVEC
Cakovec
cakovec
```

All of these return the original correctly spelled city name:

```text
Čakovec
```

## Example output

```text
CROATIAN REGIONAL LOCATOR

Enter a Croatian city, or enter 0 to exit: Cakovec

City: Čakovec
County: Međimurje County
Broad region: Central Croatia
Traditional regions: Međimurje

Enter a Croatian city, or enter 0 to exit: DAKOVO

City: Đakovo
County: Osijek-Baranja County
Broad region: Eastern Croatia
Traditional regions: Slavonia

Enter a Croatian city, or enter 0 to exit: 0
Goodbye!
```

## Technology

The project uses:

* Python
* Python standard-library modules
* JSON
* pytest

## Project structure

```text
croatian-regional-locator/
│
├── croatian_locator/
│   ├── __init__.py
│   ├── exceptions.py
│   ├── models.py
│   ├── normalization.py
│   ├── repository.py
│   └── service.py
│
├── data/
│   └── locations.json
│
├── tests/
│   ├── test_models.py
│   ├── test_normalization.py
│   ├── test_repository.py
│   └── test_service.py
│
├── main.py
├── README.md
├── requirements-dev.txt
└── .gitignore
```

## Architecture

The project separates its responsibilities into focused modules.

### `models.py`

Contains the domain models:

* `County`
* `Region`
* `City`

The models use frozen dataclasses because they represent stable geographical values.

A `City` contains:

* one `County` object
* one broad `Region` object
* a tuple of traditional, historical, or geographical `Region` objects

This demonstrates composition.

### `normalization.py`

Contains the text-normalization function used for city-name comparisons.

It:

1. removes leading and trailing whitespace
2. applies case folding
3. explicitly converts Croatian `đ` to `d`
4. applies Unicode decomposition
5. removes combining diacritic marks

Stored city names remain unchanged. Only comparison values are normalized.

### `exceptions.py`

Contains the custom exception hierarchy:

```text
Exception
└── LocationError
    ├── CityNotFoundError
    └── InvalidLocationDataError
```

`CityNotFoundError` is raised when no matching city exists.

`InvalidLocationDataError` is raised when the JSON file cannot be read or contains invalid data.

### `repository.py`

Contains `JsonLocationRepository`.

The repository:

* opens the JSON file
* decodes JSON
* validates the basic structure
* creates `County`, `Region`, and `City` objects
* returns a list of cities

It does not search cities or display terminal output.

### `service.py`

Contains `CroatianLocationService`.

The service:

* receives already-created `City` objects
* builds a normalized lookup dictionary
* finds cities using normalized names
* returns the original `City` object
* raises `CityNotFoundError` when no city matches

It does not read files or call `input()`.

### `main.py`

Contains the command-line interface.

It:

* creates the repository and service
* loads the dataset once
* reads user input
* displays results
* catches application exceptions
* repeats searches until the user enters `0`

## Object-oriented programming concepts

### Classes and objects

`County`, `Region`, and `City` are classes.

Individual places are represented by objects:

```python
county = County(name="Međimurje County")

region = Region(
    name="Međimurje",
    category="traditional",
)
```

### Dataclasses

The domain models use `@dataclass` to automatically generate:

* constructors
* readable representations
* value-based equality

### Immutability

The models use:

```python
@dataclass(frozen=True)
```

This prevents geographical values from being reassigned accidentally after an object is created.

### Composition

A city is not a type of county or region.

Instead, a city has a county and has regions:

```python
City(
    name="Čakovec",
    county=County(...),
    broad_region=Region(...),
    traditional_regions=(Region(...),),
)
```

Composition is more appropriate here than inheritance.

### Separation of responsibilities

Each class and module has one primary responsibility:

```text
Repository → loads data
Service → searches cities
Models → represent data
main.py → communicates with the user
```

## JSON data

All city information is stored in:

```text
data/locations.json
```

Example entry:

```json
{
    "name": "Čakovec",
    "county": "Međimurje County",
    "broad_region": "Central Croatia",
    "traditional_regions": [
        {
            "name": "Međimurje",
            "category": "traditional"
        }
    ]
}
```

JSON stores plain data rather than Python objects.

`JsonLocationRepository` converts each JSON dictionary into composed domain objects.

The dataset contains 128 city-level entries, including Zagreb.

## Regional classification note

Croatian counties are official administrative units.

Traditional, historical, and geographical regions such as Slavonia, Baranja, Syrmia, Kvarner, Banovina, Istria, Podravina, and Dalmatia are not all legally defined administrative territories.

Their borders and classifications may vary depending on historical, cultural, and geographical interpretation.

The regional values in this project are intended as practical educational classifications and should not be treated as official administrative boundaries.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/pavlapintaric235/croatian-regional-locator.git
cd croatian-regional-locator
```

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

Windows Command Prompt:

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install development requirements

```bash
python -m pip install -r requirements-dev.txt
```

The application itself uses only Python’s standard library. Pytest is installed for running the automated tests.

## Running the application

From the project root:

```bash
python main.py
```

Enter a Croatian city when prompted.

Enter:

```text
0
```

to exit.

## Running the tests

Run the complete test suite:

```bash
python -m pytest
```

Run tests with detailed names:

```bash
python -m pytest -v
```

Run one test file:

```bash
python -m pytest tests/test_service.py -v
```

The test suite covers:

* domain models
* dataclass equality
* frozen objects
* composition
* case-insensitive normalization
* diacritic-insensitive normalization
* explicit handling of `đ`
* malformed JSON
* missing JSON files
* invalid data structures
* missing required fields
* multiple traditional regions
* exact searches
* uppercase and lowercase searches
* searches without diacritics
* unknown-city errors
* preservation of original Croatian spelling
* completeness of the 128-city dataset

## Search normalization

The search process does not alter the stored city names.

For example:

```text
Stored name: Đakovo
Lookup key: dakovo
```

A search for any of the following:

```text
Đakovo
đakovo
ĐAKOVO
Dakovo
dakovo
```

uses the normalized lookup key:

```text
dakovo
```

The service then returns the original object containing:

```text
Đakovo
```

## Custom exceptions

The project defines application-specific errors instead of exposing only low-level Python exceptions.

Example:

```python
raise CityNotFoundError("London")
```

Readable message:

```text
No Croatian city was found for "London".
```

The service raises the error because it detects the missing city.

`main.py` catches the error because the command-line interface decides how to display it.

## Purpose

This project was built as a Python portfolio project to demonstrate:

* practical object-oriented programming
* composition
* dataclasses
* type hints
* clean module responsibilities
* JSON file handling
* custom exceptions
* Unicode text processing
* dictionary-based lookup
* automated testing with pytest

The project intentionally avoids unnecessary frameworks and abstractions so that its design and behavior remain understandable and explainable.
