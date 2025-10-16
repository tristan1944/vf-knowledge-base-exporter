"""
Helper functions for auto-calculating chunk size and generating metadata
"""

import os
from typing import Dict, Any, Optional
from pathlib import Path


def calculate_optimal_chunk_size(
    content_length: Optional[int] = None,
    file_path: Optional[str] = None,
    document_type: str = 'general'
) -> int:
    """
    Auto-calculate optimal chunk size based on content characteristics
    
    Args:
        content_length: Length of content in characters
        file_path: Path to file (to estimate size)
        document_type: Type of document (general, technical, FAQ, etc.)
        
    Returns:
        Recommended chunk size (500-1500)
    """
    # Estimate content length if not provided
    if content_length is None and file_path:
        try:
            content_length = os.path.getsize(file_path)
        except:
            content_length = 0
    
    if content_length is None:
        content_length = 0
    
    # Base chunk size recommendations
    base_sizes = {
        'faq': 600,          # Smaller chunks for Q&A
        'technical': 1200,   # Larger chunks for technical docs
        'marketing': 800,    # Medium chunks for marketing content
        'general': 1000,     # Default
        'code': 1400,        # Large chunks for code documentation
        'table': 700         # Smaller chunks for structured data
    }
    
    base_size = base_sizes.get(document_type.lower(), 1000)
    
    # Adjust based on content length
    if content_length < 1000:
        # Very short content - use smaller chunks
        return max(500, min(base_size - 200, 700))
    elif content_length < 5000:
        # Short content - slightly smaller chunks
        return max(600, min(base_size - 100, 900))
    elif content_length < 20000:
        # Medium content - use base size
        return base_size
    elif content_length < 50000:
        # Large content - slightly larger chunks
        return min(base_size + 100, 1300)
    else:
        # Very large content - use larger chunks for efficiency
        return min(base_size + 200, 1500)


def generate_metadata_suggestions(
    file_path: Optional[str] = None,
    url: Optional[str] = None,
    table_name: Optional[str] = None
) -> Dict[str, Any]:
    """
    Auto-generate metadata suggestions based on input
    
    Args:
        file_path: Path to file being uploaded
        url: URL being uploaded
        table_name: Name of table being uploaded
        
    Returns:
        Dictionary with suggested metadata
    """
    metadata = {}
    
    if file_path:
        path = Path(file_path)
        filename = path.name
        extension = path.suffix.lower()
        
        # Suggest category based on file extension
        ext_categories = {
            '.pdf': 'documentation',
            '.docx': 'documentation',
            '.doc': 'documentation',
            '.txt': 'text',
            '.md': 'documentation',
            '.csv': 'data',
            '.json': 'data',
            '.xml': 'data'
        }
        
        if extension in ext_categories:
            metadata['category'] = ext_categories[extension]
        else:
            metadata['category'] = 'document'
        
        # Extract potential type from filename
        filename_lower = filename.lower()
        if 'faq' in filename_lower:
            metadata['type'] = 'faq'
            metadata['category'] = 'support'
        elif 'guide' in filename_lower or 'manual' in filename_lower:
            metadata['type'] = 'guide'
            metadata['category'] = 'documentation'
        elif 'spec' in filename_lower or 'technical' in filename_lower:
            metadata['type'] = 'technical'
            metadata['category'] = 'documentation'
        elif 'product' in filename_lower or 'catalog' in filename_lower:
            metadata['type'] = 'catalog'
            metadata['category'] = 'products'
        
        metadata['source'] = 'file_upload'
        metadata['filename'] = filename
    
    elif url:
        from urllib.parse import urlparse
        parsed = urlparse(url)
        domain = parsed.netloc
        path = parsed.path
        
        metadata['source'] = 'url'
        metadata['domain'] = domain
        metadata['category'] = 'web_content'
        
        # Detect common URL patterns
        path_lower = path.lower()
        if '/blog' in path_lower or '/article' in path_lower:
            metadata['type'] = 'blog'
            metadata['category'] = 'content'
        elif '/docs' in path_lower or '/documentation' in path_lower:
            metadata['type'] = 'documentation'
            metadata['category'] = 'docs'
        elif '/faq' in path_lower or '/help' in path_lower:
            metadata['type'] = 'faq'
            metadata['category'] = 'support'
        elif '/api' in path_lower:
            metadata['type'] = 'api_reference'
            metadata['category'] = 'technical'
        elif '/product' in path_lower:
            metadata['type'] = 'product_page'
            metadata['category'] = 'products'
    
    elif table_name:
        metadata['source'] = 'table_upload'
        metadata['category'] = 'structured_data'
        metadata['type'] = 'table'
        
        # Detect table type from name
        name_lower = table_name.lower()
        if 'product' in name_lower or 'catalog' in name_lower:
            metadata['category'] = 'products'
            metadata['type'] = 'product_catalog'
        elif 'customer' in name_lower or 'user' in name_lower:
            metadata['category'] = 'users'
            metadata['type'] = 'user_data'
        elif 'price' in name_lower or 'pricing' in name_lower:
            metadata['category'] = 'pricing'
            metadata['type'] = 'pricing_table'
        elif 'faq' in name_lower:
            metadata['category'] = 'support'
            metadata['type'] = 'faq_table'
    
    return metadata


def format_metadata_display(metadata: Dict[str, Any]) -> str:
    """Format metadata as a nice JSON string for display"""
    import json
    return json.dumps(metadata, indent=2)

