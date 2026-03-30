"""Pydantic models for SerpAPI Google Flights MCP tools."""

from typing import Optional
from pydantic import BaseModel, Field


class FlightSearchParams(BaseModel):
    """Parameters for searching flights via Google Flights."""
    origin: str = Field(..., description="Origin airport IATA code (e.g. YUL, CDG, JFK)")
    destination: str = Field(..., description="Destination airport IATA code (e.g. TUN, CDG, CUN)")
    outbound_date: str = Field(..., description="Outbound date in YYYY-MM-DD format")
    return_date: Optional[str] = Field(None, description="Return date in YYYY-MM-DD format (for round-trip)")
    adults: int = Field(1, description="Number of adult passengers")
    children: int = Field(0, description="Number of child passengers")
    travel_class: int = Field(1, description="1=Economy, 2=Premium economy, 3=Business, 4=First")
    currency: str = Field("CAD", description="Currency code for prices (e.g. CAD, USD, EUR)")
    include_airlines: Optional[str] = Field(None, description="Comma-separated IATA airline codes to include (e.g. AT,AF,KL)")
    exclude_airlines: Optional[str] = Field(None, description="Comma-separated IATA airline codes to exclude")
    max_duration: Optional[int] = Field(None, description="Maximum flight duration in minutes (e.g. 900 for 15 hours)")
    stops: Optional[int] = Field(None, description="0=Any, 1=Nonstop only, 2=1 stop or fewer, 3=2 stops or fewer")
    sort_by: int = Field(2, description="1=Top flights, 2=Price, 3=Departure time, 4=Arrival time, 5=Duration")
    show_hidden: bool = Field(True, description="Include hidden flight results for more options")


class ReturnFlightParams(BaseModel):
    """Parameters for searching return flights using a departure token."""
    departure_token: str = Field(..., description="The departure_token from a selected outbound flight")
    origin: str = Field(..., description="Origin airport IATA code used in the original search (e.g. YUL)")
    destination: str = Field(..., description="Destination airport IATA code used in the original search (e.g. TUN)")
    outbound_date: str = Field(..., description="Outbound date used in the original search (YYYY-MM-DD)")
    return_date: str = Field(..., description="Return date used in the original search (YYYY-MM-DD)")
    adults: int = Field(1, description="Number of adult passengers (same as original search)")
    travel_class: int = Field(1, description="1=Economy, 2=Premium economy, 3=Business, 4=First")
    currency: str = Field("CAD", description="Currency code for prices")
    include_airlines: Optional[str] = Field(None, description="Comma-separated IATA airline codes to include")


class BookingOptionsParams(BaseModel):
    """Parameters for getting booking options using a booking token."""
    booking_token: str = Field(..., description="The booking_token from a selected flight")
    departure_id: str = Field(..., description="Origin airport IATA code (e.g. YUL)")
    arrival_id: str = Field(..., description="Destination airport IATA code (e.g. TUN)")
    outbound_date: str = Field(..., description="Outbound date in YYYY-MM-DD format")
    return_date: Optional[str] = Field(None, description="Return date in YYYY-MM-DD format (for round-trip)")
    adults: int = Field(1, description="Number of adult passengers")
    travel_class: int = Field(1, description="1=Economy, 2=Premium economy, 3=Business, 4=First")
    currency: str = Field("CAD", description="Currency code for prices")
