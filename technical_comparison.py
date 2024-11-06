# technical_comparison.py
#In this excel will take place the Technical comparison.
# The Mehodology needs to be explained here
#

def matching_combinations(excel_data_srm,excel_data_electrolysis):
    if excel_data_srm is None or excel_data_electrolysis is None:
        print("No data available for comparison")
        quit()
        return
    try:
    # Function to compare SMR and Electrolysis values
        matches = []   # List to store match
        no_matches =[] # List to store non matching combination and explain why 
        for smr_index, smr_data in excel_data_srm.items():
            smr_power_output = float(smr_data.get('Electricity Power Output', 0))
            smr_thermal_output = float(smr_data.get('Thermal Output', 0))
            smr_outlet_coolant = float(smr_data.get('Outlet Coolant', 0))
            for elec_index, elec_data in excel_data_electrolysis.items():
                elec_operating_temp_min = elec_data.get('Operating Temp Min')
                elec_energy_consumption = float(elec_data.get('System Electricity Cosumption'))
                elec_heat_consumption = float(elec_data.get('System heat needed'))
                elec_technology = elec_data.get('Technology')
                if elec_technology != 'SOEC' and smr_power_output >= 1 or elec_technology == 'SOEC' and smr_power_output >= 1 and smr_thermal_output >= elec_operating_temp_min: 
                    #print(elec_technology)
                    tempdiff = abs(smr_outlet_coolant-elec_operating_temp_min) #The Temperature Difference value is absolute, the SMR temperature is higher than electrolyser need
                    production_efficiency = (smr_data['Thermal efficiency'] * (elec_data['Efficiency (LHV)']/100))*100 # ηPRODUCTION = ηth x ηELECTROLYZER
                    
                    prodresults=[]  # The results of the Calculation of Max H2 will be stored there 
                    if elec_technology == 'SOEC':
                        #factorSOEC= 0.93 # 7% of the heat is needed to heat up the stack and the Water. The production of energy is therefore multiply by 0.97
                        prodresults = maxProductioncalc(smr_power_output,elec_energy_consumption,factor=0.93)
                    else :
                         #For Alk and PEM no extra heat is needed appart from the heat waste heat after the electricity production turbine 
                        prodresults = maxProductioncalc(smr_power_output,elec_energy_consumption,factor=1)
                    
                    match_info = {
                        'Name':smr_data['Project Name']+' X '+ elec_data['Technology'],
                        'SMR Project': smr_data['Project Name'],
                        'Electrolysis Technology': elec_data['Technology'],
                        'Temperature Difference (°C)': tempdiff, #Absolute value of the temperature difference
                        'Max H2 Production (kg/h)': round(prodresults['1'],2),
                        'SMR Thermal efficiency (%)': round(smr_data['Thermal efficiency'],2),
                        'Production Efficiency (%)': round(production_efficiency,2),
                        #'Tempertaure Output':smr_data['Temperature Output'],
                    }
                    matches.append(match_info)
                if smr_outlet_coolant <= elec_operating_temp_min and smr_power_output == 0:
                    nomatch_info = {
                        'SMR Project': smr_data['Project Name'],
                        'Electrolysis Technology': elec_data['Technology'],
                        'Reason':'No Electricity Output on this Type of Reactor'# CHECK IF THIS IS WORKING
                    }
                    no_matches.append(nomatch_info) #No Match is maybe if we want to display the combinations kicked out
                else :
                    nomatch_info = {
                        'SMR Project': smr_data['Project Name'],
                        'Electrolysis Technology': elec_data['Technology'],
                        'Reason':'SMR Coolant Temperature is not sufficiant for Electrolyser' # CHECK IF THIS IS WORKING
                    }
                    no_matches.append(nomatch_info) #No Match is maybe if we want to display the combinations kicked out


        # Print the matching combinations
        #print("Matching Combinations:")
        #print(matches)

        return matches
    

        
    except Exception as e:
        print(f"Error during technical comparison: {e}")


def maxProductioncalc(smr_power_output,elec_energy_consumption,factor):
    #SMR Power Output in MW
    #Electrolyser Electricity consumption in KWh => To produce 1 Kg Hydrogen

    #Capacity Factor measures its ability to generate electricity relative to its maximum potential output
    capacity_Factor= 0.93

    try:
        results=[]

        max_prod_elec = (smr_power_output*factor*capacity_Factor*1000)/elec_energy_consumption

        # factor changes regarding the technology. For Alk end PEM no Factor.
        # For SOEC 0.93% Factor is introduce because 7% of energy is used to heat up the Electrolysis Water/Stack  

        #Efficiency calculation??
        results = {
            '1': max_prod_elec,
            '2': 'Not calculated',
        }

        return results 
        
    except Exception as e:
        print(f"Error during max hydrogen output calculation: {e}")