import sqlite3
import pandas as pd
import os
from datetime import datetime
# Path to the Screen Time database
db_path = os.path.expanduser('~/Library/Application Support/Knowledge/knowledgeC.db')

# Convert Unix timestamp to human-readable date
def unix_to_date(unix_timestamp):
    try:
        return datetime.fromtimestamp(unix_timestamp).strftime('%Y-%m-%d %H:%M:%S')
    except (OSError, OverflowError, ValueError):
        return None

# Check if the database file exists
if not os.path.exists(db_path):
    print(f"Database file not found at {db_path}")
else:
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)

        # Provided query
        query = """
        SELECT
            ZOBJECT.ZVALUESTRING AS "app", 
            (ZOBJECT.ZENDDATE - ZOBJECT.ZSTARTDATE) AS "usage",
            (ZOBJECT.ZSTARTDATE + 978307200) as "start_time", 
            (ZOBJECT.ZENDDATE + 978307200) as "end_time",
            (ZOBJECT.ZCREATIONDATE + 978307200) as "created_at", 
            ZOBJECT.ZSECONDSFROMGMT AS "tz",
            ZSOURCE.ZDEVICEID AS "device_id",
            ZSYNCPEER.ZMODEL AS "device_model"
        FROM
            ZOBJECT 
            LEFT JOIN
            ZSTRUCTUREDMETADATA 
            ON ZOBJECT.ZSTRUCTUREDMETADATA = ZSTRUCTUREDMETADATA.Z_PK 
            LEFT JOIN
            ZSOURCE 
            ON ZOBJECT.ZSOURCE = ZSOURCE.Z_PK 
            LEFT JOIN
            ZSYNCPEER
            ON ZSOURCE.ZDEVICEID = ZSYNCPEER.ZDEVICEID
        WHERE
            ZSTREAMNAME = "/app/usage"
        ORDER BY
            ZSTARTDATE DESC
        """

        # Load the data into a pandas DataFrame
        df = pd.read_sql_query(query, conn)

        # Print the first few rows of the DataFrame to verify data
        print("Initial data loaded:")
        print(df.head())

        # Convert Unix timestamps to human-readable dates
        df['start_time'] = df['start_time'].apply(unix_to_date)
        df['end_time'] = df['end_time'].apply(unix_to_date)
        df['created_at'] = df['created_at'].apply(unix_to_date)

        # Print the data after date conversion
        print("Data after date conversion:")
        print(df.head())

        # Close the database connection
        conn.close()

        # Remove rows with invalid dates
        df = df.dropna(subset=['start_time', 'end_time', 'created_at'])

        # Print the data before exporting
        print("Final data before exporting:")
        print(df.head())

        # Save to CSV
        csv_path = f'../data/screentime_data_{datetime.now()}.csv'
        df.to_csv(csv_path, index=False)
        print(f"Screen Time data has been exported to {csv_path}")

        # Save to JSON
        json_path = f'../data/screentime_data_{datetime.now()}.json'
        df.to_json(json_path, orient='records', lines=True)
        print(f"Screen Time data has been exported to {json_path}")

    except sqlite3.OperationalError as e:
        print(f"An error occurred: {e}")
    except AttributeError as e:
        print(f"AttributeError: {e}")
