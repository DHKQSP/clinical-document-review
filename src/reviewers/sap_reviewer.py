"""Statistical Analysis Plan reviewer"""

from pathlib import Path
from .base_reviewer import BaseReviewer


class SAPReviewer(BaseReviewer):
    """Reviewer for Statistical Analysis Plan (SAP) documents"""

    def __init__(self):
        # Get path to SAP checklist
        config_dir = Path(__file__).parent.parent.parent / 'config'
        checklist_path = config_dir / 'sap_checklist.yaml'
        super().__init__(str(checklist_path))

    def get_document_type(self) -> str:
        return "Statistical Analysis Plan"
