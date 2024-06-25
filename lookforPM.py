import pandas as pd
import os
import glob

# Function to read CSV files with flexible encoding
def read_csv_flexible(filepath):
    encodings = ['utf-8', 'ISO-8859-1', 'ascii', 'latin1']
    for encoding in encodings:
        try:
            return pd.read_csv(filepath, encoding=encoding)
        except Exception as e:
            continue
    raise ValueError(f"Could not read the file {filepath} with any of the encodings.")

# Function to filter rows with PM2.5 and PM10 values
def filter_pm_values(df):
    pm25_columns = [col for col in df.columns if 'PM2.5' in col or 'PM25' in col]
    pm10_columns = [col for col in df.columns if 'PM10' in col]

    if pm25_columns and pm10_columns:
        return df.dropna(subset=pm25_columns + pm10_columns)
    return pd.DataFrame()

# Directory containing the CSV files
csv_dir = 'csvFiles'

# List to hold the filtered DataFrames
filtered_dfs = []

# Process each CSV file
csv_files = glob.glob(os.path.join(csv_dir, '*.csv'))
for csv_file in csv_files:
    try:
        df = read_csv_flexible(csv_file)
        filtered_df = filter_pm_values(df)
        if not filtered_df.empty:
            filtered_dfs.append(filtered_df)
    except Exception as e:
        print(f"Failed to process {csv_file}: {e}")

# Combine all the filtered DataFrames
if filtered_dfs:
    result_df = pd.concat(filtered_dfs, ignore_index=True)
else:
    result_df = pd.DataFrame()

# Save the result to a new CSV file
result_df.to_csv('filtered_pm_values.csv', index=False)

print("Process completed. Check 'filtered_pm_values.csv' for results.")
