# STREAMLIT TITLES
APP_TITLE = "PMTCT Sub-county Analysis Dashboard"

# MAP
COORDINATES_FOR_THE_CENTER_KENYA = [0.0236, 37.9062]
ZOOM_START = 6

# DATA
COLUMN_MAPPING = {
    "periodid": "period_id",
    "periodname": "year",
    "periodcode": "period_code",
    "organisationunitid": "location_id",
    "organisationunitname": "location",
    "organisationunitcode": "location_code",
    "organisationunitdescription": "location_description",
    "MOH 731 1st ANC Visits HV02-01": "first_anc_visits",
    "MOH 731 Known Positive at 1st ANC HV02-03": "known_hiv_positive_first_anc",
    "MOH 731 Initial test at ANC HV02-04": "initial_hiv_test_anc",
    "MOH 731 Total Given Penta 1 HV02-38": "total_penta1_vaccines_given",
    "MOH 731 Known Exposure_at Penta 1 HV02-37": "children_known_hiv_exposure_penta1",
    "MOH 731 Positive Results_ANC HV02-11": "positive_hiv_results_anc",
    "MOH 731 Retesting_PNC<= 6 weeks HV02-08": "hiv_retests_within_6_weeks_pnc",
    "MOH 731 Syphilis Screened_1st ANC HV02-24": "syphilis_screened_first_anc",
    "MOH 731 TB cases _New HV03-076": "new_tb_cases_diagnosed",
    "MOH 731 TB Cases Tested_HIV HV03-078": "tb_cases_tested_hiv",
    "MOH 731 TB Cases_Total HIV+ (HV03-077+080) HV03-081": "total_tb_cases_hiv_positive",
    "MOH 731 TB_Total on HAART(HV03-082+083) HV03-084": "total_tb_cases_on_haart"
}