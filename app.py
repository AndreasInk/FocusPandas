import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
from pydantic import BaseModel
import seaborn as sns

class DataFrames(BaseModel):
    screen_df: pd.DataFrame
    heart_rate_df: pd.DataFrame
    sleep_df: pd.DataFrame
    audio_exposure_df: pd.DataFrame
    sleep_grouped: pd.DataFrame
    screen_grouped: pd.DataFrame
    productivity_usage: pd.DataFrame
    audio_grouped: pd.DataFrame

    class Config:
        arbitrary_types_allowed = True

def ensure_utc(df, col):
    """
    Ensure all datetime column is in the specified DataFrames are in UTC timezone.
    """
    if df[col].dt.tz is None:
        df[col] = df[col].dt.tz_localize('UTC')
    df[col] = df[col].dt.tz_convert('UTC')

def ensure_all_utc(dfs: list[pd.DataFrame], cols: list[str]):
    """
    Ensure all datetime columns in the specified DataFrames are in UTC timezone.
    """
    for df in dfs:
        for col in cols:
            try:
                ensure_utc(df, col)
            except:
                continue

def categorize_apps(df):
    """
    Categorize apps into productivity levels given a screentime dataframe.
    """
    # Define app categories
    app_categories = {
    'com.microsoft.VSCode': 'Productive',
    'com.apple.dt.Xcode': 'Productive',
    'company.thebrowser.Browser': 'Productive',
    'com.apple.Safari': 'Productive',
    'com.apple.mail': 'Productive',
    'com.netflix.Netflix': 'Distracting',
    'com.spotify.client': 'Neutral',
    'us.zoom.xos': 'Productive',
    'com.openai.chat': 'Productive',
    'com.apple.mobilesafari': 'Productive',
    'com.lukilabs.lukiapp': 'Productive',
    'com.apple.MobileSMS': 'Neutral',
    'com.google.ios.youtube': 'Distracting',
    'com.hnc.Discord': 'Neutral',
    'com.burbn.instagram': 'Distracting',
    'com.apple.mobilenotes': 'Productive',
    'com.Ai.ScribeGuide': 'Productive',
    'com.apple.VoiceMemos': 'Productive',
    'com.hammerandchisel.discord': 'Neutral',
    'com.figma.Desktop': 'Productive',
    'com.reddit.Reddit': 'Distracting',
    'com.linkedin.LinkedIn': 'Productive',
    'com.apple.Maps': 'Neutral',
    'com.apple.AppStore': 'Neutral',
    'com.microsoft.Word': 'Productive',
    'com.apple.Notes': 'Productive',
    'com.google.Gmail': 'Productive',
    'com.google.Docs': 'Productive',
    'com.apple.weather': 'Neutral',
    'com.google.calendar': 'Productive',
    'com.google.Slides': 'Productive',
    'com.apple.PhotoBooth': 'Neutral',
    'com.apple.Health': 'Productive',
    'com.apple.Terminal': 'Productive',
    'com.apple.Preview': 'Productive',
    'com.apple.finder': 'Productive',
    'com.apple.music': 'Productive',
    'com.apple.calendar': 'Productive',
    'com.apple.reminders': 'Productive',
    'com.apple.mobilecal': 'Productive',
    'com.apple.dictionary': 'Neutral',
    'com.apple.news': 'Neutral',
    'com.apple.contacts': 'Neutral',
    'com.apple.maps': 'Neutral',
    'com.apple.mobilephone': 'Neutral',
    'com.apple.calculator': 'Productive',
    'com.apple.camera': 'Neutral',
    'com.apple.TextEdit': 'Productive',
    'com.danielyaakob.studyTool': 'Productive',
    'com.apple.archiveutility': 'Neutral',
    'com.apple.SFSymbols-beta': 'Productive',
    'com.apple.iWork.Numbers': 'Productive',
    'com.apple.iWork.Pages': 'Productive',
    'com.apple.iWork.Keynote': 'Productive',
    'com.nvidia.gfnpc.mall': 'Distracting',
    'com.Ai.NeuroNote': 'Productive',
    'com.Ai.PingPath': 'Productive',
    'com.apple.SystemPreferences': 'Neutral',
    'com.vinsol.strivepd': 'Productive'
}

    # Apply categories to the DataFrame
    df['category'] = df['app'].map(app_categories).fillna('Other')
    return df

