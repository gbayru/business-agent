from __future__ import annotations

import os
from typing import List, Dict, Any, Optional
from .wiki_client import WikiClient, ConfluenceClient, create_wiki_client
from .index import VectorStore, RAGIndex
from .ingest import chunk_text


def ingest_wiki_pages(
    wiki_client: WikiClient,
    vector_store: VectorStore,
    page_ids: Optional[List[str]] = None,
    space_key: Optional[str] = None,
    limit: int = 100,
    max_chunk_chars: int = 3500,
    index_id: Optional[str] = None,
) -> str:
    """
    Fetch pages from wiki and ingest them into RAG index.
    
    Args:
        wiki_client: WikiClient instance (Confluence, MediaWiki, etc.)
        vector_store: VectorStore instance
        page_ids: Specific page IDs to fetch (if None, fetches all pages)
        space_key: Space/key to filter pages (wiki-specific)
        limit: Maximum number of pages to fetch
        max_chunk_chars: Maximum characters per chunk
        index_id: Existing index ID to add to, or None to create new
    
    Returns:
        index_id: The RAG index ID (can be stored in session state)
    
    Example:
        from src.rag.wiki_client import create_wiki_client
        from src.rag.index import VectorStore
        
        # Create wiki client
        client = create_wiki_client(
            wiki_type="confluence",
            base_url="https://company.atlassian.net/wiki",
            username="user@example.com",
            api_token="token"
        )
        
        # Create vector store
        vector_store = VectorStore()
        
        # Ingest pages
        index_id = ingest_wiki_pages(
            wiki_client=client,
            vector_store=vector_store,
            space_key="ENG",
            limit=50
        )
    """
    import uuid
    
    # Create or get index
    if index_id:
        index = RAGIndex(index_id=index_id, meta={"collection_name": f"rag_index_{index_id}"})
    else:
        index_id = str(uuid.uuid4())
        index = vector_store.create_index(index_id)
    
    # Fetch pages
    if page_ids:
        # Fetch specific pages
        pages = []
        for page_id in page_ids:
            try:
                page = wiki_client.fetch_page(page_id)
                pages.append(page)
            except Exception as e:
                print(f"Error fetching page {page_id}: {e}")
                continue
    else:
        # Fetch all pages (with filters)
        pages = wiki_client.fetch_pages(space_key=space_key, limit=limit)
    
    print(f"Fetched {len(pages)} pages from wiki")
    
    # Extract text and chunk
    all_chunks = []
    all_metadatas = []
    
    for page in pages:
        try:
            text = wiki_client.extract_text(page)
            if not text or len(text.strip()) < 50:
                continue  # Skip empty or very short pages
            
            chunks = chunk_text(text, max_chars=max_chunk_chars)
            
            # Create metadata for each chunk
            page_title = page.get("title", page.get("displayTitle", "Unknown"))
            page_id = page.get("id", page.get("pageid", "unknown"))
            page_url = page.get("_links", {}).get("webui", page.get("url", ""))
            
            for i, chunk in enumerate(chunks):
                all_chunks.append(chunk)
                all_metadatas.append({
                    "source": "wiki",
                    "page_id": str(page_id),
                    "page_title": page_title,
                    "chunk_index": i,
                    "total_chunks": len(chunks),
                    "url": page_url,
                })
        except Exception as e:
            print(f"Error processing page {page.get('id', 'unknown')}: {e}")
            continue
    
    # Add to vector store
    if all_chunks:
        print(f"Adding {len(all_chunks)} chunks to vector store...")
        vector_store.add_texts(index, all_chunks, metadatas=all_metadatas)
        print(f"Successfully ingested {len(pages)} pages into index {index_id}")
    else:
        print("No chunks to add")
    
    return index_id


def ingest_wiki_from_config(
    wiki_type: str,
    vector_store: VectorStore,
    page_ids: Optional[List[str]] = None,
    space_key: Optional[str] = None,
    limit: int = 100,
    index_id: Optional[str] = None,
    **wiki_kwargs
) -> str:
    """
    Convenience function to ingest Confluence wiki pages from configuration.
    
    Args:
        wiki_type: Must be "confluence" (only Confluence is supported)
        vector_store: VectorStore instance
        page_ids: Specific page IDs to fetch
        space_key: Space/key to filter pages
        limit: Maximum number of pages
        **wiki_kwargs: Additional arguments for Confluence client (base_url, username, api_token, etc.)
    
    Returns:
        index_id: The RAG index ID
    
    Example:
        index_id = ingest_wiki_from_config(
            wiki_type="confluence",
            vector_store=vector_store,
            space_key="ENG",
            base_url="https://company.atlassian.net/wiki",
            username="user@example.com",
            api_token="token"
        )
    """
    if wiki_type.lower() != "confluence":
        raise ValueError(f"Only Confluence is supported. Got: {wiki_type}")
    
    wiki_client = create_wiki_client(**wiki_kwargs)
    return ingest_wiki_pages(
        wiki_client=wiki_client,
        vector_store=vector_store,
        page_ids=page_ids,
        space_key=space_key,
        limit=limit,
        index_id=index_id,
    )
