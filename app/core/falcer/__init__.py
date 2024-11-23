from .score_a_text import score_text_on_falc
from .text_to_falc import falcate_text
from .understood import get_all_falc_feedback, store_falc_feedback

__all__ = [
    "falcate_text",
    "score_text_on_falc",
    "get_all_falc_feedback",
    "store_falc_feedback",
]
