"""
Simple utility function to convert a pdf file to a txt file
"""

from papersummary.base import BaseTextExtractor

import PyPDF2

class PDF2TextExtractor(BaseTextExtractor):

    def __init__(
        self,
        default_prompt: str = "Write a clear, concise, objective summary for the following document:",
    ):
        super().__init__(
            supported_extensions = [".pdf"],
            default_prompt = default_prompt
        )

    def _extract_text(self, file: str) -> str:
        # Extract text from the PDF
        with open(file, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            text = ""

            for page in range(len(pdf_reader.pages)):
                text += pdf_reader.pages[page].extract_text()

        return text