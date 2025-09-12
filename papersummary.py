import sys
import os
from pathlib import Path

from pdf2txt import convert_pdf_to_txt

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

    print("\nCopy everything in txt file, and paste into any AI Chat of your choice.")
    print("Note: The AI chat might not be able to handle very large files.")

if __name__ == "__main__":
    main()
