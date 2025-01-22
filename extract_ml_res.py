import os
import ast
import pandas as pd
from src.model_post_process import process_main, process_region


folder = os.environ.get('FOLDER')
base_dir = f'./results/{folder}'

# Initialize an empty DataFrame to store results
results_df = pd.DataFrame()

# Iterate over subfolders in the base directory
for subdir in os.listdir(base_dir):
    subdir_path = os.path.join(base_dir, subdir)
    
    # Check if the subfolder is a directoryconda activate 
    if os.path.isdir(subdir_path):
        # Extracting variables from the subfolder name
        subdir_parts = subdir.split('__')
        if len(subdir_parts) < 5:
            print(f"Skipping directory: {subdir}. Insufficient parts found.")
            continue
        print(subdir_parts)
        column_setting = subdir_parts[4].split('_')[-1]
        train_subset_prop = subdir_parts[6].split('_')[-1]
        model_types = subdir_parts[7]
        model_quality = subdir_parts[5]
        time_limit = subdir_parts[3]
        label = subdir_parts[2]
        loc_type = subdir_parts[1]
        dataset_name =  subdir_parts[0]
        try:
            region =  subdir_parts[8]
        except:
            region = 'None'
        
        # Define the path to model_summary.txt
        summary_path = os.path.join(subdir_path, 'model_summary.txt')
        
        # Check if model_summary.txt exists
        if not os.path.exists(summary_path):
            print(f"Skipping directory: {subdir}. model_summary.txt not found.")
            continue
        
        # Read model_summary.txt into a DataFrame
        with open(summary_path, 'r') as f:
            data = f.read()
            # Convert the string representation of dictionary to a dictionary
            model_summary = ast.literal_eval(data)
            # Convert the dictionary to a DataFrame
            summary_df = pd.DataFrame(model_summary, index=[0])
            
        # Add columns for the extracted variables
        summary_df['col_setting'] = column_setting
        summary_df['train_subset'] = train_subset_prop
        summary_df['model_types'] = model_types
        summary_df['time_Limit'] = time_limit
        summary_df['model_qual'] = model_quality
        summary_df['label'] = label
        summary_df['loc_type'] = loc_type
        summary_df['dname'] = dataset_name
        summary_df['region'] = region
            
        # Append the DataFrame to the results_df
        results_df = pd.concat([results_df, summary_df], ignore_index=True)
print('processing results for ', folder)
print('results df is \n')
print(results_df.columns.tolist())

# Display the resulting DataFrame
if folder == 'regional_results':
    process_region(results_df)
else:
    process_main(results_df)
