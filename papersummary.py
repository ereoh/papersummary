import sys
import os
from pathlib import Path

from pdf2txt import generate_prompt

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

        generate_prompt(pdf_file=pdf_path, prompt=prompt)

        

    print("\nCopy everything in txt file, and paste into any AI Chat of your choice.")
    print("Note: The AI chat might not be able to handle very large files.")

if __name__ == "__main__":
    main()
