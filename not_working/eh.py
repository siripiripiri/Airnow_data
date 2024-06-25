import gpxpy
import pandas as pd

# Load and parse the GPX file
gpx_file_path = 'danielle GPX .GPX'
with open(gpx_file_path, 'r') as gpx_file:
    gpx = gpxpy.parse(gpx_file)

# Extract data
gps_data = []
for track in gpx.tracks:
    for segment in track.segments:
        for point in segment.points:
            if point.time:  # Ensure time is not None
                gps_data.append({
                    'latitude': point.latitude,
                    'longitude': point.longitude,
                    'time': point.time
                })

# Convert to DataFrame and save to CSV
gps_data_df = pd.DataFrame(gps_data)
gps_data_df.to_csv('gps_data.csv', index=False)
print("csv file created!")





import pandas as pd
import os

# Load all survey CSV files
survey_data_folder = 'SurveyData'
survey_files = ['Ping1.csv', 'Ping2.csv', 'Ping3.csv', 'Ping4.csv', 'Ping5.csv', 'Ping6.csv']
survey_data_list = [pd.read_csv(os.path.join(survey_data_folder, file)) for file in survey_files]

# Combine survey data into a single DataFrame
survey_data = pd.concat(survey_data_list, ignore_index=True)

# Display the first few rows of the survey data
# print(survey_data.head())


import requests
from datetime import datetime, timedelta
import pandas as pd

API_KEY = '76B3C277-4B06-4D17-B1C7-261A92A3E7B4'

def get_air_quality_data(latitude, longitude, start_date, end_date):
    url = "https://www.airnowapi.org/aq/data/"
    params = {
        'startDate': start_date.strftime('%Y-%m-%dT%H'),
        'endDate': end_date.strftime('%Y-%m-%dT%H'),
        'parameters': 'PM25,PM10',
        'BBOX': f'{longitude-0.05},{latitude-0.05},{longitude+0.05},{latitude+0.05}',
        'dataType': 'B',
        'format': 'application/json',
        'verbose': '1',
        'monitorType': '0',
        'API_KEY': API_KEY
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    return data

# Example usage (You would loop over actual GPS data points in practice)
latitude = 37.7749  # Example latitude
longitude = -122.4194  # Example longitude
start_date = datetime(2024, 4, 16, 0)  # Start date and time
end_date = datetime(2023, 1, 1, 23)  # End date and time

# Fetch air quality data
air_quality_data = get_air_quality_data(latitude, longitude, start_date, end_date)

# Convert to DataFrame for easier manipulation
air_quality_df = pd.DataFrame(air_quality_data)
print(air_quality_df.head())


# def calculate_hourly_average_exposure(gps_data, survey_data):
#     results = []
#     for index, row in survey_data.iterrows():
#         survey_time = datetime.strptime(row['scheduled_start_local'], '%Y-%m-%d %H:%M:%S')
#         start_time = survey_time - timedelta(hours=1)
        
#         # Filter GPS data within the hour prior to survey_time
#         relevant_gps_data = [point for point in gps_data if start_time <= point['time'] < survey_time]
        
#         if not relevant_gps_data:
#             results.append({'timestamp': survey_time, 'avg_PM25': None, 'avg_PM10': None})
#             continue
        
#         latitudes = [point['latitude'] for point in relevant_gps_data]
#         longitudes = [point['longitude'] for point in relevant_gps_data]
        
#         # Calculate midpoint for bounding box
#         avg_latitude = sum(latitudes) / len(latitudes)
#         avg_longitude = sum(longitudes) / len(longitudes)
        
#         # Retrieve air quality data for this time period
#         air_quality_data = get_air_quality_data(avg_latitude, avg_longitude, start_time, survey_time)
        
#         if not air_quality_data:
#             results.append({'timestamp': survey_time, 'avg_PM25': None, 'avg_PM10': None})
#             continue
        
#         # Calculate average PM2.5 and PM10 values
#         pm25_values = [entry['Value'] for entry in air_quality_data if entry['Parameter'] == 'PM25']
#         pm10_values = [entry['Value'] for entry in air_quality_data if entry['Parameter'] == 'PM10']
        
#         avg_pm25 = sum(pm25_values) / len(pm25_values) if pm25_values else None
#         avg_pm10 = sum(pm10_values) / len(pm10_values) if pm10_values else None
        
#         results.append({'timestamp': survey_time, 'avg_PM25': avg_pm25, 'avg_PM10': avg_pm10})
    
#     return pd.DataFrame(results)

# # Assuming gps_data and survey_data are already loaded as described earlier
# exposure_data = calculate_hourly_average_exposure(gps_data, survey_data)
# survey_data['timestamp'] = pd.to_datetime(survey_data['timestamp'])
# enhanced_survey_data = survey_data.merge(exposure_data, on='timestamp')

# # Display the first few rows of the enhanced survey data
# print(enhanced_survey_data.head())
