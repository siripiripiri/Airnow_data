import csv
import requests
import os
from urllib.parse import urlparse

# Create a folder to store the downloaded files
output_folder = 'datFiles'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Read the CSV file
with open('output.csv', 'r') as csvfile:
    csvreader = csv.DictReader(csvfile)
    
    for row in csvreader:
        timestamp = row['Timestamp']
        url = row['URL']
        
        # Get the file extension from the URL
        parsed_url = urlparse(url)
        file_extension = os.path.splitext(parsed_url.path)[1]
        
        # Download the file
        response = requests.get(url)
        
        if response.status_code == 200:
            # Use the timestamp as the filename, replacing ':' with '_' to avoid issues
            filename = f"{timestamp.replace(':', '-')}{file_extension}"
            
            # Save the file
            filepath = os.path.join(output_folder, filename)
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            print(f"Downloaded: {filename}")
        else:
            print(f"Failed to download: {url}")

print("All downloads completed.")