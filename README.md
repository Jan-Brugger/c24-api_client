# Api-Client

Small API-client to fetch data from [open-meteo-API](https://api.open-meteo.com/)

## Getting started

These instructions will get you a copy of the project up and running on your local machine

### Requirements

* python 3.12
* Docker
* [open-meteo api-client](https://github.com/Jan-Brugger/c24-application-api_client)

### Installing

Use proper python version:

    pyenv local 3.12

Create virtual environment:

    python3 -m venv ./venv

Activate virtual environment:

    source ./venv/bin/activate

Install dependencies

    pip install --upgrade pip
    pip install -r requirements/requirements-dev.txt

Install pre-commit hooks

    pre-commit install

### Start application

    fastapi run