@st.cache_data
def setup_data() -> DataFrames:
    """
    Setup the data for analysis.
    """
    asleep_values = [1, 3, 4, 5]
    data_dir = "./data"
    # Paths to your data files
    csv_files = [os.path.join(data_dir, file) for file in os.listdir(data_dir) if file.endswith(".csv")]
    healthkit_export_xml = next((os.path.join(data_dir, file) for file in os.listdir(data_dir) if file.endswith(".xml")), None)

    screentime_dfs = [parse_screentime_csv(csv_file) for csv_file in csv_files]
    screen_df = pd.concat(screentime_dfs, ignore_index=True)
    # Parse health data from the XML file
    heart_rate_df = parse_healthkit_export(healthkit_export_xml, 'HKQuantityTypeIdentifierHeartRate')
    sleep_df = parse_healthkit_export(healthkit_export_xml, 'HKCategoryTypeIdentifierSleepAnalysis')
    audio_exposure_df = parse_healthkit_export(healthkit_export_xml, 'HKQuantityTypeIdentifierHeadphoneAudioExposure')

    # Convert datetime columns and ensure they are in UTC
    screen_df['start_time'] = pd.to_datetime(screen_df['start_time'])
    screen_df['end_time'] = pd.to_datetime(screen_df['end_time'])

    ensure_all_utc([screen_df, heart_rate_df, sleep_df, audio_exposure_df], ['startDate', 'endDate', "start_time", "end_time"])

        # Convert 'value' to numeric type
    sleep_df['value'] = pd.to_numeric(sleep_df['value'], errors='coerce')

    # Map numeric codes to sleep state labels
    sleep_value_mapping = {
        0: 'InBed',
        1: 'AsleepUnspecified',
        2: 'Awake',
        3: 'AsleepCore',
        4: 'AsleepDeep',
        5: 'AsleepREM'
    }
    sleep_df['sleep_state'] = sleep_df['value'].map(sleep_value_mapping)

    # Calculate sleep duration in hours
    sleep_df['duration'] = (sleep_df['endDate'] - sleep_df['startDate']).dt.total_seconds() / 3600

    # Adjust sleep data to the next day
    sleep_df['date'] = sleep_df['startDate'].dt.date + pd.Timedelta(days=1)
    sleep_grouped = sleep_df.groupby('date').agg({'duration': 'sum'}).reset_index()

    # Group screen time usage by date
    screen_df['date'] = screen_df['start_time'].dt.date
    screen_df = categorize_apps(screen_df)
    screen_grouped = screen_df.groupby('date').agg({'usage': 'sum'}).reset_index()

    # Productivity apps list
    productivity_usage = screen_df[screen_df['category'] == 'Productive'].groupby('date')['usage'].sum().reset_index()
    productivity_usage['usage_hours'] = productivity_usage['usage'] / 3600

    # Process audio exposure data
    audio_exposure_df['date'] = audio_exposure_df['startDate'].dt.date
    audio_grouped = audio_exposure_df.groupby('date').agg({'value': 'mean'}).reset_index()
    audio_grouped.rename(columns={'value': 'audio_exposure'}, inplace=True)

    return DataFrames(screen_df=screen_df, heart_rate_df=heart_rate_df, sleep_df=sleep_df, audio_exposure_df=audio_exposure_df, sleep_grouped=sleep_grouped, screen_grouped=screen_grouped, productivity_usage=productivity_usage, audio_grouped=audio_grouped)

