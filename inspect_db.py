import sqlite3
import os

# Path to the Screen Time database
db_path = os.path.expanduser('~/Library/Application Support/Knowledge/knowledgeC.db')

# Connect to the SQLite database
conn = sqlite3.connect(db_path)

# Query to get the schema of all tables
schema_query = "SELECT name FROM sqlite_master WHERE type='table';"
tables = conn.execute(schema_query).fetchall()

print("Tables in the database:")
for table in tables:
    print(table[0])
    columns_query = f"PRAGMA table_info({table[0]});"
    columns = conn.execute(columns_query).fetchall()
    for column in columns:
        print(f"  {column[1]} ({column[2]})")

conn.close()
