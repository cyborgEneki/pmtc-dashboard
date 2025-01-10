import folium
from streamlit_folium import st_folium
import streamlit as st
from global_constants import COORDINATES_FOR_THE_CENTER_KENYA, ZOOM_START

def plot_heat_map(compound_data):
    base_map = folium.Map(
        location=COORDINATES_FOR_THE_CENTER_KENYA,
        zoom_start=ZOOM_START,
        max_bounds=True,
        min_zoom=ZOOM_START,  # Prevent scroll-zooming out too far
        max_zoom=7,
        tiles="CartoDB positron"
    )

    folium.Choropleth(
        geo_data=compound_data,
        name="Penta 1 Coverage (%)",
        data=compound_data,
        columns=["shapeName", "penta1_coverage_percent"],
        key_on="feature.properties.shapeName",
        fill_color="YlGnBu",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name="Penta 1 Coverage (%)",
    ).add_to(base_map)

    # Add tooltips for each sub-county
    folium.GeoJson(
        compound_data,
        name="Sub-county Tooltips",
        style_function=lambda x: {
            "fillColor": "transparent",
            "color": "black",
            "weight": 0.2,
            "fillOpacity": 0.0,
        },
        tooltip=folium.GeoJsonTooltip(
            fields=["shapeName", "penta1_coverage_percent"],
            aliases=["Sub-county:", "Coverage (%):"],
            localize=True,
        ),
    ).add_to(base_map)

    folium.LayerControl().add_to(base_map)

    st_folium(base_map, width=800, height=600)

    st.markdown("""
            **Data Source:** 
            The data used in this visualization is sourced from the [Kenya sub-counties GeoJSON map from HumData.](https://ckan.africadatahub.org/dataset/kenya-sub-counties-map).
            *Version as of **July 2022**.*
            """)
