"""Investigator's Brochure reviewer"""

from pathlib import Path
from .base_reviewer import BaseReviewer


class IBReviewer(BaseReviewer):
    """Reviewer for Investigator's Brochure (IB) documents"""

    def __init__(self):
        # Get path to IB checklist
        config_dir = Path(__file__).parent.parent.parent / 'config'
        checklist_path = config_dir / 'ib_checklist.yaml'
        super().__init__(str(checklist_path))

    def get_document_type(self) -> str:
        return "Investigator's Brochure"
