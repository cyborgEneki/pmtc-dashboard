import pandas as pd
import geopandas as gpd
from global_constants import COLUMN_MAPPING


def load_data():
    df = pd.read_excel("data/Sub-County level data-ed2.xlsx")
    kenya_sub_counties = "data/kenya-subcounties-simplified.geojson"
    sub_counties_geodata = gpd.read_file(kenya_sub_counties)

    return df, sub_counties_geodata


def clean_data(df):
    rename_columns_to_reader_friendly_names(df)
    # Apply the function to extract the classification
    df["Map_category"] = df["location_code"].apply(extract_classification)
    derive_subcounty_names(df)
    #derive_county_names(df)
    print(df[df['location']=='Baringo County'].head())
    # TODO: Add check for duplicates and missing values


def rename_columns_to_reader_friendly_names(df):
    df.rename(columns=COLUMN_MAPPING, inplace=True)


def derive_subcounty_names(df):
    df["subcounty"] = df["location_code"].apply(
        lambda x: x.replace(" Sub County", "") if x.endswith(" Sub County") else x
    )


def extract_classification(code):
    if "_" in code:
        # Split the text by underscores and take the first two parts
        parts = code.split("_")
        if len(parts) >= 2:
            search_item ="_".join(parts[:2]) 
            classified = classify_code(search_item)
            return classified
            #return "_".join(parts[:2])  # Combine the first two parts (e.g., "KE_SubCounty")
        
    return None  # Handle unexpected cases


# Function to classify into numeric codes
def classify_code(classification):
    if classification == "KE_SubCounty":
        return 1
    elif classification == "KE_County":
        return 2
    elif classification == "KE":
        return 3
    else:
        return None  # Handle unexpected cases