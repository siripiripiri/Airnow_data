import requests
import csv
from io import StringIO
import pandas as pd

# Common base URL for AirNow API
base_url = "https://www.airnowapi.org/aq/observation/latLong/historical/?format=text/csv&"

# Replace with your actual AirNow API key
api_key = "5136C71A-B18E-4BB8-9A74-A6475A76CD94"

# Example input data
input_data = [
    {"latitude": 34.024496, "longitude": -118.278309, "timestamp": "2016-04-16T18-0000"},
    {'latitude': 34.021526, 'longitude': -129.288752, 'timestamp': '2020-09-26T12-0000'}
    # Add more entries as needed
]

csv_data = []

for data in input_data:
    # Construct the URL
    url = f"{base_url}latitude={data['latitude']}&longitude={data['longitude']}&date={data['timestamp']}&distance=1000&API_KEY={api_key}"

    # Make the request to AirNow API
    response = requests.get(url)

    if response.status_code == 200:
        csv_data.append(response.text)
    else:
        print(f"Failed to fetch data for latitude={data['latitude']}, longitude={data['longitude']}. Status code: {response.status_code}")


if csv_data:
    filtered_data = []
    for csv_string in csv_data:
        # Use StringIO to simulate a file object from the string
        csv_file = StringIO(csv_string)
        
        # Use csv.DictReader to read the CSV file and treat each row as a dictionary
        reader = csv.DictReader(csv_file)

        # Iterate over each row in the CSV data
        for row in reader:
            # Extract specific columns and create a new dictionary
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
            
            # Append the filtered row to filtered_data
            filtered_data.append(filtered_row)

    # Print or process the filtered data as needed
    df = pd.DataFrame(filtered_data)
    print(df)


else:
    print("No CSV data fetched.")

