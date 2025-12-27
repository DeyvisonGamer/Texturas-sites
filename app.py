import os
import json
from datetime import datetime
from urllib.parse import urlparse
from flask import (
    Flask,
    render_template,
    render_template_string,
    request,
    redirect,
    url_for,
    session,
    send_from_directory,
    flash,
)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'uploads')
DATA_FOLDER = os.path.join(APP_ROOT, 'data')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DATA_FOLDER, exist_ok=True)

VERSIONS_FILE = os.path.join(DATA_FOLDER, 'versions.json')
SUGGESTIONS_FILE = os.path.join(DATA_FOLDER, 'suggestions.json')
METADATA_FILE = os.path.join(DATA_FOLDER, 'metadata.json')

ADMIN_USER = os.environ.get('ADMIN_USER', 'tenma')
ADMIN_PASS = os.environ.get('ADMIN_PASS', 'deyvison')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = os.environ.get('SECRET_KEY', 'mude-esta-chave-em-producao')


def read_json(path, default):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return default


def write_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def is_valid_url(url):
    try:
        p = urlparse(url)
        return p.scheme in ("http", "https") and bool(p.netloc)
    except Exception:
        return False


@app.errorhandler(413)
def handle_file_too_large(error):
    flash('Arquivo muito grande ou solicitação inválida.', 'danger')
    return redirect(request.referrer or url_for('admin_dashboard'))


@app.route('/')
def index():
    versions = read_json(VERSIONS_FILE, [])
    latest = versions[-1] if versions else None
    return render_template('index.html', latest=latest)


@app.route('/download')
def download():
    # If a specific name is requested, try to find it; otherwise use latest
    name = request.args.get('name')
    versions = read_json(VERSIONS_FILE, [])
    if not versions:
        flash('Nenhuma textura disponível para download.', 'warning')
        return redirect(url_for('index'))

    if name:
        v = next((x for x in versions if x.get('filename') == name or x.get('url') == name), None)
        if not v:
            flash('Versão não encontrada.', 'warning')
            return redirect(url_for('admin_dashboard'))
    else:
        v = versions[-1]

    # Prefer URL entries (new format)
    if v.get('url'):
        return redirect(v['url'])

    # Backwards compatibility: serve local file if present
    if v.get('filename'):
        return send_from_directory(app.config['UPLOAD_FOLDER'], v['filename'], as_attachment=True)

    flash('Versão inválida.', 'warning')
    return redirect(url_for('index'))


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
    file_url = request.form.get('file_url', '').strip()

    if not file_url or not is_valid_url(file_url):
        flash('Informe uma URL válida (iniciando com http:// ou https://).', 'danger')
        return redirect(url_for('admin_dashboard'))

    entry = {
        'name': texture_name,
        'version': version,
        'url': file_url,
        'uploaded_at': datetime.utcnow().isoformat(),
    }

    versions = read_json(VERSIONS_FILE, [])
    versions.append(entry)
    write_json(VERSIONS_FILE, versions)
    flash('Versão registrada com sucesso (via link).', 'success')
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


# Ensure data files exist with sane defaults
default_metadata = {
    'name': 'Tenma Texture',
    'description': 'Textura minimalista Minecraft',
    'updated_at': '',
    'filename': ''
}
if not os.path.exists(METADATA_FILE):
    write_json(METADATA_FILE, default_metadata)
if not os.path.exists(SUGGESTIONS_FILE):
    write_json(SUGGESTIONS_FILE, [])
if not os.path.exists(VERSIONS_FILE):
    write_json(VERSIONS_FILE, [])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
