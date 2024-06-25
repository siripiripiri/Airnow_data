import xml.etree.ElementTree as ET
import pandas as pd

def parse_gpx(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Namespaces in GPX file
    ns = {
        'default': 'http://www.topografix.com/GPX/1/1'
    }

    data = []
    for trk in root.findall('default:trk', ns):
        for trkseg in trk.findall('default:trkseg', ns):
            for trkpt in trkseg.findall('default:trkpt', ns):
                lat = trkpt.get('lat')
                lon = trkpt.get('lon')
                time = trkpt.find('default:time', ns).text
                data.append([time, lat, lon])

    return data

file_path = 'danielle GPX .GPX'
data = parse_gpx(file_path)

df = pd.DataFrame(data, columns=['timestamp', 'latitude', 'longitude'])

output_csv_path = 'csvData/output.csv'
df.to_csv(output_csv_path, index=False)

