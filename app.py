from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'chave_secreta_super_forte'
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def init_db():
    if not os.path.exists('database'):
        os.makedirs('database')
    conn = sqlite3.connect('database/site.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trabalhos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT,
            descricao TEXT,
            imagem_antes TEXT,
            imagem_depois TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT,
            url TEXT
        )
    ''')
    conn.commit()
    conn.close()

def is_logged_in():
    return session.get('logged_in')

@app.route('/')
def index():
    conn = sqlite3.connect('database/site.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM trabalhos')
    trabalhos = cursor.fetchall()
    conn.close()
    return render_template('index.html', trabalhos=trabalhos)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Usuário e senha fixos
        if username == 'admin' and password == 'admin':
            session['logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Credenciais inválidas!')
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    session.clear()
    return redirect(url_for('admin_login'))

@app.route('/admin/dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if not is_logged_in():
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        imagem_antes = request.files['antes']
        imagem_depois = request.files['depois']

        if not (titulo and descricao and imagem_antes and imagem_depois):
            flash('Todos os campos são obrigatórios.')
            return redirect(url_for('admin_dashboard'))

        # Salvar imagens
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        antes_path = os.path.join(app.config['UPLOAD_FOLDER'], imagem_antes.filename)
        depois_path = os.path.join(app.config['UPLOAD_FOLDER'], imagem_depois.filename)
        imagem_antes.save(antes_path)
        imagem_depois.save(depois_path)

        # Salvar no DB
        conn = sqlite3.connect('database/site.db')
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO trabalhos (titulo, descricao, imagem_antes, imagem_depois) VALUES (?, ?, ?, ?)',
            (titulo, descricao, imagem_antes.filename, imagem_depois.filename)
        )
        conn.commit()
        conn.close()
        flash('Trabalho adicionado com sucesso!')
        return redirect(url_for('admin_dashboard'))

    # Listar trabalhos
    conn = sqlite3.connect('database/site.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM trabalhos')
    trabalhos = cursor.fetchall()

    # Listar vídeos
    cursor.execute('SELECT * FROM videos')
    videos = cursor.fetchall()
    conn.close()

    return render_template('admin_dashboard.html', trabalhos=trabalhos, videos=videos)

@app.route('/admin/add_video', methods=['POST'])
def add_video():
    if not is_logged_in():
        return redirect(url_for('admin_login'))

    titulo = request.form['titulo']
    url = request.form['url']

    if not (titulo and url):
        flash('Título e URL são obrigatórios.')
        return redirect(url_for('admin_dashboard'))

    conn = sqlite3.connect('database/site.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO videos (titulo, url) VALUES (?, ?)', (titulo, url))
    conn.commit()
    conn.close()
    flash('Vídeo adicionado com sucesso!')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete_trabalho/<int:id>', methods=['POST'])
def delete_trabalho(id):
    if not is_logged_in():
        return redirect(url_for('admin_login'))

    conn = sqlite3.connect('database/site.db')
    cursor = conn.cursor()
    cursor.execute("SELECT imagem_antes, imagem_depois FROM trabalhos WHERE id = ?", (id,))
    imagens = cursor.fetchone()
    if imagens:
        for img in imagens:
            try:
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], img))
            except FileNotFoundError:
                pass
    cursor.execute("DELETE FROM trabalhos WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    flash('Trabalho excluído com sucesso!')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete_video/<int:id>', methods=['POST'])
def delete_video(id):
    if not is_logged_in():
        return redirect(url_for('admin_login'))

    conn = sqlite3.connect('database/site.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM videos WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    flash('Vídeo excluído com sucesso!')
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)

