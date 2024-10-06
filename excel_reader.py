# excel_reader.py
import pandas as pd
import os



def process_srm_excel_data():
    try:
        index = 0

        # Get the current directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Define Excel file paths
        srm_file = os.path.join(current_dir, 'DATA SMR.xlsx')
        electrolysis_file = os.path.join(current_dir, 'DATA ELECTROLYSIS.xlsx')#Change place
        criteria_file = os.path.join(current_dir, 'Criteria Ranking.xlsx')#Change place
        
        # Define Sheet Name 
        srm_sheet_name = 'SMR (Main)'    # Sheet name Data SRM excel
        #electrolysis_sheet_name = 'Elec'    # Sheet name Elctrolysis excel
        #criteria_sheet_name = 'Main'    # Sheet name Criteria ranking excel
        
        
        xl = pd.read_excel(srm_file, sheet_name=srm_sheet_name, header=0)
        # Step 3: Remove the units row (second row)
        
        xl = xl.iloc[1:] # delete Row with units, could be saved Later specifically
 
        main_dict = {} # creating the Library
 
        for name in xl['Project Name']:
            if str(name) != 'nan': # Taking only the fullfilled project names
                main_dict[index] = {} 
                for column in xl:
                    for project_name, val in zip(xl['Project Name'],xl[column]):
                        if name == project_name:
                            main_dict[index][column] = val
    
                index += 1
        
        return main_dict  
    except Exception as e:
        print(f"Error reading SRM DATA Excel files: {e}")
        return None