# import pandas as pd

# df = pd.read_csv('csvData/output500.csv')

# df['Date'] = pd.to_datetime(df['timestamp'], format='%m/%d/%Y, %I:%M:%S %p')

# df['Date'] = df['Date'].dt.strftime('%Y-%m-%d %H:%M')
# df = df.drop('timestamp', axis=1)

# df.to_csv('updated_data500.csv', index=False)

# print("Updated CSV file saved successfully.")

# import pandas as pd

# # Load your CSV file into a DataFrame (assuming it's named 'data.csv')
# df = pd.read_csv('gpxtocsv.csv')

# # Convert the date column to datetime format if it's not already
# df['timestamp'] = pd.to_datetime(df['timestamp'])

# # Convert datetime to the desired format 'YYYY-MM-DDTHH-MinMinSS'
# df['timestamp'] = df['timestamp'].dt.strftime('%Y-%m-%dT%H-%M%M%S')

# # Save the updated DataFrame to a new CSV file
# df.to_csv('updated_data_new500.csv', index=False)

# print("Date format converted and updated CSV file saved successfully.")

# import pandas as pd

# # Read the CSV file with date in 'YYYY-MM-DD HH:MM' format
# df = pd.read_csv('gpxtocsv.csv')


# # Convert each row to a dictionary in the desired format
# data_list = df.apply(lambda row: {
#     "latitude": row['latitude'],
#     "longitude": row['longitude'],
#     "timestamp": row['timestamp']
# }, axis=1).tolist()

# # Print or use the list of dictionaries as needed
# print(data_list)



# import pandas as pd

# # Function to convert date format to ISO 8601 with milliseconds and "Z"
# def convert_to_iso_format(date_str):
#     # Parse the date string
#     local_time = pd.to_datetime(date_str)
    
#     # Convert to ISO 8601 format with milliseconds and "Z"
#     iso_format_time = local_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    
#     return iso_format_time

# # Read input CSV file containing longitude, latitude, and timestamp
# input_csv = 'csvData/output500.csv'  # Replace with your input CSV file name
# df = pd.read_csv(input_csv)

# # Convert timestamp format in the DataFrame
# df['timestamp'] = df['timestamp'].apply(convert_to_iso_format)

# # Save the updated DataFrame to a new CSV file
# df.to_csv('updated_data.csv', index=False)

# print("Timestamp column updated and saved to updated_data.csv")


import pandas as pd

# Load the CSV file into a DataFrame
file_path = 'gpxtocsv.csv'
df = pd.read_csv(file_path)

# Convert the 'timestamp' column to datetime object
df['timestamp'] = pd.to_datetime(df['timestamp'], format='%m/%d/%Y, %I:%M:%S %p')

# Extract the date and time into separate columns
df['ValidDate'] = df['timestamp'].dt.strftime('%m/%d/%Y')
df['ValidTime'] = df['timestamp'].dt.strftime('%H:%M')

# Drop the original 'timestamp' column if needed
df = df.drop(columns=['timestamp'])

# Reorder columns if necessary
df = df[['ValidDate', 'ValidTime', 'latitude', 'longitude']]

# Save the updated DataFrame to a new CSV file (optional)
output_file_path = 'gpxtocsv.csv'
df.to_csv(output_file_path, index=False)

print("Process completed. Check 'updated_csv_file.csv' for results.")
