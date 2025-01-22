import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def analyze_regional_sobol(base_path, target_var, N, colset, model_folder='sobol_results', grouped=False):
    """
    Analyze Sobol indices across different regions.
    """
    # Define regions
    regions = ['SE', 'LN', 'SW', 'EE', 'EM', 'YH', 'WM', 'NE', 'NW', 'WA']
    
    # Initialize DataFrames to store combined results
    s1_combined = []
    st_combined = []
    s2_combined = []
    
    # Process each region
    for region in regions:
        folder_path = os.path.join(
            base_path, 
            target_var,
            region,
            model_folder,
            f'colset_{colset}',
            'grouped' if grouped else 'ungrouped',
            f'N{N}'
            
        )
        
        # Read S1 results
        s1_path = os.path.join(folder_path, 'sobol_S1_results.csv')
        if os.path.exists(s1_path):
            s1_df = pd.read_csv(s1_path)
            s1_df['region'] = region
            s1_combined.append(s1_df)
        else:
            print(f"Warning: S1 results not found for region {region}")
            
        # Read ST results
        st_path = os.path.join(folder_path, 'sobol_ST_results.csv')
        if os.path.exists(st_path):
            st_df = pd.read_csv(st_path)
            st_df['region'] = region
            st_combined.append(st_df)
        else:
            print(f"Warning: ST results not found for region {region}")
        
        # Read S2 results
        s2_path = os.path.join(folder_path, 'sobol_S2_results.csv')
        if os.path.exists(s2_path):
            s2_df = pd.read_csv(s2_path)
            s2_df['region'] = region
            s2_combined.append(s2_df)
        else:
            print(f"Warning: S2 results not found for region {region}")
    
    # Combine results
    s1_all, st_all, s2_all = None, None , None 
    try:
        s1_all = pd.concat(s1_combined, ignore_index=True)
    except:
        None 
    try:
        st_all = pd.concat(st_combined, ignore_index=True)
    except:
        None

    # s2_all = pd.concat(s2_combined, ignore_index=True)
    
    return s1_all, st_all, s2_all

 

def plot_regional_s1_comparison(s1_df, output_path, n):
    """Plot comparison of S1 indices using mean values across regions."""
    plt.figure(figsize=(15, 10))
    
    # Calculate mean S1 and confidence intervals
    mean_s1 = s1_df.groupby('parameter')['S1'].mean().sort_values(ascending=False)
    mean_conf = s1_df.groupby('parameter')['S1_conf'].mean()
    
    # Create bar plot of mean S1 values
    plt.figure(figsize=(15, 8))
    bars = plt.bar(range(len(mean_s1)), mean_s1)
    
    # Add error bars using mean confidence intervals
    plt.errorbar(range(len(mean_s1)), mean_s1, yerr=mean_conf, 
                fmt='none', color='black', capsize=5)
    
    # Customize the plot
    plt.xticks(range(len(mean_s1)), mean_s1.index, rotation=45, ha='right')
    plt.ylabel('Mean First-Order Sobol Index')
    plt.title('Mean First-Order Sobol Indices Across Regions')
    
    # Add value labels on top of bars
    for i, bar in enumerate(bars):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.3f}±{mean_conf.iloc[i]:.3f}',
                ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_path, f'{n}_mean_s1_barplot.png'))
    plt.close()
    
    # Create heatmap of S1 indices by region
    pivot_s1 = s1_df.pivot(index='region', columns='parameter', values='S1')
    plt.figure(figsize=(15, 8))
    sns.heatmap(pivot_s1, annot=True, fmt='.3f', cmap='YlOrRd')
    plt.title('First-Order Sobol Indices by Region')
    plt.tight_layout()
    plt.savefig(os.path.join(output_path, f'{n}_regional_s1_heatmap.png'))
    plt.close()

    # Filter out the specified variable
    s1_df_filtered = s1_df[s1_df['parameter'] != 'Floor Area'] 
    # Create heatmap of S1 indices by region with filtered data
    pivot_s1 = s1_df_filtered.pivot(index='region', columns='parameter', values='S1')
    plt.figure(figsize=(15, 8))
    sns.heatmap(pivot_s1, annot=True, fmt='.3f', cmap='YlOrRd')
    plt.title('First-Order Sobol Indices by Region')
    plt.tight_layout()
    plt.savefig(os.path.join(output_path, f'{n}_regional_s1_heatmap_excl.png'))
    plt.close()



