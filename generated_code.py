# Import necessary libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tpot import TPOTClassifier, TPOTRegressor
from sklearn.metrics import accuracy_score, mean_squared_error

# Goal 1: Load dataset and preprocess the dataset
dataset_path = r'C:\Users\ASUS\Desktop\AI Test\Auto-GPT-0.2.2\auto_gpt_workspace\dataset for students.xlsx'
df = pd.read_excel(dataset_path)

# Goal 2: Analyze if it's a classification or regression problem
# Assuming the target column is 'median_house_value'
target_col = 'median_house_value'
if len(df[target_col].unique()) / len(df) < 0.05:
    problem_type = 'classification'
else:
    problem_type = 'regression'

# Goal 3: Convert non-numeric columns to numeric
for col in df.columns:
    if df[col].dtype == 'object':
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])

# Goal 4: Split the preprocessed data into training and testing sets
X = df.drop(target_col, axis=1)
y = df[target_col]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Goal 5: Use AutoML library (TPOT) to find the best model
if problem_type == 'classification':
    tpot = TPOTClassifier(generations=5, population_size=50, verbosity=2, random_state=42)
else:
    tpot = TPOTRegressor(generations=5, population_size=50, verbosity=2, random_state=42)

tpot.fit(X_train, y_train)

# Goal 6: Evaluate the best model's performance on the testing set
y_pred = tpot.predict(X_test)

if problem_type == 'classification':
    print("Accuracy:", accuracy_score(y_test, y_pred))
else:
    print("Mean Squared Error:", mean_squared_error(y_test, y_pred))

# Goal 7: Get the best model python file as bestmodel.py for prediction on new data
tpot.export('bestmodel.py')