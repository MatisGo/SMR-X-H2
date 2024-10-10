# Comparing 2 Projects Data Presentation.py

from excel_reader import process_electrolysis_excel_data
data_elec= process_electrolysis_excel_data


# Function to get user selection from a list
def get_user_selection(options, prompt, max_selection=1):
    print(prompt)
    for idx, option in enumerate(options):
        print(f"{idx + 1}: {option}")
    
    selected_indices = input(f"Select up to {max_selection} (comma separated): ")
    try:
        selected_indices = list(map(int, selected_indices.split(',')))
        if len(selected_indices) > max_selection:
            print(f"Please select no more than {max_selection} options.")
            return []
        return [options[i - 1] for i in selected_indices if 0 < i <= len(options)]
    except ValueError:
        print("Invalid input. Please enter numbers only.")

# Main interface function
def C2P_Run(data_elec):
    # Step 1: Ask if user wants to compare electrolysers or nuclear technologies
    comparison_type = get_user_selection(["Electrolyser", "Nuclear"], "Do you want to compare electrolysers technologies or nuclear technologies?")
    
    if not comparison_type:
        return
    
    # Step 2: Process according to the user choice
    if comparison_type[0] == "Electrolyser":
        # Step 3: Load electrolyser data
        df = data_elec

        # Step 4: Offer the choice of available electrolyser technologies (maximum of 2 choices)
        techs = [df[tech]['Technology'] for tech in df]
        chosen_techs = get_user_selection(techs, "Select up to 2 electrolyser technologies to compare:", max_selection=2)
        
        if len(chosen_techs) > 2:
            print("You can only select up to two technologies.")
            return
        elif len(chosen_techs) == 0:
            print("No technologies selected.")
            return

        # Step 5: List all possible measures to compare (columns excluding 'Technology')
        measures = list(df[0].keys())
        measures.remove('Technology')  # Exclude the 'Technology' field itself
        chosen_measures = get_user_selection(measures, "Select the measures you want to compare:", max_selection=29)

        if not chosen_measures:
            print("No measures selected.")
            return

        # Step 6: Display the selected data for the chosen technologies and measures
        print(f"\nComparing {', '.join(chosen_techs)} for the following measures: {', '.join(chosen_measures)}\n")
        for tech in chosen_techs:
            for key, value in df.items():
                if value['Technology'] == tech:
                    print(f"{tech}:")
                    for measure in chosen_measures:
                        print(f"  {measure}: {value[measure]}")
                    print()  # Blank line for separation
    
    elif comparison_type[0] == "Nuclear":
        print("Nuclear technology comparison is not yet implemented in this example.")
