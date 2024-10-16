# technical_comparison.py
#In this excel will take place the Technical comparison.
# The Mehodology needs to be explained here
#

def matching_combinations(excel_data_srm,excel_data_electrolysis):
    if excel_data_srm is None or excel_data_electrolysis is None:
        print("No data available for comparison")
        quit()
        return
    #print (excel_data_srm)
    #print (excel_data_electrolysis)
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

                if smr_outlet_coolant >= elec_operating_temp_min and smr_power_output >= 1: 
                    tempdiff=abs(smr_outlet_coolant-elec_operating_temp_min) #The Temperature Difference value is absolute, the SMR temperature is higher than electrolyser need
                    prodresults=[]  # The results of the Calculation of Max H2 will be stored there 
                    prodresults = maxProductioncalc(smr_power_output,smr_thermal_output,elec_energy_consumption,elec_heat_consumption)
                    match_info = {
                        'SMR Technology': smr_data['Project Name'],
                        'Electrolysis Technology': elec_data['Technology'],
                        'Temperature Difference (°C)':tempdiff, #Absolute value of the temperature difference
                        'Max H2 Production (kg/h)':prodresults['1'],
                        'Electricity Loss (KWh)':prodresults['2'],
                        'Heat Loss (KWh)':prodresults['3'],

                    }
                    matches.append(match_info)
                if smr_outlet_coolant <= elec_operating_temp_min and smr_power_output == 0:
                    nomatch_info = {
                        'SMR Technology': smr_data['Project Name'],
                        'Electrolysis Technology': elec_data['Technology'],
                        'Reason':'No Electricity Output on this Type of Reactor'
                    }
                    no_matches.append(nomatch_info)
                else :
                    nomatch_info = {
                        'SMR Technology': smr_data['Project Name'],
                        'Electrolysis Technology': elec_data['Technology'],
                        'Reason':'SMR Coolant Temperature is not sufficiant for Electrolyser'
                    }
                    no_matches.append(nomatch_info)


        # Print the matching combinations
        #print("Matching Combinations:")
        #print(matches)

        return matches
    

        
    except Exception as e:
        print(f"Error during technical comparison: {e}")


def maxProductioncalc(smr_power_output,smr_thermal_output,elec_energy_consumption,elec_heat_consumption):
    #SMR Power Output in MW
    #SMR Thermal Output in MW
    #Electrolyser Electricity consumption in KWh => To produce 1 Kg Hydrogen
    #Electrolyser thermal consumption in KWh => To Produce 1 Kg Hydrogen

    #Capacity Factor measures its ability to generate electricity relative to its maximum potential output
    capacity_Factor= 0.93
    try:
        results=[]
        max_prod_thermal = (smr_thermal_output*capacity_Factor*1000)/elec_heat_consumption
        max_prod_elec = (smr_power_output*capacity_Factor*1000)/elec_energy_consumption
        # Here Reverse Calculation to find out 
        zerovalue = 0 
        if max_prod_thermal > max_prod_elec: 
            results = {
                '1': max_prod_elec,
                '2': zerovalue,
                '3': max_prod_thermal
            }
        else :
            results = {
                '1': max_prod_thermal,
                '2': max_prod_elec,
                '3': zerovalue
            }
        return results 
        
    except Exception as e:
        print(f"Error during max hydrogen output calculation: {e}")