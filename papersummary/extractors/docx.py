"""
Convert .docx text to .txt
"""

from papersummary.extractors.base import BaseTextExtractor
from papersummary.utils import DEFAULT_PROMPT

import docx


class DOCX2TextExtractor(BaseTextExtractor):
    """Microsoft Word .docx text extractor"""

    def __init__(
        self,
        default_prompt: str = DEFAULT_PROMPT,
    ):
        """Initializes .docx text extractor

        Args:
            default_prompt (str, optional): Summary prompt to use. Defaults to DEFAULT_PROMPT.
        """
        super().__init__(supported_extensions=[".docx"], default_prompt=default_prompt)

    def _extract_text(self, file: str) -> str:
        """Extracts text from .docx file

        Args:
            file (str): Path to .docx file

        Returns:
            str: Extracted text.
        """
        doc = docx.Document(file)

        text = []
        for para in doc.paragraphs:
            text.append(para.text)

        return "\n".join(text)
