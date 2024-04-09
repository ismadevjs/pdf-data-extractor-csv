import os
import fitz
import csv
import random
import string
import re
from datetime import datetime
import pycountry
import locale

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    pdf_text = ''

    for page_number in range(doc.page_count):
        page = doc[page_number]
        pdf_text += page.get_text()
    return pdf_text

def add_items_to_csv(file_path, data):
    with open(file_path, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data.keys())

        if file.tell() == 0:
            writer.writeheader()

        writer.writerow(data)

def get_value_for_line_number(pdf_text, line_number):
    lines = pdf_text.split('\n')
    if lines and line_number is not None and 1 <= line_number <= len(lines):
        return lines[line_number - 1].strip()
    else:
        return None

    
def find_enregistrement_in_text(pdf_text):
       # Use regular expression to find lines matching the specified pattern
    pattern = re.compile(r'\b\d{7}\s[A-Z]\b')  # Assumes 7 digits followed by a space and an uppercase letter
    values = re.findall(pattern, pdf_text)

    # Format the matched values into a readable string
    result_str = ', '.join(values)

    return result_str


def extract_dates_from_text(text):
    # Use a regular expression to find dates in the format "DD MM YYYY"
    pattern = re.compile(r'\b(\d{1,2})\n(\d{1,2})\n(\d{4})\b')

    matches = re.findall(pattern, text)

    # Format each match as a string
    date_strings = [f"{day}-{month}-{year}" for day, month, year in matches]

    result_str = ', '.join(date_strings)

    return result_str


def find_currencies_in_text(text):
    # Use a regular expression to find currency symbols or codes in the text
    pattern = re.compile(r'\b(?:[A-Z]{3}|[£€$¥₹₽]|(?:USD|EUR|GBP|JPY|CAD|AUD))\s*[,\d]+\.*\d*\b')
    # This pattern captures currency codes (e.g., USD, EUR, GBP, JPY, CAD, AUD),
    # and currency symbols (e.g., $, €, £, ¥, ₹, ₽).

    currencies = re.findall(pattern, text)

    # Format each match as a string without the list
    matches_str = ', '.join(match.replace('\n', '') for match in currencies)

    return matches_str

def find_currency_and_amount_in_text(text):
    # Use a regular expression to find currency and amounts in the text
    pattern = re.compile(r'\b(?:[A-Z]{3}|[£€$¥₹₽])\s*(?:\d{1,3}(?:[ ,]\d{3})*|\d+)\.000\b')

    # This pattern captures currency codes (e.g., USD, EUR, GBP, JPY, CAD, AUD),
    # and currency symbols (e.g., $, €, £, ¥, ₹, ₽), along with amounts that end with '.000'

    matches = re.findall(pattern, text)


    return matches

def extract_six_digit_numbers(text):
    # Use a regular expression to find six-digit numbers followed by a newline
    pattern = re.compile(r'\b(\n\d{6})\n\b')

    matches = re.findall(pattern, text)

    # Join the matched six-digit numbers into a single string
    six_digit_numbers_str = ''.join(matches)

    return six_digit_numbers_str

def extract_line_numbers_with_keyword(pdf_text, keyword):
    # Split the text into lines
    lines = pdf_text.split('\n')

    # Find line numbers containing the keyword
    line_numbers = [i + 1 for i, line in enumerate(lines) if keyword in line]

    return line_numbers


def print_line_numbers_with_currencies(text):
    # Split the text into lines
    lines = text.split('\n')

    # Define a list of common currency codes
    common_currency_list = [
        'USD', 'EUR', 'GBP', 'JPY', 'CAD', 'AUD', 'CNY', 'INR', 'BRL', 'RUB', 'MXN',
        'ZAR', 'TRY', 'AED', 'CHF', 'SEK', 'NZD', 'NOK', 'DKK', 'SGD', 'HKD', 'DZD'
        # Add more currencies as needed
    ]

    # Create a regular expression pattern for currency names
    currency_pattern = re.compile(r'\b(?:' + '|'.join(common_currency_list) + r')\b')

    for line_number, line in enumerate(lines, start=1):
        # Find currency matches in the line
        currency_matches = re.findall(currency_pattern, line)

        if currency_matches:
            # Print the line number and detected currency names
            return line_number


def convert_readable_string(input_str):
    # Remove brackets, quotes, and spaces
    cleaned_str = input_str.replace("[", "").replace("]", "").replace("'", "").strip()

    # Replace '\n' with newline character
    cleaned_str = cleaned_str.replace("\\n", "\n")

    return cleaned_str

def detect_and_print_address(text):
    # Define a regular expression for addresses
    address_pattern = re.compile(r'\b\d{1,5}\s*[\w\s]+,\s*[\w\s]+,\s*[\w\s]+\b')

    # Try to find an address
    address_match = address_pattern.search(text)
    if address_match:
        print("Address:", address_match.group())
    else:
        print("No address found in the given text.")

def detect_countries(text):
    # Get a set of all country names
    all_countries = {country.name for country in pycountry.countries}

    # Convert the text to uppercase for case-insensitive matching
    text_upper = text.upper()

    detected_countries = []

    # Check for each country in the set
    for country in all_countries:
        if country.upper() in text_upper:
            detected_countries.append(country)

    return ', '.join(detected_countries)

