"""
Client to fetch data from open-meteo historical-weather-api.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Any, Dict, Iterable

from fastapi import HTTPException
from requests import get

from src.models import TemperatureRangeResponse, TemperatureResponse


class OpenMeteoClient:
    """
    Manages the requests to open-meteo and parse the responses.
    """

    BASE_PATH = 'https://archive-api.open-meteo.com/v1/archive'
    DATE_FORMAT = '%Y-%m-%d'

    def fetch_temperature(
            self,
            latitude: float,
            longitude: float,
            search_date_time: datetime,
    ) -> TemperatureResponse:
        """
        Fetches a single temperature from open-meteo historical-weather-api.

        :param latitude: Latitude to get temperature for.
        :param longitude: Longitude to get temperature for.
        :param search_date_time: Date / time to get temperature for.
        :return: TemperatureResponse for the requested parameters.
        """
        request_params = self.__build_request_params(latitude, longitude, search_date_time.date())
        response = self.__fetch_request(request_params)
        parsed_response = self.__parse_response(response)
        closest_temperature_datetime = self.__find_closest_date(parsed_response.temperatures.keys(), search_date_time)

        if not closest_temperature_datetime:
            raise HTTPException(status_code=404, detail=f'No temperature found for datetime {search_date_time}')

        return TemperatureResponse(
            latitude=parsed_response.latitude,
            longitude=parsed_response.longitude,
            measure_datetime=closest_temperature_datetime,
            temperature=parsed_response.temperatures[closest_temperature_datetime]
        )

    def fetch_temperature_range(
            self,
            latitude: float,
            longitude: float,
            start_date: date,
            end_date: date,
            filter_by_hour: int | None
    ) -> TemperatureRangeResponse:
        """
        Fetches a range of temperatures from open-meteo historical-weather-api.

        :param latitude: Latitude to get temperature for.
        :param longitude: Longitude to get temperature for.
        :param start_date: First date to get temperature for.
        :param end_date: Last date to get temperature for.
        :param filter_by_hour: Filters temperatures to a specific hour per day.
                            e.g. 12 will return temps for each noon in range.
        :return: TemperatureRangeResponse for the requested parameters.
        """
        request_params = self.__build_request_params(latitude, longitude, start_date, end_date)
        response = self.__fetch_request(request_params)
        parsed_response = self.__parse_response(response)
        self.__filter_temperatures(parsed_response.temperatures, filter_by_hour)

        return parsed_response

    @classmethod
    def __build_request_params(
            cls,
            latitude: float,
            longitude: float,
            start_date: date,
            end_date: date | None = None
    ) -> Dict[str, str]:
        """
        Builds the requests-params for the open-meteo requests.

        :param latitude: Latitude to get temperature for.
        :param longitude: Longitude to get temperature for.
        :param start_date: First date to get temperature for.
        :param end_date: Last date to get temperature for.
        :return: Dictionary of query parameters.
        """
        request_params = {
            'hourly': 'temperature_2m',
            'latitude': str(latitude),
            'longitude': str(longitude),
            'start_date': start_date.strftime(cls.DATE_FORMAT),
            'end_date': (end_date or start_date).strftime(cls.DATE_FORMAT)

        }

        return request_params

    @classmethod
    def __fetch_request(cls, params: Dict[str, str]) -> Dict[str, Any]:
        """
        Sends an HTTP-request and returns the response-body as JSON.

        :param params: Dictionary of query parameters.
        :return: JSON-response from open-meteo as dictionary.
        """
        response = get(cls.BASE_PATH, params=params, timeout=10)

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f'Bad Open-Meteo response: {response.text}'
            )

        return response.json()

    @classmethod
    def __parse_response(cls, response: Dict[str, Any]) -> TemperatureRangeResponse:
        """
        Parses the open-meteo response into dataclass TemperatureRangeResponse.

        :param response: Open-meteo response as dictionary.
        :return: TemperatureRangeResponse.
        """
        temperature_dict = cls._parse_temperature_dict(response)

        parsed_response = TemperatureRangeResponse(
            latitude=response.get('latitude', 0.0),
            longitude=response.get('longitude', 0.0),
            temperatures=temperature_dict
        )

        return parsed_response

    @classmethod
    def _parse_temperature_dict(cls, response: Dict[str, Any]) -> Dict[datetime, float]:
        """
        Parses the datetime-list and the temperature-list from open-meteo-response into a dictionary.

        :param response: Open-meteo response as dictionary.
        :return: A dictionary which keys contain the date of measurement and values the measured temperature.
        """
        try:
            temperature_dict = {
                datetime.fromisoformat(date_time): temperature
                for date_time, temperature
                in zip(*response.get('hourly', {}).values())
            }
        except (ValueError, TypeError) as error:
            raise HTTPException(
                status_code=500,
                detail=f'Open-Meteo returned an unexpected response-format. Response: {response}'
            ) from error

        return temperature_dict

    @classmethod
    def __find_closest_date(cls, search_through_dates: Iterable[datetime], search_date: datetime) -> datetime | None:
        """
        Finds and returns the closest date in a list of dates.

        :param search_through_dates: List (or other iterable) of dates.
        :param search_date: Date to search for.
        :return: Closest date from search_through_dates.
        """
        return next(iter(sorted(search_through_dates, key=lambda x: abs(x - search_date))))

    @classmethod
    def __filter_temperatures(cls, temperatures: Dict[datetime, float], filter_by_hour: int | None) -> None:
        """
        Filters a dictionary which keys are datetime-objects for a specific hour of the day.

        :param temperatures: Dictionary which keys are datetime-objects.
        :param filter_by_hour: Hour to filter keys for.
        :return: Filtered temperatures-dictionary.
        """
        if not filter_by_hour:
            return

        for dt in list(temperatures):
            if dt.hour != filter_by_hour:
                del temperatures[dt]
