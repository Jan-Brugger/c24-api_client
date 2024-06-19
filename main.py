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
def docs():
    return RedirectResponse(url='/docs')


@app.get('/weather-archive/temperature', tags=['weather'])
def get_temperature(
        latitude: Annotated[float, Query(ge=-90, le=90)],
        longitude: Annotated[float, Query(ge=-180, le=180)],
        date_and_time: datetime

) -> TemperatureResponse:
    return OpenMeteoClient().fetch_temperature(
        latitude,
        longitude,
        date_and_time,
    )


@app.get('/weather-archive/temperature-range', tags=['weather'])
def get_temperature_range(
        latitude: Annotated[float, Query(ge=-90, le=90)],
        longitude: Annotated[float, Query(ge=-180, le=180)],
        from_date: date,
        to_date: date,
        filter_by_hour: Annotated[int | None, Query(ge=0, le=24)] = None,
) -> TemperatureRangeResponse:
    return OpenMeteoClient().fetch_temperature_range(
        latitude,
        longitude,
        from_date,
        to_date,
        filter_by_hour
    )


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
