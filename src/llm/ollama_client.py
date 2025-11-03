"""
Ollama Local LLM Client (Optional Feature)

This module provides optional integration with Ollama for advanced document analysis.
All processing remains local - no data is sent to external servers.

Requirements:
    - Ollama installed locally (https://ollama.ai)
    - A model pulled (e.g., ollama pull llama2)
"""

import json
import requests
from typing import Dict, Any, Optional, List


class OllamaClient:
    """Client for interacting with local Ollama LLM"""

    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama2"):
        """
        Initialize Ollama client

        Args:
            base_url: Ollama API endpoint (default: http://localhost:11434)
            model: Model name to use (default: llama2)
        """
        self.base_url = base_url.rstrip('/')
        self.model = model
        self.api_url = f"{self.base_url}/api/generate"

    def is_available(self) -> bool:
        """Check if Ollama is running and accessible"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False

    def analyze_section(self, section_text: str, section_name: str, document_type: str) -> Optional[str]:
        """
        Analyze a document section using local LLM

        Args:
            section_text: Text of the section to analyze
            section_name: Name of the section
            document_type: Type of document (Protocol, IB, SAP)

        Returns:
            Analysis result or None if error
        """
        if not self.is_available():
            return None

        prompt = self._build_analysis_prompt(section_text, section_name, document_type)

        try:
            response = requests.post(
                self.api_url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=60
            )

            if response.status_code == 200:
                result = response.json()
                return result.get('response', '')
            else:
                return None

        except Exception as e:
            print(f"LLM analysis error: {e}")
            return None

    def _build_analysis_prompt(self, section_text: str, section_name: str, document_type: str) -> str:
        """Build analysis prompt for LLM"""

        # Truncate text if too long (Ollama has context limits)
        max_length = 2000
        if len(section_text) > max_length:
            section_text = section_text[:max_length] + "..."

        prompt = f"""You are a clinical research expert reviewing a {document_type} document.

Section: {section_name}

Content:
{section_text}

Please analyze this section and provide:
1. Key findings or important points
2. Any potential issues or missing information
3. Recommendations for improvement

Keep your response concise and focused on regulatory compliance (ICH-GCP guidelines).

Analysis:"""

        return prompt

    def check_completeness(self, document_text: str, document_type: str, checklist_items: List[str]) -> Optional[Dict[str, Any]]:
        """
        Use LLM to check document completeness against checklist

        Args:
            document_text: Full document text (will be truncated if needed)
            document_type: Type of document
            checklist_items: List of items to check

        Returns:
            Dict with completeness analysis or None
        """
        if not self.is_available():
            return None

        # Truncate document if too long
        max_length = 3000
        if len(document_text) > max_length:
            document_text = document_text[:max_length] + "..."

        checklist_str = "\n".join([f"- {item}" for item in checklist_items[:10]])

        prompt = f"""Review this {document_type} document excerpt for completeness.

Checklist items to verify:
{checklist_str}

Document excerpt:
{document_text}

For each checklist item, indicate if it appears to be addressed in the document (Yes/No/Partial).
Provide a brief explanation.

Response:"""

        try:
            response = requests.post(
                self.api_url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=90
            )

            if response.status_code == 200:
                result = response.json()
                return {
                    'analysis': result.get('response', ''),
                    'model': self.model
                }
            else:
                return None

        except Exception as e:
            print(f"LLM completeness check error: {e}")
            return None

    def list_models(self) -> Optional[List[str]]:
        """List available Ollama models"""
        if not self.is_available():
            return None

        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                models = [model['name'] for model in data.get('models', [])]
                return models
            return None
        except:
            return None

    def summarize_document(self, document_text: str, max_words: int = 200) -> Optional[str]:
        """
        Generate a summary of the document

        Args:
            document_text: Document text to summarize
            max_words: Maximum words in summary

        Returns:
            Summary text or None
        """
        if not self.is_available():
            return None

        # Truncate if too long
        max_length = 4000
        if len(document_text) > max_length:
            document_text = document_text[:max_length] + "..."

        prompt = f"""Please provide a concise summary of this clinical document in {max_words} words or less.
Focus on the key objectives, methods, and important details.

Document:
{document_text}

Summary:"""

        try:
            response = requests.post(
                self.api_url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=90
            )

            if response.status_code == 200:
                result = response.json()
                return result.get('response', '')
            return None

        except Exception as e:
            print(f"LLM summarization error: {e}")
            return None
