import streamlit as st
import plotly.express as px
from global_data import load_data, clean_data
from modules.penta_1_vaccine_coverage.data import merge_geojson_with_analysis
from modules.penta_1_vaccine_coverage.constants import PAGE_TITLE, YEARS_FILTER_TITLE
from modules.penta_1_vaccine_coverage.analysis import calculate_penta_1_vaccine_coverage

from modules.penta_1_vaccine_coverage.visualization import plot_heat_map

st.set_page_config(layout="wide")
st.title('PMTC Dashboard')
st.subheader('Prevention of Mother to Child HIV Transmission')
st.caption('This is an app to allow exploration of Kenya\'s PMTC Data by sub-county.')

data,sub_counties_geodata = load_data()
# Clean data (optional: handle NaNs, rename columns for clarity)
data = data.rename(columns={
    'MOH 731 1st ANC Visits HV02-01': 'First_ANC_Visits',
    'MOH 731 Syphilis Screened_1st ANC HV02-24': 'Syphilis_Screened',
    'MOH 731 Initial test at ANC HV02-04': 'HIV_Tested_ANC',
    'MOH 731 Positive Results_ANC HV02-11': 'HIV_Positive_ANC',
    'MOH 731 Total Given Penta 1 HV02-38': 'Penta1_Vaccinated',
    'MOH 731 Known Exposure_at Penta 1 HV02-37': 'HIV_Exposure_Penta1',
    'MOH 731 TB cases _New HV03-076': 'New_TB_Cases',
    'MOH 731 TB Cases Tested_HIV HV03-078': 'TB_HIV_Tested',
    'MOH 731 TB Cases_Total HIV+ (HV03-077+080) HV03-081': 'TB_HIV_Positive',
    'MOH 731 TB_Total on HAART(HV03-082+083) HV03-084': 'TB_HAART'
})
# Function to format numbers in millions or thousands
def format_number(num):
    if abs(num) >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"
    elif abs(num) >= 1_000:
        return f"{num / 1_000:.1f}K"
    else:
        return f"{num:,}"

#st.title("Dashboard")
#st.caption("Prevention of Mother to child HIV transmission")

# Filter data for the last four years
data['periodname'] = data['periodname'].astype(int)
years = sorted(data['periodname'].unique())[-4:]  # Get the last four years
data_last_four_years = data[data['periodname'].isin(years)]

# Calculate totals for each section (for the top cards)
data_2023 = data[data['periodname'] == 2023]
data_2024 = data[data['periodname'] == 2024]
metrics = {
    "ANC Visits": [data_2023['First_ANC_Visits'].sum(), data_2024['First_ANC_Visits'].sum()],
    "Syphilis Screened": [data_2023['Syphilis_Screened'].sum(), data_2024['Syphilis_Screened'].sum()],
    "HIV Tested": [data_2023['HIV_Tested_ANC'].sum(), data_2024['HIV_Tested_ANC'].sum()],
    "HIV Positive": [data_2023['HIV_Positive_ANC'].sum(), data_2024['HIV_Positive_ANC'].sum()]
}

# Icons for each metric (using emojis for simplicity)
icons = {
    "ANC Visits": "👩‍⚕️",
    "Syphilis Screened": "🩺",
    "HIV Tested": "🩸",
    "HIV Positive": "➕"
}

# Display the top four cards
st.subheader("2024 vs 2023")
col1, col2, col3, col4 = st.columns(4, gap="small")
columns = [col1, col2, col3, col4]

