# AutoML with TPOT and GPT-4

In this project, we are using AutoML with TPOT and GPT-4 to find the best machine learning model for our dataset.The project is implemented using Python 3.8.16 in a Conda environment.

## Project Overview

The project consists of an `automl.py` file, which performs two main tasks:

### 1. Generate and find the best model

- The `automl.py` file creates a `generated_code.py` file to search for the best model for our dataset.
- The search process continues until the best model is found, after which a new Python file, `bestmodel.py`, is generated with the optimal model for our dataset.

### 2. Train, test, and predict with the best model

- After obtaining the `bestmodel.py` file, the `automl.py` script automatically updates some parts of its code to incorporate the best model.
- The updated `bestmodel.py` script is then ready to train and test on our dataset, providing us with the results.
- Finally, we can use the best model to make predictions on new data.

By using the combination of TPOT and GPT-4, we can efficiently find the most suitable model for our dataset and streamline the machine learning process.
