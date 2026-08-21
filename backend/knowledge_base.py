"""
Simple RAG (Retrieval-Augmented) knowledge base for Smart Methods
(الأساليب الذكية — https://s-m.com.sa/).

The site is small, so instead of a full vector database we keep it simple
and reliable: the whole bilingual knowledge file is loaded once and
injected into the LLM's system prompt (see llm_client.py). The model is
instructed to use this reference when the question is about Smart
Methods, and fall back to its own general knowledge otherwise.

To refresh the data after the website changes, re-scrape s-m.com.sa and
overwrite knowledge/smart_methods.md, then restart the app.
"""

from functools import lru_cache
from pathlib import Path

KNOWLEDGE_FILE = Path(__file__).parent / "knowledge" / "smart_methods.md"


@lru_cache(maxsize=1)
def load_knowledge() -> str:
    """Return the cached Smart Methods knowledge base text."""
    if not KNOWLEDGE_FILE.exists():
        return ""
    return KNOWLEDGE_FILE.read_text(encoding="utf-8")
