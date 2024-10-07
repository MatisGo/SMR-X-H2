# main.py
import tkinter as tk
from display_start import DisplayWindow
from excel_reader import process_srm_excel_data
from technical_comparison import compare_technologies

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
    #excel_data_electrolysis = process_electrolysis_excel_data() #To be activated when Process electrolysis_excel_data() is ready
    compare_technologies(excel_data_srm)

def compare_two_technologies():
    # To be implemented
    pass

def compare_two_projects():
    # To be implemented
    pass

def get_h2_output():
    # To be implemented
    pass

if __name__ == "__main__":
    main()