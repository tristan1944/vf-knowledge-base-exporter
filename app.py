from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
import os
import json
from voiceflow_kb import VoiceflowKB
import db
import helpers


app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'dev-secret')


def get_kb() -> VoiceflowKB:
    api_key = os.environ.get('VF_API_KEY', 'VF.DM.68ec4148e1ae57b065368bde.OZyVatxIGZnrMWce')
    project_id = os.environ.get('VF_PROJECT_ID', '68e56f7170abdf09f66dc756')
    return VoiceflowKB(api_key, project_id)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/set-creds', methods=['POST'])
def set_creds():
    os.environ['VF_API_KEY'] = request.form.get('api_key', '').strip()
    os.environ['VF_PROJECT_ID'] = request.form.get('project_id', '').strip()
    flash('Credentials updated for this session', 'success')
    return redirect(url_for('index'))


@app.route('/list')
def list_docs():
    kb = get_kb()
    try:
        docs = kb.list_documents(limit=50).get('data', [])
    except Exception as e:
        flash(f'Error listing documents: {e}', 'error')
        docs = []
    return render_template('list.html', docs=docs)


@app.route('/query', methods=['POST'])
def do_query():
    question = request.form.get('question', '')
    kb = get_kb()
    try:
        result = kb.query(question=question, chunkLimit=5, synthesis=True)
        return render_template('query.html', question=question, result=result)
    except Exception as e:
        flash(f'Query error: {e}', 'error')
        return redirect(url_for('index'))


@app.route('/upload/file', methods=['POST'])
def upload_file():
    kb = get_kb()
    f = request.files.get('file')
    metadata_raw = request.form.get('metadata')
    overwrite = request.form.get('overwrite') == 'on'
    max_chunk_size = request.form.get('max_chunk_size')
    
    metadata = None
    if metadata_raw:
        try:
            metadata = json.loads(metadata_raw)
        except Exception:
            flash('Invalid metadata JSON', 'error')
            return redirect(url_for('index'))
    
    if not f or f.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('index'))
    
    filename = secure_filename(f.filename)
    tmp_path = os.path.join('tmp', filename)
    os.makedirs('tmp', exist_ok=True)
    f.save(tmp_path)
    try:
        mcs = int(max_chunk_size) if max_chunk_size else None
        res = kb.upload_document(tmp_path, metadata=metadata, overwrite=overwrite, max_chunk_size=mcs)
        flash(f"Uploaded file. documentID: {res['data']['documentID']}", 'success')
    except Exception as e:
        flash(f'Upload error: {e}', 'error')
    finally:
        try:
            os.remove(tmp_path)
        except Exception:
            pass
    return redirect(url_for('list_docs'))


@app.route('/upload/url', methods=['POST'])
def upload_url():
    kb = get_kb()
    url = request.form.get('url')
    name = request.form.get('name') or None
    metadata_raw = request.form.get('metadata')
    overwrite = request.form.get('overwrite') == 'on'
    max_chunk_size = request.form.get('max_chunk_size')
    
    metadata = None
    if metadata_raw:
        try:
            metadata = json.loads(metadata_raw)
        except Exception:
            flash('Invalid metadata JSON', 'error')
            return redirect(url_for('index'))
    
    if not url:
        flash('URL is required', 'error')
        return redirect(url_for('index'))
    
    try:
        mcs = int(max_chunk_size) if max_chunk_size else None
        res = kb.upload_url(url, name=name, metadata=metadata, overwrite=overwrite, max_chunk_size=mcs)
        flash(f"Uploaded URL. documentID: {res['data']['documentID']}", 'success')
    except Exception as e:
        flash(f'Upload error: {e}', 'error')
    return redirect(url_for('list_docs'))


@app.route('/upload/table', methods=['POST'])
def upload_table():
    kb = get_kb()
    name = request.form.get('name')
    schema_raw = request.form.get('schema')
    items_raw = request.form.get('items')
    metadata_raw = request.form.get('metadata')
    overwrite = request.form.get('overwrite') == 'on'
    max_chunk_size = request.form.get('max_chunk_size')
    
    if not name:
        flash('Table name is required', 'error')
        return redirect(url_for('index'))
    
    try:
        schema_in = json.loads(schema_raw) if schema_raw else {}
        # Accept simple schema format: { field: { type, searchable? } }
        schema = {}
        for k, v in schema_in.items():
            schema[k] = { 'type': v.get('type'), 'searchable': v.get('searchable', False) }
        
        items = json.loads(items_raw) if items_raw else []
        metadata = json.loads(metadata_raw) if metadata_raw else None
    except Exception:
        flash('Invalid JSON in schema/items/metadata', 'error')
        return redirect(url_for('index'))
    
    try:
        mcs = int(max_chunk_size) if max_chunk_size else None
        res = kb.upload_table(name, items, schema, metadata=metadata, overwrite=overwrite, max_chunk_size=mcs)
        flash(f"Uploaded table. documentID: {res['data']['documentID']}", 'success')
    except Exception as e:
        flash(f'Upload error: {e}', 'error')
    return redirect(url_for('list_docs'))


@app.route('/delete/<document_id>', methods=['POST'])
def delete_document(document_id):
    kb = get_kb()
    try:
        # Get document info before deleting
        doc_info = kb.get_document(document_id)
        
        # Backup the document
        db.backup_document(document_id, doc_info.get('data', {}))
        
        # Delete from Voiceflow
        kb.delete_document(document_id)
        
        # Log the operation
        db.log_operation(
            operation_type='delete',
            document_id=document_id,
            document_name=doc_info.get('data', {}).get('name', 'Unknown'),
            status='success'
        )
        
        flash(f'Document {document_id} deleted and backed up successfully', 'success')
    except Exception as e:
        db.log_operation(
            operation_type='delete',
            document_id=document_id,
            status='error',
            error_message=str(e)
        )
        flash(f'Delete error: {e}', 'error')
    
    return redirect(url_for('list_docs'))


@app.route('/backups')
def view_backups():
    deleted_docs = db.get_deleted_documents(limit=100)
    return render_template('backups.html', deleted_docs=deleted_docs)


@app.route('/operations')
def view_operations():
    operations = db.get_operations(limit=100)
    return render_template('operations.html', operations=operations)


@app.route('/api/suggest-metadata', methods=['POST'])
def suggest_metadata():
    """API endpoint to get metadata suggestions"""
    data = request.get_json()
    file_name = data.get('filename')
    url = data.get('url')
    table_name = data.get('table_name')
    
    suggestions = helpers.generate_metadata_suggestions(
        file_path=file_name,
        url=url,
        table_name=table_name
    )
    
    return jsonify(suggestions)


@app.route('/api/suggest-chunk-size', methods=['POST'])
def suggest_chunk_size():
    """API endpoint to get chunk size suggestion"""
    data = request.get_json()
    content_length = data.get('content_length')
    doc_type = data.get('document_type', 'general')
    
    suggested_size = helpers.calculate_optimal_chunk_size(
        content_length=content_length,
        document_type=doc_type
    )
    
    return jsonify({'suggested_chunk_size': suggested_size})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', '5000'))
    app.run(host='127.0.0.1', port=port, debug=True)


