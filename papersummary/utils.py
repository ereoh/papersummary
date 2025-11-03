"""Utilities
"""

from typing import List

def add_prompt_txt(txt_file: str, prompt: str):
    # add prompt to top of file
    with open(txt_file, 'r') as file:
        contents = file.read()

    with open(txt_file, 'w') as file:
        file.write(prompt + '\n' + contents)

def remove_references(text: str) -> str:
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
        # else:
        #     print("\tThe word 'References' is within the first half. Writing the entire text.")
    # else:
    #     print("\tThe word 'References' was not found in the latter half of the document. Writing the entire text.")

    return text

def add_regex_filter(extensions: List[str]) -> List[str]:
    output = []

    for s in extensions:
        output.append(f"*{s}")

    return tuple(output)