# Quick Start Guide

Get up and running with the Voiceflow Knowledge Base Manager in 5 minutes!

## 1. Install Dependencies

```bash
pip install -r requirements.txt
```

## 2. Verify Your Credentials

Your project is already configured with:
- **Project ID**: `66aeff0ea380c590e96e8e70`
- **API Key**: `VF.DM.68e6a156911014714892eee8.Yeb3HK3luekO31gR`

These are embedded in the scripts, but you can override them with command-line arguments if needed.

## 3. Test the Connection

Try a simple query to verify everything works:

```bash
python kb_cli.py query "Hello, are you working?"
```

Expected output: A response with any relevant information from your knowledge base.

## 4. Upload Your First Document

### Option A: Upload a File

```bash
# Upload a PDF, TXT, or DOCX file
python kb_cli.py upload-file your_document.pdf \
  --metadata '{"category": "documentation", "version": "1.0"}'
```

### Option B: Upload a URL

```bash
# Add a webpage to your knowledge base
python kb_cli.py upload-url "https://www.voiceflow.com/features" \
  --name "Voiceflow Features Page" \
  --metadata '{"source": "website"}'
```

### Option C: Upload Table Data

```bash
# Use the provided example files
python kb_cli.py upload-table "Product Catalog" \
  --data-file examples/table_data.example.json \
  --schema-file examples/table_schema.example.json \
  --metadata '{"type": "catalog"}'
```

## 5. Query Your Knowledge Base

After uploading content, try querying it:

```bash
# Simple query
python kb_cli.py query "What products do you have?"

# Query with JSON output
python kb_cli.py query "Tell me about premium widgets" --format json

# Query with more results
python kb_cli.py query "Show me everything about services" --limit 10
```

## 6. Manage Your Documents

### List all documents

```bash
python kb_cli.py list
```

### Get document details

```bash
# Replace <doc-id> with an actual document ID from the list
python kb_cli.py get <doc-id>
```

### Update a document

```bash
# Replace <doc-id> with the document you want to update
python kb_cli.py update <doc-id> new_version.pdf \
  --metadata '{"version": "2.0"}'
```

### Delete a document

```bash
# Replace <doc-id> with the document you want to delete
python kb_cli.py delete <doc-id>

# Skip confirmation prompt
python kb_cli.py delete <doc-id> --confirm
```

## 7. Use in Python Scripts

```python
from voiceflow_kb import VoiceflowKB

# Initialize
kb = VoiceflowKB(
    api_key="VF.DM.68e6a156911014714892eee8.Yeb3HK3luekO31gR",
    project_id="66aeff0ea380c590e96e8e70"
)

# Upload
result = kb.upload_document("document.pdf")
doc_id = result['data']['documentID']
print(f"Uploaded: {doc_id}")

# Query
answer = kb.query("What is this document about?")
print(answer['output'])

# Clean up
kb.delete_document(doc_id)
```

## Common Use Cases

### Use Case 1: Documentation Upload

Upload your product documentation:

```bash
python kb_cli.py upload-file user_manual.pdf \
  --metadata '{"category": "manual", "product": "widget", "version": "1.0"}'
  
python kb_cli.py upload-file api_docs.pdf \
  --metadata '{"category": "technical", "product": "api", "version": "2.0"}'
```

Query with filters:

```bash
python kb_cli.py query "How do I use the API?" \
  --metadata '{"$eq": {"category": "technical"}}'
```

### Use Case 2: Product Catalog

Upload your product catalog and query it:

```bash
# Upload the example table
python kb_cli.py upload-table "Products" \
  --data-file examples/table_data.example.json \
  --schema-file examples/table_schema.example.json

# Query products
python kb_cli.py query "Show me premium products under $50"
python kb_cli.py query "What's the best rated product?"
python kb_cli.py query "Do you have any service plans?"
```

### Use Case 3: Website Content

Index multiple pages from your website:

```bash
python kb_cli.py upload-url "https://example.com/about" --name "About Us"
python kb_cli.py upload-url "https://example.com/pricing" --name "Pricing"
python kb_cli.py upload-url "https://example.com/support" --name "Support"
```

### Use Case 4: FAQ Management

Create a FAQ table:

```python
import json
from voiceflow_kb import VoiceflowKB

kb = VoiceflowKB(
    api_key="VF.DM.68e6a156911014714892eee8.Yeb3HK3luekO31gR",
    project_id="66aeff0ea380c590e96e8e70"
)

faq_schema = {
    "question": {"type": "string", "searchable": True},
    "answer": {"type": "string", "searchable": True},
    "category": {"type": "string", "searchable": False}
}

faq_data = [
    {
        "question": "What are your business hours?",
        "answer": "We're open Monday-Friday, 9am-5pm EST",
        "category": "general"
    },
    {
        "question": "How do I return a product?",
        "answer": "Visit our returns page or contact support within 30 days",
        "category": "returns"
    }
]

result = kb.upload_table("FAQ", faq_data, faq_schema)
print(f"FAQ uploaded: {result['data']['documentID']}")
```

## Troubleshooting

### Issue: "Authentication failed"
- Verify your API key is correct
- Check that your API key starts with `VF.DM.`
- Ensure your project ID is correct

### Issue: "File not found"
- Use absolute paths or make sure you're in the right directory
- Check file permissions

### Issue: "Invalid JSON in metadata"
- Make sure your JSON is properly formatted
- Use single quotes around the JSON and double quotes inside: `'{"key": "value"}'`

### Issue: Query returns no results
- Make sure you've uploaded documents first
- Try a broader query
- Check that your documents have been processed (may take a few moments)

## Next Steps

1. Check out `example_usage.py` for more Python examples
2. Read the full `README.md` for detailed API documentation
3. Explore the `examples/` directory for table upload templates
4. Create your own metadata schemas for better organization
5. Integrate the library into your Voiceflow assistant

## Tips for Success

1. **Use Metadata**: Organize documents with consistent metadata schemas
2. **Searchable Fields**: Mark important fields as searchable in table schemas
3. **Descriptive Names**: Give documents clear, descriptive names
4. **Test Queries**: After uploading, test various queries to ensure good results
5. **Update Regularly**: Keep your knowledge base fresh by updating outdated documents

## Need Help?

- Check the main `README.md` for full documentation
- Review `example_usage.py` for code examples
- Visit [Voiceflow Documentation](https://developer.voiceflow.com/)
- Join the [Voiceflow Discord](https://discord.gg/voiceflow)

---

Happy knowledge base building! 🚀

