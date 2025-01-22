import os
import subprocess

def set_environment_vars(vars_dict):
    os.environ.update(vars_dict)

def run_python_script(script_name):
    subprocess.run(['python', script_name])

def run_model_experiments():
    base_config = {
        'OUTPUT_PATH': './results/model_results',
        'DATA_PATH': './input_data/NEBULA_englandwales_domestic_filtered.csv',
        'MODEL_PRESET': 'best_quality',
        'TIME_LIM': '15000',
        'TRAIN_SUBSET_PROP': '1',
        'MODEL_TYPES': 'all',
        'RUN_REGIONAL': 'No',
        'run_census': 'No'
    }
    set_environment_vars(base_config)

    for target in ['totalelec', 'totalgas']:
        for col_setting in [18, 39, 42, 43, 52]:
            set_environment_vars({
                'COL_SETTING': str(col_setting),
                'TARGET': target
            })
            run_python_script('run_automl.py')

def run_regional_experiments():
    regional_config = {
        'OUTPUT_PATH': './results/regional_results',
        'DATA_PATH': './input_data/NEBULA_englandwales_domestic_filtered.csv',
        'MODEL_PRESET': 'best_quality',
        'TIME_LIM': '15000',
        'TRAIN_SUBSET_PROP': '1',
        'MODEL_TYPES': 'all',
        'COL_SETTING': '52',
        'RUN_REGIONAL': 'Yes',
        'run_census': 'No'
    }
    set_environment_vars(regional_config)

    regions = ['EE', 'WA', 'SE', 'NW', 'YH', 'WM', 'LN', 'NE', 'SW', 'EM']
    for target in ['totalelec', 'totalgas']:
        for region in regions:
            set_environment_vars({
                'REGION_ID': region,
                'TARGET': target
            })
            run_python_script('run_automl.py')

def extract_results():
    for folder in ['model_results', 'regional_results']:
        set_environment_vars({'FOLDER': folder})
        run_python_script('extract_ml_res.py')

def run_sobol_experiments():
    sobol_config = {
        'COL_SETTING': '52',
        'GROUPED': 'False',
        'N': '65536'
    }
    set_environment_vars(sobol_config)

    for label in ['total_elec', 'total_gas']:
        set_environment_vars({'LABEL': label})
        run_python_script('run_gsa.py')

def main():
    base_dir = 'results'
    subdirs = ['model_results', 'regional_results']

    os.makedirs(base_dir, exist_ok=True)
    for subdir in subdirs:
        os.makedirs(os.path.join(base_dir, subdir), exist_ok=True)

    print('Starting experiments...')
    run_model_experiments()
    
    print('Starting region experiments')
    run_regional_experiments()
    
    print("Extracting ML results")
    extract_results()
    
    print("Starting Sobol experiments")
    run_sobol_experiments()

if __name__ == '__main__':
    main()