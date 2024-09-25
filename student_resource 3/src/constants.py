entity_unit_map = {
    'width': {'centimetre', 'foot', 'inch', 'metre', 'millimetre', 'yard'},
    'depth': {'centimetre', 'foot', 'inch', 'metre', 'millimetre', 'yard'},
    'height': {'centimetre', 'foot', 'inch', 'metre', 'millimetre', 'yard'},
    'item_weight': {'gram',
        'kilogram',
        'microgram',
        'milligram',
        'ounce',
        'pound',
        'ton'},
    'maximum_weight_recommendation': {'gram',
        'kilogram',
        'microgram',
        'milligram',
        'ounce',
        'pound',
        'ton'},
    'voltage': {'kilovolt', 'millivolt', 'volt'},
    'wattage': {'kilowatt', 'watt'},
    'item_volume': {'centilitre',
        'cubic foot',
        'cubic inch',
        'cup',
        'decilitre',
        'fluid ounce',
        'gallon',
        'imperial gallon',
        'litre',
        'microlitre',
        'millilitre',
        'pint',
        'quart'}
}

allowed_units = {unit for entity in entity_unit_map for unit in entity_unit_map[entity]}

import pandas as pd
import requests
from PIL import Image
from io import BytesIO
import pytesseract
import re
import time
import csv

# Define the entity unit map
entity_unit_map = {
    'width': {'centimetre', 'foot', 'inch', 'metre', 'millimetre', 'yard'},
    'depth': {'centimetre', 'foot', 'inch', 'metre', 'millimetre', 'yard'},
    'height': {'centimetre', 'foot', 'inch', 'metre', 'millimetre', 'yard'},
    'item_weight': {'gram', 'kilogram', 'microgram', 'milligram', 'ounce', 'pound', 'ton'},
    'maximum_weight_recommendation': {'gram', 'kilogram', 'microgram', 'milligram', 'ounce', 'pound', 'ton'},
    'voltage': {'kilovolt', 'millivolt', 'volt'},
    'wattage': {'kilowatt', 'watt'},
    'item_volume': {'centilitre', 'cubic foot', 'cubic inch', 'cup', 'decilitre', 'fluid ounce', 'gallon', 'imperial gallon', 'litre', 'microlitre', 'millilitre', 'pint', 'quart'}
}

# Function to clean extracted text (remove extra spaces)
def clean_text(text):
    return re.sub(r'\s+', ' ', text).strip()

# Function to extract numeric terms with one word after them
def extract_numeric_with_word(text):
    # Regex to match numbers (decimals/integers) followed by an optional space and then a word
    pattern = r'(\d+\.?\d*\s?\w+)'  
    matches = re.findall(pattern, text)
    return ' '.join(matches)

# Function to download image and extract relevant text using Tesseract
def extract_text_from_image(url):
    try:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        # Use Tesseract to extract text
        text = pytesseract.image_to_string(img)
        # Clean and extract numeric terms with one word after them
        extracted_text = extract_numeric_with_word(text)
        return clean_text(extracted_text)
    except Exception as e:
        return f"Error: {e}"

# Function to extract and replace abbreviated units from extracted_text
def extract_and_replace_abbreviated_units(extracted_text, entity_name, entity_unit_map):
    # Extract the set of possible units for the given entity_name
    unit_set = entity_unit_map.get(entity_name, set())
    
    # Define a mapping of common abbreviations to their full forms
    # Define a mapping of common abbreviations to their full forms
    abbreviation_to_full_unit = {
        'mg': 'milligram',
        'g': 'gram',
        'GSM': 'gram',
        'gm': 'gram',
        'kg': 'kilogram',
        'KG': 'kilogram',
        'Kg':'kilogram',
        'ug': 'microgram',
        'oz': 'ounce',
        'lb': 'pound',
        'cm':'centimetre',
        'm':'metre',
        'in':'inch',
        'ft':'foot',
        'grams':'gram',
        'LBS':'pound',
        'lbs':'pound',
        't': 'ton',
        'ml': 'millilitre',
        'mm': 'millimetre',
        'l': 'litre',
        'cl': 'centilitre',
        'kV': 'kilovolt',
        'mV': 'millivolt',
        'V': 'volt',
        'W': 'watt',
        'kW': 'kilowatt'
    }
    
    # Regular expression to extract numeric value and unit
    pattern = r'(\d+(\.\d+)?)(\s*|\b)(mg|gm|g|GSM|KG|kg|Kg|ug|oz|lb|cm|mm|in|ft|grams|LBS|lbs|t|m|ml|l|cl|kV|mV|V|W|kW)'
    
    match = re.search(pattern, extracted_text)
    
    if match:
        value = match[1]  # numeric value
        abbrev = match[4]  # unit abbreviation
        
        # Check if the abbreviation corresponds to one of the valid units for the entity
        full_unit = abbreviation_to_full_unit.get(abbrev)
        if full_unit and full_unit in unit_set:
            # Format the value with ".0" if it's a whole number
            if '.' not in value:
                value = f'{value}.0'
            # Return the numeric value and the full unit as "value unit"
            return f'{value} {full_unit}'
    
    # If no match found or no valid unit, return empty string
    return ''

# Start timing
start_time = time.time()

# Load the dataset (replace 'your_dataset.csv' with your actual file)
df = pd.read_csv('/kaggle/input/test-file/test.csv')

# # Limit to first 200 rows
# df = df.head(200)

# Create a new column for extracted text (numeric terms + one word)
extracted_texts = []
for i, link in enumerate(df['image_link']):
    extracted_texts.append(extract_text_from_image(link))
    
    # Print the time elapsed after every 100 rows
    if (i + 1) % 100 == 0:
        elapsed_time = time.time() - start_time
        print(f"Processed {i + 1} rows. Time elapsed: {elapsed_time:.2f} seconds.")

# Add the extracted text to the DataFrame
df['extracted_text'] = extracted_texts

# Save the updated dataset to a new CSV file
intermediate_csv = '/kaggle/working/updated_dataset_ONTEST_200.csv'
df.to_csv(intermediate_csv, index=False)

print("Text extraction complete. Intermediate dataset saved as 'updated_dataset_ONTEST_200.csv'.")

# Function to process the CSV file and keep only the index and updated_extracted_value columns
def process_csv(input_file, output_file, entity_unit_map):
    with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        rows = list(reader)  # Read all rows in advance
        
    with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        # Add a new column 'updated_extracted_value' to the existing columns
        fieldnames = ['index', 'prediction']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        
        # Process each row and update the extracted_text with the new value
        for index, row in enumerate(rows):
            entity_name = row['entity_name']
            extracted_text = row['extracted_text']
            
            # Replace units in extracted_text based on the entity_name
            updated_value = extract_and_replace_abbreviated_units(extracted_text, entity_name, entity_unit_map)
            
            # Add the updated value in the new column
            writer.writerow({'index': index, 'prediction': updated_value})

# Define input and output file paths
final_input_file = intermediate_csv  # Intermediate CSV file path
final_output_file = '/kaggle/working/updated_output_test_3.csv'  # Final output CSV file path

# Process the CSV and save the updated version with a new column
process_csv(final_input_file, final_output_file, entity_unit_map)

print(f"CSV processing complete. Final dataset saved as '{final_output_file}'.")
