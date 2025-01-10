def merge_geojson_with_analysis(df, sub_counties_geodata):
    return sub_counties_geodata.merge(
        df, left_on="shapeName", right_on="subcounty", how="left"
    )