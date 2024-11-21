import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import json
from typing import Dict, List
import numpy as np
import tkinter as tk
from tkinter import filedialog

class ResultsDisplayWindow:
    def __init__(self, parent, final_ranking: List[Dict], data_elec: Dict, data_srm: Dict):
        self.parent = parent
        self.parent.withdraw()
        self.final_ranking = final_ranking
        self.data_elec = data_elec
        self.data_srm = data_srm
        
        # Add Criteria here to be addded in the Excel
        self.available_criteria = ["Rank", "Production Efficiency (%)","Grade","Capex","Safety","Rentability","Opex","Ecological impact","Startup time","Scalability","Availability (h/year)","Plant Area/Footprint","Technology readiness","Connection flexibility","Geopolitical barriers","Economic lifetime","Production efficiency","Waste and decomissioning"]  
        self.selected_criteria = ["Rank"]  # Start with Rank as default
        

        # Create main window
        self.window = ctk.CTkToplevel(parent)
        self.window.title("Results Analysis")
        width = self.window.winfo_screenwidth()
        height = self.window.winfo_screenheight()
        self.window.geometry(f"{width}x{height}")
        
        # Bind closing event
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Create main container
        self.container = ctk.CTkFrame(self.window)
        self.container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create tabview
        self.tabview = ctk.CTkTabview(self.container)
        self.tabview.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Add tabs
        self.tab_graph = self.tabview.add("Graph")
        self.tab_detail = self.tabview.add("Detail")
        self.tab_export = self.tabview.add("Export")
        
        # Initialize tabs
        self.setup_graph_tab()
        self.setup_detail_tab()
        self.setup_export_tab()
        
        # Selected criteria for graph
        #self.selected_criteria = ["Rank"]  # Start with Rank as default
        
    def setup_graph_tab(self):
        # Create left and right frames
        left_frame = ctk.CTkFrame(self.tab_graph)
        left_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        right_frame = ctk.CTkFrame(self.tab_graph)
        right_frame.pack(side="right", fill="y", padx=5, pady=5)
        
        # Criteria selection frame
        criteria_frame = ctk.CTkFrame(left_frame)
        criteria_frame.pack(fill="x", padx=5, pady=5)
        
        # Criteria dropdown
        self.criteria_var = ctk.StringVar(value=self.available_criteria[0])
        criteria_dropdown = ctk.CTkOptionMenu(
            criteria_frame,
            values=self.available_criteria,
            variable=self.criteria_var,
            command=self.add_criteria
        )
        criteria_dropdown.pack(side="left", padx=5)
        
        # Selected criteria display
        self.criteria_display = ctk.CTkFrame(criteria_frame)
        self.criteria_display.pack(fill="x", expand=True, padx=5)
        self.update_criteria_display()
        
        # Graph frame
        self.graph_frame = ctk.CTkFrame(left_frame)
        self.graph_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Ranked combinations list
        list_label = ctk.CTkLabel(right_frame, text="Ranked Combinations", 
                                font=("Helvetica", 16, "bold"))
        list_label.pack(pady=5)
        
        # Create scrollable frame for combinations
        combinations_frame = ctk.CTkScrollableFrame(right_frame, width=200, height=600)
        combinations_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Sort and display combinations
        sorted_combinations = sorted(self.final_ranking, key=lambda x: x['Rank'])
        for combo in sorted_combinations:
            combo_label = ctk.CTkLabel(
                combinations_frame,
                text=f"[{combo['Rank']}] {combo['Name']}"
            )
            combo_label.pack(pady=2, anchor="w")
            
        # Initial graph display
        self.update_graph()
        
    def setup_detail_tab(self):
        # Combination selection at top
        selection_frame = ctk.CTkFrame(self.tab_detail)
        selection_frame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(selection_frame, text="Select Combination:").pack(side="left", padx=5)
        
        # Create dropdown with all combination names
        combo_names = [combo['Name'] for combo in self.final_ranking]
        self.selected_combo = ctk.StringVar(value=combo_names[0])
        combo_dropdown = ctk.CTkOptionMenu(
            selection_frame,
            values=combo_names,
            variable=self.selected_combo,
            command=self.update_detail_view
        )
        combo_dropdown.pack(side="left", padx=5)
        
        # Create three columns for details
        self.detail_container = ctk.CTkFrame(self.tab_detail)
        self.detail_container.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Initial detail view
        self.update_detail_view()
        
    def setup_export_tab(self):
        export_frame = ctk.CTkFrame(self.tab_export)
        export_frame.pack(expand=True, padx=20, pady=20)
        
        # Export buttons
        ctk.CTkButton(
            export_frame,
            text="Export to Excel",
            command=self.export_to_excel
        ).pack(pady=10)
        
        ctk.CTkButton(
            export_frame,
            text="Export to JSON",
            command=self.export_to_json
        ).pack(pady=10)
        
        ctk.CTkButton(
            export_frame,
            text="Export to Text",
            command=self.export_to_text
        ).pack(pady=10)
        
    def add_criteria(self, criteria):
        if criteria not in self.selected_criteria and len(self.selected_criteria) < 5:
            self.selected_criteria.append(criteria)
            self.update_criteria_display()
            self.update_graph()
            
    def remove_criteria(self, criteria):
        if len(self.selected_criteria) > 1:
            self.selected_criteria.remove(criteria)
            self.update_criteria_display()
            self.update_graph()
            
    def update_criteria_display(self):
        # Clear existing display
        for widget in self.criteria_display.winfo_children():
            widget.destroy()
            
        # Show selected criteria as removable tags
        for criteria in self.selected_criteria:
            criteria_frame = ctk.CTkFrame(self.criteria_display)
            criteria_frame.pack(side="left", padx=2, pady=2)
            
            ctk.CTkLabel(criteria_frame, text=criteria).pack(side="left", padx=2)
            
            if len(self.selected_criteria) > 1:  # Only show remove button if more than one criteria
                ctk.CTkButton(
                    criteria_frame,
                    text="×",
                    width=20,
                    command=lambda c=criteria: self.remove_criteria(c)
                ).pack(side="left", padx=2)
                
    def update_graph(self):
        # Clear previous graph
        for widget in self.graph_frame.winfo_children():
            widget.destroy()
            
        # Get top 10 combinations based on first criteria
        sorted_combos = sorted(self.final_ranking, 
                             key=lambda x: x[self.selected_criteria[0]])[:10]
        
        # Create figure with dark style
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(12, 6))
        fig.patch.set_facecolor('#1a1a1a')
        ax.set_facecolor('#1a1a1a')
        
        # Set up bar positions
        x = np.arange(len(sorted_combos))
        width = 0.8 / len(self.selected_criteria)
        
        # Plot bars for each criteria
        for i, criteria in enumerate(self.selected_criteria):
            values = [combo[criteria] for combo in sorted_combos]
            ax.bar(x + i * width, values, width, label=criteria)
            
        # Customize graph
        ax.set_xticks(x + width * (len(self.selected_criteria) - 1) / 2)
        ax.set_xticklabels([combo['Name'] for combo in sorted_combos], 
                          rotation=45, ha='right')
        
        plt.title("Top 10 Combinations Comparison", color='white', pad=20)
        plt.legend(loc='upper right', facecolor='#1a1a1a', edgecolor='white', 
                  labelcolor='white')
        
        plt.tight_layout()
        
        # Create canvas
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        
    def update_detail_view(self, *args):
        # Clear existing details
        for widget in self.detail_container.winfo_children():
            widget.destroy()
              # Get selected combination details
        try:
            selected_combo = next(
                combo for combo in self.final_ranking 
                if combo['Name'] == self.selected_combo.get()
            )
        except StopIteration:
            print("Selected combination not found in final ranking.")
            return  
        

        # Create three columns
        smr_frame = ctk.CTkScrollableFrame(self.detail_container)
        smr_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        ctk.CTkLabel(smr_frame, text="SMR Details",
                     font=("Helvetica", 16, "bold")).pack(pady=10)
        
        if 'SMR Project' in selected_combo:
            for data in self.data_srm.values():
                if data['Project Name'] == selected_combo['SMR Project']:
                    for key, value in data.items():
                        ctk.CTkLabel(smr_frame, text=f"{key}: {value}").pack(pady=2, anchor="w")
        else:
            ctk.CTkLabel(smr_frame, text="No SMR Project details available").pack(pady=2)

        # Combo frame
        combo_frame = ctk.CTkScrollableFrame(self.detail_container)
        combo_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        ctk.CTkLabel(combo_frame, text="Combination Details", 
                    font=("Helvetica", 16, "bold")).pack(pady=10)
        for key, value in selected_combo.items():
            if key not in ['SMR Project', 'Electrolysis Technology']:
                ctk.CTkLabel(combo_frame, text=f"{key}: {value}").pack(pady=2, anchor="w")


        # Elec frame
        elec_frame = ctk.CTkScrollableFrame(self.detail_container)
        elec_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        ctk.CTkLabel(elec_frame, text="Electrolysis Details", 
                 font=("Helvetica", 16, "bold")).pack(pady=10)
        
        # Get selected combination details
        selected_combo = next(
            combo for combo in self.final_ranking
            if combo['Name'] == self.selected_combo.get()
        )

        if 'Electrolysis Technology' in selected_combo:
            for data in self.data_elec.values():
                if data['Technology'] == selected_combo['Electrolysis Technology']:
                    for key, value in data.items():
                        ctk.CTkLabel(elec_frame, text=f"{key}: {value}").pack(pady=2, anchor="w")
        else:
            ctk.CTkLabel(elec_frame, text="No Electrolysis Technology details available").pack(pady=2)
            
    def export_to_excel(self):
        filename = self.export_filename("Excel")
        filename = filename + ".xlsx"
        df = pd.DataFrame(self.final_ranking)
        df.to_excel(filename, index=False)

    def export_to_json(self):
        f = filedialog.asksaveasfile(mode='w', defaultextension=".json")
        if f is None:  # asksaveasfile return `None` if dialog closed with "cancel".
            return
        json.dump(self.final_ranking, f, indent=4)
        f.close()

    def export_to_text(self):
        f = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
        if f is None:  # asksaveasfile return `None` if dialog closed with "cancel".
            return
        for combo in self.final_ranking:
            f.write(f"Combination: {combo['Name']}\n")
            for key, value in combo.items():
                if key != 'Name':
                    f.write(f"{key}: {value}\n")
            f.write("\n")
        f.close()
        
    def on_closing(self):
        self.parent.deiconify()
        self.window.destroy()