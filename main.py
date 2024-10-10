# main.py
import tkinter as tk
from display_start import DisplayWindow
from excel_reader import process_srm_excel_data
from excel_reader import process_electrolysis_excel_data
from technical_comparison import compare_technologies
from C2P_Data_Presentation import C2P_Data_Presentation

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
    #Criteria Excel Reading
    #excel_data_electrolysis = {}
    #excel_data_electrolysis = {"value1": 42, "value2": "hello", "value3": [1, 2, 3]} 
    compare_technologies(excel_data_srm,excel_data_electrolysis)



def compare_two_technologies():
    #Being Implemented
    data_elec= process_electrolysis_excel_data()
    excel_data_srm = process_srm_excel_data()
    comparison_result = C2P_Data_Presentation(data_elec,excel_data_srm)




def compare_two_projects():
    vara = process_srm_excel_data()
    varb = process_electrolysis_excel_data() 
    print(vara,varb)
    # To be implemented
    pass



def get_h2_output():
    # To be implemented
    pass



if __name__ == "__main__":
    main()
