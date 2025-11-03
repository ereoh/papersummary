import sys
import os
from pathlib import Path
from typing import List

from papersummary.base import BaseTextExtractor
from papersummary.pdf2txt import PDF2TextExtractor
from papersummary.pptx2txt import PPTX2TextExtractor

prompt = "Write a clear, concise, objective summary for the following document:"

supported_filetypes = [
    PDF2TextExtractor,
    PPTX2TextExtractor
]

def run(file_paths: List[str | Path]) -> None:
    """Runs as the main entry point for the script."""

    print(f"Converting {len(file_paths)} PDF files...")

    converters = {}
    for extractor_class in supported_filetypes:
        
        extractor = extractor_class(
            default_prompt = prompt
        )

        for extension in extractor.supported_extensions:
            converters[extension] = extractor


    for file in file_paths:
        file = Path(file)
        if not file.is_file():
            print(f"Error: {file} does not exist. Skipping...")
            continue

        # generate_prompt(pdf_file=file, prompt=prompt)
        filetype = file.suffix

        if filetype not in converters.keys():
            print(f"Error: {file} - {filetype} not supported. Skipping...")
            continue

        for extension,extractor in converters.items():
            if filetype == extension:
                extractor(
                    file = file,
                )
                break


        

    print("\nCopy everything in txt file, and paste into any AI Chat of your choice.")
    print("Note: The AI chat might not be able to handle very large files.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python papersummary.py <pdf_file1> <pdf_file2> ...")
        sys.exit(1)
    # Get a list of Path objects for each provided argument
    file_paths = [Path(arg) for arg in sys.argv[1:]]
    run(file_paths)
