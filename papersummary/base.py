"""Base classes
"""

from typing import Any, Tuple, List
from pathlib import Path
from papersummary.utils import add_prompt_txt,remove_references

class BaseTextExtractor():

    def __init__(
            self,
            supported_extensions: List[str],
            default_prompt: str = "Write a clear, concise, objective summary for the following document:",
            **kwargs
        ):
        self.supported_extensions = supported_extensions
        self.default_prompt = default_prompt

    def _extract_text(self, file: str) -> str:
        raise NotImplementedError

    def _convert_to_txt(
            self, 
            file: str, 
            txt_file: str,
            prompt: str = None
        ):
        text = self._extract_text(file)

        text = remove_references(text)

        # Write the text to the txt file
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write(text)

        p = self.default_prompt if prompt is None else prompt

        add_prompt_txt(txt_file, p)

        print(f"Converted: {file} to {txt_file}")

    def __call__(
            self, 
            file: str, 
            txt_file: str = None, 
            prompt: str = None, 
            **kwargs
        ) -> Tuple[bool, str]:

        if not isinstance(file, str):
            try:
                file = str(file)
            except:
                print(f"Error: File path is not a string: {file} ({type(file)})")
                return False, f"Error: File path is not a string: {file} ({type(file)})"

        file = Path(file)

        try:
            # print(file)
            with open(file, 'rb') as f:
                pass
        except FileNotFoundError:
            print(f"Error: Could not find the file: {file}")
            return False, f"Error: Could not find the file: {file}"
        
        # create txt filepath
        txt_file = file.with_suffix(".txt") if txt_file is None else txt_file

        try:
            self._convert_to_txt(file=file, txt_file=txt_file, prompt=prompt)
        except:
            return False, f"Error: Could not convert pdf to txt: {file}, {txt_file}"

        return True, txt_file