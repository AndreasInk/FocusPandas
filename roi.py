import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from categories import categorize_apps

def main():
    st.title("Weekly ROI Analysis with Screentime & Browser History")

    # File uploaders
    screentime_file = st.file_uploader("Upload Screentime Data CSV", type=["csv"])
    download_file = st.file_uploader("Upload Download Data CSV", type=["csv"])
    browser_file = st.file_uploader("Upload Browser History CSV", type=["csv"])

    # Start date input
    start_date = st.date_input(
        "Select Start Date",
        value=datetime.date(2024, 11, 1),
        min_value=datetime.date(2000, 1, 1),
    )

    # --------------------------------------------------------------------
    # 1) LOAD DATA
    # --------------------------------------------------------------------
    # Screentime
    screentime_data = None
    if screentime_file:
        try:
            screentime_data = pd.read_csv(screentime_file)
            screentime_data['date'] = pd.to_datetime(screentime_data['start_time'])
            screentime_data['hours'] = pd.to_numeric(screentime_data['usage'], errors='coerce').fillna(0)
            # Filter based on start_date
            screentime_data = screentime_data[screentime_data['date'] >= pd.to_datetime(start_date)]
            screentime_data = categorize_apps(screentime_data)

            if st.checkbox("Show Screentime Raw Data"):
                st.dataframe(screentime_data.head(20))
        except Exception as e:
            st.error(f"Error loading screentime data: {e}")
            screentime_data = None

    # Download Data
    download_values = []
    if download_file:
        try:
            download_data_df = pd.read_csv(download_file)
            # Assume row 0 has the weekly downloads in columns[1:]
            download_values = download_data_df.iloc[0, 1:].tolist()
            if st.checkbox("Show Download Raw Data"):
                st.dataframe(download_data_df.head())
        except Exception as e:
            st.error(f"Error loading download data: {e}")
            download_values = []

    # Browser Data
    browser_df = None
    if browser_file:
        try:
            browser_df = pd.read_csv(browser_file)
            browser_df['Timestamp'] = pd.to_datetime(browser_df['Timestamp'])
            browser_df['date'] = browser_df['Timestamp'].dt.date

            if st.checkbox("Show Browser History Raw Data"):
                st.dataframe(browser_df.head(20))
        except Exception as e:
            st.error(f"Error loading browser data: {e}")
            browser_df = None

    # Need screentime + downloads to calculate ROI
    if not (screentime_data is not None and len(download_values) > 0):
        st.warning("Please upload both Screentime and Download data to see ROI analysis.")
        return

    # --------------------------------------------------------------------
    # 2) WEEKLY SCREENTIME & ROI
    # --------------------------------------------------------------------
    # Group screentime by category/week
    weekly_data = (
        screentime_data
        .groupby(['category', pd.Grouper(key='date', freq='W-MON')])['hours']
        .sum()
        .unstack(fill_value=0)
    )
    # Keep only columns/weeks >= start_date
    valid_cols = [c for c in weekly_data.columns if c >= pd.to_datetime(start_date)]
    weekly_data = weekly_data[valid_cols]
    # Transpose so that rows=weeks, columns=categories
    weekly_data = weekly_data.T.sort_index()

    # If we have 3 rows (weeks) but 40 download points, slice downloads to length 3
    if len(weekly_data.index) < len(download_values):
        st.warning(
            f"We have {len(weekly_data.index)} weeks of screentime but "
            f"{len(download_values)} download data points. "
            "Only partial ROI can be calculated. Slicing downloads to match screentime weeks."
        )
        download_values = download_values[:len(weekly_data.index)]
    elif len(weekly_data.index) > len(download_values):
        # Rare case if more screentime weeks than downloads
        weekly_data = weekly_data.iloc[:len(download_values)]

    # Add a 'downloads' column
    weekly_data['downloads'] = download_values
    weekly_data['downloads'] = weekly_data['downloads'].replace(0, 1e-9)  # avoid div-by-zero

    # Screentime ROI (hours per download)
    categories = [c for c in weekly_data.columns if c != 'downloads']
    roi_data = pd.DataFrame(index=weekly_data.index)
    for cat in categories:
        roi_data[cat] = weekly_data[cat] / weekly_data['downloads']

   # 3) WEEKLY BROWSER HISTORY AGGREGATION
    browser_roi = pd.DataFrame()
    if browser_df is not None:
        # Group browser data by category and weekly
        weekly_browsing = (
            browser_df
            .groupby(['Category', pd.Grouper(key='Timestamp', freq='W-MON')])
            .size()
            .unstack(fill_value=0)
        )
        
        # Transpose so rows=weeks, columns=categories
        weekly_browsing = weekly_browsing.T.sort_index()  # weekly_browsing.index = weekly Mondays
        
        st.write("Raw weekly_browsing (before alignment):", weekly_browsing)
        
        # 1) INTERSECT the weekly_browsing.index with roi_data.index (the screentime weeks)
        common_weeks = weekly_browsing.index.intersection(weekly_data.index)
        weekly_browsing = weekly_browsing.loc[common_weeks]
        weekly_data_common = weekly_data.loc[common_weeks]

        weekly_browsing['downloads'] = weekly_data_common['downloads'].replace(0, 1e-9)
        
        # 4) Finally, compute visits/download = "browser ROI"
        browser_roi = pd.DataFrame(index=common_weeks)
        for cat in weekly_browsing.columns.drop('downloads'):
            browser_roi[cat] = weekly_browsing[cat] / weekly_browsing['downloads']
        
        st.write("browser_roi (aligned with screentime weeks):", browser_roi)
    # --------------------------------------------------------------------
    # 4) BAR CHART: SCREENTIME ROI + BROWSER ROI
    #    We’ll plot two bars for each category:
    #    1) Screentime hours/download
    #    2) Browser visits/download
    # --------------------------------------------------------------------
    st.subheader("Weekly ROI: Time Spent & Browser Visits per Download by Category")

    # Let user select categories from screentime or browser
    all_possible_cats = sorted(set(roi_data.columns) | set(browser_roi.columns))
    selected_categories = st.multiselect(
        "Select Categories to Plot",
        options=all_possible_cats,
        default=["Development", "Marketing"]
    )

    if not selected_categories:
        st.warning("Please select at least one category to plot.")
        return

    fig, ax = plt.subplots(figsize=(12, 8))
    bar_width = 2
    for i, cat in enumerate(selected_categories):
        # x-values shift so bars don’t overlap
        x_positions = roi_data.index + pd.Timedelta(days=i*3)
        
        # Screentime ROI bar
        if cat in roi_data.columns:
            ax.bar(
                x_positions,
                roi_data[cat],
                width=bar_width,
                label=f"{cat} (Screentime)",
                alpha=0.7
            )
        
        # Browser ROI bar
        if cat in browser_roi.columns:
            # shift by 1 day to show side-by-side
            ax.bar(
                x_positions + pd.Timedelta(days=1),
                browser_roi[cat],
                width=bar_width,
                label=f"{cat} (Browser)",
                alpha=0.7
            )

    ax.set_title("Weekly ROI: Screentime Hours per Download", fontsize=16)
    ax.set_xlabel("Week", fontsize=12)
    ax.set_ylabel("ROI (Hours/Download)", fontsize=12)
    ax.legend()
    ax.grid(axis='y')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(fig)

