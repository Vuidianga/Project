import os
import pandas as pd

def sort_and_combine(folder_path, output_path):
    files = os.listdir(folder_path)
    new_csv = pd.DataFrame()

    for file in files:
        file_path = os.path.join(folder_path, file)
        if file.endswith('.csv'):
            temp = pd.read_csv(file_path)
            if not temp.empty:
                new_csv = pd.concat([new_csv, temp], ignore_index=True)

    # If database already exists
    if os.path.exists(output_path):
        # Read the existing database
        existing_csv = pd.read_csv(output_path)
        # Combine old and new data
        combined_csv = pd.concat([existing_csv, new_csv], ignore_index=True)
    else:
        combined_csv = new_csv

    # Sort by Date and Time
    combined_csv = combined_csv.sort_values(by=['Date', ' Time'])

    # Optional: remove exact duplicates
    combined_csv = combined_csv.drop_duplicates().reset_index(drop=True)

    # Save back to output path (overwrite)
    combined_csv.to_csv(output_path, index=False)
    print(f"Saved combined and sorted CSV to {output_path}")

    return combined_csv

if __name__ == "__main__":
    sort_and_combine(
        r"C:\Users\asantee\.node-red\projects\Project\temporal_file",
        r"C:\Users\asantee\.node-red\projects\Project\DataBase\db.csv"
    )
