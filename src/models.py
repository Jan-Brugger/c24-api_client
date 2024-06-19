from __future__ import annotations

from datetime import datetime
from typing import Annotated, Dict

from pydantic import BaseModel, Field


class TemperatureResponse(BaseModel):
    latitude: Annotated[float, Field(description='Latitude of the measured temperature')]
    longitude: Annotated[float, Field(description='Longitude of the measured temperature')]
    measure_datetime: Annotated[datetime, Field(description='Datetime of the temperature-measurement')]
    temperature: Annotated[float, Field(description='Measured temperature (in °C)')]


class TemperatureRangeResponse(BaseModel):
    latitude: Annotated[float, Field(description='Latitude of the measured temperature')]
    longitude: Annotated[float, Field(description='Longitude of the measured temperature')]
    temperatures: Annotated[Dict[datetime, float], Field({}, description='Measured temperatures (in °C)')]
