import pandas as pd
import geopandas as gpd
from global_constants import COLUMN_MAPPING


def load_data():
    df = pd.read_excel("data/Sub-County level data.xlsx")
    kenya_sub_counties = "data/kenya-subcounties-simplified.geojson"
    sub_counties_geodata = gpd.read_file(kenya_sub_counties)

    return df, sub_counties_geodata


def clean_data(df):
    rename_columns_to_reader_friendly_names(df)
    derive_subcounty_names(df)
    # TODO: Add check for duplicates and missing values


def rename_columns_to_reader_friendly_names(df):
    df.rename(columns=COLUMN_MAPPING, inplace=True)


def derive_subcounty_names(df):
    df["subcounty"] = df["location"].apply(
        lambda x: x.replace(" Sub County", "") if x.endswith(" Sub County") else x
    )
