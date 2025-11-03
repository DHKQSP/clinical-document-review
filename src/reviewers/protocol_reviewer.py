"""Protocol document reviewer"""

from pathlib import Path
from .base_reviewer import BaseReviewer


class ProtocolReviewer(BaseReviewer):
    """Reviewer for Protocol documents"""

    def __init__(self):
        # Get path to protocol checklist
        config_dir = Path(__file__).parent.parent.parent / 'config'
        checklist_path = config_dir / 'protocol_checklist.yaml'
        super().__init__(str(checklist_path))

    def get_document_type(self) -> str:
        return "Protocol"
