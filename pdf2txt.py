"""
Simple utility function to convert a pdf file to a txt file
"""

import PyPDF2

def convert_pdf_to_txt(pdf_file, txt_file):
    """
    Convert a PDF file to a text file.

    Args:
        pdf_file (str): The path to the PDF file to read from.
        txt_file (str): The path to the text file to write to.

    Returns:
        None
    """
    # Check if the PDF file exists
    try:
        with open(pdf_file, 'rb') as file:
            pass
    except FileNotFoundError:
        print(f"Could not find the file: {pdf_file}")
        return

    # Extract text from the PDF
    with open(pdf_file, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""

        for page in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page].extract_text()

    # Write the text to the text file
    prompt = "summarize the following document:"
    with open(txt_file, 'w', encoding='utf-8') as file:
        file.write(prompt + "\n" + text)

    print(f"Converted: {pdf_file} to {txt_file}")