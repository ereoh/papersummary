"""
Convert ppts text to txt
"""

from papersummary.base import BaseTextExtractor

import docx

class DOCX2TextExtractor(BaseTextExtractor):

    def __init__(
        self,
        default_prompt: str = "Write a clear, concise, objective summary for the following document:",
    ):
        super().__init__(
            supported_extensions = [".docx"],
            default_prompt = default_prompt
        )

    def _extract_text(self, file: str) -> str:
        # Extract text from the .pptx file

        doc = docx.Document(file)
        
        text = []
        for para in doc.paragraphs:
            text.append(para.text)
        
        return "\n".join(text)