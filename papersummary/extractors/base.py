"""Base classes"""

from typing import Tuple, List
from pathlib import Path
from papersummary.utils import add_prompt_txt, remove_references, DEFAULT_PROMPT


class BaseTextExtractor:
    """Base class for extracting text from a file and converting to .txt"""

    def __init__(
        self,
        supported_extensions: List[str],
        default_prompt: str = DEFAULT_PROMPT,
    ):
        """Initializes `BaseTextExtractor` with supported file extensions and prompt.

        Args:
            supported_extensions (List[str]): List of supported file extensions.
            default_prompt (str, optional): Default summarizing prompt. Defaults to DEFAULT_PROMPT.
        """
        self.supported_extensions = supported_extensions
        self.default_prompt = default_prompt

    def _extract_text(self, file: str) -> str:
        """Extracts text from given file

        Args:
            file (str): Path to file

        Raises:
            NotImplementedError: Subclasses must implement this method.

        Returns:
            str: Extract text from file.
        """
        raise NotImplementedError

    def _convert_to_txt(self, file: str, txt_file: str, prompt: str = "") -> None:
        """Extracts text from file, adds prompt, and writes to .txt file.

        Args:
            file (str): Path to file.
            txt_file (str): Path to text file to output.
            prompt (str, optional): Summary prompt to prepend to text file. Defaults to `self.default_prompt`.
        """
        text = self._extract_text(file)

        text = remove_references(text)

        # Write the text to the txt file
        with open(txt_file, "w", encoding="utf-8") as f:
            f.write(text)

        p = self.default_prompt if len(prompt) == 0 else prompt

        add_prompt_txt(txt_file, p)

        print(f"Converted: {file} to {txt_file}")

    def __call__(self, file: str, txt_file: str = "", prompt: str = "", **kwargs) -> Tuple[bool, str]:

        if isinstance(file, Path):
            file = str(file)
        
        if not isinstance(file, str):
            print(f"Error: File path is not a string: {file} ({type(file)})")
            return False, f"Error: File path is not a string: {file} ({type(file)})"

        file_obj = Path(file)

        if not file_obj.is_file():
            print(f"Error: Could not find the file: {file}")
            return False, f"Error: Could not find the file: {file}"
        
        if file_obj.suffix.lower() not in self.supported_extensions:
            print(f"Error: Wrong filetype for extractor {self.__class__.__name__}: {file}")
            return False, f"Error: Wrong filetype for extractor {self.__class__.__name__}: {file}"

        # create txt filepath
        txt_file = file_obj.with_suffix(".txt") if len(txt_file) == 0 else txt_file

        try:
            self._convert_to_txt(file=file, txt_file=txt_file, prompt=prompt)
        except:
            return False, f"Error: Could not convert pdf to txt: {file}, {txt_file}"

        return True, txt_file
