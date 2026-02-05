"""Chart builders."""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def price_vs_school_chart(data: pd.DataFrame):
    """Create scatter plot: price vs school rating."""
    if data.empty:
        return None

    fig = px.scatter(
        data,
        x="school_rating",
        y="listing_price",
        color="crime_index",
        hover_data=["zip_code", "bedrooms", "sq_ft"],
        title="Property Price vs School Rating",
        labels={
            "listing_price": "Price ($)",
            "school_rating": "School Rating",
            "crime_index": "Crime Level",
        },
    )
    # Add glow effect by layering a larger, translucent trace underneath
    glow_traces = []
    for trace in fig.data:
        glow_traces.append(
            go.Scatter(
                x=trace.x,
                y=trace.y,
                mode="markers",
                marker=dict(
                    size=18,
                    color=trace.marker.color,
                    opacity=0.18,
                ),
                hoverinfo="skip",
                showlegend=False,
            )
        )

    fig.update_traces(
        marker=dict(size=8, opacity=0.9),
        selector=dict(mode="markers")
    )

    for glow in glow_traces:
        fig.add_trace(glow)
    fig.update_layout(height=500)
    return fig


def price_distribution_chart(data: pd.DataFrame):
    """Create histogram: distribution of prices."""
    if data.empty:
        return None

    fig = px.histogram(
        data,
        x="listing_price",
        nbins=30,
        title="Distribution of Property Prices",
        labels={"listing_price": "Price ($)", "count": "Number of Properties"},
    )
    fig.update_layout(height=500, showlegend=False)
    return fig


def price_per_sqft_by_zip(data: pd.DataFrame):
    """Create bar chart: average price per sqft by ZIP."""
    if data.empty:
        return None

    by_zip = data.groupby("zip_code")["price_per_sqft"].mean().sort_values(ascending=False)

    fig = px.bar(
        x=by_zip.index,
        y=by_zip.values,
        title="Average Price per Square Foot by ZIP Code",
        labels={"x": "ZIP Code", "y": "Price per Sq Ft ($)"},
    )
    fig.update_layout(height=500, showlegend=False)
    return fig
