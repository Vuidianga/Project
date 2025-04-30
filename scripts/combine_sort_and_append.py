import os
import pandas as pd
import sqlite3

def sort_and_combine(folder_path, output_csv_path, sqlite_db_path, table_name="data"):
    files = os.listdir(folder_path)
    new_csv = pd.DataFrame()

    for file in files:
        file_path = os.path.join(folder_path, file)
        if file.endswith('.csv'):
            temp = pd.read_csv(file_path)
            if not temp.empty:
                new_csv = pd.concat([new_csv, temp], ignore_index=True)

    # If database already exists
    if os.path.exists(output_csv_path):
        existing_csv = pd.read_csv(output_csv_path)
        combined_csv = pd.concat([existing_csv, new_csv], ignore_index=True)
    else:
        combined_csv = new_csv

    # Sort by Date and Time
    combined_csv = combined_csv.sort_values(by=['Date', 'Time'])

    # Group by Date, Time, and Timezone and merge non-null values
    combined_csv = combined_csv.groupby(['Date', 'Time', 'Timezone'], as_index=False).first()

    # Save to CSV
    combined_csv.to_csv(output_csv_path, index=False)
    print(f"Appended new data to CSV successfully.")

    # Write to SQLite database
    conn = sqlite3.connect(sqlite_db_path)
    combined_csv.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.close()
    print(f"Written data to SQLite database at {sqlite_db_path}.")

    return combined_csv

if __name__ == "__main__":
    sort_and_combine(
        r"C:\Users\asantee\.node-red\projects\Project\temporal_file",
        r"C:\Users\asantee\.node-red\projects\Project\DataBase\db.csv",
        r"C:\Users\asantee\.node-red\projects\Project\DataBase\db.sqlite"
    )
