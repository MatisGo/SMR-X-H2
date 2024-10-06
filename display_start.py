# display_start.py
import tkinter as tk
from tkinter import ttk

class DisplayWindow:
    def __init__(self, root, callbacks):
        self.root = root
        self.root.title("Technology Comparison Tool")
        self.root.geometry("800x600")  # Increased window size
        
        # Configure style
        style = ttk.Style()
        style.theme_use('default')
        style.configure('TButton', font=('Arial', 12))
        style.configure('TLabel', font=('Arial', 16))
        
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(expand=True, fill="both")
        
        # Welcome label
        welcome_label = ttk.Label(main_frame, text="Welcome to the Technology Comparison Tool", 
                                 font=("Arial", 20, "bold"))
        welcome_label.pack(pady=30)
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(expand=True)
        
        # Buttons
        buttons = [
            ("Run Complete Comparison", callbacks['complete_comparison']),
            ("Compare 2 Technologies Coupling", callbacks['two_technologies']),
            ("Compare 2 Projects", callbacks['two_projects']),
            ("Give H2 Output Value", callbacks['h2_output'])
        ]
        
        for text, command in buttons:
            btn = ttk.Button(button_frame, text=text, command=command)
            btn.pack(pady=15, padx=20, ipady=10, ipadx=20)
        
        # Footer frame
        footer_frame = ttk.Frame(main_frame)
        footer_frame.pack(side="bottom", pady=20)
        
        footer_text = ttk.Label(footer_frame, 
                               text="Select an option ",
                               font=("Arial", 12))
        footer_text.pack()

    def show_message(self, message):
        # Utility method for displaying messages
        tk.messagebox.showinfo("Information", message)