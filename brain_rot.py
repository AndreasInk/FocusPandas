import streamlit as st
import xml.etree.ElementTree as ET
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px


# Function to parse HealthKit export.xml
def parse_healthkit_export(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Extract relevant health metrics
    health_data = []
    for record in root.findall("Record"):
        if record.attrib.get('type') in [
            "HKQuantityTypeIdentifierHeartRate",
            "HKQuantityTypeIdentifierHeartRateVariabilitySDNN",
            "HKQuantityTypeIdentifierRestingHeartRate",
            "HKQuantityTypeIdentifierWalkingHeartRateAverage",
            "HKQuantityTypeIdentifierStepCount",
        ]:
            health_data.append({
                "timestamp": record.attrib['startDate'],
                "type": record.attrib['type'],
                "value": float(record.attrib['value']),
            })

    health_df = pd.DataFrame(health_data)
    health_df['timestamp'] = pd.to_datetime(health_df['timestamp'])
    return health_df


# Function to parse screentime CSV
def parse_screentime_csv(csv_file):
    screentime_df = pd.read_csv(csv_file)
    screentime_df['start_time'] = pd.to_datetime(screentime_df['start_time'])
    screentime_df['end_time'] = pd.to_datetime(screentime_df['end_time'])
    screentime_df['duration'] = (screentime_df['end_time'] - screentime_df['start_time']).dt.total_seconds() / 60
    return screentime_df


# Analyze 24-hour periods before and after app usage
def analyze_app_impact(app_name, health_df, screentime_df):
    # Filter for the selected app usage
    app_usage = screentime_df[screentime_df['app'].str.contains(app_name, case=False, na=False)]

    # Get timestamps of app usage
    app_hours = app_usage['start_time'].dt.floor('H').unique()

    # Identify 24-hour periods before and after app usage
    before_app_periods = []
    after_app_periods = []
    for hour in app_hours:
        before_app_periods.extend(pd.date_range(start=hour - pd.Timedelta(hours=24), periods=24, freq='h'))
        after_app_periods.extend(pd.date_range(start=hour, periods=24, freq='h'))

    before_app_periods = pd.Series(before_app_periods)
    after_app_periods = pd.Series(after_app_periods)

    # Ensure timestamps are timezone-naive
    health_df['timestamp'] = health_df['timestamp'].dt.tz_localize(None)

    # Approximate match health data with periods
    health_before = pd.merge_asof(
        pd.DataFrame({'timestamp': before_app_periods}).sort_values(by='timestamp'),
        health_df.sort_values(by='timestamp'),
        on='timestamp',
        direction='nearest'
    )

    health_after = pd.merge_asof(
        pd.DataFrame({'timestamp': after_app_periods}).sort_values(by='timestamp'),
        health_df.sort_values(by='timestamp'),
        on='timestamp',
        direction='nearest'
    )

    # Aggregate health data for comparison
    health_agg_before = health_before.groupby('type').agg({'value': ['mean', 'std']}).reset_index()
    health_agg_after = health_after.groupby('type').agg({'value': ['mean', 'std']}).reset_index()

    # Aggregate screentime data for before and after periods
    screentime_before = screentime_df[screentime_df['start_time'].dt.floor('H').isin(before_app_periods)]
    screentime_after = screentime_df[screentime_df['start_time'].dt.floor('H').isin(after_app_periods)]

    screentime_agg_before = screentime_before.groupby('app').agg({'duration': 'sum'}).reset_index()
    screentime_agg_after = screentime_after.groupby('app').agg({'duration': 'sum'}).reset_index()

    return health_agg_before, health_agg_after, screentime_agg_before, screentime_agg_after


def main():
    st.title("Brain Rot App Usage & Health Metrics Analysis")
    st.markdown("""
        This app analyzes correlations between selected app usage (e.g., Reddit, TikTok) and health metrics such as 
        heart rate, HRV, resting HR, walking HR, and step count.
    """)

    # File upload
    healthkit_file = "./data/export.xml"
    screentime_file = "./data/screentime_data_2024-12-19 20:27:29.388001.csv"

    if healthkit_file and screentime_file:
        # Parse data
        st.write("Parsing files...")
        health_df = parse_healthkit_export(healthkit_file)
        screentime_df = parse_screentime_csv(screentime_file)

        # App picker
        st.write("Select an app to analyze:")
        app_name = st.selectbox("Pick an app from the screentime data:", screentime_df['app'].unique())

        if app_name:
            # Analyze app impact
            st.write(f"Analyzing data for 24-hour periods before and after {app_name} usage...")
            health_agg_before, health_agg_after, screentime_agg_before, screentime_agg_after = analyze_app_impact(
                app_name, health_df, screentime_df
            )

            # Display aggregated health data
            st.write("Health Metrics (24 Hours Before App Usage):")
            st.dataframe(health_agg_before)

            st.write("Health Metrics (24 Hours After App Usage):")
            st.dataframe(health_agg_after)

            # Visualization: Health Metrics Comparison
            st.write("Health Metrics Comparison (Before vs. After App Usage)")
            health_agg_before.columns = ['_'.join(col).strip() if isinstance(col, tuple) else col for col in health_agg_before.columns]
            health_agg_after.columns = ['_'.join(col).strip() if isinstance(col, tuple) else col for col in health_agg_after.columns]

            fig = px.bar(
                pd.concat([
                    health_agg_before.assign(period='Before'),
                    health_agg_after.assign(period='After')
                ]),
                x='type_',
                y='value_mean',
                color='period',
                barmode='group',
                error_y='value_std',
                labels={'type_': 'Health Metric', 'value_mean': 'Average Value'},
                title="Health Metrics Comparison (Mean and Std Dev)"
            )
            st.plotly_chart(fig)

            # Display aggregated screentime data
            st.write("Screentime (24 Hours Before App Usage):")
            st.dataframe(screentime_agg_before)

            st.write("Screentime (24 Hours After App Usage):")
            st.dataframe(screentime_agg_after)

            # Visualization: Screentime Comparison
            st.write("Screentime Comparison (Before vs. After App Usage)")
            fig = px.bar(
                pd.concat([
                    screentime_agg_before.assign(period='Before'),
                    screentime_agg_after.assign(period='After')
                ]),
                x='app',
                y='duration',
                color='period',
                barmode='group',
                labels={'app': 'App', 'duration': 'Usage Duration'},
                title="Screentime Comparison (Before vs. After App Usage)"
            )
            st.plotly_chart(fig)


if __name__ == "__main__":
    main()