# criteria_function.py
import pandas as pd
import os

def criteria_ranking_function(excel_data_srm,excel_data_electrolysis,combinations,criteria_weighting):
    try:
        #Read combinations
        #For each Match take out SMR Name and Electrolyser Name 
        #Data example of Combination:
        #{'SMR Technology': 'SSR-U ', 'Electrolysis Technology': 'Alkaline', 'Temperature Difference (°C)': 725.0, 'Max H2 Production (kg/h)': 323.4782608695652, 'Electricity Loss (KWh)': 0, 'Heat Loss (KWh)': 5095.890410958904}
        for combination in combinations: # Loop all the possible combinations after technical _comparison
            smr_tech = combination['SMR Project'] # Get the name from the SMR Technology in the combination
            electrolysis_tech = combination['Electrolysis Technology'] # Get the name from Electrolysis in the combination
            for smr_index,smr_data in excel_data_srm.items(): # This loop is too look for the name of the SMR Technology(Coupling) matching it in the SMR Data 
                callable_smr= smr_data.get('Project Name')
                if smr_tech == callable_smr: # If the Project name Matches it goes to the next step
                    for elec_index, elec_data in excel_data_electrolysis.items(): # This loop is too look for the name of the SMR Technology(Coupling) matching it in the SMR Data
                        callable_elec= elec_data.get('Technology')
                        if electrolysis_tech == callable_elec:
                            #Here we have the correct values to start the Calculation of the Grade
                            #UPDATE THIS IF FACTOR IS NEEDED
                            cCapex=float(smr_data.get('Capex'))*float(criteria_weighting.get('Low Capex'))+float(elec_data.get('Capex'))*float(criteria_weighting.get('Low Capex'))
                            cSafety=(float(smr_data.get('Safety'))*float(criteria_weighting.get('Safety')))+(float(elec_data.get('Safety'))*float(criteria_weighting.get('Safety')))
                            cRentabilité=(float(smr_data.get('Rentability'))*float(criteria_weighting.get('Rentability')))+(float(elec_data.get('Rentability'))*float(criteria_weighting.get('Rentability')))
                            cOpex=(float(smr_data.get('Opex'))*float(criteria_weighting.get('Low Opex')))+(float(elec_data.get('Opex'))*float(criteria_weighting.get('Low Opex')))
                            cEcological=(float(smr_data.get('Ecological impact'))*float(criteria_weighting.get('Ecological Impact')))+(float(elec_data.get('Ecological impact'))*float(criteria_weighting.get('Ecological Impact')))
                            cStartup=(float(smr_data.get('Startup time'))*float(criteria_weighting.get('Fast startup time')))+(float(elec_data.get('Startup time'))*float(criteria_weighting.get('Fast startup time')))
                            cScalability=(float(smr_data.get('Scalability'))*float(criteria_weighting.get('Scalability')))+(float(elec_data.get('Scalability'))*float(criteria_weighting.get('Scalability')))
                            cAvailability=(float(smr_data.get('Availability (h/year)'))*float(criteria_weighting.get('High Availability (h/year)')))+(float(elec_data.get('Availability (h/year)'))*float(criteria_weighting.get('High Availability (h/year)')))
                            cPlantArea=(float(smr_data.get('Plant Area/Footprint'))*float(criteria_weighting.get('Plant Area/Footprint')))+(float(elec_data.get('Plant Area/Footprint'))*float(criteria_weighting.get('Plant Area/Footprint')))
                            cTechnology=(float(smr_data.get('Technology readiness'))*float(criteria_weighting.get('Technology readiness')))+(float(elec_data.get('Technology readiness'))*float(criteria_weighting.get('Technology readiness')))
                            cFlexibility=(float(smr_data.get('Connection flexibility'))*float(criteria_weighting.get('Connection flexibility')))+(float(elec_data.get('Connection flexibility'))*float(criteria_weighting.get('Connection flexibility')))
                            cGeopolitical=(float(smr_data.get('Geopolitical barriers'))*float(criteria_weighting.get('Geopolitical barriers')))+(float(elec_data.get('Geopolitical barriers'))*float(criteria_weighting.get('Geopolitical barriers')))
                            cLifetime=(float(smr_data.get('Economic lifetime'))*float(criteria_weighting.get('Economic lifetime')))+(float(elec_data.get('Economic lifetime'))*float(criteria_weighting.get('Economic lifetime')))
                            cEfficiency=(float(smr_data.get('Production efficiency'))*float(criteria_weighting.get('Production efficiency')))+(float(elec_data.get('Production efficiency'))*float(criteria_weighting.get('Production efficiency')))
                            cWaste=(float(smr_data.get('Waste and decomissioning'))*float(criteria_weighting.get('Waste and decomissioning')))+(float(elec_data.get('Waste and decomissioning'))*float(criteria_weighting.get('Waste and decomissioning')))


                            
                            final_grade= cCapex + cSafety + cRentabilité +cOpex + cEcological + cStartup + cScalability + cAvailability + cPlantArea + cTechnology + cFlexibility + cGeopolitical + cLifetime + cEfficiency + cWaste
                            grade_info ={
                                'Grade': int(final_grade),
                                'Capex': cCapex,
                                'Safety': cSafety,
                                'Rentability': cRentabilité,
                                'Opex': cOpex,
                                'Ecological Impact': cEcological,
                                'Startup time' : cStartup,
                                'Scalability' : cScalability,
                                'Availability' : cAvailability,
                                'Plant Area/Footprint' : cPlantArea,
                                'Technology readiness' : cTechnology,
                                'Connection flexibility' : cFlexibility,
                                'Geopolitical barriers' : cGeopolitical,
                                'Economic lifetime' : cLifetime,
                                'Production efficiency' : cEfficiency,
                                'Waste and decomissioning' : cWaste
                                                            
                            }
                            combination.update(grade_info)
        
        #print(combinations) #See combinations 
        for item in combinations:
            if not isinstance(item, dict):
                print(f"Error: {item} is not a dictionary")
                continue  # Skip invalid items

            # Sort the combinations by 'Grade' in descending order
        sorted_combinations = sorted(combinations, key=lambda x: x['Grade'], reverse=True)

            # Assign rank based on the sorted order
        for idx, combo in enumerate(sorted_combinations, start=1):
            combo['Rank'] = idx

            # Display the ranked combinations
        '''
        for combo in sorted_combinations:
                
            print(combo)  #Display the rank 
        '''
        return combinations

    except Exception as e:
        print(f"Error during criteria ranking: {e}")