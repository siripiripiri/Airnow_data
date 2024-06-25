import csv
import re

# Specify the path to the text file
file_path = '2024-04-16.txt'

# Open the file and read its content
with open(file_path, 'r') as file:
    content = file.read()

# Input text
input_text = content

# Function to parse the input text and convert it to CSV format
def convert_to_csv(input_text, output_file):
    # Split the input text into rows
    rows = input_text.strip().split('\n')

    # Define the CSV header
    header = ["Timestamp", "File Size", "URL", "File Name"]

    # Open the output CSV file in write mode
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)

        # Process each row
        for row in rows:
            # Use regex to extract the timestamp, file size, URL, and file name
            match = re.match(r'(\S+)\s+(\d+)\s+<a href="([^"]+)">([^<]+)</a>', row)
            if match:
                timestamp = match.group(1)
                file_size = match.group(2)
                url = match.group(3)
                file_name = match.group(4)
                # Write the row to the CSV file
                writer.writerow([timestamp, file_size, url, file_name])
            else:
                print(f"Row skipped due to unexpected format: {row}")

# Specify the output CSV file path
output_file = 'output.csv'

# Call the function to convert the input text to CSV
convert_to_csv(input_text, output_file)

print(f"CSV file '{output_file}' has been created successfully.")
