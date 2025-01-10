import streamlit as st
import plotly.graph_objects as go

def plot_missed_opportunities(filtered_df):
    chart_data = filtered_df.groupby("subcounty")[
        ["first_anc_visits", "missed_hiv_tests", "missed_syphilis_screenings"]].sum()

    chart_data["missed_hiv_percent"] = (chart_data["missed_hiv_tests"] / chart_data["first_anc_visits"]) * 100
    chart_data["missed_syphilis_percent"] = (chart_data["missed_syphilis_screenings"] / chart_data[
        "first_anc_visits"]) * 100
    chart_data["total_percent"] = 100

    fig = go.Figure()

    # Total bar
    fig.add_trace(
        go.Bar(
            x=chart_data.index,
            y=chart_data["total_percent"],
            name="Total (100%)",
            marker=dict(color="lightgrey"),
            text=["100%"] * len(chart_data),  # Static tooltip for total
            textfont=dict(color="black"),
            hoverinfo="text",
            width=0.4
        )
    )

    # Missed HIV Tests
    fig.add_trace(
        go.Bar(
            x=chart_data.index,
            y=chart_data["missed_hiv_percent"],
            name="Missed HIV Tests (%)",
            marker=dict(color="blue"),
            text=chart_data["missed_hiv_percent"].round(2).astype(str) + "%",  # Dynamic tooltip
            textfont=dict(color="black"),
            hoverinfo="text",
            offset=0,
            width=0.2
        )
    )

    # Missed Syphilis Screenings
    fig.add_trace(
        go.Bar(
            x=chart_data.index,
            y=chart_data["missed_syphilis_percent"],
            name="Missed Syphilis Screenings (%)",
            marker=dict(color="green"),
            text=chart_data["missed_syphilis_percent"].round(2).astype(str) + "%",  # Dynamic tooltip
            textfont=dict(color="black"),
            hoverinfo="text",
            offset=-0.2,
            width=0.2
        )
    )

    fig.update_layout(
        xaxis=dict(title="Sub-county", tickangle=-45),
        yaxis=dict(title="Percentage (%)"),
        barmode="overlay",  # Grouped bars
        legend=dict(title="Legend", x=1.05, y=1),
        margin=dict(l=40, r=40, t=40, b=100),
    )

    # Display in Streamlit
    st.plotly_chart(fig, use_container_width=True)