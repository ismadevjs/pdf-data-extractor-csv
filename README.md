# pdf-data-extractor-csv

The "PDF Data Extractor and Compiler" script is a utility tool designed to scan a specified folder for PDF files, extract relevant information from these PDFs, and compile the extracted data into a CSV (Comma Separated Values) file. The script utilizes various functionalities such as text extraction from PDFs, text pattern recognition using regular expressions, and data parsing to accomplish this task.

Features:
PDF Text Extraction:

Extracts text content from PDF files using the fitz library.
Data Extraction from Text:

Enregistrement Identification: Finds and retrieves specific identification numbers.
Date Extraction: Extracts dates in the format "DD MM YYYY" from the text.
Currency Extraction: Identifies and extracts currency codes or symbols and their corresponding amounts from the text.
Address Detection: Detects and prints addresses from the text.
Country Detection: Identifies countries mentioned in the text.
Line Number Identification: Finds line numbers containing specific keywords.
Data Compilation and CSV Creation:

Compiles the extracted data into a structured dictionary.
Creates or appends the compiled data to a CSV file with specified field names.
Utility Functions:

Random CSV File Generation: Generates a random CSV file name for the output.
String Cleaning and Formatting: Cleans and formats the extracted string values for better readability.
Line Number Detection in Text Files: Identifies the line number in a text file where a specific text is found.
