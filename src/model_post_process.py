import pandas as pd 

import pandas as pd 
import sys
sys.path.append('../')
from .column_settings import settings_dict 

from src.column_settings import *
import pandas as pd
import numpy as np

# Function to format the table for each energy type
def format_table(df, energy_type):
    table = df[['name', 'r2', 'root_mean_squared_error', 'mean_absolute_error']].copy()
    table.columns = [
        'Model', 
        f'{energy_type} R-squared',
        f'{energy_type} RMSE',
        f'{energy_type} MAE'
    ]
    table[f'{energy_type} R-squared'] = table[f'{energy_type} R-squared'].apply(lambda x: f"{x:.2f}")
    table[f'{energy_type} RMSE'] = table[f'{energy_type} RMSE'].abs().apply(lambda x: f"{x:,.0f}")
    table[f'{energy_type} MAE'] = table[f'{energy_type} MAE'].abs().apply(lambda x: f"{x:,.0f}")
    return table

def generate_energy_table(df):
    # Reset index
    df = df.reset_index()
    
    # Separate data for electricity and gas
    df_elec = df[df['label'] == 'total_elec'].sort_values('r2', ascending=False)
    df_gas = df[df['label'] == 'total_gas'].sort_values('r2', ascending=False)
    
    # Generate tables
    gas_table = format_table(df_gas, 'Gas')
    elec_table = format_table(df_elec, 'Electricity')
    
    # Merge tables
    combined_table = pd.merge(gas_table, elec_table, on='Model', how='outer')
    
    # Sort by the average R-squared (considering both gas and electricity)
    combined_table['Avg R-squared'] = combined_table.apply(lambda row: 
        (float(row['Gas R-squared']) + float(row['Electricity R-squared'])) / 2 
        if pd.notnull(row['Gas R-squared']) and pd.notnull(row['Electricity R-squared'])
        else float(row['Gas R-squared']) if pd.notnull(row['Gas R-squared'])
        else float(row['Electricity R-squared']),
        axis=1
    )
    combined_table = combined_table.sort_values('Avg R-squared', ascending=False)
    
    # Drop the average column as it was just for sorting
    combined_table = combined_table.drop('Avg R-squared', axis=1)
    
    return combined_table

def process_main(results_df):
    results_df['name'] = [settings_dict[int(x)][0] for x in results_df.col_setting]
    results_df = results_df.set_index('col_setting').reset_index().sort_values('col_setting')
    results_df.to_csv(f'./results/model_prediction_results.csv', index=False)

def format_table_region(df, energy_type):
    table = df[['reg_name', 'r2', 'root_mean_squared_error', 'mean_absolute_error']].copy()
    table.columns = [
        'Region', 
        f'{energy_type} R-squared',
        f'{energy_type} RMSE',
        f'{energy_type} MAE'
    ]
    table[f'{energy_type} R-squared'] = table[f'{energy_type} R-squared'].apply(lambda x: f"{x:.2f}")
    table[f'{energy_type} RMSE'] = table[f'{energy_type} RMSE'].abs().apply(lambda x: f"{x:.0f}")
    table[f'{energy_type} MAE'] = table[f'{energy_type} MAE'].abs().apply(lambda x: f"{x:.0f}")
    return table
    
def process_region(df):

    region_mapping = {0: 'SW',
    1: 'EM',
    2: 'EE',
    3: 'WA',
    4: 'NW',
    5: 'YH',
    6: 'WM',
    7: 'SC',
    8: 'LN',
    9: 'NE',
    10: 'SE'}

    label_mapping = {0: 'South West',
    1: 'East Midlands',
    2: 'East of England',
    3: 'Wales',
    4: 'North West',
    5: 'Yorkshire',
    6: 'West Midlands',
    7: 'Scotlnd',
    8: 'London',
    9: 'North East',
    10: 'South East'}

    # invert this mapping: region_mapping
    invt_reg = {v: k for k, v in region_mapping.items()}
    invt_reg, region_mapping  

    df['name'] = [settings_dict[int(x)][0] for x in df.col_setting]
    df = df.set_index('col_setting').reset_index().sort_values('col_setting')
    
    df['reg_name']  = [label_mapping[invt_reg[x]] for x in df['region']]
    df['root_mean_squared_error'] = abs(df['root_mean_squared_error'] ) 
    gas=df[df['label']=='total_gas'].copy()  
    elec = df[df['label']=='total_elec'].copy()  
    gas_table = format_table_region(gas, 'Gas')
    elec_table = format_table_region(elec, 'Electricity')
    gas_table.merge(elec_table , on='Region').to_csv('./results/region_results.csv', index=False)
