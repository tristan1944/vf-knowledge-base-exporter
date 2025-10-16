# Example Files

This directory contains example files for using the Voiceflow Knowledge Base Manager.

## Table Upload Examples

### `table_data.example.json`
Example data for uploading a product catalog table. This file contains sample product information including IDs, names, prices, descriptions, and metadata.

### `table_schema.example.json`
Schema definition for the product catalog table. Defines field types and searchability settings.

### Usage

To upload the example table:

```bash
python ../kb_cli.py upload-table "Product Catalog" \
  --data-file examples/table_data.example.json \
  --schema-file examples/table_schema.example.json \
  --metadata '{"type": "catalog", "version": "1.0"}'
```

Or in Python:

```python
import json
from voiceflow_kb import VoiceflowKB

kb = VoiceflowKB("YOUR_API_KEY", "YOUR_PROJECT_ID")

# Load the example files
with open('examples/table_data.example.json') as f:
    data = json.load(f)

with open('examples/table_schema.example.json') as f:
    schema = json.load(f)

# Upload the table
result = kb.upload_table(
    name="Product Catalog",
    data=data,
    schema=schema,
    metadata={"type": "catalog", "version": "1.0"}
)

print(f"Table uploaded! Document ID: {result['data']['documentID']}")
```

## Schema Field Types

The schema supports the following field types:

- `string` - Text data
- `number` - Numeric data (integers or floats)
- `boolean` - True/False values
- `array` - Lists of values
- `object` - Nested JSON objects

## Searchable Fields

Set `"searchable": true` for fields that should be:
- Included in semantic search
- Used for query matching
- Returned in search results

Set `"searchable": false` for metadata fields that should:
- Be stored but not searched
- Remain in the document for reference
- Not affect search relevance

## Creating Your Own Tables

1. Create a JSON file with your data (array of objects)
2. Create a schema file defining the structure
3. Ensure all data rows match the schema
4. Upload using the CLI or Python library

Example for a FAQ table:

**faq_data.json:**
```json
[
  {
    "question": "What are your business hours?",
    "answer": "We're open Monday-Friday, 9am-5pm EST",
    "category": "general"
  },
  {
    "question": "How do I reset my password?",
    "answer": "Click 'Forgot Password' on the login page",
    "category": "account"
  }
]
```

**faq_schema.json:**
```json
{
  "question": {"type": "string", "searchable": true},
  "answer": {"type": "string", "searchable": true},
  "category": {"type": "string", "searchable": false}
}
```

