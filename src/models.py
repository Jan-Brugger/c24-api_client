"""
This module contains all data-models.
"""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, Dict

from pydantic import BaseModel, Field


class TemperatureResponse(BaseModel):
    """
    Dataclass for a single temperature.

    Args:
        latitude (float): Latitude of the center of the weather grid-cell which was used for measurement.
        longitude (float): Longitude of the center of the weather grid-cell which was used for measurement.
        measure_datetime (float): Datetime of measurement.
        temperature (float): Measured temperature.
    """
    latitude: Annotated[float, Field(description='Latitude of the measured temperature')]
    longitude: Annotated[float, Field(description='Longitude of the measured temperature')]
    measure_datetime: Annotated[datetime, Field(description='Datetime of the temperature-measurement')]
    temperature: Annotated[float, Field(description='Measured temperature (in °C)')]


class TemperatureRangeResponse(BaseModel):
    """
    Dataclass for temperatures in a range of dates.

    Args:
        latitude (float): Latitude of the center of the weather grid-cell which was used for measurement.
        longitude (float): Longitude of the center of the weather grid-cell which was used for measurement.
        temperatures (Dict[datetime, float]): A dictionary which keys contain the date of measurement
                                                and values the measured temperature.
    """
    latitude: Annotated[float, Field(description='Latitude of the measured temperature')]
    longitude: Annotated[float, Field(description='Longitude of the measured temperature')]
    temperatures: Annotated[Dict[datetime, float], Field({}, description='Measured temperatures (in °C)')]
