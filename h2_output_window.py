import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from tkinter import messagebox

class H2OutputAnalysisWindow:
    def __init__(self, root, combinations):
        # Close the main window
        root.withdraw()
        
        # Create new window
        self.window = ctk.CTkToplevel()
        self.window.title("H2 Output Analysis")
        self.window.geometry("1000x800")
        self.window.protocol("WM_DELETE_WINDOW", lambda: self.on_closing(root))
        
        self.combinations = combinations
        self.root = root
        
        # Unit conversion factors to kg/h
        self.conversion_factors = {
            "kg/h": 1,
            "t/h": 1000,
            "kg/day": 1/24,
            "t/day": 1000/24
        }
        
        # Inverse conversion factors (kg/h to selected unit)
        self.inverse_conversion_factors = {
            "kg/h": 1,
            "t/h": 0.001,
            "kg/day": 24,
            "t/day": 24/1000
        }
        
        # Range limits in kg/h
        self.min_kg_h = 20
        self.max_kg_h = 10000
        
        self.create_widgets()
        
    def create_widgets(self):
        # Create main frame
        self.main_frame = ctk.CTkFrame(self.window)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Input section
        input_frame = ctk.CTkFrame(self.main_frame)
        input_frame.pack(fill="x", padx=10, pady=10)
        
        # Label for production input
        ctk.CTkLabel(input_frame, text="H2 Production Amount:").pack(side="left", padx=5)
        
        # Entry for production value
        self.production_entry = ctk.CTkEntry(input_frame, width=120)
        self.production_entry.pack(side="left", padx=5)
        
        # Dropdown for units
        self.unit_var = ctk.StringVar(value="kg/h")
        unit_dropdown = ctk.CTkOptionMenu(
            input_frame,
            values=list(self.conversion_factors.keys()),
            variable=self.unit_var,
            command=self.update_range_message
        )
        unit_dropdown.pack(side="left", padx=5)
        
        # Range message label
        self.range_label = ctk.CTkLabel(input_frame, text="")
        self.range_label.pack(side="left", padx=5)
        self.update_range_message()
        
        # Calculate button
        ctk.CTkButton(
            input_frame,
            text="Calculate",
            command=self.calculate_and_display
        ).pack(side="left", padx=20)
        
        # Home button
        ctk.CTkButton(
            input_frame,
            text="Home",
            command=lambda: self.return_home()
        ).pack(side="right", padx=5)
        
        # Frame for graph
        self.graph_frame = ctk.CTkFrame(self.main_frame)
        self.graph_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    def update_range_message(self, *args):
        current_unit = self.unit_var.get()
        inv_factor = self.inverse_conversion_factors[current_unit]
        min_val = round(self.min_kg_h * inv_factor, 3)
        max_val = round(self.max_kg_h * inv_factor, 3)
        self.range_label.configure(text=f"Range: {min_val} - {max_val} {current_unit}")
        
    def calculate_and_display(self):
        try:
            # Get user input and convert to kg/h
            user_value = float(self.production_entry.get())
            current_unit = self.unit_var.get()
            conversion_factor = self.conversion_factors[current_unit]
            user_value_kgh = user_value * conversion_factor
            
            # Convert range limits to current unit for error message
            inv_factor = self.inverse_conversion_factors[current_unit]
            min_val = round(self.min_kg_h * inv_factor, 3)
            max_val = round(self.max_kg_h * inv_factor, 3)
            
            # Validate input range
            if not (self.min_kg_h <= user_value_kgh <= self.max_kg_h):
                messagebox.showerror("Invalid Input", 
                    f"Production must be between {min_val} and {max_val} {current_unit}")
                return
            
            # Calculate differences and get 10 nearest combinations
            differences = []
            for combo in self.combinations:
                h2_prod = combo['Max H2 Production (kg/h)']
                diff = abs(h2_prod - user_value_kgh)
                differences.append((diff, combo))
            
            # Sort by difference and get top 10
            differences.sort(key=lambda x: x[0])
            nearest_combos = differences[:10]
            
            # Create and display graph
            self.display_graph(nearest_combos, user_value_kgh)
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")
    
    def display_graph(self, nearest_combos, user_value_kgh):
        # Clear previous graph
        for widget in self.graph_frame.winfo_children():
            widget.destroy()
        
        # Create figure and axis with dark background
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(10, 5))  # Reduced size
        fig.patch.set_facecolor('#1a1a1a')  # Dark background
        ax.set_facecolor('#1a1a1a')  # Dark background for plot area
        
        # Extract data for plotting
        names = [combo[1]['Name'] for combo in nearest_combos]
        productions = [combo[1]['Max H2 Production (kg/h)'] for combo in nearest_combos]
        ranks = [combo[1].get('Rank', 'N/A') for combo in nearest_combos]
        
        # Convert values to selected unit for display
        current_unit = self.unit_var.get()
        inv_factor = self.inverse_conversion_factors[current_unit]
        productions_converted = [p * inv_factor for p in productions]
        user_value_converted = user_value_kgh * inv_factor
        
        # Create bar chart
        bars = ax.bar(names, productions_converted)
        
        # Add user target line
        ax.axhline(y=user_value_converted, color='r', linestyle='--', 
                  label=f'Target Production ({user_value_converted:.2f} {current_unit})')
        
        # Customize graph
        ax.set_xlabel('Combinations', color='white')
        ax.set_ylabel(f'H2 Production ({current_unit})', color='white')
        ax.set_title('Nearest Matching Combinations', color='white', pad=20)
        plt.xticks(rotation=45, ha='right', color='white')
        plt.yticks(color='white')
        
        # Add rank labels on top of bars
        for i, bar in enumerate(bars):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                   f'Rank: {ranks[i]}',
                   ha='center', va='bottom', color='white')
        
        # Add legend with better positioning
        ax.legend(loc='upper right', bbox_to_anchor=(1, -0.15),
                 facecolor='#1a1a1a', edgecolor='white', labelcolor='white')
        
        # Adjust layout to prevent legend cutoff
        plt.tight_layout()
        
        # Create canvas and pack it
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)
        
        # Add Export to Excel button
        ctk.CTkButton(
            self.graph_frame,
            text="Export to Excel",
            command=lambda: self.export_to_excel(nearest_combos)
        ).pack(pady=10)
        
    def export_to_excel(self, combinations_to_export):
        try:
            # Convert combinations to DataFrame
            df = pd.DataFrame([combo[1] for combo in combinations_to_export])
            
            # Save to Excel
            filename = "h2_output_analysis.xlsx"
            df.to_excel(filename, index=False)
            messagebox.showinfo("Success", f"Data exported to {filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export: {str(e)}")
    
    def return_home(self):
        self.window.destroy()
        self.root.deiconify()
    
    def on_closing(self, root):
        self.window.destroy()
        root.deiconify()