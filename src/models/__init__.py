"""Data models for property and demographics."""
from dataclasses import dataclass


@dataclass
class Property:
    """Property listing."""
    raw_address: str
    postal_code: str
    sq_ft: float
    bedrooms: int
    listing_price: float
    zip_code: str = None
    clean_address: str = None
    price_per_sqft: float = None


@dataclass
class DemographicData:
    """Demographic data for ZIP code."""
    zip_code: str
    median_income: float
    school_rating: float
    crime_index: str
