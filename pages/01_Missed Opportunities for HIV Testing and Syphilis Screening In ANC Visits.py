from global_constants import APP_TITLE
from global_data import load_data, clean_data
from modules.missed_opportunities.constants import *
from modules.missed_opportunities.analysis import \
    calculate_missed_opportunities_for_hiv_and_syphilis_screening_during_anc_visits
from modules.missed_opportunities.visualization import *


def main():
    st.set_page_config(page_title=APP_TITLE, layout="wide")
    st.title(PAGE_TITLE)

    # LOAD AND CLEAN DATA
    df, sub_counties_geodata = load_data()
    clean_data(df)

    # ANALYSIS
    calculate_missed_opportunities_for_hiv_and_syphilis_screening_during_anc_visits(df)

    # DISPLAY FILTERS
    subcounty_filter = create_subcounty_filter(df)
    year_filter = create_year_filter(df)

    # VISUALIZATION
    filtered_df = filter_data(df, subcounty_filter, year_filter)
    plot_missed_opportunities(filtered_df)


def create_subcounty_filter(df):
    st.sidebar.header(SUBCOUNTIES_FILTER_TITLE)

    return st.sidebar.multiselect(
        "(Only the first 3 are shown by default)",
        options=df["subcounty"].unique(),
        default=df["subcounty"].unique()[:3]
    )

def create_year_filter(df):
    st.sidebar.header(YEARS_FILTER_TITLE)

    return st.sidebar.multiselect(
        "(The most recent year with data is shown by default)",
        options=df["year"].unique(),
        default=df["year"].max()
    )


def filter_data(df, subcounty_filter, year_filter):
    filtered_df = df

    if subcounty_filter:
        filtered_df = filtered_df[filtered_df["subcounty"].isin(subcounty_filter)]

    if year_filter:
        filtered_df = filtered_df[filtered_df["year"].isin(year_filter)]

    return filtered_df.copy()

main()