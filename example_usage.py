"""
Example usage script for Voiceflow Knowledge Base Manager

This script demonstrates how to use the VoiceflowKB class to:
- Upload documents (files, URLs, tables)
- Query the knowledge base
- Update and delete documents
"""

from voiceflow_kb import VoiceflowKB

# Initialize the KB manager with your credentials
API_KEY = "VF.DM.68e6a156911014714892eee8.Yeb3HK3luekO31gR"
PROJECT_ID = "66aeff0ea380c590e96e8e70"

kb = VoiceflowKB(API_KEY, PROJECT_ID)


def example_upload_file():
    """Example: Upload a PDF, TXT, or DOCX file"""
    print("\n=== Uploading a file ===")
    
    # Upload with metadata (recommended over deprecated tags)
    result = kb.upload_document(
        file_path="example.pdf",
        metadata={
            "category": "documentation",
            "department": "support",
            "version": "1.0"
        }
    )
    
    print(f"Document uploaded successfully!")
    print(f"Document ID: {result.get('data', {}).get('documentID')}")
    return result


def example_upload_url():
    """Example: Upload a URL"""
    print("\n=== Uploading a URL ===")
    
    result = kb.upload_url(
        url="https://www.example.com/help",
        name="Example Help Page",
        metadata={
            "type": "external",
            "source": "website"
        }
    )
    
    print(f"URL uploaded successfully!")
    print(f"Document ID: {result.get('data', {}).get('documentID')}")
    return result


def example_upload_table():
    """Example: Upload table data"""
    print("\n=== Uploading table data ===")
    
    # Define the schema
    schema = {
        "product_id": {"type": "number", "searchable": True},
        "name": {"type": "string", "searchable": True},
        "price": {"type": "number", "searchable": True},
        "description": {"type": "string", "searchable": True},
        "categories": {"type": "array", "searchable": False}
    }
    
    # Define the data
    data = [
        {
            "product_id": 1,
            "name": "Widget A",
            "price": 29.99,
            "description": "High-quality widget for everyday use",
            "categories": ["hardware", "tools"]
        },
        {
            "product_id": 2,
            "name": "Widget B",
            "price": 49.99,
            "description": "Premium widget with advanced features",
            "categories": ["hardware", "premium"]
        },
        {
            "product_id": 3,
            "name": "Service Plan",
            "price": 99.99,
            "description": "Annual maintenance service",
            "categories": ["services"]
        }
    ]
    
    result = kb.upload_table(
        name="Product Catalog",
        data=data,
        schema=schema,
        metadata={
            "type": "catalog",
            "last_updated": "2025-10-14"
        }
    )
    
    print(f"Table uploaded successfully!")
    print(f"Document ID: {result.get('data', {}).get('documentID')}")
    return result


def example_query():
    """Example: Query the knowledge base"""
    print("\n=== Querying the knowledge base ===")
    
    # Simple query
    result = kb.query(
        question="What products do you offer?",
        chunkLimit=3,
        synthesis=True
    )
    
    print(f"Query: 'What products do you offer?'")
    if result.get('output'):
        print(f"\nSynthesized Answer: {result['output']}")
    
    if result.get('chunks'):
        print(f"\nFound {len(result['chunks'])} relevant chunks:")
        for i, chunk in enumerate(result['chunks'], 1):
            print(f"\n  Chunk {i}:")
            print(f"    Score: {chunk.get('score')}")
            print(f"    Content: {chunk.get('content')[:100]}...")
    
    return result


def example_query_with_filters():
    """Example: Query with metadata filters"""
    print("\n=== Querying with metadata filters ===")
    
    # Query with metadata filter
    result = kb.query(
        question="Show me documentation",
        chunkLimit=5,
        metadata={
            "$eq": {"category": "documentation"}
        }
    )
    
    print(f"Query with filter: category='documentation'")
    print(f"Found {len(result.get('chunks', []))} chunks")
    return result


def example_get_document(document_id: str):
    """Example: Retrieve a document by ID"""
    print(f"\n=== Getting document {document_id} ===")
    
    result = kb.get_document(document_id)
    print(f"Document retrieved:")
    print(f"  Name: {result.get('data', {}).get('name')}")
    print(f"  Type: {result.get('data', {}).get('type')}")
    return result


def example_update_document(document_id: str):
    """Example: Update an existing document"""
    print(f"\n=== Updating document {document_id} ===")
    
    result = kb.update_document(
        document_id=document_id,
        file_path="updated_example.pdf",
        metadata={
            "category": "documentation",
            "version": "2.0",
            "updated": "2025-10-14"
        }
    )
    
    print(f"Document updated successfully!")
    return result


def example_delete_document(document_id: str):
    """Example: Delete a document"""
    print(f"\n=== Deleting document {document_id} ===")
    
    result = kb.delete_document(document_id)
    print(f"Document deleted successfully!")
    return result


def example_list_documents():
    """Example: List all documents"""
    print("\n=== Listing documents ===")
    
    try:
        result = kb.list_documents(limit=10, offset=0)
        print(f"Found documents:")
        for doc in result.get('data', []):
            print(f"  - {doc.get('name')} (ID: {doc.get('documentID')})")
        return result
    except Exception as e:
        print(f"Note: list_documents may not be available in API: {e}")
        return None


if __name__ == "__main__":
    print("=" * 60)
    print("Voiceflow Knowledge Base Manager - Example Usage")
    print("=" * 60)
    
    # Uncomment the examples you want to run:
    
    # 1. Upload examples
    # example_upload_file()  # Requires example.pdf file
    # example_upload_url()
    # example_upload_table()
    
    # 2. Query examples
    # example_query()
    # example_query_with_filters()
    
    # 3. Document management examples
    # Replace 'YOUR_DOCUMENT_ID' with actual document ID
    # example_get_document('YOUR_DOCUMENT_ID')
    # example_update_document('YOUR_DOCUMENT_ID')  # Requires updated_example.pdf
    # example_delete_document('YOUR_DOCUMENT_ID')
    
    # 4. List documents
    # example_list_documents()
    
    print("\n" + "=" * 60)
    print("Examples completed!")
    print("=" * 60)
    print("\nTo run specific examples, uncomment them in the __main__ section")

