# Project Structure:
# project_folder/
#   ├── startup.py
#   ├── main.py
#   ├── excel_reader.py
#   ├── technical_comparison.py
#   ├── DATA SMR.xlsx
#   ├── Criteria Ranking.xlsx
#   ├── C2P_display.py
#   ├── display_start.py
#   ├── criteria_function.py
#   └── results.display.py

# startup.py
import subprocess
import sys
import os

#Just the start of the script // will lauch main 
def start_application():
    try:
        # Get the directory where startup.py is located
        current_dir = os.path.dirname(os.path.abspath(__file__))
        main_script = os.path.join(current_dir, 'main.py')
        
        # Start the main application
        subprocess.run([sys.executable, main_script])
    except Exception as e: 
        print(f"Error starting application: {e}")

if __name__ == "__main__":
    start_application()