import pandas as pd 
import openai
import subprocess
import sys

openai.api_key = "Your API KEY"

# Load your data file
file = input("Load your CSV/Excel file: ")

try:
    if file.endswith('.csv'):
        data = pd.read_csv(file)
    elif file.endswith('.xlsx') or file.endswith('.xls'):
        data = pd.read_excel(file)
    else:
        print("Invalid file format. Please provide a CSV or Excel file.")
        sys.exit(1)
except FileNotFoundError:
    print(f"File '{file}' not found. Please check the file name and try again.")
    sys.exit(1)

target = input("Enter target value: ")    

prompt_code = (
        f"Goal 1: load dataset from {file} and preprocess the dataset and perform feature engineering.\n"
        f"Goal 2: Analyze the data if it's a classification problem or Regression problem.\n"
        f"Goal 3: Check if there is any non-numeric column, if there is any use pd.get_dummies()\n"
        f"Goal 4: split the preprocessed data into training and testing sets and use target column as {target}.\n"
        f"Goal 5: use an AutoML library (e.g.TPOT) to find the best model for our problem.\n"
        f"Goal 6: evaluate the best model's performance on the testing set.\n"
        f"Goal 7: Get the best model python file as bestmodel.py for prediction on new data\n"
               
)

messages_code = [
    {"role": "system", "content": "You are a 'AutoML Expert' to help us throughout the entire AutoML process. This role would involve:1. Understanding the dataset,2. Preprocessing and feature engineering,3. Model selection and hyperparameter tuning,4. Evaluation and interpretation,5. Deployment and monitoring. By taking on this role, you can provide valuable guidance and expertise throughout the AutoML process, ensuring that you make informed decisions and obtain the best possible results from the models you build. Use '#' before every line except the python code.\n"},
    {"role": "user", "content": prompt_code}
]

response_code = openai.ChatCompletion.create(
    model="gpt-4-0314",
    messages=messages_code,
    n=1,
    stop=None,
    temperature=0.5,
)

# Extract the generated code
generated_code = response_code['choices'][0]['message']['content']


# Save the generated code to a file
generated_code_file = "generated_code.py"
with open(generated_code_file, "w") as output_file:
    output_file.write(generated_code)

print("Generated code saved in 'generated_code.py'")

# Execute the generated code
print("\nExecuting the generated code...\n")


subprocess.run([sys.executable, generated_code_file])

# Break the connection
openai.api_key = None

# Reconnect with OpenAI
openai.api_key = "Your API KEY"

file = input("Load your CSV/Excel file: ")

# try:
#     if file.endswith('.csv'):
#         data = pd.read_csv(file)
#     elif file.endswith('.xlsx') or file.endswith('.xls'):
#         data = pd.read_excel(file)
#     else:
#         print("Invalid file format. Please provide a CSV or Excel file.")
#         sys.exit(1)
# except FileNotFoundError:
#     print(f"File '{file}' not found. Please check the file name and try again.")
#     sys.exit(1)

with open('bestmodel.py', 'r') as f:
    model_code = f.read()

target_column = input("Enter Target Value: ")    
  

prompt_update =(
    f"Read {model_code} file and update the code according to below info.\n"
    f"load dataset {file} and preprocess the dataset and perform feature engineering.\n"
    f"check for null or missing values if there is any either take average or remove them.\n"
    f"Check if there is any non-numeric column, if there is any use pd.get_dummies() \n"
    f"update target Value as {target_column}.\n"
    f"print the results\n"
    f"find mean squared error , Root Mean Squared Error, Mean Absolute Error and print them.\n"
    f"Calculate R-squared for the train dataset and Calculate R-squared for the test dataset\n"
)   

messages_update = [
    {"role": "system", "content": "You are a Python programmer.Use '#' before every line except the python code.\n"},
    {"role": "user", "content": prompt_update}
]

response_code = openai.ChatCompletion.create(
    model="gpt-4-0314",
    messages=messages_update,
    n=1,
    stop=None,
    temperature=0.5,
)

# Extract the generated code
generated_update = response_code['choices'][0]['message']['content']

# Save the updated code to the bestmodel.py file
with open('bestmodel.py', 'w') as f:
    f.write(generated_update)

# Execute the updated code
subprocess.run([sys.executable, 'bestmodel.py'])