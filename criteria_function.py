# criteria_function.py
import pandas as pd
import os

def criteria_ranking_function(excel_data_srm,excel_data_electrolysis,combinations,criteria_weighting):
    try:
        #print(combinations)
        #Read combinations
        #For each Match take out SMR Name and Electrolyser Name 
        #{'SMR Technology': 'SSR-U ', 'Electrolysis Technology': 'Alkaline', 'Temperature Difference (°C)': 725.0, 'Max H2 Production (kg/h)': 323.4782608695652, 'Electricity Loss (KWh)': 0, 'Heat Loss (KWh)': 5095.890410958904}
        for combination in combinations:
            smr_tech = combination['SMR Technology']
            electrolysis_tech = combination['Electrolysis Technology']
            print(smr_tech,electrolysis_tech)
            for smr_index,smr_data in excel_data_srm.items():
                callable_smr= smr_data.get('Project Name')
                if smr_tech == callable_smr:
                    for elec_index, elec_data in excel_data_electrolysis.items():
                        callable_elec= elec_data.get('Technology')
                        if electrolysis_tech == callable_elec:
                            #print(excel_data_srm('Project Name'),excel_data_electrolysis('Technology'))
                            print('ici')
                            print(callable_smr,callable_elec)





                            
        return 

    except Exception as e:
        print(f"Error during criteria ranking: {e}")
