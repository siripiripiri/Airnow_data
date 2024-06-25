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

# Further filter the DataFrame for latitude and longitude starting values
def filter_lat_long(df):
    lat_columns = [col for col in df.columns if 'lat' in col.lower()]
    long_columns = [col for col in df.columns if 'long' in col.lower()]

    if lat_columns and long_columns:
        lat_col = lat_columns[0]
        long_col = long_columns[0]
        filtered_df = df[df[lat_col].astype(str).str.startswith('34.0') & 
                         df[long_col].astype(str).str.startswith('-118.2')]
        
        
        filtered_df[['Hour']] = filtered_df[['ValidTime']]
        filtered_df = filtered_df.drop('ValidTime',axis=1)
        filtered_df[['lat_Approx']] = filtered_df[['Latitude']]
        filtered_df = filtered_df.drop('Latitude',axis=1)
        filtered_df[['long_Approx']] = filtered_df[['Longitude']]
        filtered_df = filtered_df.drop('Longitude',axis=1)

        filtered_df = filtered_df[['lat_Approx','long_Approx','Hour','PM10_AQI','PM25_AQI']]

        filtered_df = filtered_df.sort_values(by='Hour')
        filtered_df.reset_index(drop=True, inplace=True)

        return filtered_df
    return pd.DataFrame()

result_df = filter_lat_long(result_df)

# Save the result to a new CSV file
result_df.to_csv('nice.csv', index=False)

print("Process completed. Check 'nice.csv' for results.")