def plot_regional_st_comparison(st_df, output_path, n):
    """Plot comparison of ST indices using mean values across regions."""
    plt.figure(figsize=(15, 10))
    
    # Calculate mean ST and confidence intervals
    mean_st = st_df.groupby('parameter')['ST'].mean().sort_values(ascending=False)
    mean_conf = st_df.groupby('parameter')['ST_conf'].mean()
    
    # Create bar plot of mean ST values
    plt.figure(figsize=(15, 8))
    bars = plt.bar(range(len(mean_st)), mean_st)
    
    # Add error bars using mean confidence intervals
    plt.errorbar(range(len(mean_st)), mean_st, yerr=mean_conf, 
                fmt='none', color='black', capsize=5)
    
    # Customize the plot
    plt.xticks(range(len(mean_st)), mean_st.index, rotation=45, ha='right')
    plt.ylabel('Mean Total-Order Sobol Index')
    plt.title('Mean Total-Order Sobol Indices Across Regions')
    
    # Add value labels on top of bars
    for i, bar in enumerate(bars):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.3f}±{mean_conf.iloc[i]:.3f}',
                ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_path, f'{n}_mean_st_barplot.png'))
    plt.close()
    
    # Create heatmap of ST indices by region
    pivot_st = st_df.pivot(index='region', columns='parameter', values='ST')
    plt.figure(figsize=(15, 8))
    sns.heatmap(pivot_st, annot=True, fmt='.3f', cmap='YlOrRd')
    plt.title('Total-Order Sobol Indices by Region')
    plt.tight_layout()
    plt.savefig(os.path.join(output_path, f'{n}_regional_st_heatmap.png'))
    plt.close()

        # Filter out the specified variable
    st_df_filtered = st_df[st_df['parameter'] != 'Floor Area'] 
    # Create heatmap of S1 indices by region with filtered data
    pivot_st = st_df_filtered.pivot(index='region', columns='parameter', values='ST')
    plt.figure(figsize=(15, 8))
    sns.heatmap(pivot_st, annot=True, fmt='.3f', cmap='YlOrRd')
    plt.title('Total-Order Sobol Indices by Region')
    plt.tight_layout()
    plt.savefig(os.path.join(output_path, f'{n}_regional_st_heatmap_excl.png'))
    plt.close()



# Define parameters and mappings
PARAMETERS = [
    'all_res_total_fl_area_H_total',
    'Pre 1919_pct',
    'Standard size detached_pct',
    'postcode_area',
    'HDD_winter',
    'economic_activity_perc_Economically active (excluding full-time students): In employment: Employee: Full-time',
    'ethnic_group_perc_White: English, Welsh, Scottish, Northern Irish or British',
    'socio_class_perc_L1, L2 and L3: Higher managerial, administrative and professional occupations',
    'household_comp_perc_One-person household',
    'Domestic outbuilding_pct',
    '3-4 storey and smaller flats_pct'
]

PARAM_MAPPING = {
    'all_res_total_fl_area_H_total': 'Floor Area',
    'Pre 1919_pct': 'Pre-1919',
    'Standard size detached_pct': 'Detached Houses',
    'postcode_area': 'Postcode Area',
    'HDD_winter': 'Winter HDD',
    'economic_activity_perc_Economically active (excluding full-time students): In employment: Employee: Full-time': 'Full-time Employed',
    'ethnic_group_perc_White: English, Welsh, Scottish, Northern Irish or British': 'White British',
    'socio_class_perc_L1, L2 and L3: Higher managerial, administrative and professional occupations': 'Higher Managerial',
    'household_comp_perc_One-person household': 'Single Person HH',
    'Domestic outbuilding_pct': 'Outbuildings',
    '3-4 storey and smaller flats_pct': 'Small Flats'
}


