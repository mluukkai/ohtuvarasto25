[![CI](https://github.com/mluukkai/ohtuvarasto25/actions/workflows/main.yml/badge.svg)](https://github.com/mluukkai/ohtuvarasto25/actions/workflows/main.yml)

[![codecov](https://codecov.io/gh/mluukkai/ohtuvarasto25/graph/badge.svg?token=TARX4T76UM)](https://codecov.io/gh/mluukkai/ohtuvarasto25)

# Varasto - Varastonhallintajärjestelmä

A warehouse management system (Varasto) with a web user interface that supports managing multiple warehouses.

## Features

- 🏪 Create and manage multiple warehouses
- ➕ Add items to warehouses
- ➖ Take items from warehouses
- 📊 Visual progress bars showing warehouse capacity
- 🗑️ Delete warehouses
- 💚 Beautiful and responsive UI

## Installation

Install dependencies using Poetry:

```bash
poetry install
```

## Running the Application

### Web Interface

Start the web application:

```bash
cd src
poetry run python app.py
```

Then open your browser and navigate to `http://127.0.0.1:5000`

**Note:** For development with debugging features, set the `FLASK_DEBUG` environment variable:

```bash
cd src
FLASK_DEBUG=true poetry run python app.py
```

### Command Line Interface

Run the original command-line demo:

```bash
cd src
poetry run python index.py
```

## Development

### Running Tests

```bash
poetry run pytest
```

### Linting

```bash
poetry run pylint src
```

### Coverage

```bash
poetry run coverage run --branch -m pytest
poetry run coverage report
```