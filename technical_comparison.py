# technical_comparison.py
#In this excel will take place the Technical comparison.
# The Mehodology needs to be explained here
#

var=0

def matching_combinations(excel_data_srm,excel_data_electrolysis):
    if excel_data_srm is None or excel_data_electrolysis is None:
        print("No data available for comparison")
        quit()
        return
    #print (excel_data_srm)
    #print (excel_data_electrolysis)
    try:
    # Function to compare SMR and Electrolysis values
        smr_index =0
        elec_index =0
        matches = []   # List to store match


        ""
        for smr_index, smr_data in excel_data_srm.items():
            smr_outlet_coolant = smr_data.get('Outlet Coolant')
            print(smr_index,smr_outlet_coolant)
            for elec_index, elec_data in excel_data_electrolysis.items():
                elec_operating_temp_max = elec_data.get('Operating Temp Max')
                print(smr_index,smr_outlet_coolant,elec_operating_temp_max)
                if smr_outlet_coolant <= elec_operating_temp_max + 80 and smr_outlet_coolant >= elec_operating_temp_max - 80:
                    # Create a dictionary for the match
                    print('Match!!!')
                    match_info = {
                        'SMR Technology': smr_data['Project Name'],
                        'Electrolysis Technology': elec_data['Technology']
                    }
                    matches.append(match_info)

        # Print the matching combinations
        print("Matching Combinations:")
        print(matches)

        return matches
        ""


        # If you want to save the matches to a new library
        matches_library = {i: match for i, match in enumerate(matching_combinations)}
                

        
    except Exception as e:
        print(f"Error during technical comparison: {e}")