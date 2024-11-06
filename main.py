import customtkinter as ctk
from display_start import DisplayWindow
from excel_reader import (
    process_srm_excel_data,
    process_electrolysis_excel_data,
    process_criteria_excel_data
)
from technical_comparison import matching_combinations
from criteria_function import criteria_ranking_function
from C2P_Display import TechnologyComparisonWindow  
from results_display import ResultsDisplayWindow
from h2_output_window import H2OutputAnalysisWindow

class MainApplication:
    def __init__(self):
        # Initialize root window with CustomTkinter
        self.root = ctk.CTk()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Pre-load data to avoid repeated loading
        self.data_elec = process_electrolysis_excel_data()
        self.data_srm = process_srm_excel_data()
        self.criteria_weighting = process_criteria_excel_data()
        
        # Create callback dictionary
        callbacks = {
            'complete_comparison': self.run_complete_comparison,
            'two_technologies': self.compare_two_technologies,
            'h2_output': self.get_h2_output
        }
        
        # Initialize main window with callbacks
        self.main_window = DisplayWindow(self.root, callbacks)

    def run_complete_comparison(self):
        """First possibility of the script// Normal mode // Will give out the best option"""
        # Create combinations and first technical comparison
        combinations = matching_combinations(
            self.data_srm,
            self.data_elec
        )
        #print(combinations)
        # Criteria ranking of all combinations
        final_ranking = criteria_ranking_function(
            self.data_srm,
            self.data_elec,
            combinations,
            self.criteria_weighting
        )
        #print(final_ranking)
        # Display the results
        self.show_complete_comparison_results(final_ranking)

    def show_complete_comparison_results(self, final_ranking):
        """Display complete comparison results in a new window"""
        #ResultsDisplayWindow(self.root, final_ranking)
        ResultsDisplayWindow(self.root, final_ranking, self.data_elec, self.data_srm)
        
    def compare_two_technologies(self):
        """Compare two technologies """
        # Create new window for technology comparison
        TechnologyComparisonWindow(self.root, self.data_elec)
        

    def get_h2_output(self):
        """Analyze H2 output with specified criteria"""
        # First get the technical combinations
        combinations = matching_combinations(
            self.data_srm,
            self.data_elec
        )
        
        # Get the ranking based on criteria
        final_ranking = criteria_ranking_function(
            self.data_srm,
            self.data_elec,
            combinations,
            self.criteria_weighting
        )
        
        # Show H2 output window
        self.show_h2_output_window(final_ranking)

    def show_h2_output_window(self, final_ranking):
        """Display H2 output analysis in a new window"""
        H2OutputAnalysisWindow(self.root, final_ranking)

        

    def run(self):
        """Start the application"""
        self.root.mainloop()

def main():
    app = MainApplication()
    app.run()

if __name__ == "__main__":
    main()