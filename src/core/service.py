from __future__ import annotations

import os
from typing import Any, Dict, Optional, List

from .state import create_session as _create_session, load_session, save_session
from .flow import start_or_resume, handle_user_message
from .brd_generator import BRDGenerator
from ..export.exporter_docx import export_docx_file
from ..export.exporter_txt import export_txt_file
from ..rag.index import VectorStore
from ..rag.wiki_ingest import ingest_wiki_from_config


def create_session(data_dir: str = "data/sessions") -> Dict[str, Any]:
    state = _create_session(data_dir=data_dir)
    payload = start_or_resume(state.session_id, data_dir=data_dir)
    return payload


def resume(session_id: str, data_dir: str = "data/sessions") -> Dict[str, Any]:
    return start_or_resume(session_id, data_dir=data_dir)


def message(
    session_id: str,
    current_field: str,
    user_text: str,
    question_id: Optional[str] = None,
    data_dir: str = "data/sessions",
) -> Dict[str, Any]:
    return handle_user_message(
        session_id=session_id,
        user_text=user_text,
        current_field=current_field,
        question_id=question_id,
        data_dir=data_dir,
    )


def preview(session_id: str, data_dir: str = "data/sessions") -> Dict[str, Any]:
    state = load_session(session_id, data_dir=data_dir)
    gen = BRDGenerator()
    sections = gen.generate_preview(state.fields, rag_snippets_by_section=None)
    return {"session_id": session_id, "sections": sections}


def export(
    session_id: str,
    fmt: str = "docx",
    data_dir: str = "data/sessions",
    out_dir: str = "data/exports",
) -> Dict[str, Any]:
    state = load_session(session_id, data_dir=data_dir)
    os.makedirs(out_dir, exist_ok=True)

    if fmt.lower() == "txt":
        path = export_txt_file(out_dir, session_id, state.fields, scores=state.scores)
        return {"session_id": session_id, "format": "txt", "path": path}

    path = export_docx_file(out_dir, session_id, state.fields, scores=state.scores)
    return {"session_id": session_id, "format": "docx", "path": path}


def add_wiki_documents(
    session_id: str,
    wiki_type: str,
    page_ids: Optional[List[str]] = None,
    space_key: Optional[str] = None,
    limit: int = 100,
    data_dir: str = "data/sessions",
    **wiki_kwargs
) -> Dict[str, Any]:
    """
    Add Confluence wiki documents to RAG index for a session.
    
    Args:
        session_id: Session ID
        wiki_type: Must be "confluence" (only Confluence is supported)
        page_ids: Specific page IDs to fetch (optional)
        space_key: Space/key to filter pages (optional)
        limit: Maximum number of pages to fetch
        data_dir: Session data directory
        **wiki_kwargs: Confluence client configuration (base_url, username, api_token, etc.)
    
    Returns:
        Dict with session_id, index_id, and pages_ingested
    
    Example:
        result = add_wiki_documents(
            session_id="abc123",
            wiki_type="confluence",
            space_key="ENG",
            base_url="https://company.atlassian.net/wiki",
            username="user@example.com",
            api_token="token"
        )
    """
    state = load_session(session_id, data_dir=data_dir)
    
    # Create vector store
    vector_store = VectorStore()
    
    # Use existing index or create new one
    existing_index_id = state.rag_index_id
    
    # Ingest wiki pages
    index_id = ingest_wiki_from_config(
        wiki_type=wiki_type,
        vector_store=vector_store,
        page_ids=page_ids,
        space_key=space_key,
        limit=limit,
        index_id=existing_index_id,
        **wiki_kwargs
    )
    
    # Update session state
    state.rag_index_id = index_id
    save_session(state, data_dir=data_dir)
    
    return {
        "session_id": session_id,
        "index_id": index_id,
        "message": "Wiki documents successfully added to RAG index"
    }
