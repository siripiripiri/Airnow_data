import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# Set up the WebDriver
service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# URL to scrape
url = "https://files.airnowtech.org/?prefix=airnow/2024/20240416/"
driver.get(url)

# Wait for the page to load
time.sleep(10)

# Extract the content
pre_tag = driver.find_element(By.TAG_NAME, 'pre')
lines = pre_tag.text.split('\n')

# Extract file details from the text lines
data = []
for line in lines[3:]:  # Skip the header lines
    parts = line.split()
    if len(parts) >= 4 and parts[-1].startswith('https'):  # Adjusted for the URL structure
        timestamp = parts[0] + ' ' + parts[1]
        size = parts[2]
        url = parts[-1]
        filename = url.split('/')[-1]
        data.append([filename, timestamp, size, url])

# Convert to DataFrame
df = pd.DataFrame(data, columns=['File Name', 'Timestamp', 'Size', 'URL'])

# Save to CSV
df.to_csv('airnow_files.csv', index=False)

print("CSV file has been created successfully.")

# Close the WebDriver
driver.quit()
