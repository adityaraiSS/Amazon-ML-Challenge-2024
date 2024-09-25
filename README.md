# Amazon ML Challenge 2024
- **Rank**: 263
- [View our rank on the leaderboard](https://unstop.com/hackathons/amazon-ml-challenge-amazon-1100713/coding-challenge/200089)



# Problem Statement
The objective of this project is to build a machine learning model capable of extracting entity values from images. This functionality is vital in fields such as healthcare, e-commerce, and content moderation, where precise product information is critical. As digital marketplaces expand, many products lack detailed textual descriptions, making it necessary to extract essential details directly from images. These details include product specifications like weight, volume, voltage, wattage, dimensions, and more, which are crucial for digital stores.

# Dataset Description
The dataset consists of the following columns:

* index: A unique identifier (ID) for the data sample.
* image_link: Public URL for downloading the product image.
  * Example link: Product Image
  * You can use the download_images function from src/utils.py to download the images. Sample code is provided in src/test.ipynb.
* group_id: The category code of the product.
* entity_name: The product's entity name (e.g., item_weight).
* entity_value: The value of the entity (e.g., 34 gram).
  * In the test.csv file, the entity_value column is not available as it is the target variable to predict.
  
# Task
For the test dataset, the task is to predict the entity_value for each sample using the product images and entity information. The output must follow the specified format provided in the Output Format section.

# Output Format
The output file must be a CSV with the following columns:

* index: The unique identifier (ID) for each test sample.
* prediction: A string in the format "x unit", where:
  * x is a floating-point number (properly formatted).
  * unit is one of the allowed units (defined in src/constants.py and in the Appendix).

Ensure to generate predictions for all indices. If no value is found in the image for a test sample, return an empty string (""). Mismatches in the number of predictions compared to the test file will result in an error.

# Files
## Dataset Files:
* dataset/train.csv: Training file with entity_value labels.
* dataset/test.csv: Test file without the entity_value labels. You will generate predictions for this file.
* dataset/sample_test.csv: Sample input test file.
* dataset/sample_test_out.csv: Sample output file for sample_test.csv. Your output should follow this format exactly.
  
# Source Files:
* src/sanity.py: A sanity checker to ensure the final output file passes all formatting checks.
  * Note: This script doesn't verify if the number of predictions matches the test file.
* src/utils.py: Contains helper functions for downloading images from the image_link.
* src/constants.py: Contains the allowed units for each entity type.
* sample_code.py: A sample code for generating a dummy output file (optional).
  
# Constraints
You are provided with a sample output file (sample_test_out.csv) and a sanity checker (src/sanity.py). Your output file should:

* Match the exact format of sample_test_out.csv.
* Pass through the sanity checker for validation.
  * If successful, you will receive a message like: Parsing successful for file: ...csv.

# Evaluation Criteria
The model's performance will be evaluated based on the F1 score, a standard measure for classification problems. Predictions will be classified into the following categories:

* True Positives (TP): OUT != "" and GT != "" and OUT == GT
* False Positives (FP):
  * OUT != "" and GT != "" and OUT != GT
  * OUT != "" and GT == ""
* False Negatives (FN): OUT == "" and GT != ""
