"""Base parser class for document parsing"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
from pathlib import Path


class BaseParser(ABC):
    """Base class for all document parsers"""

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

    @abstractmethod
    def parse(self) -> Dict[str, Any]:
        """
        Parse the document and extract structured information

        Returns:
            Dict containing:
                - text: Full text content
                - metadata: Document metadata
                - sections: Parsed sections if applicable
        """
        pass

    @abstractmethod
    def extract_sections(self) -> Dict[str, str]:
        """Extract document sections"""
        pass

    def get_file_info(self) -> Dict[str, Any]:
        """Get basic file information"""
        return {
            'filename': self.file_path.name,
            'size_bytes': self.file_path.stat().st_size,
            'extension': self.file_path.suffix,
            'path': str(self.file_path.absolute())
        }
