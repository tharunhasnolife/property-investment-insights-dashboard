"""ZIP code matching and data merging."""
from typing import Iterable, Optional

import numpy as np
import pandas as pd
from rapidfuzz import fuzz, process


def fuzzy_match_zip(
    zip_code: str | None,
    choices: Iterable[str],
    threshold: int = 90
) -> Optional[str]:
    """Fuzzy match ZIP code to closest valid ZIP in choices."""
    if not zip_code:
        return None
    match = process.extractOne(zip_code, choices, scorer=fuzz.ratio)
    if match and match[1] >= threshold:
        return match[0]
    return None


def resolve_zip_codes(
    listings: pd.DataFrame,
    demographics: pd.DataFrame
) -> pd.DataFrame:
    """Resolve missing or mismatched ZIP codes using fuzzy matching."""
    cleaned = listings.copy()
    choices = demographics["zip_code"].dropna().unique().tolist()
    missing_mask = cleaned["zip_code"].isna() | ~cleaned["zip_code"].isin(choices)
    cleaned.loc[missing_mask, "zip_code"] = cleaned.loc[missing_mask, "zip_code"].map(
        lambda value: fuzzy_match_zip(value, choices)
    )
    return cleaned


def zip_to_lat_lon(zip_code: str) -> tuple[float, float]:
    """Generate deterministic latitude/longitude coordinates from ZIP code."""
    seed = int(zip_code) if zip_code.isdigit() else 0
    rng = np.random.RandomState(seed)
    lat = rng.uniform(25.0, 49.0)
    lon = rng.uniform(-124.0, -66.0)
    return float(lat), float(lon)


def add_geo_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Add latitude and longitude columns based on ZIP codes."""
    with_geo = df.copy()
    lat_lon = with_geo["zip_code"].dropna().map(zip_to_lat_lon)
    with_geo.loc[lat_lon.index, "lat"] = [pair[0] for pair in lat_lon]
    with_geo.loc[lat_lon.index, "lon"] = [pair[1] for pair in lat_lon]
    return with_geo


def merge_data(
    demographics: pd.DataFrame,
    listings: pd.DataFrame
) -> pd.DataFrame:
    """Merge listings with demographics data on ZIP code."""
    merged = listings.merge(demographics, on="zip_code", how="left", validate="m:1")
    return merged
