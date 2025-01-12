def calculate_penta_1_vaccine_coverage(filtered_df):
    filtered_df["penta1_coverage_percent"] = (filtered_df["children_known_hiv_exposure_penta1"] / filtered_df["total_penta1_vaccines_given"] * 100).round(2)
    return filtered_df
