"""Core papersummary
"""
import sys
from pathlib import Path
from typing import List, Tuple

import pyperclip

from papersummary.extractors import (
    PDF2TextExtractor,
    PPTX2TextExtractor,
    DOCX2TextExtractor,
)
from papersummary.utils import DEFAULT_PROMPT

TEXT_EXTRACTORS: list = [PDF2TextExtractor, PPTX2TextExtractor, DOCX2TextExtractor]
converters: dict = {}
for extractor_class in TEXT_EXTRACTORS:

    ext = extractor_class(default_prompt=DEFAULT_PROMPT)

    for e in ext.supported_extensions:
        converters[e] = ext

SUPPORTED_FILETYPES: list = converters.keys()


def run(
    file_paths: List[str], 
    prompt: str = DEFAULT_PROMPT, 
    copy_to_clipoard: bool = False
) -> List[Tuple[bool, str, str]]:
    """Runs as the main entry point for the script."""

    print(f"Converting {len(file_paths)} files...")

    results = []
    for file in file_paths:
        file = Path(file)
        txt_file = file.with_suffix(".txt")
        if not file.is_file():
            print(f"Error: {file} does not exist. Skipping...")
            continue

        filetype = file.suffix

        if filetype not in converters.keys():
            print(f"Error: {file} - {filetype} not supported. Skipping...")
            continue

        for extension, extractor in converters.items():
            if filetype == extension:
                success, msg = extractor(file=file, prompt=prompt)
                with open(txt_file, "r", encoding='utf-8') as file:
                    contents = file.read()
                results.append((success, msg, contents))
                break
        if copy_to_clipoard:

            pyperclip.copy(contents)
            print("Output copied to clipboard!")

    print("\nCopy everything in txt file, and paste into any AI Chat of your choice.")
    print("Note: The AI chat might not be able to handle very large files.")

    return results


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python papersummary.py <pdf_file1> <pdf_file2> ...")
        sys.exit(1)
    # Get a list of Path objects for each provided argument
    file_paths_command = [str(arg) for arg in sys.argv[1:]]
    run(file_paths_command)
