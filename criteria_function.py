# criteria_function.py
import pandas as pd
import os

def criteria_ranking_function(excel_data_srm,excel_data_electrolysis,combinations,criteria_weighting):
    try:
        #print(combinations)
        #Read combinations
        #For each Match take out SMR Name and Electrolyser Name 
        #Data example of Combination:
        #{'SMR Technology': 'SSR-U ', 'Electrolysis Technology': 'Alkaline', 'Temperature Difference (°C)': 725.0, 'Max H2 Production (kg/h)': 323.4782608695652, 'Electricity Loss (KWh)': 0, 'Heat Loss (KWh)': 5095.890410958904}
        for combination in combinations: # Loop all the possible combinations after technical _comparison
            smr_tech = combination['SMR Project'] # Get the name from the SMR Technology in the combination
            electrolysis_tech = combination['Electrolysis Technology'] # Get the name from Electrolysis in the combination
            #print(smr_tech,electrolysis_tech)
            for smr_index,smr_data in excel_data_srm.items(): # This loop is too look for the name of the SMR Technology(Coupling) matching it in the SMR Data 
                callable_smr= smr_data.get('Project Name')
                if smr_tech == callable_smr: # If the Project name Matches it goes to the next step
                    for elec_index, elec_data in excel_data_electrolysis.items(): # This loop is too look for the name of the SMR Technology(Coupling) matching it in the SMR Data
                        callable_elec= elec_data.get('Technology')
                        if electrolysis_tech == callable_elec:
                            

                            print('ici')
                            print(callable_smr,callable_elec)





                            
        return 

    except Exception as e:
        print(f"Error during criteria ranking: {e}")
