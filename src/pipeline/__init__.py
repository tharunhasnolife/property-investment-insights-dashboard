"""Pipeline orchestration."""
from pipeline.loader import DataFiles, load_raw_data
from pipeline.cleaner import clean_listings, clean_demographics
from pipeline.merger import resolve_zip_codes, add_geo_columns, merge_data


def execute_pipeline(files: DataFiles) -> dict:
    """Execute full data processing pipeline."""
    # Load
    demographics_raw, listings_raw = load_raw_data(files)

    # Clean
    demographics = clean_demographics(demographics_raw)
    listings = clean_listings(listings_raw)

    # Resolve & Merge
    listings = resolve_zip_codes(listings, demographics)
    merged = merge_data(demographics, listings)

    # Add geolocation
    merged = add_geo_columns(merged)

    return {"data": merged, "demographics": demographics}
