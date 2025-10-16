# Voiceflow Knowledge Base Manager

A Python library for managing documents in your Voiceflow Knowledge Base. Upload, query, update, and delete documents with ease.

## Features

- 📤 **Upload Documents**: Support for PDF, TXT, DOCX, URLs, and tabular data
- 🔍 **Query Knowledge Base**: Search and retrieve relevant information with optional filtering
- ✏️ **Update Documents**: Replace existing documents with new versions
- 🗑️ **Delete Documents**: Remove documents from your knowledge base
- 🏷️ **Metadata Support**: Organize documents with custom metadata fields
- 📊 **Table Support**: Upload structured data with customizable schemas

## Installation

1. Clone or download this repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Test your connection:

```bash
python test_connection.py
```

This will verify your API credentials and connection to Voiceflow.

## Quick Start

### Python Library

```python
from voiceflow_kb import VoiceflowKB

# Initialize with your credentials
kb = VoiceflowKB(
    api_key="VF.DM.your-api-key",
    project_id="your-project-id"
)

# Upload a document
result = kb.upload_document(
    file_path="example.pdf",
    metadata={"category": "documentation"}
)

# Query the knowledge base
answer = kb.query(
    question="What are your business hours?",
    chunkLimit=5
)
print(answer['output'])
```

### Command Line Interface

```bash
# Query the knowledge base
python kb_cli.py query "What are your business hours?"

# Upload a file
python kb_cli.py upload-file document.pdf --metadata '{"category": "support"}'

# Upload a URL
python kb_cli.py upload-url "https://example.com/help" --name "Help Page"

# List all documents
python kb_cli.py list

# Get document details
python kb_cli.py get <document-id>

# Delete a document
python kb_cli.py delete <document-id>
```

## Configuration

Your credentials are configured in the example files:
- **Project ID**: `66aeff0ea380c590e96e8e70`
- **API Key**: `VF.DM.68e6a156911014714892eee8.Yeb3HK3luekO31gR`

⚠️ **Security Note**: In production, store credentials in environment variables or a secure configuration file, not in your code.

## API Methods

### Upload Methods

#### `upload_document(file_path, tags=None, metadata=None)`
Upload a file (PDF, TXT, DOCX) to the knowledge base.

```python
result = kb.upload_document(
    file_path="documentation.pdf",
    metadata={
        "category": "user-guide",
        "version": "1.0"
    }
)
```

#### `upload_url(url, name=None, tags=None, metadata=None)`
Upload a URL to the knowledge base.

```python
result = kb.upload_url(
    url="https://example.com/help",
    name="Help Center",
    metadata={"source": "website"}
)
```

#### `upload_table(name, data, schema, tags=None, metadata=None)`
Upload structured table data.

```python
schema = {
    "id": {"type": "number", "searchable": True},
    "name": {"type": "string", "searchable": True},
    "description": {"type": "string", "searchable": True}
}

data = [
    {"id": 1, "name": "Product A", "description": "Great product"},
    {"id": 2, "name": "Product B", "description": "Better product"}
]

result = kb.upload_table(
    name="Product Catalog",
    data=data,
    schema=schema,
    metadata={"type": "catalog"}
)
```

### Query Methods

#### `query(question, chunkLimit=5, synthesis=True, temperature=0.1, tags=None, metadata=None)`
Query the knowledge base for information.

```python
# Simple query
result = kb.query("What products do you offer?")

# Query with metadata filter
result = kb.query(
    question="Show me documentation",
    chunkLimit=10,
    metadata={"$eq": {"category": "documentation"}}
)

print(result['output'])  # Synthesized answer
print(result['chunks'])  # Retrieved chunks
```

### Document Management

#### `get_document(document_id)`
Retrieve a document by its ID.

```python
doc = kb.get_document("document-id-here")
print(doc['data']['name'])
```

#### `update_document(document_id, file_path, tags=None, metadata=None)`
Replace an existing document with a new version.

```python
result = kb.update_document(
    document_id="document-id-here",
    file_path="updated_file.pdf",
    metadata={"version": "2.0"}
)
```

#### `delete_document(document_id)`
Delete a document from the knowledge base.

```python
result = kb.delete_document("document-id-here")
```

#### `list_documents(limit=50, offset=0)`
List all documents in the knowledge base.

```python
docs = kb.list_documents(limit=20)
for doc in docs.get('data', []):
    print(f"{doc['name']} - {doc['documentID']}")
```

## Examples

