import pandas as pd
import os

# Load all survey CSV files
survey_data_folder = 'SurveyData'
survey_files = ['Ping1.csv', 'Ping2.csv', 'Ping3.csv', 'Ping4.csv', 'Ping5.csv', 'Ping6.csv']
survey_data_list = [pd.read_csv(os.path.join(survey_data_folder, file)) for file in survey_files]

# Combine survey data into a single DataFrame
survey_data = pd.concat(survey_data_list, ignore_index=True)

# Display the first few rows of the survey data
print(survey_data.head())
