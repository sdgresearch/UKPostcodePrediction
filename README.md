![Project Logo](images/logo.jpg)
# Machine Learning Methods for Domestic Energy Prediction for Small-Neighbourhoods at National Scales in England and Wales

## Overview

This repository contains the code to accompany the paper of the same name. An implementation of neighborhood energy modeling using the NEBULA dataset to predict domestic energy consumption at postcode level across England and Wales.

The NEBULA stock mmodel and associated papers can be found at https://github.com/sdgresearch/NebulaStockModel

Pre Print - coming soon.

## Installation & Setup

```bash
# Clone the repository
git clone https://github.com/sdgresearch/UKPostcodePrediction.git

# Navigate to the project directory
cd UKPostcodePrediction

conda create -n nebula --file requirements.txt -c pytorch -c conda-forge -c defaults
conda activate nebula
pip install SALib==1.5.1

```
We recomend user then installs the correct version of autogluon for their operating system; https://auto.gluon.ai/dev/install.html

## Project Structure

```
UKPostcodePrediction/
.
├── input_data/          # place Nebula stock model data here
├── results/             # Model outputs
│   ├── model_results/   # ML model predictions
│   ├── regional_results/# Regional analysis 
│   └── sobol_results/   # Sensitivity analysis  
├── src/                 # Core source code
└── scripts/
    ├── extract_ml_res.py  # method file
    ├── run_automl.py      # method file
    ├── run_experiments.py # Main ML pipeline
    └── run_gsa.py         # method file 
```

## Usage
To recreate the experiments, run all ML experiments, sobol analysis and collate results 

```python
python run_experiments.py

```

## Citation

# If you use this code in your research, please cite the accompanying paper:

Citation coming soon


## License

This work is licensed under a Creative Commons Attribution 4.0 International License:

Creative Commons Attribution 4.0 International (CC BY 4.0)

Copyright (c) 2025 Grace Colverd

This work is licensed under the Creative Commons Attribution 4.0 International License. 
To view a copy of this license, visit http://creativecommons.org/licenses/by/4.0/ or 
send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.

You are free to:
- Share: copy and redistribute the material in any medium or format
- Adapt: remix, transform, and build upon the material for any purpose, even commercially

Under the following terms:
- Attribution: You must give appropriate credit, provide a link to the license, and 
  indicate if changes were made. You may do so in any reasonable manner, but not in 
  any way that suggests the licensor endorses you or your use.

No additional restrictions — You may not apply legal terms or technological measures 
that legally restrict others from doing anything the license permits.



## Contact

Grace Colverd
- GitHub: @graceebc9
