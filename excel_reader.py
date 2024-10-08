# excel_reader.py
import pandas as pd
import os


#SRM
def process_srm_excel_data():
    try:
        index = 0

        # Get the current directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Define Excel file paths
        srm_file = os.path.join(current_dir, 'DATA SMR.xlsx')
        electrolysis_file = os.path.join(current_dir, 'DATA ELECTROLYSIS.xlsx')#Change place
        
        
        # Define Sheet Name 
        srm_sheet_name = 'SMR (Main)'    # Sheet name Data SRM excel
        
        xl = pd.read_excel(srm_file, sheet_name=srm_sheet_name, header=0)
        
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

#Electrolyser
def process_electrolysis_excel_data():#Script to read the electrolysis excel Data 
    try:
        index1 = 0

        # Get the current directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        electrolysis_file = os.path.join(current_dir, 'Electrolyser data.xlsx')
        
        # Define Sheet Name 
        elec_sheet_name = 'Electrolyser'    # Sheet name Electrolyser >Need to be changed

        xl2 = pd.read_excel(electrolysis_file, sheet_name=elec_sheet_name, header=0)
        xl2 = xl2.iloc[1:] # delete Row with units, could be saved Later specifically
        
        

        return
    

    except Exception as e:
        print(f"Error reading SRM DATA Excel files: {e}")
        return None


#Criteria
def process_criteria_excel_data():#Script to read the Criteria excel Data 
    try:
        index2 = 0

        # Get the current directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        criteria_file = os.path.join(current_dir, 'Criteria Ranking.xlsx')


        # Define Sheet Name 
        criteria_sheet_name = 'DATA'    # Sheet name Criteria >Need to be changed

        xl3 = pd.read_excel(criteria_file, sheet_name=criteria_sheet_name, header=0)
        
        

        return
    

    except Exception as e:
        print(f"Error reading Criteria Excel files: {e}")
        return None 