import os
import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory, flash
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.utils import secure_filename
DATA_FOLDER = os.path.join(APP_ROOT, 'data')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DATA_FOLDER, exist_ok=True)

VERSIONS_FILE = os.path.join(DATA_FOLDER, 'versions.json')
SUGGESTIONS_FILE = os.path.join(DATA_FOLDER, 'suggestions.json')

ADMIN_USER = 'tenma'
ADMIN_PASS = 'deyvison'

ALLOWED_EXT = {'zip'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'mude-esta-chave-em-producao'
import os
import json
from datetime import datetime
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    send_from_directory,
    flash,
)
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'uploads')
DATA_FOLDER = os.path.join(APP_ROOT, 'data')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DATA_FOLDER, exist_ok=True)

VERSIONS_FILE = os.path.join(DATA_FOLDER, 'versions.json')
SUGGESTIONS_FILE = os.path.join(DATA_FOLDER, 'suggestions.json')

ADMIN_USER = os.environ.get('ADMIN_USER', 'tenma')
ADMIN_PASS = os.environ.get('ADMIN_PASS', 'deyvison')

ALLOWED_EXT = {'zip'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# use environment secret if provided
app.secret_key = os.environ.get('SECRET_KEY', 'mude-esta-chave-em-producao')
# Limite máximo de upload: 1 GB
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024 * 1024


def read_json(path, default):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return default


def write_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT


@app.errorhandler(RequestEntityTooLarge)
def handle_file_too_large(error):
    flash('Arquivo muito grande. O limite é de 1 GB. Envie um arquivo menor.', 'danger')
    return redirect(request.referrer or url_for('admin_dashboard'))


@app.route('/')
def index():
    versions = read_json(VERSIONS_FILE, [])
    latest = versions[-1] if versions else None
    return render_template('index.html', latest=latest)


@app.route('/download')
def download():
    versions = read_json(VERSIONS_FILE, [])
    if not versions:
        flash('Nenhuma textura disponível para download.', 'warning')
        return redirect(url_for('index'))
    latest = versions[-1]
    return send_from_directory(app.config['UPLOAD_FOLDER'], latest['filename'], as_attachment=True)


@app.route('/suggest', methods=['GET', 'POST'])
def suggest():
    if request.method == 'POST':
        text = request.form.get('suggestion', '').strip()
        if not text:
            flash('Sugestão vazia não enviada.', 'warning')
            return redirect(url_for('suggest'))
        suggestions = read_json(SUGGESTIONS_FILE, [])
        suggestions.append({'text': text, 'at': datetime.utcnow().isoformat()})
        write_json(SUGGESTIONS_FILE, suggestions)
        flash('Obrigado pela sugestão!', 'success')
        return redirect(url_for('suggest'))
    return render_template('suggest.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        user = request.form.get('username')
        pwd = request.form.get('password')
        if user == ADMIN_USER and pwd == ADMIN_PASS:
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        flash('Credenciais inválidas', 'danger')
    return render_template('admin_login.html')


def admin_required(f):
    from functools import wraps

    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)

    return decorated


@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('index'))


@app.route('/admin')
@admin_required
def admin_dashboard():
    versions = read_json(VERSIONS_FILE, [])
    suggestions = read_json(SUGGESTIONS_FILE, [])
    return render_template('admin_dashboard.html', versions=versions, suggestions=suggestions)


@app.route('/admin/upload', methods=['POST'])
@admin_required
def admin_upload():
    texture_name = request.form.get('texture_name', 'Tenma').strip()
    version = request.form.get('version', '').strip()
    file = request.files.get('file')
    if not file or not allowed_file(file.filename):
        flash('Envie um arquivo .zip válido.', 'danger')
        return redirect(url_for('admin_dashboard'))
    filename = secure_filename(file.filename)
    ts = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    stored = f"{os.path.splitext(filename)[0]}_{ts}.zip"
    path = os.path.join(app.config['UPLOAD_FOLDER'], stored)
    file.save(path)
    versions = read_json(VERSIONS_FILE, [])
    versions.append({'name': texture_name, 'version': version, 'filename': stored, 'uploaded_at': datetime.utcnow().isoformat()})
    write_json(VERSIONS_FILE, versions)
    flash('Textura enviada com sucesso.', 'success')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/suggestions/delete/<int:idx>', methods=['POST'])
@admin_required
def delete_suggestion(idx):
    suggestions = read_json(SUGGESTIONS_FILE, [])
    if 0 <= idx < len(suggestions):
        suggestions.pop(idx)
        write_json(SUGGESTIONS_FILE, suggestions)
        flash('Sugestão removida.', 'success')
    return redirect(url_for('admin_dashboard'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
    'updated_at': '',
    'filename': ''
}
if not os.path.exists(METADATA_FILE):
    write_json(METADATA_FILE, default_metadata)
if not os.path.exists(SUGGESTIONS_FILE):
    write_json(SUGGESTIONS_FILE, [])


@app.route('/')
def index():
    meta = read_json(METADATA_FILE, default_metadata)
    # Serve static index.html; inject metadata via a tiny template
    with open(os.path.join(app.static_folder, 'index.html'), 'r', encoding='utf-8') as f:
        html = f.read()
    html = html.replace('<!--METADATA-->', json.dumps(meta))
    return render_template_string(html)


@app.route('/about')
def about():
    return app.send_static_file('about.html')


@app.route('/suggestions')
def suggestions_page():
    return app.send_static_file('suggestions.html')


@app.route('/api/suggest', methods=['POST'])
def api_suggest():
    data = read_json(SUGGESTIONS_FILE, [])
    text = request.form.get('text', '').strip()
    if text:
        data.append({'text': text, 'at': datetime.utcnow().isoformat()})
        write_json(SUGGESTIONS_FILE, data)
        return jsonify({'ok': True})
    return jsonify({'ok': False, 'error': 'empty'})


@app.route('/download')
def download():
    meta = read_json(METADATA_FILE, default_metadata)
    fname = meta.get('filename')
    if not fname:
        return 'Nenhum arquivo disponível', 404
    return send_from_directory(UPLOAD_FOLDER, fname, as_attachment=True)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('username')
        pwd = request.form.get('password')
        if user == ADMIN_USER and pwd == ADMIN_PASS:
            session['admin'] = True
            return redirect(url_for('admin'))
        return 'Credenciais inválidas', 403
    return app.send_static_file('login.html')


@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('index'))


def admin_required(fn):
    from functools import wraps

    @wraps(fn)
    def wrapper(*a, **k):
        if not session.get('admin'):
            return redirect(url_for('login'))
        return fn(*a, **k)

    return wrapper


@app.route('/admin')
@admin_required
def admin():
    return app.send_static_file('admin.html')


@app.route('/admin/upload', methods=['POST'])
@admin_required
def admin_upload():
    file = request.files.get('texture_zip')
    name = request.form.get('name', 'Tenma')
    version = request.form.get('version', '')
    release_time = request.form.get('release_time', '')
    if not file:
        return 'Nenhum arquivo', 400
    # save file
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    safe_name = f"{timestamp}_{file.filename}"
    path = os.path.join(UPLOAD_FOLDER, safe_name)
    file.save(path)
    # update metadata
    meta = {
        'name': name,
        'version': version or read_json(METADATA_FILE, default_metadata).get('version', ''),
        'updated_at': release_time or datetime.utcnow().isoformat(),
        'filename': safe_name
    }
    write_json(METADATA_FILE, meta)
    return redirect(url_for('admin'))


@app.route('/admin/suggestions')
@admin_required
def admin_suggestions():
    data = read_json(SUGGESTIONS_FILE, [])
    return jsonify(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
