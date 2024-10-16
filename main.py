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



def run_complete_comparison():
    excel_data_srm = process_srm_excel_data()
    excel_data_electrolysis = process_electrolysis_excel_data()
    criteria_weighting = process_criteria_excel_data()
    Combinations = matching_combinations(excel_data_srm,excel_data_electrolysis)
    #Here maybe insert a small Frontend Recap to see the Data Selected/deleted
    final_ranking = criteria_ranking_function(excel_data_srm,excel_data_electrolysis,Combinations,criteria_weighting)
    # Here Create the Frontend of the results 




def compare_two_technologies():
    #Being Implemented
    data_elec= process_electrolysis_excel_data()
    #excel_data_srm = process_srm_excel_data()
    C2P_Run(data_elec)




def compare_two_projects():
    vara = process_criteria_excel_data()
    
    print()
    # To be implemented
    pass



def get_h2_output():
    # To be implemented
    pass



if __name__ == "__main__":
    main()
