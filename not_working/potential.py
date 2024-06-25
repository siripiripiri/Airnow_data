import requests
import csv
from io import StringIO
import pandas as pd

# Common base URL for AirNow API
base_url = "https://www.airnowapi.org/aq/observation/latLong/historical/?format=text/csv&"

api_key = "76B3C277-4B06-4D17-B1C7-261A92A3E7B4"

def fetch_airnow_data(latitude, longitude, timestamp):
    url = f"{base_url}latitude={latitude}&longitude={longitude}&date={timestamp}&distance=25&API_KEY={api_key}"
    response = requests.get(url)
    return response.text

    # if response.status_code == 200:
    #     return response.text
    # else:
    #     print(f"Failed to fetch data for latitude={latitude}, longitude={longitude}, timestamp={timestamp}. Status code: {response.status_code}")
    #     return None


input_csv = 'updated_data_new500.csv' 
df_input = pd.read_csv(input_csv)

csv_data = []

for index, row in df_input.iterrows():
    latitude = row['latitude']
    longitude = row['longitude']
    timestamp = row['Date']

    fetched_data = fetch_airnow_data(latitude, longitude, timestamp)

    if fetched_data:
        csv_data.append(fetched_data)

if csv_data:
    filtered_data = []
    for csv_string in csv_data:
        csv_file = StringIO(csv_string)
        
        # Use csv.DictReader to read the CSV file and treat each row as a dictionary
        reader = csv.DictReader(csv_file)

        for row in reader:
            filtered_row = {
                "DateObserved": row["DateObserved"],
                "HourObserved": row["HourObserved"],
                "Latitude": row["Latitude"],
                "Longitude": row["Longitude"],
                "ParameterName": row["ParameterName"],
                "AQI": row["AQI"],
                "CategoryNumber": row["CategoryNumber"],
                "CategoryName": row["CategoryName"]
            }
            filtered_data.append(filtered_row)

    
    df_filtered = pd.DataFrame(filtered_data)
    df_merged = pd.merge(df_input, df_filtered, left_on=['latitude', 'longitude', 'timestamp'], right_on=['Latitude', 'Longitude', 'DateObserved'], how='left')
    df_merged.to_csv('merged_data.csv', index=False)
    print("Merged CSV file saved successfully.")

else:
    print("No CSV data fetched.")