# --------------------------------------------------------------------
    # 4B) SEPARATE CHART FOR BROWSER ROI ONLY
    # --------------------------------------------------------------------
    st.subheader("Browser ROI: Visits per Download by Category")

    # Gather browser-only categories (columns in browser_roi)
    browser_categories = sorted(browser_roi.columns)

    # Prompt user to select which browser categories to visualize
    selected_browser_cats = st.multiselect(
        "Select Browser Categories to Plot",
        options=browser_categories,
        default=browser_categories[:3]  # Pick the first few as a default
    )

    if not selected_browser_cats:
        st.warning("Please select at least one browser category to plot.")
    else:
        # Build a bar chart similar to your screentime chart
        fig_browser, ax_browser = plt.subplots(figsize=(12, 8))
        bar_width = 2
        for i, cat in enumerate(selected_browser_cats):
            x_positions = browser_roi.index + pd.Timedelta(days=i * 3)
            ax_browser.bar(
                x_positions,
                browser_roi[cat],
                width=bar_width,
                label=cat,
                alpha=0.7
            )
        
        ax_browser.set_title("Weekly Browser ROI: Visits per Download", fontsize=16)
        ax_browser.set_xlabel("Week Start (Mon)", fontsize=12)
        ax_browser.set_ylabel("Visits per Download", fontsize=12)
        ax_browser.legend()
        ax_browser.grid(axis='y')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(fig_browser)
    # --------------------------------------------------------------------
    # 5) DOWNLOAD PROCESSED DATA
    # --------------------------------------------------------------------
    @st.cache_data
    def convert_df_to_csv(df):
        return df.to_csv(index=True).encode('utf-8')

    # Optionally let the user download screentime ROI data
    st.download_button(
        label="Download Screentime ROI Data as CSV",
        data=convert_df_to_csv(roi_data),
        file_name="screentime_ROI.csv",
        mime="text/csv",
    )
    # And optionally the browser ROI data
    if browser_df is not None:
        st.download_button(
            label="Download Browser ROI Data as CSV",
            data=convert_df_to_csv(browser_roi),
            file_name="browser_ROI.csv",
            mime="text/csv",
        )

if __name__ == "__main__":
    main()