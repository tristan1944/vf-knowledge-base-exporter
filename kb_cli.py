#!/usr/bin/env python3
"""
Voiceflow Knowledge Base CLI

A command-line interface for managing your Voiceflow Knowledge Base.
"""

import argparse
import os
import json
import sys
from pathlib import Path
from voiceflow_kb import VoiceflowKB


# Default credentials (can be overridden with env or CLI)
DEFAULT_API_KEY = os.environ.get("VF_API_KEY", "VF.DM.68e6a156911014714892eee8.Yeb3HK3luekO31gR")
DEFAULT_PROJECT_ID = os.environ.get("VF_PROJECT_ID", "68e56f7170abdf09f66dc756")


def upload_file_cmd(args, kb):
    """Upload a file to the knowledge base"""
    metadata = json.loads(args.metadata) if args.metadata else None
    
    try:
        result = kb.upload_document(
            file_path=args.file,
            metadata=metadata
        )
        doc_id = result.get('data', {}).get('documentID')
        print(f"✓ File uploaded successfully!")
        print(f"  Document ID: {doc_id}")
        if args.verbose:
            print(f"  Full response: {json.dumps(result, indent=2)}")
    except Exception as e:
        print(f"✗ Error uploading file: {e}", file=sys.stderr)
        sys.exit(1)


def upload_url_cmd(args, kb):
    """Upload a URL to the knowledge base"""
    metadata = json.loads(args.metadata) if args.metadata else None
    
    try:
        result = kb.upload_url(
            url=args.url,
            name=args.name,
            metadata=metadata
        )
        doc_id = result.get('data', {}).get('documentID')
        print(f"✓ URL uploaded successfully!")
        print(f"  Document ID: {doc_id}")
        if args.verbose:
            print(f"  Full response: {json.dumps(result, indent=2)}")
    except Exception as e:
        print(f"✗ Error uploading URL: {e}", file=sys.stderr)
        sys.exit(1)


def upload_table_cmd(args, kb):
    """Upload table data to the knowledge base"""
    try:
        # Load data and schema from JSON files
        with open(args.data_file, 'r') as f:
            data = json.load(f)
        
        with open(args.schema_file, 'r') as f:
            schema = json.load(f)
        
        metadata = json.loads(args.metadata) if args.metadata else None
        
        result = kb.upload_table(
            name=args.name,
            data=data,
            schema=schema,
            metadata=metadata
        )
        doc_id = result.get('data', {}).get('documentID')
        print(f"✓ Table uploaded successfully!")
        print(f"  Document ID: {doc_id}")
        if args.verbose:
            print(f"  Full response: {json.dumps(result, indent=2)}")
    except Exception as e:
        print(f"✗ Error uploading table: {e}", file=sys.stderr)
        sys.exit(1)


def query_cmd(args, kb):
    """Query the knowledge base"""
    metadata = json.loads(args.metadata) if args.metadata else None
    
    try:
        result = kb.query(
            question=args.question,
            chunkLimit=args.limit,
            synthesis=not args.no_synthesis,
            metadata=metadata
        )
        
        if args.output_format == 'json':
            print(json.dumps(result, indent=2))
        else:
            # Human-readable format
            print("\n" + "="*60)
            print(f"Question: {args.question}")
            print("="*60)
            
            if result.get('output'):
                print(f"\n📝 Answer:\n{result['output']}\n")
            
            if result.get('chunks'):
                print(f"📚 Found {len(result['chunks'])} relevant chunks:\n")
                for i, chunk in enumerate(result['chunks'], 1):
                    print(f"  [{i}] Score: {chunk.get('score', 'N/A')}")
                    content = chunk.get('content', '')
                    # Truncate long content
                    if len(content) > 200 and not args.verbose:
                        content = content[:200] + '...'
                    print(f"      {content}")
                    print()
    except Exception as e:
        print(f"✗ Error querying knowledge base: {e}", file=sys.stderr)
        sys.exit(1)


def get_document_cmd(args, kb):
    """Get document details"""
    try:
        result = kb.get_document(args.document_id)
        
        if args.output_format == 'json':
            print(json.dumps(result, indent=2))
        else:
            data = result.get('data', {})
            print(f"\n📄 Document Details:")
            print(f"  ID: {data.get('documentID')}")
            print(f"  Name: {data.get('name')}")
            print(f"  Type: {data.get('type')}")
            print(f"  Status: {data.get('status')}")
            if data.get('metadata'):
                print(f"  Metadata: {json.dumps(data.get('metadata'), indent=4)}")
    except Exception as e:
        print(f"✗ Error getting document: {e}", file=sys.stderr)
        sys.exit(1)


