import pandas as pd
import numpy as np
from scipy.spatial import cKDTree
import os
import glob
from datetime import datetime, timedelta

# Function to find nearest station
def find_nearest_station(gps_point, stations):
    distances, indices = stations.query(gps_point)
    return indices

# Read gpxtocsv.csv
gps_data = pd.read_csv('gpxtocsv.csv')
gps_data['timestamp'] = pd.to_datetime(gps_data['timestamp'], format="%m/%d/%Y, %I:%M:%S %p")

# Read all dat2csv files
csv_files = glob.glob('csvFiles/*.csv')
air_quality_data = pd.concat([pd.read_csv(f) for f in csv_files])

# Prepare air quality data
air_quality_data['Datetime'] = pd.to_datetime(air_quality_data['ValidDate'] + ' ' + air_quality_data['ValidTime'], format="%m/%d/%Y %H:%M")
air_quality_data = air_quality_data[['Datetime', 'Latitude', 'Longitude', 'PM25', 'PM10']]
air_quality_data = air_quality_data.dropna(subset=['Latitude', 'Longitude'])

# Convert PM25 and PM10 to numeric, replacing empty strings with NaN
air_quality_data['PM25'] = pd.to_numeric(air_quality_data['PM25'], errors='coerce')
air_quality_data['PM10'] = pd.to_numeric(air_quality_data['PM10'], errors='coerce')

# Create KD-Tree for efficient nearest neighbor search
tree = cKDTree(air_quality_data[['Latitude', 'Longitude']])

# Function to get air quality for a specific point and time
def get_air_quality(row, air_quality_data, tree):
    gps_point = np.array([[row['latitude'], row['longitude']]])
    nearest_index = find_nearest_station(gps_point, tree)[0]
    
    nearest_station = air_quality_data.iloc[nearest_index]
    time_diff = abs(nearest_station['Datetime'] - row['timestamp'])
    
    if time_diff <= timedelta(hours=1):
        return nearest_station['PM25'], nearest_station['PM10']
    else:
        return np.nan, np.nan

# Apply the function to each row in gps_data
gps_data[['PM25', 'PM10']] = gps_data.apply(lambda row: pd.Series(get_air_quality(row, air_quality_data, tree)), axis=1)

# Save the updated gps_data to a new CSV file
gps_data.to_csv('gpxtocsv_with_air_quality.csv', index=False)

print("Process completed. Check 'gpxtocsv_with_air_quality.csv' for results.")