def detect_pattern(text):
    pattern = re.compile(r'\b\d{2}\|\d+\|\d+-\d+\|[A-Z]+\b')
    matches = [text.count('\n', 0, match.start()) + 1 for match in re.finditer(pattern, text)]
    return int(matches[0]) if matches else 0


def remove_last_four_digits(number):
    if len(number) > 4:
        return number[:-4]
    return ""


def clean_and_format_value(value):
    # Replace dots with commas and remove white spaces
    cleaned_value = value.replace('.', ',').replace(' ', '')
    return cleaned_value

def check_address_or_country(text):
    # Regular expression for detecting addresses
    address_pattern = re.compile(r'\b\d{1,5}\s*[\w\s]+,\s*[\w\s]+,\s*[\w\s]+\b')

    # Regular expression for detecting countries
    country_pattern = re.compile(r'\b' + '|'.join([country.name for country in pycountry.countries]) + r'\b', flags=re.IGNORECASE)

    # Check for address
    address_match = address_pattern.search(text)
    if address_match:
        address_line_numbers = extract_line_numbers_with_keyword(text, address_match.group())
        if address_line_numbers:
            print("Address found:", address_line_numbers[0])
            return address_line_numbers[0]
        else:
            print("No line numbers found for the address.")
            return None

    # Check for country
    country_match = country_pattern.search(text)
    if country_match:
        country_line_numbers = extract_line_numbers_with_keyword(text, country_match.group())
        if country_line_numbers:
            print("Country found:", country_line_numbers[0])
            return country_line_numbers[0]
        else:
            print("No line numbers found for the country.")
            return None

    # No address or country found
    print("No address or country found in the given text.")
    return None

def detect_line_number(text_file_path, searched_text):
    with open(text_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for i, line in enumerate(lines, start=1):
        if searched_text in line:
            return i

    return None


def scan_and_compile_pdfs():
    folder_to_scan = input("Enter the folder path to scan for PDFs: ")
    output_folder = input("Enter the output folder path for the CSV file: ")

    csv_file_name = ''.join(random.choices(string.ascii_letters + string.digits, k=8)) + '.csv'
    csv_file_path = os.path.join(output_folder, csv_file_name)

    for root, _, files in os.walk(folder_to_scan):
        for file in files:
            if file.lower().endswith('.pdf'):
                pdf_file_path = os.path.join(root, file)
                pdf_text = extract_text_from_pdf(pdf_file_path)
                enregistrement_line_numbers = extract_line_numbers_with_keyword(pdf_text, find_enregistrement_in_text(pdf_text))
                enregistrement_value = get_value_for_line_number(pdf_text, int(enregistrement_line_numbers[0])) if enregistrement_line_numbers else None
                
                note_line_numbers = extract_line_numbers_with_keyword(pdf_text, 'NOTE')
                note_value = get_value_for_line_number(pdf_text, note_line_numbers[0])  if note_line_numbers else None
                currency_line_number = print_line_numbers_with_currencies(pdf_text)


                sample_data = {
                    'id': file.lower(),
                    'Exportateur / Expéditeur': get_value_for_line_number(pdf_text, 18),
                    'Payé': get_value_for_line_number(pdf_text, 32),
                    'DECLARATION': get_value_for_line_number(pdf_text, 17),
                    'Importateur / Destinataire': get_value_for_line_number(pdf_text, 25),
                    'Address': get_value_for_line_number(pdf_text, 26),
                    'order de lart': get_value_for_line_number(pdf_text, extract_line_numbers_with_keyword(pdf_text, 'Franchise')[0] - 3) + get_value_for_line_number(pdf_text, extract_line_numbers_with_keyword(pdf_text, 'Franchise')[0] - 2),
                    'ENREGISTREMENT': enregistrement_value,
                    'Date d\'arrivée': extract_dates_from_text(pdf_text),
                    'Déclarant': get_value_for_line_number(pdf_text, 25),
                    'Localisation des marchandises': extract_six_digit_numbers(pdf_text),
                    'Colis et désignation des marchandise': get_value_for_line_number(pdf_text, extract_line_numbers_with_keyword(pdf_text, 'Franchise')[0]),
                    'CONTENEUR': get_value_for_line_number(pdf_text, int(extract_line_numbers_with_keyword(pdf_text, 'Franchise')[0] + 1)),
                    'Pays de provenance': get_value_for_line_number(pdf_text, 32),
                    'Pays d\'origine': get_value_for_line_number(pdf_text, 34),
                    'Pays destination': "here comes the country",
                    'Currency': get_value_for_line_number(pdf_text, print_line_numbers_with_currencies(pdf_text)),
                    'monnaie et montant total facturé': remove_last_four_digits(clean_and_format_value(get_value_for_line_number(pdf_text, int(currency_line_number) + 1) if currency_line_number is not None else "")),
                    'Note': note_value,
                }

                add_items_to_csv(csv_file_path, sample_data)

    print(f"CSV file '{csv_file_path}' created successfully.")

# Run the script
scan_and_compile_pdfs()
