"""Format SerpAPI Google Flights responses into clean, readable results."""

import json


def _format_flight_leg(flight):
    dep = flight.get("departure_airport", {})
    arr = flight.get("arrival_airport", {})
    return {
        "from": f"{dep.get('id', '?')} ({dep.get('name', '?')})",
        "departure_time": dep.get("time", "?"),
        "to": f"{arr.get('id', '?')} ({arr.get('name', '?')})",
        "arrival_time": arr.get("time", "?"),
        "duration_min": flight.get("duration"),
        "airline": flight.get("airline", "?"),
        "flight_number": flight.get("flight_number", "?"),
        "airplane": flight.get("airplane", "?"),
        "travel_class": flight.get("travel_class", "?"),
        "legroom": flight.get("legroom", "?"),
    }


def _format_layover(layover):
    return {
        "airport": f"{layover.get('id', '?')} ({layover.get('name', '?')})",
        "duration_min": layover.get("duration"),
        "overnight": layover.get("overnight", False),
    }


def _format_offer(offer):
    flights = [_format_flight_leg(f) for f in offer.get("flights", [])]
    layovers = [_format_layover(l) for l in offer.get("layovers", [])]
    total_duration = offer.get("total_duration")
    result = {
        "price": offer.get("price"),
        "type": offer.get("type", "?"),
        "total_duration_min": total_duration,
        "flights": flights,
        "layovers": layovers,
        "departure_token": offer.get("departure_token"),
        "booking_token": offer.get("booking_token"),
    }
    carbon = offer.get("carbon_emissions", {})
    if carbon:
        result["carbon_emissions_kg"] = carbon.get("this_flight", 0) / 1000 if carbon.get("this_flight") else None
    extensions = offer.get("extensions", [])
    if extensions:
        result["notes"] = extensions
    return result


def format_search_results(data, currency):
    """Format a full search response into a clean JSON string."""
    result = {
        "currency": currency,
        "best_flights": [],
        "other_flights": [],
        "price_insights": None,
    }
    for offer in data.get("best_flights", []):
        result["best_flights"].append(_format_offer(offer))
    for offer in data.get("other_flights", []):
        result["other_flights"].append(_format_offer(offer))
    insights = data.get("price_insights", {})
    if insights:
        result["price_insights"] = {
            "lowest_price": insights.get("lowest_price"),
            "price_level": insights.get("price_level"),
            "typical_price_range": insights.get("typical_price_range"),
            "price_history": insights.get("price_history"),
        }
    total = len(result["best_flights"]) + len(result["other_flights"])
    result["total_offers"] = total
    return json.dumps(result, indent=2, ensure_ascii=False)


def format_booking_options(data, currency):
    """Format booking options response."""
    options = []
    for opt in data.get("booking_options", []):
        together = opt.get("together", {})
        options.append({
            "book_with": together.get("book_with", "?"),
            "price": together.get("price"),
            "airline_logos": together.get("airline_logos", []),
            "marketed_as": together.get("marketed_as", []),
            "booking_request": together.get("booking_request", {}),
        })
    result = {
        "currency": currency,
        "booking_options": options,
        "total_options": len(options),
    }
    return json.dumps(result, indent=2, ensure_ascii=False)
