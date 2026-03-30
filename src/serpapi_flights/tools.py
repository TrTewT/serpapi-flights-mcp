"""MCP tools for searching flights via SerpAPI Google Flights."""

import os
import logging
from serpapi import GoogleSearch
from fastmcp import FastMCP

from .models import FlightSearchParams, ReturnFlightParams, BookingOptionsParams
from .formatter import format_search_results, format_booking_options

logger = logging.getLogger(__name__)
mcp = FastMCP("serpapi-flights")


def _get_api_key() -> str:
    key = os.getenv("SERPAPI_API_KEY")
    if not key:
        raise ValueError("SERPAPI_API_KEY environment variable not set")
    return key


@mcp.tool()
def search_flights(params: FlightSearchParams) -> str:
    """Search for flights on Google Flights. Returns best and other flight options with prices.
    For round-trips, this returns outbound flights. Use search_return_flights with a departure_token to get return options."""
    api_key = _get_api_key()
    is_round_trip = params.return_date is not None
    search_params = {
        "engine": "google_flights",
        "departure_id": params.origin,
        "arrival_id": params.destination,
        "outbound_date": params.outbound_date,
        "type": "1" if is_round_trip else "2",
        "adults": params.adults,
        "travel_class": params.travel_class,
        "currency": params.currency,
        "hl": "fr",
        "gl": "ca",
        "sort_by": params.sort_by,
        "deep_search": "true",
        "show_hidden": str(params.show_hidden).lower(),
        "api_key": api_key,
    }
    if is_round_trip:
        search_params["return_date"] = params.return_date
    if params.children > 0:
        search_params["children"] = params.children
    if params.include_airlines:
        search_params["include_airlines"] = params.include_airlines
    if params.exclude_airlines:
        search_params["exclude_airlines"] = params.exclude_airlines
    if params.max_duration is not None:
        search_params["max_duration"] = params.max_duration
    if params.stops is not None:
        search_params["stops"] = params.stops
    logger.info(f"Searching flights: {params.origin} -> {params.destination} on {params.outbound_date}")
    search = GoogleSearch(search_params)
    results = search.get_dict()
    if "error" in results:
        raise RuntimeError(f"SerpAPI error: {results['error']}")
    return format_search_results(results, params.currency)


@mcp.tool()
def search_return_flights(params: ReturnFlightParams) -> str:
    """Search for return flights using a departure_token from a previously selected outbound flight.
    Use this after search_flights to get return flight options for a round-trip."""
    api_key = _get_api_key()
    search_params = {
        "engine": "google_flights",
        "departure_id": params.origin,
        "arrival_id": params.destination,
        "outbound_date": params.outbound_date,
        "return_date": params.return_date,
        "type": "1",
        "adults": params.adults,
        "travel_class": params.travel_class,
        "currency": params.currency,
        "hl": "fr",
        "gl": "ca",
        "sort_by": 2,
        "deep_search": "true",
        "show_hidden": "true",
        "departure_token": params.departure_token,
        "api_key": api_key,
    }
    if params.include_airlines:
        search_params["include_airlines"] = params.include_airlines
    logger.info(f"Searching return flights for {params.origin}->{params.destination}")
    search = GoogleSearch(search_params)
    results = search.get_dict()
    if "error" in results:
        raise RuntimeError(f"SerpAPI error: {results['error']}")
    return format_search_results(results, params.currency)


@mcp.tool()
def get_booking_options(params: BookingOptionsParams) -> str:
    """Get booking options (which OTAs/airlines sell this flight and at what price) using a booking_token."""
    api_key = _get_api_key()
    search_params = {
        "engine": "google_flights",
        "booking_token": params.booking_token,
        "departure_id": params.departure_id,
        "arrival_id": params.arrival_id,
        "outbound_date": params.outbound_date,
        "type": "1" if params.return_date else "2",
        "adults": params.adults,
        "travel_class": params.travel_class,
        "currency": params.currency,
        "hl": "fr",
        "gl": "ca",
        "api_key": api_key,
    }
    if params.return_date:
        search_params["return_date"] = params.return_date
    logger.info("Getting booking options with booking_token")
    search = GoogleSearch(search_params)
    results = search.get_dict()
    if "error" in results:
        raise RuntimeError(f"SerpAPI error: {results['error']}")
    return format_booking_options(results, params.currency)
