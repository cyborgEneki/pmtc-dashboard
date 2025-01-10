def calculate_missed_opportunities_for_hiv_and_syphilis_screening_during_anc_visits(df):
    df["missed_hiv_tests"] = df["first_anc_visits"] - df["initial_hiv_test_anc"]
    df["missed_syphilis_screenings"] = df["first_anc_visits"] - df["syphilis_screened_first_anc"]