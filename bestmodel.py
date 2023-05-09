# Import necessary libraries
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import ElasticNetCV
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline, make_union
from tpot.builtins import StackingEstimator
from sklearn.impute import SimpleImputer
from tpot.export_utils import set_param_recursive
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# Load dataset
tpot_data = pd.read_excel('C:/Users/ASUS/Desktop/AI Test/Auto-GPT-0.2.2/auto_gpt_workspace/dataset for students.xlsx')

# Preprocess the dataset
tpot_data = pd.get_dummies(tpot_data)  # Convert non-numeric columns to numeric using one-hot encoding
tpot_data = tpot_data.dropna()  # Remove rows with missing values

# Perform feature engineering
features = tpot_data.drop('median_house_value', axis=1)
training_features, testing_features, training_target, testing_target = \
    train_test_split(features, tpot_data['median_house_value'], random_state=42)

imputer = SimpleImputer(strategy="median")
imputer.fit(training_features)
training_features = imputer.transform(training_features)
testing_features = imputer.transform(testing_features)

# Create the pipeline
exported_pipeline = make_pipeline(
    StackingEstimator(estimator=ElasticNetCV(l1_ratio=0.7000000000000001, tol=0.01)),
    RandomForestRegressor(bootstrap=True, max_features=0.55, min_samples_leaf=2, min_samples_split=4, n_estimators=100)
)

# Fix random state for all the steps in exported pipeline
set_param_recursive(exported_pipeline.steps, 'random_state', 42)

# Fit the pipeline and predict
exported_pipeline.fit(training_features, training_target)
results = exported_pipeline.predict(testing_features)

# Print the results
print("Predicted results:", results)

# Calculate mean squared error, Root Mean Squared Error, Mean Absolute Error
mse = mean_squared_error(testing_target, results)
rmse = np.sqrt(mse)
mae = mean_absolute_error(testing_target, results)
print("Mean Squared Error:", mse)
print("Root Mean Squared Error:", rmse)
print("Mean Absolute Error:", mae)

# Calculate R-squared for the train dataset
train_r2 = r2_score(training_target, exported_pipeline.predict(training_features))
print("R-squared for the train dataset:", train_r2)

# Calculate R-squared for the test dataset
test_r2 = r2_score(testing_target, results)
print("R-squared for the test dataset:", test_r2)


new_instance = pd.DataFrame({
    'longitude': [-122.23],
    'latitude': [37.88],
    'housing_median_age': [41.0],
    'total_rooms': [880.0],
    'total_bedrooms': [129.0],
    'population': [322.0],
    'households': [126.0],
    'median_income': [8.3252],
    'ocean_proximity_<1H OCEAN': [0],
    'ocean_proximity_INLAND': [1],
    'ocean_proximity_ISLAND': [0],
    'ocean_proximity_NEAR BAY': [0],
    'ocean_proximity_NEAR OCEAN': [0]
})

new_instance_imputed = imputer.transform(new_instance)

predicted_median_house_price = exported_pipeline.predict(new_instance_imputed)
print("Predicted Median House Price:", predicted_median_house_price[0])