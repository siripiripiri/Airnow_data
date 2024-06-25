import csv
import re
import requests
import os
import chardet
from urllib.parse import urlparse
import glob
import pandas as pd

def convert_to_csv(file_path, output_file):
    with open(file_path, 'r') as file:
        content = file.read()

    # Input text
    input_text = content
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

    print(f"CSV file '{output_file}' has been created successfully.")

# file_path = '04-17-2024_and_04-22-2024.txt'
# output_file = "resources.csv"
# convert_to_csv(file_path, output_file)

def download_datFiles(resources_path):
    output_folder = 'datFiles'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Read the CSV file
    with open(resources_path, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        
        for row in csvreader:
            timestamp = row['Timestamp']
            url = row['URL']
            
            # Get the file extension from the URL
            parsed_url = urlparse(url)
            file_extension = os.path.splitext(parsed_url.path)[1]
            
            # Check if the file extension is .dat
            if file_extension.lower() == '.dat':
                # Download the file
                response = requests.get(url)
                
                if response.status_code == 200:
                    filename = f"{timestamp.replace(':', '-')}{file_extension}"
                    
                    # Save the file
                    filepath = os.path.join(output_folder, filename)
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                    
                    print(f"Downloaded: {filename}")
                else:
                    print(f"Failed to download: {url}")
            else:
                print(f"Skipped non-.dat file: {url}")

    print("All downloads completed.")

# download_datFiles("resources.csv")





def detect_encoding(file_path):
        with open(file_path, 'rb') as file:
            raw_data = file.read()
        return chardet.detect(raw_data)['encoding']


def convert_dat_to_csv(dat_file, csv_file):
        encoding = detect_encoding(dat_file)
        
        try:
            with open(dat_file, 'r', encoding=encoding) as dat, open(csv_file, 'w', newline='', encoding='utf-8') as csv_out:
                # Read the entire content
                content = dat.read()
                
                # Split the content into lines
                lines = content.split('\n')
                
                csv_writer = csv.writer(csv_out)
                
                # Write the header
                header = lines[0].strip('"').split('","')
                csv_writer.writerow(header)
                
                # Process and write each data row
                for line in lines[1:]:
                    if line.strip():  # Skip empty lines
                        row = line.strip('"').split('","')
                        csv_writer.writerow(row)
            
            print(f"Converted {os.path.basename(dat_file)} to CSV using {encoding} encoding")
        except Exception as e:
            print(f"Error converting {os.path.basename(dat_file)}: {str(e)}")



def dat_to_csv(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Process all .dat files in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith('.dat'):
            dat_path = os.path.join(input_dir, filename)
            csv_path = os.path.join(output_dir, filename[:-4] + '.csv')
            
            convert_dat_to_csv(dat_path, csv_path)

    print("All conversions completed.")

# input_dir = 'datFiles'
# output_dir = 'csvFiles'

# dat_to_csv(input_dir,output_dir)












def read_csv_flexible(filepath):
    encodings = ['utf-8', 'ISO-8859-1', 'ascii', 'latin1']
    for encoding in encodings:
        try:
            return pd.read_csv(filepath, encoding=encoding)
        except Exception as e:
            continue
    raise ValueError(f"Could not read the file {filepath} with any of the encodings.")



def filter_pm_values(df):
    pm25_columns = [col for col in df.columns if 'PM2.5' in col or 'PM25' in col]
    pm10_columns = [col for col in df.columns if 'PM10' in col]

    if pm25_columns and pm10_columns:
        return df.dropna(subset=pm25_columns + pm10_columns)
    return pd.DataFrame()


def filter_lat_long(df):
        lat_columns = [col for col in df.columns if 'lat' in col.lower()]
        long_columns = [col for col in df.columns if 'long' in col.lower()]

        if lat_columns and long_columns:
            lat_col = lat_columns[0]
            long_col = long_columns[0]
            filtered_df = df[df[lat_col].astype(str).str.startswith('34.0') & 
                            df[long_col].astype(str).str.startswith('-118.2')]
            
            
            filtered_df[['Hour']] = filtered_df[['ValidTime']]
            filtered_df = filtered_df.drop('ValidTime',axis=1)
            filtered_df[['lat_Approx']] = filtered_df[['Latitude']]
            filtered_df = filtered_df.drop('Latitude',axis=1)
            filtered_df[['long_Approx']] = filtered_df[['Longitude']]
            filtered_df = filtered_df.drop('Longitude',axis=1)

            filtered_df = filtered_df[['ValidDate','Hour','lat_Approx','long_Approx','PM10_AQI','PM25_AQI']]

            filtered_df = filtered_df.sort_values(by='Hour')
            filtered_df.reset_index(drop=True, inplace=True)

            return filtered_df
        return pd.DataFrame()




def hero(csv_dir):
    filtered_dfs = []

    # Process each CSV file
    csv_files = glob.glob(os.path.join(csv_dir, '*.csv'))
    for csv_file in csv_files:
        try:
            df = read_csv_flexible(csv_file)
            filtered_df = filter_pm_values(df)
            if not filtered_df.empty:
                filtered_dfs.append(filtered_df)
        except Exception as e:
            print(f"Failed to process {csv_file}: {e}")

    # Combine all the filtered DataFrames
    if filtered_dfs:
        result_df = pd.concat(filtered_dfs, ignore_index=True)
    else:
        result_df = pd.DataFrame()

    result_df = filter_lat_long(result_df)

    # Save the result to a new CSV file
    result_df.to_csv('nice.csv', index=False)

    print("Process completed. Check 'nice.csv' for results.")


# csv_dir = 'csvFiles'
# hero(csv_dir)





def slice_csv(file_path,output_file_path,date):
    df = pd.read_csv(file_path)
    df = df[df['ValidDate'] == date]
    df.to_csv(output_file_path, index=False)

    print(f"Process completed. Check '{output_file_path}' for results.")

# slice_csv('gpxtocsv.csv','17.csv','04/17/2024')
# slice_csv('gpxtocsv.csv','18.csv','04/18/2024')
# slice_csv('gpxtocsv.csv','19.csv','04/19/2024')
# slice_csv('gpxtocsv.csv','20.csv','04/20/2024')
# slice_csv('gpxtocsv.csv','21.csv','04/21/2024')
# slice_csv('gpxtocsv.csv','22.csv','04/22/2024')


# slice_csv('nice.csv','nice_17.csv','04/17/2024')
# slice_csv('nice.csv','nice_18.csv','04/18/2024')
# slice_csv('nice.csv','nice_19.csv','04/19/2024')
# slice_csv('nice.csv','nice_20.csv','04/20/2024')
# slice_csv('nice.csv','nice_21.csv','04/21/2024')
# slice_csv('nice.csv','nice_22.csv','04/22/2024')




def merge_entries(gpxtocsv_path, nice_path):
    gpxtocsv = pd.read_csv(gpxtocsv_path)
    nice = pd.read_csv(nice_path)

    date = gpxtocsv_path.split('.')[0]
    # Convert 'ValidTime' to hour and add a 'ValidDate' column (assuming it's in format MM/DD/YYYY, HH:MM)
    gpxtocsv['Hour_gpxtocsv'] = pd.to_datetime(gpxtocsv['ValidTime'], format='%H:%M').dt.hour
    nice['Hour_nice'] = pd.to_datetime(nice['Hour'], format='%H:%M').dt.hour

    # Filter rows in gpxtocsv where ValidDate is '04/16/2024'
    gpxtocsv_filtered = gpxtocsv

    merged_data = pd.merge(gpxtocsv_filtered, nice, left_on='Hour_gpxtocsv', right_on='Hour_nice', how='inner')

    merged_data.drop(columns=['Hour_gpxtocsv', 'Hour_nice'], inplace=True)

    merged_data.to_csv(f'{date}_merged.csv', index=False)

    print("Merged and filtered data saved to 'final_merged_filtered.csv'.")

# for i in range(17,23):
#     merge_entries(f'{i}.csv',f'nice_{i}.csv')



def combine_all(directory):
    

    csv_files = [
        'final_merged_filtered.csv',
        '17_merged.csv',
        '18_merged.csv',
        '19_merged.csv',
        '20_merged.csv',
        '21_merged.csv',
        '22_merged.csv',
    ]

    csv_files = [os.path.join(directory, file) for file in csv_files]

    merged_rows = []

    # Read rows from each CSV file in the specified sequence
    for file in csv_files:
        with open(file, 'r', newline='') as csvfile:
            csvreader = csv.reader(csvfile)
            # Skip header if present (assuming first row is header)
            header_skipped = False
            for row in csvreader:
                if not header_skipped:
                    header_skipped = True
                    continue  # Skip header row
                merged_rows.append(row)

# Example: Printing merged rows
    for row in merged_rows:
        print(row)

    # Optionally, write merged data to a new CSV file
    output_file = 'merged_data.csv'
    with open(output_file, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(merged_rows)

    print(f'Merged data has been written to {output_file}')


combine_all('merged_files')