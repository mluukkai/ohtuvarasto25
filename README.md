[![CI](https://github.com/mluukkai/ohtuvarasto25/actions/workflows/main.yml/badge.svg)](https://github.com/mluukkai/ohtuvarasto25/actions/workflows/main.yml)

[![codecov](https://codecov.io/gh/mluukkai/ohtuvarasto25/graph/badge.svg?token=TARX4T76UM)](https://codecov.io/gh/mluukkai/ohtuvarasto25)

# Warehouse Management System

A Python-based warehouse management system with a Flask web UI.

## Features

- **Create Warehouses**: Create new warehouses with custom names and capacities
- **List Warehouses**: View all warehouses with their current status
- **Manage Content**: Add or remove content from warehouses
- **Delete Warehouses**: Remove warehouses that are no longer needed

## Installation

Install dependencies using Poetry:

```bash
poetry install
```

## Running the Web Application

To start the Flask web server:

```bash
cd src
poetry run python app.py
```

Then open your browser and navigate to `http://localhost:5000`

## Running Tests

Run all tests:

```bash
poetry run pytest
```

Run tests with coverage:

```bash
poetry run coverage run --branch -m pytest
poetry run coverage report
```

## Code Quality

Check code quality with pylint:

```bash
poetry run pylint src
```