def delete_document_cmd(args, kb):
    """Delete a document"""
    if not args.confirm:
        response = input(f"Are you sure you want to delete document {args.document_id}? (yes/no): ")
        if response.lower() not in ['yes', 'y']:
            print("Deletion cancelled.")
            return
    
    try:
        result = kb.delete_document(args.document_id)
        print(f"✓ Document {args.document_id} deleted successfully!")
        if args.verbose:
            print(f"  Full response: {json.dumps(result, indent=2)}")
    except Exception as e:
        print(f"✗ Error deleting document: {e}", file=sys.stderr)
        sys.exit(1)


def update_document_cmd(args, kb):
    """Update a document"""
    metadata = json.loads(args.metadata) if args.metadata else None
    
    try:
        result = kb.update_document(
            document_id=args.document_id,
            file_path=args.file,
            metadata=metadata
        )
        print(f"✓ Document {args.document_id} updated successfully!")
        if args.verbose:
            print(f"  Full response: {json.dumps(result, indent=2)}")
    except Exception as e:
        print(f"✗ Error updating document: {e}", file=sys.stderr)
        sys.exit(1)


def list_documents_cmd(args, kb):
    """List all documents"""
    try:
        result = kb.list_documents(limit=args.limit, offset=args.offset)
        
        if args.output_format == 'json':
            print(json.dumps(result, indent=2))
        else:
            docs = result.get('data', [])
            print(f"\n📚 Documents (showing {len(docs)}):\n")
            for doc in docs:
                print(f"  • {doc.get('name', 'Unnamed')}")
                print(f"    ID: {doc.get('documentID')}")
                print(f"    Type: {doc.get('type')}")
                print()
    except Exception as e:
        print(f"✗ Error listing documents: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Voiceflow Knowledge Base CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Global arguments
    parser.add_argument('--api-key', default=DEFAULT_API_KEY,
                       help='Voiceflow API Key (default: from script)')
    parser.add_argument('--project-id', default=DEFAULT_PROJECT_ID,
                       help='Voiceflow Project ID (default: from script)')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Verbose output')
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Upload file command
    upload_file = subparsers.add_parser('upload-file', help='Upload a file')
    upload_file.add_argument('file', help='Path to file to upload')
    upload_file.add_argument('--metadata', help='Metadata as JSON string')
    
    # Upload URL command
    upload_url = subparsers.add_parser('upload-url', help='Upload a URL')
    upload_url.add_argument('url', help='URL to upload')
    upload_url.add_argument('--name', help='Name for the document')
    upload_url.add_argument('--metadata', help='Metadata as JSON string')
    
    # Upload table command
    upload_table = subparsers.add_parser('upload-table', help='Upload table data')
    upload_table.add_argument('name', help='Name for the table')
    upload_table.add_argument('--data-file', required=True, help='JSON file with table data')
    upload_table.add_argument('--schema-file', required=True, help='JSON file with table schema')
    upload_table.add_argument('--metadata', help='Metadata as JSON string')
    
    # Query command
    query = subparsers.add_parser('query', help='Query the knowledge base')
    query.add_argument('question', help='Question to ask')
    query.add_argument('--limit', type=int, default=5, help='Max chunks to return')
    query.add_argument('--no-synthesis', action='store_true', help='Disable answer synthesis')
    query.add_argument('--metadata', help='Metadata filter as JSON string')
    query.add_argument('--format', dest='output_format', choices=['text', 'json'], 
                      default='text', help='Output format')
    
    # Get document command
    get_doc = subparsers.add_parser('get', help='Get document details')
    get_doc.add_argument('document_id', help='Document ID')
    get_doc.add_argument('--format', dest='output_format', choices=['text', 'json'],
                        default='text', help='Output format')
    
    # Delete document command
    delete_doc = subparsers.add_parser('delete', help='Delete a document')
    delete_doc.add_argument('document_id', help='Document ID to delete')
    delete_doc.add_argument('--confirm', action='store_true', help='Skip confirmation')
    
    # Update document command
    update_doc = subparsers.add_parser('update', help='Update a document')
    update_doc.add_argument('document_id', help='Document ID to update')
    update_doc.add_argument('file', help='Path to new file')
    update_doc.add_argument('--metadata', help='Metadata as JSON string')
    
    # List documents command
    list_docs = subparsers.add_parser('list', help='List all documents')
    list_docs.add_argument('--limit', type=int, default=50, help='Number of documents to return')
    list_docs.add_argument('--offset', type=int, default=0, help='Offset for pagination')
    list_docs.add_argument('--format', dest='output_format', choices=['text', 'json'],
                          default='text', help='Output format')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Initialize KB manager
    kb = VoiceflowKB(args.api_key, args.project_id)
    
    # Route to appropriate command handler
    commands = {
        'upload-file': upload_file_cmd,
        'upload-url': upload_url_cmd,
        'upload-table': upload_table_cmd,
        'query': query_cmd,
        'get': get_document_cmd,
        'delete': delete_document_cmd,
        'update': update_document_cmd,
        'list': list_documents_cmd
    }
    
    handler = commands.get(args.command)
    if handler:
        handler(args, kb)
    else:
        print(f"Unknown command: {args.command}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

