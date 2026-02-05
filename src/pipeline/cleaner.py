"""Data cleaning and normalization."""
import re
from typing import Optional

import pandas as pd

# Regex patterns
ZIP_REGEX = re.compile(r"\b(\d{5})(?:-\d{4})?\b")


def normalize_zip(value: str | float | int | None) -> Optional[str]:
    """Normalize ZIP code to 5-digit string format."""
    if value is None or pd.isna(value):
        return None
    digits = re.sub(r"\D", "", str(value))
    if not digits:
        return None
    if len(digits) > 5:
        digits = digits[-5:]
    return digits.zfill(5)


def extract_zip_from_text(text: str | None) -> Optional[str]:
    """Extract ZIP code from unstructured text."""
    if not text or pd.isna(text):
        return None
    match = ZIP_REGEX.search(str(text))
    return match.group(1) if match else None


def normalize_address(text: str | None) -> Optional[str]:
    """Normalize address text for consistent matching."""
    if not text or pd.isna(text):
        return None
    cleaned = re.sub(r"[\.,]", " ", str(text).lower())
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    replacements = {
        "street": "st", "st": "st", "avenue": "ave", "ave": "ave",
        "boulevard": "blvd", "blvd": "blvd", "road": "rd", "rd": "rd",
        "drive": "dr", "dr": "dr", "lane": "ln", "ln": "ln",
        "place": "pl", "pl": "pl", "court": "ct", "ct": "ct",
        "parkway": "pkwy", "pkwy": "pkwy",
    }
    tokens = [replacements.get(token, token) for token in cleaned.split()]
    return " ".join(tokens)


def clean_listings(listings: pd.DataFrame) -> pd.DataFrame:
    """Clean and normalize listings data."""
    cleaned = listings.copy()
    cleaned["clean_address"] = cleaned["raw_address"].map(normalize_address)
    extracted_zip = cleaned["raw_address"].map(extract_zip_from_text)
    cleaned["postal_code"] = cleaned["postal_code"].where(
        cleaned["postal_code"].notna(), extracted_zip
    )
    cleaned["zip_code"] = cleaned["postal_code"].map(normalize_zip)

    for col in ["sq_ft", "bedrooms", "listing_price"]:
        cleaned[col] = pd.to_numeric(cleaned[col], errors="coerce")

    cleaned["price_per_sqft"] = cleaned["listing_price"] / cleaned["sq_ft"]
    return cleaned


def clean_demographics(demographics: pd.DataFrame) -> pd.DataFrame:
    """Clean and normalize demographics data."""
    cleaned = demographics.copy()
    cleaned["zip_code"] = cleaned["zip_code"].map(normalize_zip)
    cleaned["median_income"] = pd.to_numeric(cleaned["median_income"], errors="coerce")
    cleaned["school_rating"] = pd.to_numeric(cleaned["school_rating"], errors="coerce")
    cleaned["crime_index"] = cleaned["crime_index"].astype("string")
    return cleaned
