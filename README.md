## Amazon ML Challenge 2024
- **Rank**: 263
- [View our rank on the leaderboard](https://unstop.com/hackathons/amazon-ml-challenge-amazon-1100713/coding-challenge/200089)



Problem Statement
The goal of this hackathon is to create a machine learning model that extracts entity values from images. This functionality is essential in fields like healthcare, e-commerce, and content moderation, where precise product information is crucial. As digital marketplaces grow, many products lack detailed textual descriptions, making it necessary to extract key details directly from images. These images may include product details such as weight, volume, voltage, wattage, dimensions, etc., which are critical for digital stores.

Dataset Description
The dataset contains the following columns:

index: A unique identifier (ID) for the data sample.
image_link: Public URL where the product image is available for download.
Example link: Product Image
Use the download_images function from src/utils.py to download images. Sample code can be found in src/test.ipynb.
group_id: Category code of the product.
entity_name: Product entity name (e.g., item_weight).
entity_value: Product entity value (e.g., 34 gram).
For test.csv, the entity_value column will not be present as it is the target variable.
Task
For the test dataset, predict the entity_value for each sample based on the image and entity information. The output should follow the format outlined in the Output Format section below.

Output Format
The output file must be a CSV containing two columns:

index: The unique identifier (ID) of the data sample (same as in the test file).
prediction: A string formatted as "x unit", where:
x is a float value in standard formatting.
unit is one of the allowed units (provided in the Appendix and src/constants.py).
Example Valid Predictions:
2 gram
12.5 centimetre
2.56 ounce
Example Invalid Predictions:
2 gms
60 ounce/1.7 kilogram
2.2e2 kilogram
Ensure to output a prediction for all indices. If no value can be found in the image for any test sample, return an empty string (i.e., ""). Mismatches in the number of predictions compared to the test file will result in errors.

Data Files
The dataset includes the following files:

dataset/train.csv: Training data with entity_value labels.
dataset/test.csv: Test data without entity_value labels. Use this file for generating predictions.
dataset/sample_test.csv: Sample test input file.
dataset/sample_test_out.csv: Sample output file for sample_test.csv. Format your submission to match this file exactly.
Source Files
The repository includes various helper scripts:

src/sanity.py: Sanity checker to ensure the final output file passes all formatting checks.
Note: The script does not check for mismatches in the number of predictions.
src/utils.py: Helper functions for downloading images from image_link.
src/constants.py: Contains the allowed units for each entity type.
sample_code.py: Sample dummy code for generating output files. Usage of this file is optional.
Constraints
You are provided with a sample output file and a sanity checker (src/sanity.py). Your output should:

Match the format of the sample output file exactly.
Pass through the sanity checker for validation.
The message "Parsing successful for file: ...csv" indicates the output is correctly formatted.
Evaluation Criteria
Submissions will be evaluated based on the F1 Score, a standard metric for classification problems. The predictions will be classified into four categories:

True Positives (TP): OUT != "" and GT != "" and OUT == GT
False Positives (FP):
OUT != "" and GT != "" and OUT != GT
OUT != "" and GT == ""
False Negatives (FN): OUT == "" and GT != ""
True Negatives (TN): OUT == "" and GT == ""
The F1 score is calculated as follows:

F1 Score
=
2
×
Precision
×
Recall
Precision
+
Recall
F1 Score= 
Precision+Recall
2×Precision×Recall
​
 
Where:

Precision = TP / (TP + FP)
Recall = TP / (TP + FN)
