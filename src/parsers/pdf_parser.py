"""PDF parser for clinical documents"""

import re
from typing import Dict, Any, List
import pdfplumber
from pathlib import Path
from .base_parser import BaseParser


class PDFParser(BaseParser):
    """Parser for PDF documents"""

    def __init__(self, file_path: str):
        super().__init__(file_path)
        self.pdf = None

    def parse(self) -> Dict[str, Any]:
        """Parse PDF document"""
        with pdfplumber.open(self.file_path) as pdf:
            self.pdf = pdf

            # Extract text from all pages
            text_content = []
            for page in pdf.pages:
                text_content.append(page.extract_text() or "")

            full_text = "\n\n".join(text_content)

            # Extract metadata
            metadata = pdf.metadata or {}

            # Extract sections
            sections = self.extract_sections_from_text(full_text)

            return {
                'text': full_text,
                'metadata': {
                    'title': metadata.get('Title', ''),
                    'author': metadata.get('Author', ''),
                    'subject': metadata.get('Subject', ''),
                    'creator': metadata.get('Creator', ''),
                    'num_pages': len(pdf.pages)
                },
                'sections': sections,
                'page_count': len(pdf.pages),
                'file_info': self.get_file_info()
            }

    def extract_sections(self) -> Dict[str, str]:
        """Extract sections from PDF"""
        parsed_data = self.parse()
        return parsed_data['sections']

    def extract_sections_from_text(self, text: str) -> Dict[str, str]:
        """
        Extract sections from text using common patterns

        Looks for patterns like:
        - 1. Introduction
        - 1.0 Introduction
        - Section 1: Introduction
        """
        sections = {}

        # Split text into lines
        lines = text.split('\n')

        current_section = "Introduction"
        current_content = []

        # Common section patterns in clinical documents
        section_pattern = re.compile(
            r'^(\d+\.?\d*)\s+([A-Z][A-Za-z\s]+)|'  # 1. Title or 1.1 Title
            r'^(Section\s+\d+[:\.])\s+([A-Za-z\s]+)|'  # Section 1: Title
            r'^([A-Z][A-Z\s]{2,})\s*$'  # ALL CAPS TITLE
        )

        for line in lines:
            line = line.strip()
            if not line:
                continue

            match = section_pattern.match(line)
            if match:
                # Save previous section
                if current_content:
                    sections[current_section] = '\n'.join(current_content).strip()

                # Start new section
                current_section = line
                current_content = []
            else:
                current_content.append(line)

        # Save last section
        if current_content:
            sections[current_section] = '\n'.join(current_content).strip()

        return sections

    def extract_tables(self) -> List[List[List[str]]]:
        """Extract tables from PDF"""
        tables = []
        with pdfplumber.open(self.file_path) as pdf:
            for page in pdf.pages:
                page_tables = page.extract_tables()
                if page_tables:
                    tables.extend(page_tables)
        return tables

    def search_text(self, pattern: str, case_sensitive: bool = False) -> List[Dict[str, Any]]:
        """
        Search for text pattern in document

        Args:
            pattern: Regex pattern to search
            case_sensitive: Whether search should be case sensitive

        Returns:
            List of matches with context
        """
        flags = 0 if case_sensitive else re.IGNORECASE
        regex = re.compile(pattern, flags)

        matches = []
        with pdfplumber.open(self.file_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                text = page.extract_text() or ""
                for match in regex.finditer(text):
                    matches.append({
                        'page': page_num,
                        'match': match.group(),
                        'start': match.start(),
                        'end': match.end(),
                        'context': text[max(0, match.start()-50):match.end()+50]
                    })

        return matches
