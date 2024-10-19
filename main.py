# main.py
import tkinter as tk
from display_start import DisplayWindow
from excel_reader import process_srm_excel_data
from excel_reader import process_electrolysis_excel_data
from excel_reader import process_criteria_excel_data
from C2P_Data_Presentation import C2P_Run
from technical_comparison import matching_combinations
from criteria_function import criteria_ranking_function


def main():
    root = tk.Tk()
    app = DisplayWindow(root, callbacks={
        'complete_comparison': run_complete_comparison,
        'two_technologies': compare_two_technologies,
        'two_projects': compare_two_projects,
        'h2_output': get_h2_output
    })
    root.mainloop()


#First possibility of the script// Normal mode // Will give out the best option
def run_complete_comparison():
    excel_data_srm = process_srm_excel_data() # Will get the Data from the SRM excel file
    excel_data_electrolysis = process_electrolysis_excel_data() #Will get the Data from the Electrolysis excel file 
    criteria_weighting = process_criteria_excel_data() #Will get the data from the criteria weighting excel file
    Combinations = matching_combinations(excel_data_srm,excel_data_electrolysis) # Create combinations and first technical comparison 
    # Here maybe insert a small Frontend Recap to see the Data Selected/deleted
    final_ranking = criteria_ranking_function(excel_data_srm,excel_data_electrolysis,Combinations,criteria_weighting) # Criteria ranking of all the combinations
    # Here Create the Frontend of the results 




def compare_two_technologies():
    #Being Implemented
    data_elec= process_electrolysis_excel_data()
    #excel_data_srm = process_srm_excel_data()
    C2P_Run(data_elec)



#To be deleted 
def compare_two_projects():
    vara = process_criteria_excel_data()
    
    print()
    # To be implemented
    pass



def get_h2_output():
    excel_data_srm = process_srm_excel_data()
    excel_data_electrolysis = process_electrolysis_excel_data()
    criteria_weighting = process_criteria_excel_data()
    Combinations = matching_combinations(excel_data_srm,excel_data_electrolysis)
    final_ranking = criteria_ranking_function(excel_data_srm,excel_data_electrolysis,Combinations,criteria_weighting)

    # To be implemented
    # Get the desired production Value 
    # Display the best solution according to the Input and Criteria ranking.
    pass



if __name__ == "__main__":
    main()
