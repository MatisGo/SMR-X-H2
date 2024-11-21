import pandas as pd
import os

def calculate_weighted_criteria(smr_data, elec_data, criteria_weighting, elec_coefficient=0.5):
    """
    Calculate weighted criteria for SMR and Electrolysis data.
    
    :param smr_data: Dictionary containing SMR data values
    :param elec_data: Dictionary containing Electrolysis data values
    :param criteria_weighting: Dictionary containing weights for each criteria
    :param elec_coefficient: Optional coefficient for electrolysis data (default 0.5)
    :return: Tuple of (final_grade, grade_info)
    """
    # List of criteria to calculate
    criteria_list = [
        ('Capex', 'Low Capex'),
        ('Safety', 'Safety'),
        ('Rentability', 'Rentability'),
        ('Opex', 'Low Opex'),
        ('Ecological impact', 'Ecological Impact'),
        ('Startup time', 'Fast startup time'),
        ('Scalability', 'Scalability'),
        ('Availability (h/year)', 'High Availability (h/year)'),
        ('Plant Area/Footprint', 'Plant Area/Footprint'),
        ('Technology readiness', 'Technology readiness'),
        ('Connection flexibility', 'Connection flexibility'),
        ('Geopolitical barriers', 'Geopolitical barriers'),
        ('Economic lifetime', 'Economic lifetime'),
        ('Production efficiency', 'Production efficiency'),
        ('Waste and decomissioning', 'Waste and decomissioning')
    ]
    
    # Calculate weighted criteria
    weighted_criteria = {}
    
    for criteria, weighting_key in criteria_list:
        # Weight criteria for SMR and Electrolysis
        smr_weighted = float(smr_data.get(criteria, 0)) * float(criteria_weighting.get(weighting_key, 0))
        elec_weighted = float(elec_data.get(criteria, 0)) * float(criteria_weighting.get(weighting_key, 0))
        
        # Combine SMR and Electrolysis with optional coefficient
        combined_weighted = smr_weighted + elec_coefficient * elec_weighted

        # Store the weighted value
        weighted_criteria[criteria] = combined_weighted
    
    # Calculate final grade
    final_grade = (sum(weighted_criteria.values()))/10
    
    # Prepare grade info dictionary
    grade_info = {
        'Grade': round(final_grade, 2)
    }
    
    # Add individual criteria scores to grade_info
    for criteria, value in weighted_criteria.items():
        grade_info[criteria.replace(" ", " ")] = round(value, 2)
    #print (grade_info)
    return final_grade, grade_info

def criteria_ranking_function(excel_data_srm, excel_data_electrolysis, combinations, criteria_weighting):
    try:
        for combination in combinations:
            smr_tech = combination['SMR Project']
            electrolysis_tech = combination['Electrolysis Technology']
            
            for smr_index, smr_data in excel_data_srm.items():
                callable_smr = smr_data.get('Project Name')
                if smr_tech == callable_smr:
                    for elec_index, elec_data in excel_data_electrolysis.items():
                        callable_elec = elec_data.get('Technology')
                        if electrolysis_tech == callable_elec:
                            # Calculate weighted criteria
                            final_grade, grade_info = calculate_weighted_criteria(
                                smr_data, elec_data, criteria_weighting
                            )
                            
                            # Update combination with grade information
                            combination.update(grade_info)
        
        # Sort combinations by 'Grade' in descending order
        sorted_combinations = sorted(combinations, key=lambda x: x['Grade'], reverse=True)
        
        # Assign rank based on the sorted order
        for idx, combo in enumerate(sorted_combinations, start=1):
            combo['Rank'] = idx
        
        return combinations
    
    except Exception as e:
        print(f"Error during criteria ranking: {e}")
        return None