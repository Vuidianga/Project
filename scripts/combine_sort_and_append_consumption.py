import os
import pandas as pd
import sqlite3
import json
import warnings
from datetime import datetime


def process_consumption_data(input_folder, output_csv_path, sqlite_db_path, table_name="consumption"):
    # Suppress future warnings
    warnings.simplefilter(action='ignore', category=FutureWarning)

    # Define all possible columns in the order you want them to appear
    all_columns = [
        "Date", "Time", "id",
        "a_current", "a_voltage", "a_act_power", "a_aprt_power", "a_pf", "a_freq",
        "b_current", "b_voltage", "b_act_power", "b_aprt_power", "b_pf", "b_freq",
        "c_current", "c_voltage", "c_act_power", "c_aprt_power", "c_pf", "c_freq",
        "n_current", "total_current", "total_act_power", "total_aprt_power",
        "a_total_act_energy", "a_total_act_ret_energy",
        "b_total_act_energy", "b_total_act_ret_energy",
        "c_total_act_energy", "c_total_act_ret_energy",
        "total_act", "total_act_ret",
        "user_calibrated_phase", "Date_Time"
    ]

    # Initialize empty DataFrame with all columns
    new_data = pd.DataFrame(columns=all_columns)

    # Process all JSON files in the input folder
    for file in os.listdir(input_folder):
        if file.endswith('.json'):
            file_path = os.path.join(input_folder, file)
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)

                    # Convert empty lists to None and ensure all fields are present
                    processed_data = {}
                    for col in all_columns:
                        if col in data:
                            if isinstance(data[col], list) and not data[col]:
                                processed_data[col] = None
                            else:
                                processed_data[col] = data[col]
                        else:
                            processed_data[col] = None

                    # Create DataFrame from the processed data
                    temp_df = pd.DataFrame([processed_data])

                    # Ensure all columns are present
                    for col in all_columns:
                        if col not in temp_df.columns:
                            temp_df[col] = None

                    # Reorder columns to match our defined order
                    temp_df = temp_df[all_columns]

                    # Find existing rows with same Date+Time
                    if not new_data.empty:
                        mask = (new_data['Date'] == processed_data['Date']) & \
                               (new_data['Time'] == processed_data['Time'])
                        if mask.any():
                            # Update existing row with new non-null values
                            idx = mask.idxmax()
                            for col in all_columns:
                                if pd.notna(temp_df[col].iloc[0]):
                                    new_data.at[idx, col] = temp_df[col].iloc[0]
                            continue

                    # If no existing row, append new data
                    new_data = pd.concat([new_data, temp_df], ignore_index=True)

            except Exception as e:
                print(f"Warning: Failed to process file {file}: {e}")

    # If no new data was loaded, return
    if new_data.empty:
        print("No new JSON data found.")
        return None

    # Check required columns
    if 'Date' not in new_data.columns or 'Time' not in new_data.columns:
        print("Error: 'Date' or 'Time' columns are missing.")
        return None

    # Create datetime column for sorting
    new_data["Date_Time"] = pd.to_datetime(new_data["Date"] + " " + new_data["Time"])
    new_data = new_data.sort_values(by=["Date_Time"])

    # Handle CSV file (same as before)
    if os.path.exists(output_csv_path):
        try:
            existing_csv_data = pd.read_csv(output_csv_path)
            for col in all_columns:
                if col not in existing_csv_data.columns:
                    existing_csv_data[col] = None
            existing_csv_data = existing_csv_data[all_columns]
            
            # Combine with new data and remove duplicates
            combined_csv_data = pd.concat([existing_csv_data, new_data], ignore_index=True)
            combined_csv_data = combined_csv_data.drop_duplicates(subset=['Date', 'Time'], keep='last')
            combined_csv_data["Date_Time"] = pd.to_datetime(combined_csv_data["Date"] + " " + combined_csv_data["Time"])
            combined_csv_data = combined_csv_data.sort_values(by=["Date_Time"])
        except Exception as e:
            print(f"Warning: Failed to read existing CSV, using new data only. Error: {e}")
            combined_csv_data = new_data
    else:
        combined_csv_data = new_data

    # Save to CSV
    try:
        combined_csv_data.to_csv(output_csv_path, index=False)
        print(f"Data successfully saved to CSV at {output_csv_path}")
    except Exception as e:
        print(f"Error: Failed to write CSV. {e}")
        return None

    # Handle SQLite database - THE KEY FIX IS HERE
    try:
        conn = sqlite3.connect(sqlite_db_path)
        
        # Read existing database data
        try:
            existing_db_data = pd.read_sql(f"SELECT * FROM {table_name}", conn)
            for col in all_columns:
                if col not in existing_db_data.columns:
                    existing_db_data[col] = None
            existing_db_data = existing_db_data[all_columns]
        except:
            # Table doesn't exist or is empty
            existing_db_data = pd.DataFrame(columns=all_columns)
        
        # Combine with new data and remove duplicates
        combined_db_data = pd.concat([existing_db_data, new_data], ignore_index=True)
        combined_db_data = combined_db_data.drop_duplicates(subset=['Date', 'Time'], keep='last')
        combined_db_data["Date_Time"] = pd.to_datetime(combined_db_data["Date"] + " " + combined_db_data["Time"])
        combined_db_data = combined_db_data.sort_values(by=["Date_Time"])
        
        # Convert lists to strings for database compatibility
        combined_db_data['user_calibrated_phase'] = combined_db_data['user_calibrated_phase'].apply(
            lambda x: str(x) if isinstance(x, list) else x
        )
        
        # Write the complete dataset back to database
        combined_db_data.to_sql(
            table_name,
            conn,
            if_exists='replace',  # Safe because we've merged all data
            index=False,
            dtype={'user_calibrated_phase': 'TEXT'}
        )
        conn.close()
        print(f"Data successfully written to SQLite database at {sqlite_db_path}")
    except Exception as e:
        print(f"Error: Failed to write to SQLite database. {e}")
        return None

    return combined_db_data

if __name__ == "__main__":
    process_consumption_data(
        "/home/pi/.node-red/projects/Project/temporal_file/consumption",
        "/home/pi/.node-red/projects/Project/DataBase/cons_.csv",
        "/home/pi/.node-red/projects/Project/DataBase/cons_db.sqlite"
    )
