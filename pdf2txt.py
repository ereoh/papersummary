"""
Simple utility function to convert a pdf file to a txt file
"""

import PyPDF2
from pathlib import Path

from typing import Tuple

def generate_prompt(
        pdf_file: str, 
        prompt: str = "Write a clear, concise, objective summary for the following document:", 
        txt_file: str = None
    ) -> Tuple[bool, str]:
    pdf_file = Path(pdf_file)
    # Check if the PDF file exists
    try:
        print(pdf_file)
        with open(pdf_file, 'rb') as file:
            pass
    except FileNotFoundError:
        print(f"Error: Could not find the file: {pdf_file}")
        return False, f"Error: Could not find the file: {pdf_file}"
    
    # create txt filepath
    txt_file = pdf_file.with_suffix(".txt") if txt_file is None else txt_file
    try:
        convert_pdf_to_txt(pdf_file, txt_file)

        add_prompt_txt(txt_file, prompt)
    except:
        return False, f"Error: Could not convert pdf to txt: {pdf_file}, {txt_file}"

    return True, txt_file

def add_prompt_txt(txt_file: str, prompt: str):
    # add prompt to top of file
    with open(txt_file, 'r') as file:
        contents = file.read()

    with open(txt_file, 'w') as file:
        file.write(prompt + '\n' + contents)

def convert_pdf_to_txt(pdf_file: str, txt_file: str):
    """
    Convert a PDF file to a text file.

    Args:
        pdf_file (str): The path to the PDF file to read from.
        txt_file (str): The path to the text file to write to.

    Returns:
        None
    """

    # Extract text from the PDF
    with open(pdf_file, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""

        for page in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page].extract_text()

    # Split text into half for validation
    total_length = len(text)
    half_length = total_length // 2
    first_half = text[:half_length]
    latter_half = text[half_length:]

    # Check if "references" is in the latter half of the file.
    if "references" in latter_half.lower():
        # Find the position of the word "references" in the full text, ignoring case
        index = text.lower().index("references")
        # Ensure it's in the latter half
        if index > half_length:
            text = text[:index]
        else:
            print("\tThe word 'References' is within the first half. Writing the entire text.")
    else:
        print("\tThe word 'References' was not found in the latter half of the document. Writing the entire text.")


    # Write the text to the txt file
    with open(txt_file, 'w', encoding='utf-8') as file:
        file.write(text)

    print(f"Converted: {pdf_file} to {txt_file}")

    return txt_file