def plot_joint_sobol_comparison(s1_df, st_df, output_path, n):
    """Create joint plot of S1 and ST indices with shared y-axis and consistent colors."""
    # Set up a darker color palette - using tableau colors for better visibility
    colors = ['#1f77b4',  # blue
            '#ff7f0e',   # orange
            '#2ca02c',   # green
            '#d62728',   # red
            '#9467bd',   # purple
            '#8c564b',   # brown
            '#e377c2',   # pink
            '#7f7f7f',   # gray
            '#bcbd22',   # olive
            '#17becf',   # cyan
            '#eb8b6a']   # salmon
        
    # Create color mapping for parameters
    all_params = sorted(set(s1_df['parameter'].unique()) | set(st_df['parameter'].unique()))
    color_dict = dict(zip(all_params, colors[:len(all_params)]))
    
    # Calculate means and confidence intervals
    mean_s1 = s1_df.groupby('parameter')['S1'].mean().sort_values(ascending=False)
    mean_s1_conf = s1_df.groupby('parameter')['S1_conf'].mean()
 
    mean_st = st_df.groupby('parameter')['ST'].mean().sort_values(ascending=False)
    mean_st_conf = st_df.groupby('parameter')['ST_conf'].mean()
 
    # Create figure with two subplots sharing y-axis
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 4), sharey=True)
    
    # Plot S1 indices
    bars_s1 = ax1.bar(range(len(mean_s1)), mean_s1)
    for i, bar in enumerate(bars_s1):
        bar.set_color(color_dict[mean_s1.index[i]])
        
    # Add error bars for S1
    ax1.errorbar(range(len(mean_s1)), mean_s1, yerr=mean_s1_conf,
                fmt='none', color='black', capsize=5)
    
    # Plot ST indices
    bars_st = ax2.bar(range(len(mean_st)), mean_st)
    for i, bar in enumerate(bars_st):
        bar.set_color(color_dict[mean_st.index[i]])
        
    # Add error bars for ST
    ax2.errorbar(range(len(mean_st)), mean_st, yerr=mean_st_conf,
                fmt='none', color='black', capsize=5)
    
    # Customize plots
    ax1.set_xticks(range(len(mean_s1)))
    ax1.set_xticklabels(mean_s1.index, rotation=45, ha='right')
    ax1.set_ylabel('Sobol Index')
    ax1.set_title('First-Order (S1) Indices')
    
    ax2.set_xticks(range(len(mean_st)))
    ax2.set_xticklabels(mean_st.index, rotation=45, ha='right')
    ax2.set_title('Total-Order (ST) Indices')
    
    # Add value labels - only means, no confidence intervals
    for ax, means in [(ax1, mean_s1), (ax2, mean_st)]:
        for i, mean in enumerate(means):
            ax.text(i, mean, f'{mean:.3f}',
                   ha='center', va='bottom')
    
    # Add overall title
    # plt.suptitle('Comparison of First-Order and Total-Order Sobol Indices', y=1.05)
    
    # Save figure
    plt.savefig(os.path.join(output_path, f'{n}_joint_sobol_comparison.png'),
                bbox_inches='tight', dpi=300)
    plt.close()
    return mean_s1, mean_s1_conf, mean_st, mean_st_conf
    
    

def analyse_sobol_single(BASE_PATH, TARGET_VAR, N, MODEL_FOLDER, COLSET):
    op = os.path.join(BASE_PATH, f'{TARGET_VAR}_regional_analysis')
    os.makedirs(op, exist_ok=True)
    s1_df, st_df, s2_df = analyze_regional_sobol(BASE_PATH, TARGET_VAR, N, model_folder=MODEL_FOLDER, colset=COLSET)
    s1_df['parameter'] = [PARAM_MAPPING[x] for x in s1_df['parameter']]
    st_df['parameter'] = [PARAM_MAPPING[x] for x in st_df['parameter']]
    plot_regional_s1_comparison(s1_df, op, N)
    plot_regional_st_comparison(st_df, op, N)
    m1, m1c, mt, mtc  = plot_joint_sobol_comparison(s1_df, st_df, op, N)
    pd.concat([m1, m1c, mt, mtc], axis=1) .reset_index().to_csv(os.path.join(op, f'{TARGET_VAR}_{N}_sobol.csv'), index=False)
        
