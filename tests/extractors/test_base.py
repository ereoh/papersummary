import pytest
from unittest.mock import patch
from pathlib import Path
from papersummary.utils import add_prompt_txt, remove_references, DEFAULT_PROMPT
from papersummary.extractors.base import BaseTextExtractor

class MockTextExtractor(BaseTextExtractor):
    """Mock implementation of BaseTextExtractor for testing purposes."""

    def _extract_text(self, file: str) -> str:
        """Mock text extraction."""
        return "Extracted text."

@pytest.fixture
def mock_extractor():
    """Fixture to create a mock text extractor instance."""
    return MockTextExtractor(supported_extensions=[".txt", ".pdf"])

def test_initialization(mock_extractor):
    """Test the initialization of the BaseTextExtractor."""
    assert mock_extractor.supported_extensions == [".txt", ".pdf"]
    assert mock_extractor.default_prompt == DEFAULT_PROMPT

def test_extract_text_not_implemented():
    """Test that _extract_text raises NotImplementedError in base class."""
    with pytest.raises(NotImplementedError):
        BaseTextExtractor(supported_extensions=[".txt"])._extract_text("dummy_file.txt")

def test_convert_to_txt(mock_extractor, tmp_path):
    """Test the _convert_to_txt method."""
    test_file = tmp_path / "test_file.txt"
    output_txt = tmp_path / "output.txt"

    # Mock or get the necessary data for processing
    mock_text = "Test content without references."
    with patch("papersummary.extractors.base.remove_references") as mock_remove_references:
        mock_remove_references.return_value = mock_text

        # Call the _convert_to_txt method
        mock_extractor._convert_to_txt(str(test_file), str(output_txt), "Custom prompt")

        # Check that the output file was created with correct content.
        assert output_txt.is_file()
        with open(output_txt, "r", encoding="utf-8") as f:
            content = f.read()
        expected_content = "Custom prompt\n" + mock_text
        assert content == expected_content

def test_call_with_non_string_file(mock_extractor):
    """Test the __call__ method with a non-string filepath parameter."""
    success, message = mock_extractor(123)
    assert not success

def test_call_with_nonexistent_file(mock_extractor):
    """Test the __call__ method with a non-existent file."""
    nonexistent_file = "nonexistent_file.txt"
    success, message = mock_extractor(nonexistent_file)
    assert not success
    assert "Error: Could not find the file:" in message 

def test_call_with_unsupported_file_extension(mock_extractor, tmp_path):
    """Test the __call__ method with an unsupported file extension."""
    unsupported_file = tmp_path / "test_file.png"
    unsupported_file.touch()

    success, message = mock_extractor(str(unsupported_file))
    assert not success

    error_message = f"Error: Wrong filetype for extractor {mock_extractor.__class__.__name__}: {unsupported_file}"
    assert error_message in message

def test_call_with_valid_file(mock_extractor, tmp_path):
    """Test the __call__ method with a valid file."""
    valid_file = tmp_path / "test_file.txt"
    valid_file.write_text("Test content.")

    output_txt = tmp_path / "test_file.txt"  # The same name with a `.txt` extension

    success, output = mock_extractor(str(valid_file), str(output_txt))
    assert success
    assert output == str(output_txt)
    assert valid_file.is_file()

def test_call_with_valid_file(mock_extractor, tmp_path):
    """Test the __call__ method with a valid file Path."""
    valid_file = tmp_path / "test_file.txt"
    valid_file.write_text("Test content.")

    output_txt = tmp_path / "test_file.txt"  # The same name with a `.txt` extension

    success, output = mock_extractor(valid_file, str(output_txt))
    assert success
    assert output == str(output_txt)
    assert valid_file.is_file()