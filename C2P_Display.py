import customtkinter as ctk
from tkinter import messagebox
import pandas as pd
from typing import Dict, List

class TechnologyComparisonWindow:
    def __init__(self, data_elec):
        # Create new window
        self.window = ctk.CTkToplevel()
        self.window.title("Technology Comparison")
        self.window.geometry("1000x800")
        
        # Bring window to front and focus
        self.window.lift()  # Brings window to front
        self.window.focus_force()  # Forces focus on the window
        
        # Store data
        self.data_elec = data_elec
        self.selected_techs = []
        self.selected_measures = []
        
        # Create main container
        self.main_frame = ctk.CTkFrame(self.window)
        self.main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Create selection frame (will hold technology and measures selection)
        self.selection_frame = ctk.CTkFrame(self.main_frame)
        self.selection_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Create results frame
        self.comparison_frame = ctk.CTkFrame(self.main_frame)
        
        # Create sections
        self.create_header()
        self.create_selection_view()
        
    def create_header(self):
        # Header frame
        header_frame = ctk.CTkFrame(self.window, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=10)
        
        # Title
        title = ctk.CTkLabel(
            header_frame,
            text="Technology Coupling Comparison",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.pack(pady=(0, 10))
        
        # Description
        description = ctk.CTkLabel(
            header_frame,
            text="Compare different technologies and their coupling characteristics",
            font=ctk.CTkFont(size=14),
            text_color="gray70"
        )
        description.pack()
        
        # Navigation buttons frame
        nav_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        nav_frame.pack(fill="x", pady=10)
        
        # Return button (hidden initially)
        self.return_button = ctk.CTkButton(
            nav_frame,
            text="Return to Selection",
            command=self.return_to_selection,
            width=150
        )
        self.return_button.pack(side="left", padx=5)
        self.return_button.pack_forget()  # Hide initially
        
        # Home button
        self.home_button = ctk.CTkButton(
            nav_frame,
            text="Close Window",
            command=self.close_window,
            width=150
        )
        self.home_button.pack(side="right", padx=5)

    def create_selection_view(self):
        # Technology selection frame
        tech_frame = ctk.CTkFrame(self.selection_frame)
        tech_frame.pack(fill="x", padx=10, pady=10)
        
        # Technology type selection
        tech_type_label = ctk.CTkLabel(
            tech_frame,
            text="Select Technology Type:",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        tech_type_label.pack(pady=(10, 5))
        
        # Technology type radio buttons
        self.tech_type_var = ctk.StringVar(value="Electrolyser")
        tech_types = ["Electrolyser", "Nuclear"]
        
        radio_frame = ctk.CTkFrame(tech_frame, fg_color="transparent")
        radio_frame.pack(pady=5)
        
        for tech_type in tech_types:
            radio = ctk.CTkRadioButton(
                radio_frame,
                text=tech_type,
                variable=self.tech_type_var,
                value=tech_type,
                command=self.update_technology_list
            )
            radio.pack(side="left", padx=10)
        
        # Technology selection label
        tech_select_label = ctk.CTkLabel(
            tech_frame,
            text="Select Technologies to Compare (max 2):",
            font=ctk.CTkFont(size=14)
        )
        tech_select_label.pack(pady=(15, 5))
        
        # Technology listbox
        self.tech_listbox = ctk.CTkScrollableFrame(tech_frame, height=100)
        self.tech_listbox.pack(fill="x", padx=20, pady=5)
        
        # Measures frame
        measures_frame = ctk.CTkFrame(self.selection_frame)
        measures_frame.pack(fill="x", padx=10, pady=10)
        
        # Measures label
        measures_label = ctk.CTkLabel(
            measures_frame,
            text="Select Measures to Compare:",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        measures_label.pack(pady=(10, 5))
        
        # Measures scrollable frame
        self.measures_scroll = ctk.CTkScrollableFrame(measures_frame, height=150)
        self.measures_scroll.pack(fill="x", padx=20, pady=5)
        
        # Compare button
        self.compare_button = ctk.CTkButton(
            self.selection_frame,
            text="Compare Technologies",
            command=self.perform_comparison,
            height=40,
            font=ctk.CTkFont(size=15, weight="bold")
        )
        self.compare_button.pack(pady=15)
        
        # Initialize lists
        self.update_technology_list()
        self.update_measures_list()

    def update_technology_list(self):
        # Clear existing checkboxes
        for widget in self.tech_listbox.winfo_children():
            widget.destroy()
        
        # Get technologies based on selected type
        if self.tech_type_var.get() == "Electrolyser":
            techs = [self.data_elec[tech]['Technology'] for tech in self.data_elec]
        else:
            techs = []  # Add nuclear technologies when implemented
        
        # Create checkboxes for technologies
        self.tech_vars = {}
        for tech in techs:
            var = ctk.BooleanVar()
            checkbox = ctk.CTkCheckBox(
                self.tech_listbox,
                text=tech,
                variable=var,
                command=self.check_tech_selection
            )
            checkbox.pack(anchor="w", pady=2)
            self.tech_vars[tech] = var

    def update_measures_list(self):
        # Clear existing checkboxes
        for widget in self.measures_scroll.winfo_children():
            widget.destroy()
        
        if self.data_elec:  # Check if data exists
            # Get measures (excluding 'Technology')
            first_tech = next(iter(self.data_elec.values()))
            measures = [key for key in first_tech.keys() if key != 'Technology']
            
            # Create checkboxes for measures
            self.measure_vars = {}
            for measure in measures:
                var = ctk.BooleanVar()
                checkbox = ctk.CTkCheckBox(
                    self.measures_scroll,
                    text=measure,
                    variable=var
                )
                checkbox.pack(anchor="w", pady=2)
                self.measure_vars[measure] = var

    def check_tech_selection(self):
        # Limit technology selection to 2
        selected_count = sum(var.get() for var in self.tech_vars.values())
        if selected_count > 2:
            messagebox.showwarning("Selection Limit", "Please select no more than 2 technologies.")
            # Reset the last selected checkbox
            for tech, var in self.tech_vars.items():
                if var.get():
                    var.set(False)
                    break

    def perform_comparison(self):
        # Get selected technologies
        selected_techs = [tech for tech, var in self.tech_vars.items() if var.get()]
        
        # Get selected measures
        selected_measures = [measure for measure, var in self.measure_vars.items() if var.get()]
        
        if len(selected_techs) == 0:
            messagebox.showwarning("Selection Required", "Please select at least one technology.")
            return
        
        if len(selected_measures) == 0:
            messagebox.showwarning("Selection Required", "Please select at least one measure.")
            return
        
        # Hide selection frame and show comparison
        self.selection_frame.pack_forget()
        self.create_comparison_view(selected_techs, selected_measures)
        
        # Show return button
        self.return_button.pack(side="left", padx=5)

    def create_comparison_view(self, selected_techs, selected_measures):
        # Clear and configure comparison frame
        for widget in self.comparison_frame.winfo_children():
            widget.destroy()
        
        self.comparison_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Create columns for technologies
        for tech in selected_techs:
            tech_frame = ctk.CTkFrame(self.comparison_frame)
            tech_frame.pack(side="left", fill="both", expand=True, padx=10)
            
            # Technology header
            tech_header = ctk.CTkLabel(
                tech_frame,
                text=tech,
                font=ctk.CTkFont(size=20, weight="bold")
            )
            tech_header.pack(pady=10)
            
            # Find technology data
            tech_data = None
            for data in self.data_elec.values():
                if data['Technology'] == tech:
                    tech_data = data
                    break
            
            if tech_data:
                for measure in selected_measures:
                    measure_frame = ctk.CTkFrame(tech_frame, fg_color="transparent")
                    measure_frame.pack(fill="x", pady=5, padx=10)
                    
                    measure_label = ctk.CTkLabel(
                        measure_frame,
                        text=f"{measure}:",
                        font=ctk.CTkFont(size=14, weight="bold")
                    )
                    measure_label.pack(anchor="w")
                    
                    value_label = ctk.CTkLabel(
                        measure_frame,
                        text=str(tech_data[measure]),
                        font=ctk.CTkFont(size=14),
                        text_color="gray70"
                    )
                    value_label.pack(anchor="w")

    def return_to_selection(self):
        # Hide comparison frame and return button
        self.comparison_frame.pack_forget()
        self.return_button.pack_forget()
        
        # Show selection frame
        self.selection_frame.pack(expand=True, fill="both", padx=10, pady=10)

    def close_window(self):
        self.window.destroy()