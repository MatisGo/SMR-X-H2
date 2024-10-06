# excel_reader.py
import pandas as pd
import os

def process_excel_data():
    try:
        # Get the current directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Define Excel file paths
        srm_file = os.path.join(current_dir, 'DATA SMR.xlsx')
        electrolysis_file = os.path.join(current_dir, 'DATA ELECTROLYSIS.xlsx')
        criteria_file = os.path.join(current_dir, 'Criteria Ranking.xlsx')
        
        # Read Excel files
        srm_data = pd.read_excel(srm_file)
        electrolysis_data = pd.read_excel(electrolysis_file)
        criteria_data = pd.read_excel(criteria_file)
        
        # Return the data as a dictionary
        return {
            'srm': srm_data,
            'electrolysis': electrolysis_data,
            'criteria': criteria_data
        }
    except Exception as e:
        print(f"Error reading Excel files: {e}")
        return None