See `example_usage.py` for comprehensive examples of all features:

```bash
python example_usage.py
```

The example file includes:
- Uploading different document types
- Querying with and without filters
- Document CRUD operations
- Table data uploads

## Metadata vs Tags

**Note**: Tags API was deprecated in July 2025. Use `metadata` instead for organizing and filtering documents.

### Metadata Example

```python
# Upload with metadata
kb.upload_document(
    file_path="doc.pdf",
    metadata={
        "category": "support",
        "department": "sales",
        "priority": "high"
    }
)

# Query with metadata filter
kb.query(
    question="Find sales documents",
    metadata={"$eq": {"department": "sales"}}
)
```

### Metadata Filter Operators

- `$eq`: Equality filter `{"$eq": {"category": "support"}}`
- `$ne`: Not equal `{"$ne": {"status": "archived"}}`
- `$in`: In array `{"$in": {"category": ["support", "sales"]}}`
- `$and`: Logical AND for multiple conditions
- `$or`: Logical OR for multiple conditions

## API Endpoints

This library uses the following Voiceflow API endpoints:

- **Document Management**: `https://api.voiceflow.com/v1/knowledge-base/docs/*`
- **Query**: `https://general-runtime.voiceflow.com/knowledge-base/query`

## Error Handling

The library raises exceptions for API errors. Wrap calls in try-except blocks:

```python
try:
    result = kb.upload_document("file.pdf")
except FileNotFoundError:
    print("File not found")
except requests.HTTPError as e:
    print(f"API error: {e}")
```

## Supported File Types

- **Documents**: PDF, TXT, DOCX
- **URLs**: Any valid HTTP/HTTPS URL
- **Tables**: JSON-formatted structured data

## CLI Usage

The project includes a command-line interface (`kb_cli.py`) for easy management:

### Available Commands

```bash
# Query
python kb_cli.py query "Your question here" [--limit 5] [--format json]

# Upload file
python kb_cli.py upload-file path/to/file.pdf [--metadata '{"key": "value"}']

# Upload URL
python kb_cli.py upload-url "https://example.com" [--name "Page Name"]

# Upload table
python kb_cli.py upload-table "Table Name" --data-file data.json --schema-file schema.json

# Get document
python kb_cli.py get <document-id> [--format json]

# Update document
python kb_cli.py update <document-id> path/to/newfile.pdf

# Delete document
python kb_cli.py delete <document-id> [--confirm]

# List documents
python kb_cli.py list [--limit 50] [--offset 0]
```

### CLI Options

- `--api-key`: Override default API key
- `--project-id`: Override default project ID
- `-v, --verbose`: Show detailed output
- `--format`: Output format (text or json)

### Example: Upload and Query

```bash
# Upload a document
python kb_cli.py upload-file support_docs.pdf --metadata '{"category": "support", "version": "1.0"}'

# Query with filter
python kb_cli.py query "How do I reset my password?" --metadata '{"$eq": {"category": "support"}}'

# View in JSON format
python kb_cli.py query "Store hours" --format json
```

## Project Structure

```
vf-knowledge-base-exporter/
├── voiceflow_kb.py          # Main library
├── kb_cli.py                # Command-line interface
├── example_usage.py         # Python usage examples
├── test_connection.py       # Connection test script
├── requirements.txt         # Dependencies
├── config.example.json      # Configuration template
├── .gitignore               # Git ignore rules
├── README.md                # Full documentation (this file)
├── QUICKSTART.md            # Quick start guide
└── examples/                # Example files directory
    ├── README.md            # Examples documentation
    ├── table_data.example.json
    └── table_schema.example.json
```

## Requirements

- Python 3.7+
- requests library

## Authentication

All requests require a Dialog Manager API Key from your Voiceflow project:

1. Go to your Voiceflow project
2. Navigate to **Settings** → **Integration**
3. Copy your API Key (starts with `VF.DM.`)

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License

This project is open source and available for use in your Voiceflow projects.

## Resources

- [Voiceflow Documentation](https://developer.voiceflow.com/)
- [Knowledge Base API Reference](https://developer.voiceflow.com/reference/knowledge-base)
- [Voiceflow Community](https://community.voiceflow.com/)

## Support

For issues with:
- **This library**: Open an issue in this repository
- **Voiceflow API**: Visit [Voiceflow Support](https://help.voiceflow.com/)
- **General Questions**: Join the [Voiceflow Discord](https://discord.gg/voiceflow)

