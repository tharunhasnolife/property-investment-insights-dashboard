"""Data loading from CSV files."""
from dataclasses import dataclass

import pandas as pd
import streamlit as st


@dataclass
class DataFiles:
    """Configuration container for data file paths."""
    demographics_path: str
    listings_path: str


@st.cache_data(show_spinner=False)
def load_raw_data(files: DataFiles) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load raw data from CSV files."""
    demographics = pd.read_csv(files.demographics_path, dtype={"zip_code": "string"})
    listings = pd.read_csv(files.listings_path, dtype={"postal_code": "string"})
    return demographics, listings
