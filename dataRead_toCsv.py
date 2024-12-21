import pandas as pd
import json
import os

# # Path to the uploaded file

# # Directory containing the JSON files
# directory = '/Users/photcharakallayanasiri/Desktop/DataSci Final Exam/Project/2023'

# # Initialize an empty list to store DataFrames
# dfs = []

# # Loop through all files in the directory
# for filename in os.listdir(directory):
#         file_path = os.path.join(directory, filename)
        
#         # Read the JSON file
#         with open(file_path, 'r', encoding='utf-8') as file:
#             json_data = json.load(file)
        
#         # Convert nested JSON to DataFrame
#         df = pd.json_normalize(json_data)
        
#         # Append the DataFrame to the list
#         dfs.append(df)

# # Concatenate all DataFrames into a single DataFrame
# df = pd.concat(dfs, ignore_index=True)

# df.columns = [col.split(':')[-1] for col in df.columns]

# # Save the DataFrame to an Excel file
output_file = '/Users/photcharakallayanasiri/Desktop/DataSci Final Exam/Project/outputAll.xlsx'
# df.to_excel(output_file, index=False)

# Directory containing the folders for each year
base_directory = '/Users/photcharakallayanasiri/Desktop/DataSci Final Exam/Project'

# Initialize a dictionary to store DataFrames for each year
year_dfs = []
# Loop through each year directory
for year in range(2018, 2024):
    print(year)
    year_directory = os.path.join(base_directory, str(year))
    
    # Initialize an empty list to store DataFrames for the current year
    
    
    # Loop through all files in the year directory
    for filename in os.listdir(year_directory):
        file_path = os.path.join(year_directory, filename)
        
        # Read the JSON file
        with open(file_path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
        
        # Convert nested JSON to DataFrame
        df = pd.json_normalize(json_data)
        # Add filename to the DataFrame
        df['filename'] = filename
        # Move 'filename' column to the first position
        df.insert(0, 'filename', df.pop('filename'))
        # Append the DataFrame to the list
        year_dfs.append(df)
        print(filename)
    
    # Concatenate all DataFrames for the current year into a single DataFrame

    

# Save all DataFrames to an Excel file with separate sheets for each year
# Save all DataFrames to separate CSV files for each year
# Concatenate all DataFrames for each year into a single DataFrame
year_df = pd.concat(year_dfs, ignore_index=True)
    
    # Clean column names
year_df.columns = [col.split(':')[-1] for col in year_df.columns]

# Save the concatenated DataFrame to a single CSV file
year_df.to_csv(output_file.replace('.xlsx', '.csv'), index=False)
