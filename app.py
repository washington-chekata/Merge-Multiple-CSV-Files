# Specify the folder containing your CSV files
import csv
import logging
import os
import pandas as pd

# Setup logging functionality
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

folder_path = '/home/wchekata/Programming/python/GMC_Image_Analysis/violating products'
path_to_merged_csv = '/home/wchekata/Documents/merged.csv'

logging.info(f"Checking for files within the folder located at {folder_path}")

def is_csv(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # Check if the file has a valid header
            csv.Sniffer().sniff(file.read(1024))
            file.seek(0)  # Reset file pointer
            return True
    except Exception as e:
        logging.error(f"Error while verifying if file is a CSV: {e}")
        return False

# Create a list to hold dataframes
dataframes = []
files = []

try:
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        files = os.listdir(folder_path)
        logging.debug(f"Files in the folder: {files}")
    else:
        logging.error(f"The folder '{folder_path}' is invalid or does not exist.")
except FileNotFoundError:
    logging.error(f"Error: The folder path '{folder_path}' does not exist. Please check the path and try again.")
except PermissionError:
    logging.error(f"Error: You do not have permission to access the folder '{folder_path}'.")

# Loop through all files in the folder
for filename in files:
    filepath = os.path.join(folder_path, filename)
    if is_csv(filepath):
        try:
            dataframe = pd.read_csv(filepath, on_bad_lines='skip', encoding='utf-8')
            dataframes.append(dataframe)
        except Exception as e:
            logging.error(f"Error reading file {filename}: {e}")
    else:
        logging.error(f"The file {filename} is not a CSV file.")

# Combine all dataframes
if dataframes:
    combined_dataframes = pd.concat(dataframes, ignore_index=True)
    combined_dataframes.to_csv(path_to_merged_csv, index=False)
    logging.info(f"Combined CSV saved to {path_to_merged_csv}")
else:
    logging.warning(f"No valid CSV files found in the folder {folder_path}.")
