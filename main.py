"""
Entry-point for the API-client.
start application with `fastapi run` or debug it with `python3 main.py`
"""
from __future__ import annotations

from datetime import date, datetime
from typing import Annotated

import uvicorn
from fastapi import FastAPI, Query
from fastapi.responses import RedirectResponse

from src.models import TemperatureRangeResponse, TemperatureResponse
from src.open_meteo_client import OpenMeteoClient

app = FastAPI(
    title='Open-Meteo Client'
)


@app.get('/', include_in_schema=False)
def home_handler():
    """
    Redirect base-URI requests to OAS specification.
    """
    return RedirectResponse(url='/docs')


@app.get('/weather-archive/temperature', tags=['weather'])
def weather_archive_temperature_handler(
        latitude: Annotated[float, Query(ge=-90, le=90)],
        longitude: Annotated[float, Query(ge=-180, le=180)],
        date_and_time: datetime

) -> TemperatureResponse:
    """
    Handles the /weather-archive/temperature endpoint.

    :param latitude: Latitude to get temperature for.
    :param longitude: Longitude to get temperature for.
    :param date_and_time: Date / time to get temperature for.
    :return: TemperatureResponse for the requested parameters.
    """
    return OpenMeteoClient().fetch_temperature(
        latitude,
        longitude,
        date_and_time,
    )


@app.get('/weather-archive/temperature-range', tags=['weather'])
def weather_archive_temperature_range_handler(
        latitude: Annotated[float, Query(ge=-90, le=90)],
        longitude: Annotated[float, Query(ge=-180, le=180)],
        from_date: date,
        to_date: date,
        filter_by_hour: Annotated[int | None, Query(ge=0, le=24)] = None,
) -> TemperatureRangeResponse:
    """
    Handles the /weather-archive/temperature-range endpoint.

    :param latitude: Latitude to get temperature for.
    :param longitude: Longitude to get temperature for.
    :param from_date: First date to get temperature for.
    :param to_date: Last date to get temperature for.
    :param filter_by_hour: Filters temperatures to a specific hour per day.
                            e.g. 12 will return temps for each noon in range.
    :return: TemperatureRangeResponse for the requested parameters.
    """
    return OpenMeteoClient().fetch_temperature_range(
        latitude,
        longitude,
        from_date,
        to_date,
        filter_by_hour
    )


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
