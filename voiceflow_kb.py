"""
Voiceflow Knowledge Base Manager

A Python library for managing documents in Voiceflow Knowledge Base.
Supports uploading, querying, updating, and deleting documents.
"""

import requests
import json
from typing import Dict, List, Optional, Any
from pathlib import Path


class VoiceflowKB:
    """Main class for interacting with Voiceflow Knowledge Base API"""
    
    def __init__(self, api_key: str, project_id: str):
        """
        Initialize the Voiceflow KB manager
        
        Args:
            api_key: Voiceflow Dialog Manager API Key (VF.DM.xxx)
            project_id: Your Voiceflow project ID
        """
        self.api_key = api_key
        self.project_id = project_id
        self.base_url = "https://api.voiceflow.com"
        self.query_url = "https://general-runtime.voiceflow.com"
        self.headers = {
            "Authorization": api_key,
            "Content-Type": "application/json; charset=utf-8"
        }
    
    def upload_document(
        self, 
        file_path: str, 
        tags: Optional[List[Dict[str, str]]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        overwrite: Optional[bool] = None,
        max_chunk_size: Optional[int] = None
    ) -> Dict:
        """
        Upload a document to the Knowledge Base (PDF, TXT, DOCX)
        
        Args:
            file_path: Path to the file to upload
            tags: Optional list of tags (deprecated, use metadata instead)
            metadata: Optional metadata dict for the document
            
        Returns:
            Response from the API with document details
        """
        url = f"{self.base_url}/v1/knowledge-base/docs/upload"
        
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Prepare multipart form data
        files = {
            'file': (file_path.name, open(file_path, 'rb'))
        }
        
        data = {}
        
        # Add tags if provided (deprecated but still supported)
        if tags:
            data['tags'] = json.dumps(tags)
        
        # Add metadata if provided
        if metadata:
            data['metadata'] = json.dumps(metadata)
        
        # Remove Content-Type header for multipart/form-data
        headers = {
            "Authorization": self.api_key
        }
        
        params: Dict[str, Any] = {}
        if overwrite is not None:
            params["overwrite"] = "true" if overwrite else "false"
        if max_chunk_size is not None:
            params["maxChunkSize"] = max_chunk_size
        
        response = requests.post(url, headers=headers, params=params, files=files, data=data)
        response.raise_for_status()
        return response.json()
    
    def upload_url(
        self, 
        url: str, 
        name: Optional[str] = None,
        tags: Optional[List[Dict[str, str]]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        overwrite: Optional[bool] = None,
        max_chunk_size: Optional[int] = None
    ) -> Dict:
        """
        Upload a URL document to the Knowledge Base
        
        Args:
            url: The URL to add to the knowledge base
            name: Optional name for the document
            tags: Optional list of tags
            metadata: Optional metadata dict for the document
            
        Returns:
            Response from the API with document details
        """
        endpoint = f"{self.base_url}/v1/knowledge-base/docs/upload"
        
        # Per docs, URL uploads must be JSON with a top-level `data` object
        payload: Dict[str, Any] = {
            "data": {
                "type": "url",
                "url": url
            }
        }
        
        if metadata:
            payload["data"]["metadata"] = metadata
        if name:
            # Name is optional; API may generate one from the URL
            payload["data"]["name"] = name
        if tags:
            # Tags are deprecated but still supported as legacy
            payload["data"]["tags"] = tags
        
        params: Dict[str, Any] = {}
        if overwrite is not None:
            params["overwrite"] = "true" if overwrite else "false"
        if max_chunk_size is not None:
            params["maxChunkSize"] = max_chunk_size
        
        response = requests.post(endpoint, headers=self.headers, params=params, json=payload)
        response.raise_for_status()
        return response.json()
    
    def upload_table(
        self,
        name: str,
        data: List[Dict[str, Any]],
        schema: Dict[str, Dict[str, Any]],
        tags: Optional[List[Dict[str, str]]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        overwrite: Optional[bool] = None,
        max_chunk_size: Optional[int] = None
    ) -> Dict:
        """
        Upload table data to the Knowledge Base
        
        Args:
            name: Name for the table
            data: List of row dictionaries
            schema: Schema definition for the table columns
            tags: Optional list of tags
            metadata: Optional metadata dict for the table
            
        Returns:
            Response from the API with table details
            
        Example:
            schema = {
                "id": {"type": "number", "searchable": True},
                "name": {"type": "string", "searchable": True},
                "description": {"type": "string", "searchable": False}
            }
            data = [
                {"id": 1, "name": "Product A", "description": "Great product"},
                {"id": 2, "name": "Product B", "description": "Better product"}
            ]
        """
        url = f"{self.base_url}/v1/knowledge-base/docs/upload/table"
        
        # Build schema with searchableFields and fields map
        fields: Dict[str, Any] = {}
        searchable_fields: List[str] = []
        for field_name, field_cfg in schema.items():
            field_type = field_cfg.get("type")
            if not field_type:
                continue
            fields[field_name] = {"type": field_type}
            if field_cfg.get("searchable") is True:
                searchable_fields.append(field_name)
        
        # Per API validation errors, expects: data.items (array) and schema.searchableFields (array)
        payload: Dict[str, Any] = {
            "data": {
                "name": name,
                "schema": {
                    "fields": fields,
                    "searchableFields": searchable_fields
                },
                "items": data
            }
        }
        
        if metadata:
            payload["data"]["metadata"] = metadata
        if tags:
            payload["data"]["tags"] = tags
        
        params: Dict[str, Any] = {}
        if overwrite is not None:
            params["overwrite"] = "true" if overwrite else "false"
        if max_chunk_size is not None:
            params["maxChunkSize"] = max_chunk_size
        
        response = requests.post(url, headers=self.headers, params=params, json=payload)
        response.raise_for_status()
        return response.json()
    
    def get_document(self, document_id: str) -> Dict:
        """
        Retrieve a document by its ID
        
        Args:
            document_id: The document ID
            
        Returns:
            Document details
        """
        url = f"{self.base_url}/v1/knowledge-base/docs/{document_id}"
        
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def delete_document(self, document_id: str) -> Dict:
        """
        Delete a document by its ID
        
        Args:
            document_id: The document ID to delete
            
        Returns:
            Response from the API
        """
        url = f"{self.base_url}/v1/knowledge-base/docs/{document_id}"
        
        response = requests.delete(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def update_document(
        self, 
        document_id: str,
        file_path: str,
        tags: Optional[List[Dict[str, str]]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict:
        """
        Replace/update an existing document by its ID
        
        Args:
            document_id: The document ID to update
            file_path: Path to the new file
            tags: Optional list of tags
            metadata: Optional metadata dict for the document
            
        Returns:
            Response from the API
        """
        url = f"{self.base_url}/v1/knowledge-base/docs/{document_id}/upload"
        
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        files = {
            'file': (file_path.name, open(file_path, 'rb'))
        }
        
        data = {}
        
        if tags:
            data['tags'] = json.dumps(tags)
            
        if metadata:
            data['metadata'] = json.dumps(metadata)
        
        headers = {
            "Authorization": self.api_key
        }
        
        response = requests.put(url, headers=headers, files=files, data=data)
        response.raise_for_status()
        return response.json()
    
    def query(
        self,
        question: str,
        chunkLimit: int = 5,
        synthesis: bool = True,
        tags: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict:
        """
        Query the Knowledge Base
        
        Args:
            question: The question to ask
            chunkLimit: Maximum number of chunks to return (default: 5)
            synthesis: Whether to synthesize an answer (default: True)
            tags: Optional tag filters
            metadata: Optional metadata filters
            
        Returns:
            Query results with chunks and optional synthesized answer
            
        Example:
            result = kb.query(
                question="What are your business hours?",
                metadata={"$eq": {"category": "store-info"}}
            )
        """
        url = f"{self.query_url}/knowledge-base/query"
        
        payload = {
            "question": question,
            "chunkLimit": chunkLimit,
            "synthesis": synthesis
        }
        
        # Add settings for filtering
        settings = {}
        if tags:
            settings["tags"] = tags
        if metadata:
            settings["metadata"] = metadata
            
        if settings:
            payload["settings"] = settings
        
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()
    
    def list_documents(
        self,
        limit: int = 50,
        offset: int = 0
    ) -> Dict:
        """
        List all documents in the knowledge base
        Note: This endpoint may need to be confirmed from API docs
        
        Args:
            limit: Number of documents to return
            offset: Offset for pagination
            
        Returns:
            List of documents
        """
        url = f"{self.base_url}/v1/knowledge-base/docs"
        params = {
            "limit": limit,
            "offset": offset
        }
        
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()


# Convenience functions for quick access
def create_kb_manager(api_key: str, project_id: str) -> VoiceflowKB:
    """
    Create a Knowledge Base manager instance
    
    Args:
        api_key: Voiceflow Dialog Manager API Key
        project_id: Your Voiceflow project ID
        
    Returns:
        VoiceflowKB instance
    """
    return VoiceflowKB(api_key, project_id)


if __name__ == "__main__":
    # Example usage
    API_KEY = "VF.DM.68e6a156911014714892eee8.Yeb3HK3luekO31gR"
    PROJECT_ID = "68e56f7170abdf09f66dc756"
    
    kb = VoiceflowKB(API_KEY, PROJECT_ID)
    print("Voiceflow Knowledge Base Manager initialized!")
    print(f"Project ID: {PROJECT_ID}")
    print("\nAvailable methods:")
    print("  - upload_document(file_path)")
    print("  - upload_url(url)")
    print("  - upload_table(name, data, schema)")
    print("  - query(question)")
    print("  - get_document(document_id)")
    print("  - delete_document(document_id)")
    print("  - update_document(document_id, file_path)")
    print("  - list_documents()")

