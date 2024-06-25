import pandas as pd

# Load the CSV files into DataFrames
gpxtocsv = pd.read_csv('gpxtocsv.csv')
nice = pd.read_csv('nice.csv')

# Convert 'ValidTime' to hour and add a 'ValidDate' column (assuming it's in format MM/DD/YYYY, HH:MM)
gpxtocsv['Hour_gpxtocsv'] = pd.to_datetime(gpxtocsv['ValidTime'], format='%H:%M').dt.hour
nice['Hour_nice'] = pd.to_datetime(nice['Hour'], format='%H:%M').dt.hour

# Filter rows in gpxtocsv where ValidDate is '04/16/2024'
gpxtocsv_filtered = gpxtocsv[gpxtocsv['ValidDate'] == '04/16/2024']

# Merge DataFrames based on matching hours
merged_data = pd.merge(gpxtocsv_filtered, nice, left_on='Hour_gpxtocsv', right_on='Hour_nice', how='inner')

# Drop redundant columns and 'Hour' columns
merged_data.drop(columns=['Hour_gpxtocsv', 'Hour_nice'], inplace=True)

# Save merged data to CSV file
merged_data.to_csv('final_merged_filtered.csv', index=False)

print("Merged and filtered data saved to 'final_merged_filtered.csv'.")
