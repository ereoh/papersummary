"""Utilities"""

DEFAULT_PROMPT = "Write a clear, concise, objective summary for the following document:"

def add_prompt_txt(txt_file: str, prompt: str) -> None:
    """Adds summary prompt to top of txt file

    Args:
        txt_file (str): Path to text file.
        prompt (str): Summary prompt.
    """    
    # add prompt to top of file
    with open(txt_file, "r", encoding='utf-8') as file:
        contents = file.read()

    with open(txt_file, "w", encoding='utf-8') as file:
        file.write(prompt + "\n" + contents)


def remove_references(text: str) -> str:
    """Removes "References" section from text. 

    Only removes the References" section if found in second half of string.

    Args:
        text (str): Text to check.

    Returns:
        str: Updated text.
    """    
    total_length = len(text)
    half_length = total_length // 2
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
