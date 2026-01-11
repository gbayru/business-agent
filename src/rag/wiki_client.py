from __future__ import annotations

import os
import requests
from typing import List, Dict, Optional, Any
from abc import ABC, abstractmethod


class WikiClient(ABC):
    """Abstract base class for wiki clients"""
    
    @abstractmethod
    def fetch_page(self, page_id: str) -> Dict[str, Any]:
        """Fetch a single page by ID"""
        pass
    
    @abstractmethod
    def fetch_pages(self, space_key: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Fetch multiple pages"""
        pass
    
    @abstractmethod
    def extract_text(self, page_data: Dict[str, Any]) -> str:
        """Extract plain text from page data"""
        pass


class ConfluenceClient(WikiClient):
    """
    Atlassian Confluence wiki client
    
    Usage:
        client = ConfluenceClient(
            base_url="https://your-domain.atlassian.net/wiki",
            username="your-email@example.com",
            api_token="your-api-token"
        )
        pages = client.fetch_pages(space_key="YOUR_SPACE")
    """
    
    def __init__(
        self,
        base_url: str,
        username: Optional[str] = None,
        api_token: Optional[str] = None,
        password: Optional[str] = None,
    ):
        self.base_url = base_url.rstrip('/')
        self.username = username or os.getenv("CONFLUENCE_USERNAME")
        self.api_token = api_token or os.getenv("CONFLUENCE_API_TOKEN")
        self.password = password or os.getenv("CONFLUENCE_PASSWORD")
        
        if not self.username:
            raise ValueError("Confluence username required (env: CONFLUENCE_USERNAME)")
        if not (self.api_token or self.password):
            raise ValueError("Confluence API token or password required (env: CONFLUENCE_API_TOKEN or CONFLUENCE_PASSWORD)")
        
        self.auth = (self.username, self.api_token or self.password)
        self.session = requests.Session()
        self.session.auth = self.auth
    
    def fetch_page(self, page_id: str) -> Dict[str, Any]:
        """Fetch a single Confluence page by ID"""
        url = f"{self.base_url}/rest/api/content/{page_id}"
        params = {
            "expand": "body.storage,version,space"
        }
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def fetch_pages(
        self,
        space_key: Optional[str] = None,
        limit: int = 100,
        cql: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Fetch multiple Confluence pages
        
        Args:
            space_key: Filter by space key (e.g., "ENG", "PROD")
            limit: Maximum number of pages to fetch
            cql: Confluence Query Language query (e.g., "type=page AND space=ENG")
        """
        url = f"{self.base_url}/rest/api/content/search"
        params = {
            "expand": "body.storage,version,space",
            "limit": limit,
        }
        
        if cql:
            params["cql"] = cql
        elif space_key:
            params["cql"] = f"type=page AND space={space_key}"
        else:
            params["cql"] = "type=page"
        
        all_pages = []
        start = 0
        
        while True:
            params["start"] = start
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            pages = data.get("results", [])
            if not pages:
                break
            
            all_pages.extend(pages)
            
            if len(all_pages) >= limit or not data.get("_links", {}).get("next"):
                break
            
            start += len(pages)
        
        return all_pages[:limit]
    
    def extract_text(self, page_data: Dict[str, Any]) -> str:
        """Extract plain text from Confluence page"""
        body = page_data.get("body", {})
        storage = body.get("storage", {})
        html_content = storage.get("value", "")
        
        # Simple HTML to text conversion (you can use BeautifulSoup for better results)
        import re
        from html import unescape
        
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', html_content)
        # Decode HTML entities
        text = unescape(text)
        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text


def create_wiki_client(**kwargs) -> ConfluenceClient:
    """
    Factory function to create Confluence wiki client
    
    Args:
        **kwargs: Confluence client parameters (base_url, username, api_token, etc.)
    
    Example:
        client = create_wiki_client(
            base_url="https://company.atlassian.net/wiki",
            username="user@example.com",
            api_token="token"
        )
    """
    return ConfluenceClient(**kwargs)