for idx, (section, (value_2023, value_2024)) in enumerate(metrics.items()):
    change = value_2024 - value_2023
    percentage_change = (change / value_2023 * 100) if value_2023 != 0 else 0
    change_color = "#4CAF50" if change > 0 else "#db8c1d"  # Green for positive, red for negative
    arrow = "↑" if change > 0 else "↓"  # Up or down arrow based on change

    # Format the change value
    formatted_change = format_number(change)

    with columns[idx]:
        st.markdown(f"""
            <div style="
                background-color: #ffffff;
                padding: 20px;
                border-radius: 12px;
                box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.05);
                text-align: center;
                aspect-ratio: 3 / 2;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                border: 1px solid #e0e0e0;
                width: 100%;  /* Ensure the card fills the column width */
                min-width: 200px;  /* Set a minimum width for the card */
            ">
                <div style="font-size: 24px; margin-bottom: 10px;">
                    {icons.get(section, "📊")}
                </div>
                <div style="font-size: 16px; font-weight: 600; margin-bottom: 10px; color: #555;">
                    {section}
                </div>
                <div style="font-size: 28px; font-weight: bold; color: #000;">
                    {format_number(value_2024)}
                </div>
                <div style="font-size: 14px; margin-top: 5px; color: {change_color};">
                    <span style="font-size: 18px; vertical-align: middle;">{arrow}</span>
                    {f"+{formatted_change}" if change > 0 else formatted_change} ({f"+{percentage_change:.1f}%" if percentage_change > 0 else f"{percentage_change:.1f}%"})
                </div>
                <div style="font-size: 12px; color: #777; margin-top: 10px;">
                    <span style="font-weight: 500;">2023:</span> {format_number(value_2023)}
                </div>
            </div>
        """, unsafe_allow_html=True)

# Add a new section for yearly trends
#st.subheader("Yearly Trends (Last Four Years)")

# Define the metrics for the yearly trends
trend_metrics = {
    "ANC Visits": "First_ANC_Visits",
    "Syphilis Screened": "Syphilis_Screened",
    "HIV Tested": "HIV_Tested_ANC",
    "HIV Positive": "HIV_Positive_ANC"
}
st.markdown("---")  # Horizontal separator
#-------------MAP CHARTS--------------------------------
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



st.markdown("---")  # Horizontal separator
# Create a modern and stylish bar chart for each metric
for idx, (section, column_name) in enumerate(trend_metrics.items()):
    # Prepare data for the bar chart
    trend_data = data_last_four_years.groupby('periodname')[column_name].sum().reset_index()
    trend_data.rename(columns={'periodname': 'Year', column_name: 'Value'}, inplace=True)

    # Format the values in millions or thousands
    trend_data['Formatted_Value'] = trend_data['Value'].apply(format_number)

    # Ensure the 'Year' column is treated as integers
    trend_data['Year'] = trend_data['Year'].astype(int)

    # Create the bar chart
    fig = px.bar(
        trend_data,
        x="Year",
        y="Value",
        text="Formatted_Value",
        title=f"{section} Over Last Four Years",
        color="Value",  # Add color gradient based on value
        color_continuous_scale=px.colors.sequential.Viridis,  # Use a modern color scale
    )
    st.markdown("---")  # Horizontal separator
    # Update chart styling
    fig.update_traces(
        textposition="outside",
        marker_line_color="black",  # Add a border to bars
        marker_line_width=1.5,  # Border width
        opacity=0.8,  # Slightly transparent bars
    )

    # Update layout for a modern look
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",  # Transparent background
        paper_bgcolor="rgba(0,0,0,0)",  # Transparent background
        xaxis_title=None,
        yaxis_title=None,
        showlegend=False,
        xaxis=dict(type='category', tickmode='array', tickvals=trend_data['Year']),  # Ensure years are treated as categories
        #font=dict(family="Arial, sans-serif", size=14, color="black"),  # Modern font
        font=dict(family="Helvetica, Arial, sans-serif", size=14, color="black"),  # Modern font
        title_font=dict(size=18, color="black"),  # Title font
        hoverlabel=dict(bgcolor="white", font_size=14, font_family="Arial, sans-serif"),  # Hover label styling
        margin=dict(l=20, r=20, t=40, b=20),  # Adjust margins
    )

    # Display the bar chart
    st.plotly_chart(fig, use_container_width=True)

    # Add a horizontal separator between bar charts (except after the last one)

