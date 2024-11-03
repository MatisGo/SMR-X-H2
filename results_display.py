import customtkinter as ctk
from typing import Dict, List
import json

class ResultsDisplayWindow:
    def __init__(self, parent, final_ranking: List[Dict]):
        # Store parent reference
        self.parent = parent
        
        # Hide parent window
        self.parent.withdraw()
        
        # Create the window
        self.window = ctk.CTkToplevel(parent)
        self.window.title("Top 3 Combinations")
        width= self.window.winfo_screenwidth()
        height= self.window.winfo_screenheight()
        #setting tkinter window size
        self.window.geometry("%dx%d" % (width, height))

        # Bind the closing event
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Make sure this window appears in front
        self.window.lift()
        self.window.focus_force()
        
        # Create main container frame
        self.container_frame = ctk.CTkFrame(self.window)
        self.container_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create title frame
        self.title_frame = ctk.CTkFrame(self.container_frame)
        self.title_frame.pack(fill="x", padx=10, pady=5)
        
        # Title
        title_label = ctk.CTkLabel(
            self.title_frame,
            text="Top 3 Technology Combinations",
            font=("Helvetica", 24, "bold")
        )
        title_label.pack(pady=10)
        
        # Create scrollable frame
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self.container_frame,
            width=900,
            height=600
        )
        self.scrollable_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Sort final_ranking by Rank and get top 3
        sorted_ranking = sorted(final_ranking, key=lambda x: x['Rank'], reverse=False)
        top_three = sorted_ranking[:3]
        
        # Create frames for top 3 combinations
        self.create_combination_frames(top_three)
        
        # Create bottom frame for button
        self.button_frame = ctk.CTkFrame(self.container_frame)
        self.button_frame.pack(fill="x", padx=10, pady=5)
        
        # Create home button in bottom frame
        self.home_button = ctk.CTkButton(
            self.button_frame,
            text="Return to Home",
            command=self.return_to_home,
            width=200,
            height=40,
            font=("Helvetica", 14, "bold")
        )
        self.home_button.pack(pady=10)

    def create_combination_frames(self, combinations: List[Dict]):
        """Create a frame for each of the top 3 combinations"""
        medals = ["🥇 First Place", "🥈 Second Place", "🥉 Third Place"]
        for i, combo in enumerate(combinations):
            # Create frame for this combination
            combo_frame = ctk.CTkFrame(self.scrollable_frame)
            combo_frame.pack(padx=10, pady=10, fill="x")
            
            # Title for this combination with medal emoji
            rank_label = ctk.CTkLabel(
                combo_frame,
                text=f"{medals[i]} (Rank: {combo['Rank']})",
                font=("Helvetica", 18, "bold")
            )
            rank_label.pack(pady=10)
            
            # Create grid for details
            details_frame = ctk.CTkFrame(combo_frame)
            details_frame.pack(padx=20, pady=10, fill="x")
            
            # Add details in a grid layout
            self.add_detail_row(details_frame, 0, "SMR Project:", combo['SMR Project'])
            self.add_detail_row(details_frame, 1, "Electrolysis Technology:", combo['Electrolysis Technology'])
            self.add_detail_row(details_frame, 2, "Temperature Difference:", f"{combo['Temperature Difference (°C)']:.2f} °C")
            self.add_detail_row(details_frame, 3, "Max H₂ Production:", f"{combo['Max H2 Production (kg/h)']:.2f} kg/h")
            self.add_detail_row(details_frame, 4, "Production Efficiency:", f"{combo['Production Efficiency (%)']:.2f} %")
            self.add_detail_row(details_frame, 5, "Grade:", f"{combo['Grade']}")

    def add_detail_row(self, parent, row: int, label_text: str, value_text: str):
        """Add a row of details with label and value"""
        # Label
        label = ctk.CTkLabel(
            parent,
            text=label_text,
            font=("Helvetica", 14, "bold")
        )
        label.grid(row=row, column=0, padx=10, pady=5, sticky="e")
        
        # Value
        value = ctk.CTkLabel(
            parent,
            text=value_text,
            font=("Helvetica", 14)
        )
        value.grid(row=row, column=1, padx=10, pady=5, sticky="w")

    def return_to_home(self):
        """Handle return to home button click"""
        self.parent.deiconify()  # Show parent window
        self.window.destroy()     # Close this window

    def on_closing(self):
        """Handle window closing"""
        self.parent.deiconify()  # Show parent window
        self.window.destroy()     # Close this window

    def export_to_json(self, data: Dict, filename: str):
        """Export the data to a JSON file"""
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)