from global_constants import APP_TITLE
from global_data import load_data, clean_data
from modules.penta_1_vaccine_coverage.data import merge_geojson_with_analysis
from modules.penta_1_vaccine_coverage.constants import PAGE_TITLE, YEARS_FILTER_TITLE
from modules.penta_1_vaccine_coverage.analysis import calculate_penta_1_vaccine_coverage
from modules.penta_1_vaccine_coverage.visualization import plot_heat_map
import streamlit as st


def main():
    st.set_page_config(page_title=APP_TITLE, layout="wide")
    st.title(PAGE_TITLE)

    # LOAD AND CLEAN DATA
    df, sub_counties_geodata = load_data()
    clean_data(df)

    # FILTER
    year_filter = create_year_filter(df)
    filtered_df = filter_data_by_year(df, year_filter)

    # ANALYSIS
    filtered_df = calculate_penta_1_vaccine_coverage(filtered_df)

    # VISUALIZATION
    compound_data = merge_geojson_with_analysis(filtered_df, sub_counties_geodata)
    plot_heat_map(compound_data)


def create_year_filter(df):
    st.sidebar.header(YEARS_FILTER_TITLE)

    return st.sidebar.selectbox(
        "Select Year",
        options=sorted(df["year"].unique(), reverse=True),
        index=0,
        format_func=lambda x: str(x)
    )


def filter_data_by_year(df, year_filter):
    return df[df["year"] == year_filter].copy()


main()
