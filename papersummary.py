import sys
import os
from pathlib import Path

from pdf2txt import convert_pdf_to_txt

prompt = "Write a clear, concise, objective summary for the following document:"

def main():
    """Runs as the main entry point for the script."""
    if len(sys.argv) < 2:
        print("Usage: python papersummary.py <pdf_file1> <pdf_file2> ...")
        sys.exit(1)

    # Get a list of Path objects for each provided argument
    pdf_paths = [Path(arg) for arg in sys.argv[1:]]

    print(f"Converting {len(pdf_paths)} PDF files...")

    for pdf_path in pdf_paths:
        if not pdf_path.is_file():
            print(f"Error: {pdf_path} does not exist. Skipping...")
            continue

        # Convert the PDF to a TXT file
        txt_path = pdf_path.with_suffix(".txt")
        convert_pdf_to_txt(pdf_path, txt_path)

        # add prompt to top of file
        with open(txt_path, 'r') as file:
            contents = file.read()

        with open(txt_path, 'w') as file:
            file.write(prompt + '\n' + contents)

    print("\nCopy everything in txt file, and paste into any AI Chat of your choice.")
    print("Note: The AI chat might not be able to handle very large files.")

if __name__ == "__main__":
    main()
