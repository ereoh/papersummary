"""
Convert .pdf text to .txt
"""


from papersummary.base import BaseTextExtractor
from papersummary.utils import DEFAULT_PROMPT

import PyPDF2


class PDF2TextExtractor(BaseTextExtractor):
    """.pdf text extractor 
    """
    def __init__(
        self,
        default_prompt: str = DEFAULT_PROMPT,
    ):
        """Initializes .pdf text extractor

        Args:
            default_prompt (str, optional): Summary prompt to use. Defaults to DEFAULT_PROMPT.
        """ 
        super().__init__(supported_extensions=[".pdf"], default_prompt=default_prompt)

    def _extract_text(self, file: str) -> str:
        """Extracts text from .pdf file

        Args:
            file (str): Path to .pdf file

        Returns:
            str: Extracted text.
        """
        with open(file, "rb") as f:
            pdf_reader = PyPDF2.PdfReader(f)
            text = ""

            for page in range(len(pdf_reader.pages)):
                text += pdf_reader.pages[page].extract_text()

        return text
