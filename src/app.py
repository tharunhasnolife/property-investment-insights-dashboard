"""Property Investment Insights: Interactive Streamlit Dashboard."""
from __future__ import annotations

import pandas as pd
import pydeck as pdk
import streamlit as st

from pipeline import execute_pipeline
from pipeline.loader import DataFiles
from visualizations import (
    map_layers,
    map_view,
    price_distribution_chart,
    price_per_sqft_by_zip,
    price_vs_school_chart,
)


# Configure Streamlit page settings
st.set_page_config(
    page_title="Property Investment Insights",
    page_icon="🏘️",
    layout="wide",
)

# Apply custom CSS styling for professional appearance
st.markdown(
    """
    <style>
    .block-container { padding-top: 2rem; }
    .kpi-card { background: #0f172a; padding: 1rem; border-radius: 10px; color: white; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Display page header
st.title("Property Investment Insights")
st.caption("Single source of truth for listings vs. neighborhood demographics")

# Initialize data file paths
files = DataFiles(
    demographics_path="data/demographics.csv",
    listings_path="data/listings.csv",
)

# Execute pipeline
result = execute_pipeline(files)
merged = result["data"]

# Build interactive sidebar filters for what-if analysis
st.sidebar.header("Filters")
zip_options = sorted(merged["zip_code"].dropna().unique().tolist())

# ZIP code filter (multi-select)
selected_zips = st.sidebar.multiselect("ZIP Codes", options=zip_options, default=zip_options)

# Price range filter (slider)
price_min, price_max = merged["listing_price"].min(), merged["listing_price"].max()
price_range = st.sidebar.slider(
    "Listing Price Range",
    float(price_min),
    float(price_max),
    (float(price_min), float(price_max)),
)

# Minimum median income filter (threshold slider)
income_min, income_max = merged["median_income"].min(), merged["median_income"].max()
income_threshold = st.sidebar.slider(
    "Minimum Median Income",
    float(income_min),
    float(income_max),
    float(income_min),
)

# School rating range filter (slider)
school_min, school_max = merged["school_rating"].min(), merged["school_rating"].max()
school_range = st.sidebar.slider(
    "School Rating Range",
    float(school_min),
    float(school_max),
    (float(school_min), float(school_max)),
)

# Crime index filter (multi-select categorical)
crime_options = sorted(merged["crime_index"].dropna().unique().tolist())
selected_crime = st.sidebar.multiselect("Crime Index", options=crime_options, default=crime_options)

# Bedrooms filter (multi-select)
bedroom_options = sorted(merged["bedrooms"].dropna().unique().tolist())
selected_bedrooms = st.sidebar.multiselect(
    "Bedrooms", options=bedroom_options, default=bedroom_options
)

# Apply all filters to create subset of data for analysis
filtered = merged[
    (merged["zip_code"].isin(selected_zips))
    & (merged["listing_price"].between(price_range[0], price_range[1]))
    & (merged["median_income"] >= income_threshold)
    & (merged["school_rating"].between(school_range[0], school_range[1]))
    & (merged["crime_index"].isin(selected_crime))
    & (merged["bedrooms"].isin(selected_bedrooms))
].copy()

# Display key performance indicators
st.subheader("Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)

# Calculate KPIs from filtered data
avg_price_per_sqft = filtered["price_per_sqft"].mean()
median_price = filtered["listing_price"].median()
avg_school = filtered["school_rating"].mean()
avg_income = filtered["median_income"].mean()

# Display KPI metrics with formatted values
col1.metric("Avg Price / SqFt", f"${avg_price_per_sqft:,.0f}" if pd.notna(avg_price_per_sqft) else "N/A")
col2.metric("Median Listing Price", f"${median_price:,.0f}" if pd.notna(median_price) else "N/A")
col3.metric("Avg School Rating", f"{avg_school:.1f}" if pd.notna(avg_school) else "N/A")
col4.metric("Avg Median Income", f"${avg_income:,.0f}" if pd.notna(avg_income) else "N/A")

# Display geospatial visualizations
st.subheader("Geospatial Insights")
map_data = filtered.dropna(subset=["lat", "lon"])
if not map_data.empty:
    # Create map with scatter and heatmap layers
    view = map_view(map_data)
    layers = map_layers(map_data)
    deck = pdk.Deck(
        layers=layers,
        initial_view_state=view,
        tooltip={"text": "{raw_address}\n${listing_price}"},
    )
    st.pydeck_chart(deck, use_container_width=True)
else:
    st.info("No geo data available for selected filters.")

# Display interactive charts for price and demographic analysis
st.subheader("Price & Demographics Analysis")
chart_col1, chart_col2 = st.columns(2)

# Scatter plot: School rating vs listing price (colored by crime, sized by sqft)
with chart_col1:
    st.plotly_chart(price_vs_school_chart(filtered), use_container_width=True)

# Histogram: Distribution of listing prices by crime index
with chart_col2:
    st.plotly_chart(price_distribution_chart(filtered), use_container_width=True)

# Bar chart: Average price per sqft by ZIP code (sorted descending)
st.plotly_chart(price_per_sqft_by_zip(filtered), use_container_width=True)

# Display detailed merged data table sorted by price (highest first)
st.subheader("Merged Data")
st.dataframe(
    filtered.sort_values("listing_price", ascending=False),
    use_container_width=True,
    height=420,
)