# Function to parse screentime CSV
@st.cache_data
def parse_screentime_csv(csv_file):
    """
    Parses the screentime CSV file and returns a DataFrame.
    """
    screentime_df = pd.read_csv(csv_file)
    screentime_df['start_time'] = pd.to_datetime(screentime_df['start_time'])
    screentime_df['end_time'] = pd.to_datetime(screentime_df['end_time'])
    return screentime_df

@st.cache_data
def parse_healthkit_export(xml_file, data_type):
    """
    Parses the HealthKit XML export file and returns a DataFrame of the specified data type.
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    # Extract records of the specified type
    health_data = []
    for record in root.findall("Record"):
        if record.attrib.get('type') == data_type:
            health_data.append(record.attrib)
    
    # Convert to DataFrame
    health_df = pd.DataFrame(health_data)
    
    # Convert timestamp columns
    if 'startDate' in health_df.columns:
        health_df['startDate'] = pd.to_datetime(health_df['startDate'])
    if 'endDate' in health_df.columns:
        health_df['endDate'] = pd.to_datetime(health_df['endDate'])
    # Convert 'value' column to numeric if possible
    if 'value' in health_df.columns:
        health_df['value'] = pd.to_numeric(health_df['value'], errors='coerce')
    return health_df

@st.cache_data
def peak_usage_times(screen_df):
    """
    Gets the largest usage times of the day.
    """
    st.title('Peak Usage Times')

    # Peak usage times
    screen_df['hour'] = screen_df['start_time'].dt.hour
    peak_usage_times = screen_df.groupby('hour')['usage'].sum().reset_index()

    # Convert usage to hours for better readability
    peak_usage_times['usage_hours'] = peak_usage_times['usage'] / 3600

    # Plot peak usage times
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(peak_usage_times['hour'], peak_usage_times['usage_hours'], width=0.8, align='center')
    ax.set_xlabel('Hour of the Day')
    ax.set_ylabel('Total Usage (hours)')
    ax.set_title('Peak Usage Times')
    ax.grid(True)

    st.pyplot(fig)

@st.cache_data
def screen_time_analysis(screen_df):
    """
    Analyzes the screen time data.
    """
    st.title('Screen Time Data Analysis')

    # Display Screen Time DataFrame
    st.subheader('Screen Time Data')

     # Group by date and category
    category_usage = screen_df.groupby(['date', 'category'])['usage'].sum().reset_index()
    category_usage['usage_hours'] = category_usage['usage'] / 3600

    # Pivot the DataFrame for easier plotting
    category_pivot = category_usage.pivot(index='date', columns='category', values='usage_hours').fillna(0)

    # Plot stacked bar chart
    fig, ax = plt.subplots(figsize=(12, 6))
    category_pivot.plot(kind='bar', stacked=True, ax=ax)
    ax.set_xlabel('Date')
    ax.set_ylabel('Usage (hours)')
    ax.set_title('Daily Usage by App Category')
    plt.xticks(rotation=45)
    st.pyplot(fig)

    
    total_usage_per_app = screen_df.groupby('app')['usage'].sum().reset_index()
    total_usage_per_app = total_usage_per_app.sort_values(by='usage', ascending=False)

    # Limit to top 10 apps by usage
    top_apps = total_usage_per_app.head(4)['app'].tolist()
    screen_df_top = screen_df[screen_df['app'].isin(top_apps)]

    # Aggregate usage by day for better readability
    screen_df_top['date'] = screen_df_top['start_time'].dt.date
    daily_usage = screen_df_top.groupby(['date', 'app'])['usage'].sum().unstack().fillna(0)

    # Plot total usage per app
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    daily_usage.plot(ax=ax1)
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Total Usage (seconds)')
    ax1.set_title('Total Usage per App')
    plt.xticks(rotation=45)
    ax1.legend(title='App', bbox_to_anchor=(1.05, 1), loc='upper left')
    st.pyplot(fig1)

    # Peak usage times
    screen_df['hour'] = screen_df['start_time'].dt.hour
    peak_usage_times = screen_df.groupby('hour')['usage'].sum().reset_index()
    peak_usage_times['usage_hours'] = peak_usage_times['usage'] / 3600

    # Plot peak usage times
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    ax2.bar(peak_usage_times['hour'], peak_usage_times['usage_hours'], width=0.8, align='center')
    ax2.set_xlabel('Hour of the Day')
    ax2.set_ylabel('Total Usage (hours)')
    ax2.set_title('Peak Usage Times')
    ax2.grid(True)
    st.pyplot(fig2)

    st.title('Usage Patterns Over Time')

    # Group by hour and category
    hourly_usage = screen_df.groupby(['hour', 'category'])['usage'].sum().reset_index()
    hourly_usage['usage_hours'] = hourly_usage['usage'] / 3600

    # Pivot for heatmap
    heatmap_data = hourly_usage.pivot(index='hour', columns='category', values='usage_hours').fillna(0)

    # Plot heatmap
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(heatmap_data, annot=True, fmt=".1f", cmap='YlGnBu', ax=ax)
    ax.set_title('Hourly Usage Heatmap by Category')
    st.pyplot(fig)
    

     # Total usage per app
    with st.expander(label="Data"):

        # Basic Statistics
        st.subheader('Basic Statistics')
        st.write(screen_df.describe())

        st.subheader('Daily Usage by Category')
        st.write(category_pivot)

        st.subheader('Total Usage per App')
        
        st.write(total_usage_per_app)


        st.subheader('Peak Usage Times')
        st.write(heatmap_data)

    # Summary
    st.subheader('Summary of Analysis')
    summary = {
        'total_usage': screen_df['usage'].sum(),
        'average_session_length': screen_df['usage'].mean(),
        'most_used_app': total_usage_per_app.iloc[0]['app'],
        'peak_usage_hour': peak_usage_times['hour'][peak_usage_times['usage'].idxmax()]
    }
    st.write(summary)

@st.cache_data
def peak_usage_and_heart_rate(screen_df, heart_rate_df):
    """
    Compares heart rate and screen time usage.
    """
    st.title('Peak Usage Times and Heart Rate')

    # Aggregate screen time usage by hour
    screen_df['hour'] = screen_df['start_time'].dt.hour
    hourly_screen_usage = screen_df.groupby('hour')['usage'].sum().reset_index()
    hourly_screen_usage['usage_hours'] = hourly_screen_usage['usage'] / 3600

    # Aggregate heart rate by hour
    heart_rate_df['hour'] = heart_rate_df['startDate'].dt.hour
    hourly_heart_rate = heart_rate_df.groupby('hour')['value'].mean().reset_index()

    # Plot screen time and heart rate
    fig, ax1 = plt.subplots(figsize=(10, 6))

    color = 'tab:blue'
    ax1.set_xlabel('Hour of the Day')
    ax1.set_ylabel('Screen Time Usage (hours)', color=color)
    ax1.bar(hourly_screen_usage['hour'], hourly_screen_usage['usage_hours'], color=color, alpha=0.6, label='Screen Time')
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('Heart Rate (count/min)', color=color)
    ax2.plot(hourly_heart_rate['hour'], hourly_heart_rate['value'], color=color, marker='o', linestyle='-', label='Heart Rate')
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()
    plt.title('Screen Time Usage and Heart Rate by Hour')
    ax1.grid(True)
    st.pyplot(fig)

@st.cache_data
def heart_rate_analysis(heart_rate_df, screen_df):
    st.title('Heart Rate Data Analysis')

    # Display Heart Rate DataFrame
    st.subheader('Heart Rate Data')
    st.write(heart_rate_df)

    # Basic Statistics
    st.subheader('Basic Statistics')
    st.write(heart_rate_df.describe())

    # Correlate screen time with heart rate data
    st.subheader('Correlation Analysis with Heart Rate')
    merged_df = pd.merge_asof(screen_df.sort_values('start_time'), heart_rate_df.sort_values('startDate'), left_on='start_time', right_on='startDate')
    correlation = merged_df[['usage', 'value']].corr()
    st.write(correlation)

    # Plot peak usage times and heart rate
    peak_usage_and_heart_rate(screen_df, heart_rate_df)

    # Plot heart rate vs screen time usage
    fig4, ax4 = plt.subplots(figsize=(10, 6))
    ax4.scatter(merged_df['value'], merged_df['usage'])
    ax4.set_xlabel('Heart Rate (count/min)')
    ax4.set_ylabel('Screen Time Usage (seconds)')
    ax4.set_title('Heart Rate vs Screen Time Usage')
    st.pyplot(fig4)


@st.cache_data
def sleep_analysis(sleep_df, screen_df, heart_rate_df, screen_grouped):
    """
    Analyze sleep data in relation to screen time and heart rate, including daily sleep patterns,
    correlations with screen time, and hourly patterns.
    """
    # Calculate sleep duration in hours
    sleep_df['duration'] = (sleep_df['endDate'] - sleep_df['startDate']).dt.total_seconds() / 3600

    # Adjust sleep data to the next day to better align with daily cycles
    sleep_df['date'] = sleep_df['startDate'].dt.date + pd.Timedelta(days=1)

    # Group sleep data by date
    sleep_grouped = sleep_df.groupby('date').agg({'duration': 'sum'}).reset_index()

    # Group screen time usage by hour
    screen_df['hour'] = screen_df['start_time'].dt.hour
    hourly_screen_usage = screen_df.groupby('hour')['usage'].sum().reset_index()
    hourly_screen_usage['usage_hours'] = hourly_screen_usage['usage'] / 3600

    # Group heart rate data by hour
    heart_rate_df['hour'] = heart_rate_df['startDate'].dt.hour
    hourly_heart_rate = heart_rate_df.groupby('hour')['value'].mean().reset_index()

    # Display comprehensive analysis
    st.title('Comprehensive Sleep Data Analysis')

    # Plot sleep duration over time
    st.subheader('Sleep Duration Over Time')
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    ax1.plot(sleep_grouped['date'], sleep_grouped['duration'], marker='o')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Sleep Duration (hours)')
    ax1.set_title('Sleep Duration Over Time')
    ax1.grid(True)
    plt.xticks(rotation=45)
    st.pyplot(fig1)

    # Correlation analysis with screen time
    st.subheader('Correlation Analysis with Screen Time')
    merged_sleep_df = pd.merge(screen_grouped, sleep_grouped, on='date', how='inner')
    correlation_sleep = merged_sleep_df[['usage', 'duration']].corr()
    st.write(correlation_sleep)

    # Scatter plot for sleep vs. screen time usage
    st.subheader('Sleep Duration vs Screen Time Usage')
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    ax2.scatter(merged_sleep_df['duration'], merged_sleep_df['usage'], color='purple', alpha=0.7)
    ax2.set_xlabel('Sleep Duration (hours)')
    ax2.set_ylabel('Screen Time Usage (seconds)')
    ax2.set_title('Sleep Duration vs Screen Time Usage')
    ax2.grid(True)
    st.pyplot(fig2)

    # Heatmap: Hourly sleep vs. screen time
    st.subheader('Hourly Sleep vs. Screen Time Heatmap')

    # Ensure 'usage_hours' column is numeric and fill missing values
    hourly_screen_usage['usage_hours'] = pd.to_numeric(hourly_screen_usage['usage_hours'], errors='coerce').fillna(0)

    # Create the pivot table for the heatmap
    heatmap_data = hourly_screen_usage.pivot_table(values='usage_hours', index='hour', aggfunc='sum')

    # Plot the heatmap
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    sns.heatmap(heatmap_data, cmap='Blues', annot=True, fmt='.1f', ax=ax3)

    ax3.set_title("Hourly Sleep vs. Screen Time Usage")
    st.pyplot(fig3)

    # Overlay heart rate and screen time usage throughout the day
    st.subheader('Hourly Heart Rate and Screen Time Usage')
    fig4, ax4 = plt.subplots(figsize=(10, 6))

    # Bar plot for screen time usage
    ax4.bar(hourly_screen_usage['hour'], hourly_screen_usage['usage_hours'], color='blue', alpha=0.6, label='Screen Time Usage (hours)')
    ax4.set_xlabel('Hour of the Day')
    ax4.set_ylabel('Screen Time Usage (hours)', color='blue')
    ax4.tick_params(axis='y', labelcolor='blue')
    ax4.legend(loc='upper left')

    # Line plot for heart rate
    ax5 = ax4.twinx()
    ax5.plot(hourly_heart_rate['hour'], hourly_heart_rate['value'], color='red', marker='o', linestyle='-', label='Heart Rate (count/min)')
    ax5.set_ylabel('Heart Rate (count/min)', color='red')
    ax5.tick_params(axis='y', labelcolor='red')
    ax5.legend(loc='upper right')

    ax4.set_title('Heart Rate and Screen Time Usage by Hour of the Day')
    ax4.grid(True)
    fig4.tight_layout()
    st.pyplot(fig4)

    # Display Sleep DataFrame
    st.subheader('Sleep Data')
    st.write(sleep_df)


@st.cache_data
def additional_insights(screen_df, audio_exposure_df):
    st.title('Additional Insights')

    # Daily Screen Time Patterns
    st.subheader('Daily Screen Time Patterns')
    daily_screen_usage = screen_df.groupby('date')['usage'].sum().reset_index()
    daily_screen_usage['usage_hours'] = daily_screen_usage['usage'] / 3600

    fig1, ax1 = plt.subplots(figsize=(10, 6))
    ax1.plot(daily_screen_usage['date'], daily_screen_usage['usage_hours'], marker='o')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Screen Time Usage (hours)')
    ax1.set_title('Daily Screen Time Usage Patterns')
    plt.xticks(rotation=45)
    ax1.grid(True)
    st.pyplot(fig1)

    # Productivity vs. Music Loudness
    st.subheader('Productivity vs. Music Loudness')
    productivity_apps = ['com.microsoft.VSCode', 'com.apple.dt.Xcode', 'company.thebrowser.Browser', 'com.openai.chat']

    screen_df['category'] = screen_df['app'].apply(lambda x: 'Productive' if x in productivity_apps else 'Other')
    productivity_usage = screen_df[screen_df['category'] == 'Productive'].groupby('date')['usage'].sum().reset_index()
    productivity_usage['usage_hours'] = productivity_usage['usage'] / 3600

    audio_exposure_df['date'] = audio_exposure_df['startDate'].dt.date
    daily_audio_exposure = audio_exposure_df.groupby('date')['value'].mean().reset_index()

    # Merge DataFrames
    merged_productivity_audio = pd.merge(productivity_usage, daily_audio_exposure, on='date', how='inner')
    correlation_audio = merged_productivity_audio[['usage_hours', 'value']].corr()

    st.write(correlation_audio)

    fig2, ax2 = plt.subplots(figsize=(10, 6))
    ax2.scatter(merged_productivity_audio['value'], merged_productivity_audio['usage_hours'])
    ax2.set_xlabel('Average Audio Exposure (dBASPL)')
    ax2.set_ylabel('Productivity App Usage (hours)')
    ax2.set_title('Productivity App Usage vs. Average Audio Exposure')
    st.pyplot(fig2)

@st.cache_data
def productivity_analysis(sleep_grouped, productivity_usage, audio_grouped):
    st.title('Productivity Analysis')

    # Ensure 'date' columns are datetime
    sleep_grouped['date'] = pd.to_datetime(sleep_grouped['date'])
    productivity_usage['date'] = pd.to_datetime(productivity_usage['date'])
    audio_grouped['date'] = pd.to_datetime(audio_grouped['date'])

    # Create sleep_grouped_next_day by shifting the 'date' back by one day
    sleep_grouped_next_day = sleep_grouped.copy()
    sleep_grouped_next_day['date'] = sleep_grouped_next_day['date'] - pd.Timedelta(days=1)

    # Merge DataFrames for analysis
    merged_df_same_day = productivity_usage.merge(sleep_grouped, on='date', how='left')
    merged_df_next_day = productivity_usage.merge(sleep_grouped_next_day, on='date', how='left')
    merged_df_audio = productivity_usage.merge(audio_grouped, on='date', how='left')

    # Rename columns for clarity
    merged_df_same_day.rename(columns={'duration': 'same_day_sleep_duration'}, inplace=True)
    merged_df_next_day.rename(columns={'duration': 'next_day_sleep_duration'}, inplace=True)

    st.subheader('Productivity vs. Same Day Sleep Duration')
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    ax1.scatter(merged_df_same_day['same_day_sleep_duration'], merged_df_same_day['usage_hours'])
    ax1.set_xlabel('Same Day Sleep Duration (hours)')
    ax1.set_ylabel('Productivity App Usage (hours)')
    ax1.set_title('Productivity vs. Same Day Sleep Duration')
    st.pyplot(fig1)

    st.subheader('Productivity vs. Next Day Sleep Duration')
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    ax2.scatter(merged_df_next_day['next_day_sleep_duration'], merged_df_next_day['usage_hours'])
    ax2.set_xlabel('Next Day Sleep Duration (hours)')
    ax2.set_ylabel('Productivity App Usage (hours)')
    ax2.set_title('Productivity vs. Next Day Sleep Duration')
    st.pyplot(fig2)

    st.subheader('Productivity vs. Audio Exposure')
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    ax3.scatter(merged_df_audio['audio_exposure'], merged_df_audio['usage_hours'])
    ax3.set_xlabel('Average Audio Exposure (dBASPL)')
    ax3.set_ylabel('Productivity App Usage (hours)')
    ax3.set_title('Productivity vs. Audio Exposure')
    st.pyplot(fig3)

    st.subheader('Correlation Analysis')
    correlation_same_day = merged_df_same_day[['usage_hours', 'same_day_sleep_duration']].corr()
    correlation_next_day = merged_df_next_day[['usage_hours', 'next_day_sleep_duration']].corr()
    correlation_audio = merged_df_audio[['usage_hours', 'audio_exposure']].corr()

    st.write("Correlation with Same Day Sleep Duration")
    st.write(correlation_same_day)
    st.write("Correlation with Next Day Sleep Duration")
    st.write(correlation_next_day)
    st.write("Correlation with Audio Exposure")
    st.write(correlation_audio)

    # Insights summary
    st.subheader('Insights Summary')
    st.write('This analysis provides insights into how your productivity is influenced by sleep duration and audio exposure. Key correlations and trends are highlighted.')

@st.cache_data
def productivity_metrics(screen_df):
    st.title('Productivity Metrics')

    # Total usage per day
    total_daily_usage = screen_df.groupby('date')['usage'].sum().reset_index()
    total_daily_usage['usage_hours'] = total_daily_usage['usage'] / 3600

    # Productive usage per day
    productive_daily_usage = screen_df[screen_df['category'] == 'Productive'].groupby('date')['usage'].sum().reset_index()
    productive_daily_usage['usage_hours'] = productive_daily_usage['usage'] / 3600

    # Merge DataFrames
    daily_productivity = pd.merge(total_daily_usage[['date', 'usage_hours']], productive_daily_usage[['date', 'usage_hours']], on='date', how='left', suffixes=('_total', '_productive')).fillna(0)

    # Calculate productivity ratio
    daily_productivity['productivity_ratio'] = (daily_productivity['usage_hours_productive'] / daily_productivity['usage_hours_total']) * 100

    # Calculate averages
    avg_productive_hours = daily_productivity['usage_hours_productive'].mean()
    avg_productivity_ratio = daily_productivity['productivity_ratio'].mean()
    
    # Ensure daily_productivity DataFrame exists
    if 'daily_productivity' not in locals():
        # Total usage per day
        total_daily_usage = screen_df.groupby('date')['usage'].sum().reset_index()
        total_daily_usage['usage_hours'] = total_daily_usage['usage'] / 3600

        # Productive usage per day
        productive_daily_usage = screen_df[screen_df['category'] == 'Productive'].groupby('date')['usage'].sum().reset_index()
        productive_daily_usage['usage_hours'] = productive_daily_usage['usage'] / 3600

        # Merge DataFrames
        daily_productivity = pd.merge(
            total_daily_usage[['date', 'usage_hours']],
            productive_daily_usage[['date', 'usage_hours']],
            on='date',
            how='left',
            suffixes=('_total', '_productive')
        ).fillna(0)

        # Calculate productivity ratio
        daily_productivity['productivity_ratio'] = (daily_productivity['usage_hours_productive'] / daily_productivity['usage_hours_total']) * 100

    # Calculate 7-day rolling average for productivity ratio
    daily_productivity['rolling_productivity_ratio'] = daily_productivity['productivity_ratio'].rolling(window=7, min_periods=1).mean()

    # Plot productivity ratio over time
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(daily_productivity['date'], daily_productivity['productivity_ratio'], label='Daily Productivity Ratio')
    ax.plot(daily_productivity['date'], daily_productivity['rolling_productivity_ratio'], label='7-Day Rolling Average', linestyle='--')
    ax.set_xlabel('Date')
    ax.set_ylabel('Productivity Ratio (%)')
    ax.set_title('Productivity Ratio Over Time')
    plt.xticks(rotation=45)
    ax.legend()
    st.pyplot(fig)

    # Analyze productivity by day of the week
    daily_productivity['day_of_week'] = pd.to_datetime(daily_productivity['date']).dt.day_name()
    productivity_by_day = daily_productivity.groupby('day_of_week')['productivity_ratio'].mean().reindex([
        'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])

    # Plot productivity by day of the week
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    ax2.bar(productivity_by_day.index, productivity_by_day.values)
    ax2.set_xlabel('Day of the Week')
    ax2.set_ylabel('Average Productivity Ratio (%)')
    ax2.set_title('Average Productivity by Day of the Week')
    plt.xticks(rotation=45)
    st.pyplot(fig2)

    # Display metrics
    st.subheader('Daily Productivity Metrics')
    st.write(daily_productivity)
    
    st.write(screen_df.head())

    st.subheader('Average Productivity')
    st.write(f"Average Daily Productive Hours: {avg_productive_hours:.2f} hours")
    st.write(f"Average Productivity Ratio: {avg_productivity_ratio:.2f}%")

sidebar = st.sidebar
sidebar.title("HealthKit and Screen Time Data Analyzer")
sidebar.subheader("Understand your digital habits and health data.")


data = setup_data()

page = sidebar.radio("Go to", ["Screen Time Analysis", "Sleep Analysis", "Productivity Metrics", "Productivity Analysis", "Heart Rate Analysis", "Additional Insights"])

sidebar.markdown("""
---
Created by **Andreas Ink**
""")

sidebar.markdown("""  
[Github](https://github.com/AndreasInk)
[LinkedIn](https://www.linkedin.com/in/andreas-ink/)              
""")

if page == "Screen Time Analysis":
    screen_time_analysis(data.screen_df)
elif page == "Heart Rate Analysis":
    heart_rate_analysis(data.heart_rate_df, data.screen_df)
elif page == "Sleep Analysis":
    sleep_analysis(data.sleep_df, data.screen_df, data.heart_rate_df, data.screen_grouped)
elif page == "Productivity Analysis":
    productivity_analysis(data.sleep_grouped, data.productivity_usage, data.audio_grouped)
elif page == "Productivity Metrics":
    productivity_metrics(data.screen_df)
elif page == "Additional Insights":
    additional_insights(data.screen_df, data.audio_exposure_df)

