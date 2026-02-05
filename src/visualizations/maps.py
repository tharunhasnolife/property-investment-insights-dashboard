"""Map builders."""
import pandas as pd
import pydeck as pdk


def map_layers(data: pd.DataFrame):
    """Create map layers: scatter and heatmap."""
    layers = [
        pdk.Layer(
            "ScatterplotLayer",
            data=data,
            get_position=["lon", "lat"],
            get_color=[200, 30, 0, 160],
            get_radius=150,
            pickable=True,
        ),
        pdk.Layer(
            "HeatmapLayer",
            data=data,
            get_position=["lon", "lat"],
            radiusPixels=50,
            elevationScale=4,
            opacity=0.7,
        ),
    ]
    return layers


def map_view(data: pd.DataFrame):
    """Create map initial view state."""
    return pdk.ViewState(
        latitude=data["lat"].mean(),
        longitude=data["lon"].mean(),
        zoom=3,
        pitch=0,
    )
