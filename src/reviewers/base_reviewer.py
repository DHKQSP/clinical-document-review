"""Base reviewer class for document review"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
from pathlib import Path
import yaml
import re


class BaseReviewer(ABC):
    """Base class for all document reviewers"""

    def __init__(self, checklist_path: str):
        self.checklist_path = Path(checklist_path)
        self.checklist = self._load_checklist()

    def _load_checklist(self) -> Dict[str, Any]:
        """Load checklist from YAML file"""
        with open(self.checklist_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def review_document(self, parsed_document: Dict[str, Any]) -> Dict[str, Any]:
        """
        Review document against checklist

        Args:
            parsed_document: Parsed document data containing text, metadata, sections

        Returns:
            Dict containing review results
        """
        results = {
            'document_type': self.checklist['document_type'],
            'file_info': parsed_document.get('file_info', {}),
            'metadata': parsed_document.get('metadata', {}),
            'checks_performed': 0,
            'checks_passed': 0,
            'checks_failed': 0,
            'findings': [],
            'summary': {},
            'severity_counts': {
                'critical': {'total': 0, 'passed': 0, 'failed': 0},
                'major': {'total': 0, 'passed': 0, 'failed': 0},
                'minor': {'total': 0, 'passed': 0, 'failed': 0}
            }
        }

        document_text = parsed_document.get('text', '').lower()

        # Process each section in checklist
        for section_key, section_data in self.checklist['sections'].items():
            section_name = section_data['name']
            section_findings = []

            for check in section_data['checks']:
                check_result = self._perform_check(check, document_text, parsed_document)
                results['checks_performed'] += 1

                severity = check.get('severity', 'minor')
                results['severity_counts'][severity]['total'] += 1

                if check_result['passed']:
                    results['checks_passed'] += 1
                    results['severity_counts'][severity]['passed'] += 1
                else:
                    results['checks_failed'] += 1
                    results['severity_counts'][severity]['failed'] += 1

                section_findings.append(check_result)

            results['findings'].append({
                'section': section_name,
                'section_key': section_key,
                'checks': section_findings
            })

        # Calculate summary
        results['summary'] = {
            'total_checks': results['checks_performed'],
            'passed': results['checks_passed'],
            'failed': results['checks_failed'],
            'pass_rate': round(results['checks_passed'] / results['checks_performed'] * 100, 2) if results['checks_performed'] > 0 else 0,
            'critical_issues': results['severity_counts']['critical']['failed'],
            'major_issues': results['severity_counts']['major']['failed'],
            'minor_issues': results['severity_counts']['minor']['failed']
        }

        return results

    def _perform_check(self, check: Dict[str, Any], document_text: str, parsed_document: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform individual check

        Args:
            check: Check definition from checklist
            document_text: Full document text (lowercased)
            parsed_document: Full parsed document data

        Returns:
            Dict with check result
        """
        keywords = check.get('keywords', [])
        check_id = check.get('id', 'unknown')
        description = check.get('description', '')
        severity = check.get('severity', 'minor')

        # Check if any keyword is found in document
        found_keywords = []
        for keyword in keywords:
            if keyword.lower() in document_text:
                found_keywords.append(keyword)

        # A check passes if at least one keyword is found
        passed = len(found_keywords) > 0

        result = {
            'id': check_id,
            'category': check.get('category', ''),
            'description': description,
            'severity': severity,
            'passed': passed,
            'found_keywords': found_keywords,
            'missing_keywords': [kw for kw in keywords if kw.lower() not in document_text]
        }

        # If check failed, add recommendation
        if not passed:
            result['recommendation'] = f"문서에 '{keywords[0]}' 관련 내용을 추가하세요."

        return result

    def search_patterns(self, document_text: str) -> Dict[str, List[str]]:
        """
        Search for defined patterns in document

        Args:
            document_text: Document text to search

        Returns:
            Dict of pattern_name: [matched_strings]
        """
        patterns = self.checklist.get('patterns', {})
        results = {}

        for pattern_name, pattern_data in patterns.items():
            regex = pattern_data['regex']
            matches = re.findall(regex, document_text, re.IGNORECASE)
            if matches:
                results[pattern_name] = list(set(matches))  # Remove duplicates

        return results

    @abstractmethod
    def get_document_type(self) -> str:
        """Return document type"""
        pass
