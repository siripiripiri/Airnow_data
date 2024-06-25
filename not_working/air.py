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
    {"latitude": 34.024496, "longitude": -118.278309, "timestamp": "2024-06-23T00-0000"},
    # Add more entries as needed
]

csv_data = []

for data in input_data:
    # Construct the URL
    url = f"{base_url}latitude={data['latitude']}&longitude={data['longitude']}&date={data['timestamp']}&distance=25&API_KEY={api_key}"

    # Make the request to AirNow API
    response = requests.get(url)

    if response.status_code == 200:
        csv_data.append(response.text)
    else:
        print(f"Failed to fetch data for latitude={data['latitude']}, longitude={data['longitude']}. Status code: {response.status_code}")

# Process CSV data
if csv_data:
    # Initialize lists to store filtered data
    filtered_data = []

    # Parse each CSV string
    for csv_string in csv_data:
        # Use StringIO to simulate a file object from the string
        csv_file = StringIO(csv_string)
        
        # Use csv.DictReader to read the CSV file and treat each row as a dictionary
        reader = csv.DictReader(csv_file)

        # Iterate over each row in the CSV data
        for row in reader:
            # Filter out rows with ParameterName "OZONE"
            if row["ParameterName"] != "OZONE":
                # Initialize new row dictionary with common columns
                new_row = {
                    "DateObserved": row["DateObserved"],
                    "HourObserved": row["HourObserved"],
                    "Latitude": row["Latitude"],
                    "Longitude": row["Longitude"],
                    "CategoryNumber": row["CategoryNumber"],
                    "CategoryName": row["CategoryName"]
                }
                
                # Check if PM2.5 or PM10 are present in ParameterName and add corresponding AQI
                if row["ParameterName"] == "PM2.5":
                    new_row["PM2.5_AQI"] = row["AQI"]
                elif row["ParameterName"] == "PM10":
                    new_row["PM10_AQI"] = row["AQI"]
                
                # Append the filtered row to filtered_data
                filtered_data.append(new_row)

    # Convert filtered_data to DataFrame for easier manipulation and analysis
    df = pd.DataFrame(filtered_data)

    # Display the resulting DataFrame
    print(df)

else:
    print("No CSV data fetched.")
