import sys
import os
from pathlib import Path
from typing import List, Tuple, Dict

from papersummary.base import BaseTextExtractor
from papersummary.pdf2txt import PDF2TextExtractor
from papersummary.pptx2txt import PPTX2TextExtractor
from papersummary.docx2txt import DOCX2TextExtractor

prompt = "Write a clear, concise, objective summary for the following document:"

TEXT_EXTRACTORS: list = [
    PDF2TextExtractor,
    PPTX2TextExtractor,
    DOCX2TextExtractor
]
converters: dict = {}
for extractor_class in TEXT_EXTRACTORS:
    
    extractor = extractor_class(
        default_prompt = prompt
    )

    for extension in extractor.supported_extensions:
        converters[extension] = extractor

SUPPORTED_FILETYPES: list = converters.keys()

def run(file_paths: List[str]) -> List[Tuple[bool, str]]:
    """Runs as the main entry point for the script."""

    print(f"Converting {len(file_paths)} files...")

    results = []
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
                success, msg = extractor(file = file)
                results.append((success, msg))
                break

    return results


        

    print("\nCopy everything in txt file, and paste into any AI Chat of your choice.")
    print("Note: The AI chat might not be able to handle very large files.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python papersummary.py <pdf_file1> <pdf_file2> ...")
        sys.exit(1)
    # Get a list of Path objects for each provided argument
    file_paths = [str(arg) for arg in sys.argv[1:]]
    run(file_paths)
