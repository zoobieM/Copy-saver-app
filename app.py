from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3, os

app = Flask(__name__)
app.secret_key = "dev_secret_key"  # change for production

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "snippets.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS snippets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            tag TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

def get_db_conn():
    return sqlite3.connect(DB_PATH)

@app.route('/', methods=['GET'])
def home():
    q = request.args.get('q', '').strip()
    conn = get_db_conn()
    c = conn.cursor()
    if q:
        c.execute("SELECT id, content, tag FROM snippets WHERE content LIKE ? OR tag LIKE ? ORDER BY id DESC", (f"%{q}%", f"%{q}%"))
    else:
        c.execute("SELECT id, content, tag FROM snippets ORDER BY id DESC")
    snippets = c.fetchall()
    conn.close()
    return render_template('index.html', snippets=snippets, q=q)

@app.route('/add', methods=['POST'])
def add_snippet():
    content = request.form.get('content', '').strip()
    tag = request.form.get('tag', '').strip()
    if not content:
        flash('Snippet is empty — nothing saved.', 'warning')
        return redirect(url_for('home'))
    conn = get_db_conn()
    c = conn.cursor()
    c.execute("INSERT INTO snippets (content, tag) VALUES (?, ?)", (content, tag))
    conn.commit()
    conn.close()
    flash('Snippet saved.', 'success')
    return redirect(url_for('home'))

@app.route('/delete/<int:snippet_id>', methods=['POST'])
def delete_snippet(snippet_id):
    conn = get_db_conn()
    c = conn.cursor()
    c.execute("DELETE FROM snippets WHERE id = ?", (snippet_id,))
    conn.commit()
    conn.close()
    flash('Snippet deleted.', 'info')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
