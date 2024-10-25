import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk

class DisplayWindow:
    def __init__(self, root, callbacks):
        self.root = root
        self.root.title("Technology Comparison Tool")
        self.root.geometry("900x700")
        
        # Set the appearance mode and color theme
        ctk.set_appearance_mode("system")  # Use system theme
        ctk.set_default_color_theme("blue")  # Set default color theme
        
        # Create main frame with modern styling
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Welcome section
        self.create_header()
        
        # Create scrollable frame for buttons
        self.create_button_section(callbacks)
        
        # Create footer
        self.create_footer()

    def create_header(self):
        # Title frame
        title_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        title_frame.pack(pady=(20, 30))

        # Main title
        welcome_label = ctk.CTkLabel(
            title_frame,
            text="Technology Comparison Tool",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        welcome_label.pack(pady=(0, 10))
        
        # Subtitle
        subtitle_label = ctk.CTkLabel(
            title_frame,
            text="Analyze and compare technology solutions efficiently",
            font=ctk.CTkFont(size=16),
            text_color="gray70"
        )
        subtitle_label.pack()

    def create_button_section(self, callbacks):
        # Button container
        button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        button_frame.pack(expand=True, fill="both", padx=40)

        # Button configurations with descriptions
        buttons_config = [
            {
                "text": "Run Complete Comparison",
                "command": callbacks['complete_comparison'],
                "description": "Perform a comprehensive analysis of all available technologies",
                "icon": "🔍"
            },
            {
                "text": "Compare Technologies Coupling",
                "command": callbacks['two_technologies'],
                "description": "Analyze the coupling between two specific technologies",
                "icon": "🔄"
            },
            {
                "text": "H2 Output Value Analysis",
                "command": callbacks['h2_output'],
                "description": "Calculate and evaluate H2 output measurements",
                "icon": "📊"
            }
        ]

        for btn_config in buttons_config:
            # Create container for each button group
            button_container = ctk.CTkFrame(button_frame, fg_color="transparent")
            button_container.pack(pady=15, fill="x")

            # Create modern button with hover effect
            button = ctk.CTkButton(
                button_container,
                text=f"{btn_config['icon']} {btn_config['text']}",
                command=btn_config['command'],
                height=45,
                font=ctk.CTkFont(size=15, weight="bold"),
                corner_radius=10,
                hover_color=("gray70", "gray30")
            )
            button.pack(fill="x", padx=20)

            # Add description label
            description = ctk.CTkLabel(
                button_container,
                text=btn_config['description'],
                font=ctk.CTkFont(size=12),
                text_color="gray60"
            )
            description.pack(pady=(5, 0))

    def create_footer(self):
        # Footer frame
        footer_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        footer_frame.pack(side="bottom", pady=20)

        # Footer text
        footer_text = ctk.CTkLabel(
            footer_frame,
            text="Select an option above to begin your analysis",
            font=ctk.CTkFont(size=13),
            text_color="gray60"
        )
        footer_text.pack()

    def show_message(self, message):
        messagebox.showinfo("Information", message)

    def toggle_color_theme(self):
        # Add method to toggle between light and dark mode
        if ctk.get_appearance_mode() == "Dark":
            ctk.set_appearance_mode("Light")
        else:
            ctk.set_appearance_mode("Dark")

# Example usage:
if __name__ == "__main__":
    root = ctk.CTk()
    callbacks = {
        'complete_comparison': lambda: print("Complete comparison"),
        'two_technologies': lambda: print("Compare technologies"),
        'h2_output': lambda: print("H2 output")
    }
    app = DisplayWindow(root, callbacks)
    root.mainloop()