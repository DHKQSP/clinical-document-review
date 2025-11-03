"""
Example test file demonstrating how to test the clinical document review tool

To run tests:
    pip install pytest pytest-cov
    pytest tests/
"""

import pytest
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))


class TestReviewers:
    """Test reviewer classes"""

    def test_protocol_reviewer_init(self):
        """Test Protocol reviewer initialization"""
        from reviewers import ProtocolReviewer

        reviewer = ProtocolReviewer()
        assert reviewer.get_document_type() == "Protocol"
        assert reviewer.checklist is not None
        assert 'sections' in reviewer.checklist

    def test_ib_reviewer_init(self):
        """Test IB reviewer initialization"""
        from reviewers import IBReviewer

        reviewer = IBReviewer()
        assert reviewer.get_document_type() == "Investigator's Brochure"
        assert reviewer.checklist is not None

    def test_sap_reviewer_init(self):
        """Test SAP reviewer initialization"""
        from reviewers import SAPReviewer

        reviewer = SAPReviewer()
        assert reviewer.get_document_type() == "Statistical Analysis Plan"
        assert reviewer.checklist is not None


class TestReports:
    """Test report generators"""

    def test_html_report_generator_init(self):
        """Test HTML report generator initialization"""
        from reports import HTMLReportGenerator

        generator = HTMLReportGenerator()
        assert generator.template is not None

    def test_text_report_generator_init(self):
        """Test text report generator initialization"""
        from reports import TextReportGenerator

        generator = TextReportGenerator()
        assert generator is not None


class TestLLM:
    """Test LLM integration"""

    def test_ollama_client_init(self):
        """Test Ollama client initialization"""
        from llm import OllamaClient

        client = OllamaClient()
        assert client.base_url == "http://localhost:11434"
        assert client.model == "llama2"

    def test_ollama_client_custom_model(self):
        """Test Ollama client with custom model"""
        from llm import OllamaClient

        client = OllamaClient(model="mistral")
        assert client.model == "mistral"


# Example of how to test with a mock PDF
class TestParsers:
    """Test parser classes"""

    def test_base_parser_file_not_found(self):
        """Test that BaseParser raises FileNotFoundError for non-existent files"""
        from parsers import PDFParser

        with pytest.raises(FileNotFoundError):
            PDFParser("/nonexistent/file.pdf")


# Example of testing review logic with mock data
def test_review_logic():
    """Test review logic with mock parsed document"""
    from reviewers import ProtocolReviewer

    reviewer = ProtocolReviewer()

    # Mock parsed document
    mock_doc = {
        'text': 'This is a protocol version 1.0 with primary objective to test safety. '
                'Inclusion criteria are defined. Adverse event reporting will be performed.',
        'metadata': {'num_pages': 10},
        'sections': {'Introduction': 'Test content'},
        'file_info': {'filename': 'test.pdf', 'size_bytes': 1000}
    }

    results = reviewer.review_document(mock_doc)

    # Assertions
    assert results['document_type'] == 'Protocol'
    assert results['checks_performed'] > 0
    assert 'summary' in results
    assert 'findings' in results
    assert isinstance(results['summary']['pass_rate'], (int, float))


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
