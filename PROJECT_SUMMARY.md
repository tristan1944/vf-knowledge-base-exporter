# Voiceflow Knowledge Base Manager - Project Summary

## Overview

This project provides a complete Python-based solution for managing your Voiceflow Knowledge Base. It includes both a Python library and a command-line interface for easy interaction with the Voiceflow API.

## What's Included

### Core Library (`voiceflow_kb.py`)
A comprehensive Python library with the following capabilities:

**Upload Methods:**
- `upload_document()` - Upload PDF, TXT, DOCX files
- `upload_url()` - Add web pages to your knowledge base
- `upload_table()` - Upload structured data with custom schemas

**Query Methods:**
- `query()` - Search the knowledge base with optional filters
- Advanced filtering by metadata and tags
- Customizable chunk limits and synthesis settings

**Document Management:**
- `get_document()` - Retrieve document details
- `update_document()` - Replace existing documents
- `delete_document()` - Remove documents
- `list_documents()` - View all documents

### Command-Line Interface (`kb_cli.py`)
A user-friendly CLI for all operations:
- Upload files, URLs, and tables
- Query with natural language
- Manage documents (get, update, delete, list)
- JSON or text output formats
- Verbose mode for debugging

### Documentation
- **README.md** - Complete API reference and documentation
- **QUICKSTART.md** - 5-minute getting started guide
- **examples/README.md** - Examples and templates

### Testing & Examples
- **test_connection.py** - Verify your API connection
- **example_usage.py** - Comprehensive Python examples
- **examples/** - JSON templates for table uploads

### Configuration
- **requirements.txt** - Python dependencies (just `requests`)
- **config.example.json** - Configuration template
- **.gitignore** - Protects sensitive data

## Your Configuration

The project is pre-configured with your credentials:

```python
PROJECT_ID = "66aeff0ea380c590e96e8e70"
API_KEY = "VF.DM.68e6a156911014714892eee8.Yeb3HK3luekO31gR"
```

⚠️ **Security Note**: These credentials are embedded in the code for convenience. For production use, consider using environment variables or a secure config file.

## Key Features

### 1. Multiple Upload Types
- **Files**: PDF, TXT, DOCX documents
- **URLs**: Web pages and online content
- **Tables**: Structured data with customizable schemas

### 2. Advanced Querying
- Natural language questions
- Metadata filtering with operators ($eq, $ne, $in, $and, $or)
- Adjustable result limits
- Optional answer synthesis
- Configurable temperature for AI responses

### 3. Metadata Support
Organize your knowledge base with custom metadata:
```python
metadata = {
    "category": "documentation",
    "department": "support",
    "version": "1.0",
    "priority": "high"
}
```

### 4. Table Uploads
Upload structured data with schemas:
```python
schema = {
    "id": {"type": "number", "searchable": True},
    "name": {"type": "string", "searchable": True},
    "description": {"type": "string", "searchable": True}
}
```

### 5. Two Ways to Use
- **Python Library**: For integration into your applications
- **CLI**: For quick operations and automation scripts

## Quick Start

1. **Install**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Test Connection**:
   ```bash
   python test_connection.py
   ```

3. **Upload Content**:
   ```bash
   python kb_cli.py upload-file document.pdf
   ```

4. **Query**:
   ```bash
   python kb_cli.py query "What's in my knowledge base?"
   ```

## Use Cases

### Documentation Management
Upload and search through product documentation, user manuals, and technical guides.

### Product Catalogs
Create searchable product databases with pricing, descriptions, and categorization.

### FAQ Systems
Build question-answering systems from your FAQ content.

### Website Indexing
Import content from multiple web pages for unified search.

### Customer Support
Integrate with Voiceflow assistants to provide accurate, sourced answers.

## API Endpoints Used

The library interacts with these Voiceflow API endpoints:

- **Document Management**: `https://api.voiceflow.com/v1/knowledge-base/docs/*`
- **Query**: `https://general-runtime.voiceflow.com/knowledge-base/query`

All requests are authenticated using your Dialog Manager API Key.

## File Structure

```
vf-knowledge-base-exporter/
├── Core Library
│   └── voiceflow_kb.py (320 lines)
│
├── Command-Line Tools
│   ├── kb_cli.py (360 lines)
│   └── test_connection.py (150 lines)
│
├── Documentation
│   ├── README.md (350 lines)
│   ├── QUICKSTART.md (250 lines)
│   └── PROJECT_SUMMARY.md (this file)
│
├── Examples
│   ├── example_usage.py (200 lines)
│   └── examples/
│       ├── README.md
│       ├── table_data.example.json
│       └── table_schema.example.json
│
└── Configuration
    ├── requirements.txt
    ├── config.example.json
    └── .gitignore
```

## Technical Details

### Dependencies
- **requests**: HTTP library for API calls
- **Python 3.7+**: Minimum Python version

### Error Handling
The library includes comprehensive error handling:
- File not found errors
- HTTP errors with status codes
- Authentication failures
- JSON parsing errors
- API rate limiting

### Response Format
All API methods return dictionaries with this general structure:
```python
{
    "data": {
        "documentID": "abc123",
        "name": "Document Name",
        "type": "file",
        "status": "uploaded"
    }
}
```

Query responses include:
```python
{
    "output": "Synthesized answer...",
    "chunks": [
        {
            "content": "Relevant text...",
            "score": 0.95
        }
    ]
}
```

## Best Practices

1. **Use Metadata**: Organize documents with consistent metadata schemas
2. **Searchable Fields**: Mark important table fields as searchable
3. **Test Queries**: Verify uploads with test queries
4. **Version Control**: Track document versions in metadata
5. **Descriptive Names**: Use clear, searchable document names

## Extending the Library

The code is well-structured for extensions:

```python
class VoiceflowKB:
    def __init__(self, api_key, project_id):
        # Initialize
    
    def your_custom_method(self, ...):
        # Add custom functionality
        url = f"{self.base_url}/your/endpoint"
        response = requests.post(url, headers=self.headers, json=data)
        return response.json()
```

## Support & Resources

- **Documentation**: See README.md for complete API reference
- **Quick Start**: See QUICKSTART.md for getting started
- **Examples**: See example_usage.py for code examples
- **Voiceflow Docs**: https://developer.voiceflow.com/
- **Community**: https://discord.gg/voiceflow

## Version Information

- **Created**: October 2025
- **API Version**: Voiceflow Knowledge Base API v1
- **Python Version**: 3.7+

## Notes

- Tags API was deprecated in July 2025; use metadata instead
- Some endpoints may have rate limits
- Large files may take time to process
- Document IDs are required for update/delete operations

## Future Enhancements

Potential additions to consider:
- Batch upload operations
- Progress bars for large uploads
- Async operations for better performance
- Export functionality
- Document comparison tools
- Analytics and reporting

## License

Open source - free to use and modify for your Voiceflow projects.

---

**Ready to go!** Start with `python test_connection.py` to verify everything works, then explore the examples.

For detailed usage, see:
- `README.md` - Full documentation
- `QUICKSTART.md` - Quick start guide
- `example_usage.py` - Code examples

