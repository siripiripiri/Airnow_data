import os
import csv
import chardet

# Directory containing .dat files
input_dir = 'datFiles'
# Directory to save .csv files
output_dir = 'csvFiles'

# Create output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read()
    return chardet.detect(raw_data)['encoding']

def convert_dat_to_csv(dat_file, csv_file):
    # Detect the file encoding
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

# Process all .dat files in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith('.dat'):
        dat_path = os.path.join(input_dir, filename)
        csv_path = os.path.join(output_dir, filename[:-4] + '.csv')
        
        convert_dat_to_csv(dat_path, csv_path)

print("All conversions completed.")