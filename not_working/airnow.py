import pandas as pd
import requests
from datetime import datetime, timedelta

# Load the GPX data CSV file
input_csv_path = 'csvData/output500.csv'
df = pd.read_csv(input_csv_path)

# AirNow API details
api_key = '76B3C277-4B06-4D17-B1C7-261A92A3E7B4'
base_url = 'http://www.airnowapi.org/aq/observation/latLong/historical/'

def fetch_air_quality(lat, lon, date_time):
    # Format the date_time for the API request
    date_time_str = date_time.strftime('%Y-%m-%dT%H:%M:%S')
    
    # API request parameters
    params = {
        'format': 'application/json',
        'latitude': lat,
        'longitude': lon,
        'date': date_time_str,
        'distance': 25,
        'API_KEY': api_key
    }
    
    # Make the API request
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return []

# Calculate average pollution exposure for the hour prior to each timestamp
average_pm25 = []
average_pm10 = []

for index, row in df.iterrows():
    # Parse the timestamp with the appropriate format
    timestamp = datetime.strptime(row['timestamp'], '%m/%d/%Y, %I:%M:%S %p')
    start_time = timestamp - timedelta(hours=1)
    
    hourly_pm25 = []
    hourly_pm10 = []
    
    for minute in range(60):
        time_point = start_time + timedelta(minutes=minute)
        air_quality_data = fetch_air_quality(row['latitude'], row['longitude'], time_point)
        
        for data_point in air_quality_data:
            if data_point['ParameterName'] == 'PM2.5':
                hourly_pm25.append(data_point['AQI'])
            elif data_point['ParameterName'] == 'PM10':
                hourly_pm10.append(data_point['AQI'])
    
    # Calculate averages
    if hourly_pm25:
        average_pm25.append(sum(hourly_pm25) / len(hourly_pm25))
    else:
        average_pm25.append(None)
    
    if hourly_pm10:
        average_pm10.append(sum(hourly_pm10) / len(hourly_pm10))
    else:
        average_pm10.append(None)

# Add the average values to the DataFrame
df['avg_pm25'] = average_pm25
df['avg_pm10'] = average_pm10

# Save the updated DataFrame to a new CSV file
output_csv_path_with_air_quality = 'csvData/aqi_output.csv'
df.to_csv(output_csv_path_with_air_quality, index=False)

output_csv_path_with_air_quality
