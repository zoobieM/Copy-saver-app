from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import sqlite3, os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "dev_secret_key_change_in_production"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "snippets.db")

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Users table
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Snippets table with user_id
    c.execute("""
        CREATE TABLE IF NOT EXISTS snippets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            tag TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_edited TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    
    conn.commit()
    conn.close()

init_db()

def get_db_conn():
    return sqlite3.connect(DB_PATH)

# User class for Flask-Login
class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

@login_manager.user_loader
def load_user(user_id):
    conn = get_db_conn()
    c = conn.cursor()
    c.execute("SELECT id, username FROM users WHERE id = ?", (user_id,))
    user = c.fetchone()
    conn.close()
    if user:
        return User(user[0], user[1])
    return None

def format_timestamp(timestamp_str):
    """Convert timestamp to relative time"""
    if not timestamp_str:
        return ""
    try:
        created = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        now = datetime.utcnow()
        diff = now - created
        seconds = diff.total_seconds()
        
        if seconds < 60:
            return "just now"
        elif seconds < 3600:
            mins = int(seconds / 60)
            return f"{mins} min{'s' if mins != 1 else ''} ago"
        elif seconds < 86400:
            hours = int(seconds / 3600)
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        elif seconds < 604800:
            days = int(seconds / 86400)
            return f"{days} day{'s' if days != 1 else ''} ago"
        else:
            return created.strftime("%b %d, %Y")
    except:
        return timestamp_str

app.jinja_env.filters['format_timestamp'] = format_timestamp

# Routes
@app.route('/', methods=['GET'])
def home():
    q = request.args.get('q', '').strip()
    snippets = []
    
    if current_user.is_authenticated:
        conn = get_db_conn()
        c = conn.cursor()
        if q:
            c.execute("SELECT id, content, tag, created_at, last_edited FROM snippets WHERE user_id = ? AND (content LIKE ? OR tag LIKE ?) ORDER BY id DESC", 
                     (current_user.id, f"%{q}%", f"%{q}%"))
        else:
            c.execute("SELECT id, content, tag, created_at, last_edited FROM snippets WHERE user_id = ? ORDER BY id DESC", (current_user.id,))
        snippets = c.fetchall()
        conn.close()
    
    return render_template('index.html', snippets=snippets, q=q)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        if not username or not password:
            flash('Username and password are required.', 'warning')
            return redirect(url_for('signup'))
        
        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'warning')
            return redirect(url_for('signup'))
        
        conn = get_db_conn()
        c = conn.cursor()
        
        # Check if username exists
        c.execute("SELECT id FROM users WHERE username = ?", (username,))
        if c.fetchone():
            conn.close()
            flash('Username already taken.', 'warning')
            return redirect(url_for('signup'))
        
        # Create user
        password_hash = generate_password_hash(password)
        c.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))
        conn.commit()
        conn.close()
        
        flash('Account created! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        if not username or not password:
            flash('Username and password are required.', 'warning')
            return redirect(url_for('login'))
        
        conn = get_db_conn()
        c = conn.cursor()
        c.execute("SELECT id, username, password_hash FROM users WHERE username = ?", (username,))
        user_data = c.fetchone()
        conn.close()
        
        if user_data and check_password_hash(user_data[2], password):
            user = User(user_data[0], user_data[1])
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password.', 'warning')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('home'))

@app.route('/add', methods=['POST'])
@login_required
def add_snippet():
    content = request.form.get('content', '').strip()
    tag = request.form.get('tag', '').strip()
    
    if not content:
        flash('Snippet is empty — nothing saved.', 'warning')
        return redirect(url_for('home'))
    
    conn = get_db_conn()
    c = conn.cursor()
    c.execute("INSERT INTO snippets (user_id, content, tag) VALUES (?, ?, ?)", (current_user.id, content, tag))
    conn.commit()
    conn.close()
    
    flash('Snippet saved.', 'success')
    return redirect(url_for('home'))

@app.route('/edit/<int:snippet_id>', methods=['POST'])
@login_required
def edit_snippet(snippet_id):
    content = request.form.get('content', '').strip()
    tag = request.form.get('tag', '').strip()
    
    if not content:
        flash('Snippet is empty — nothing updated.', 'warning')
        return redirect(url_for('home'))
    
    conn = get_db_conn()
    c = conn.cursor()
    c.execute("UPDATE snippets SET content = ?, tag = ?, last_edited = CURRENT_TIMESTAMP WHERE id = ? AND user_id = ?", 
              (content, tag, snippet_id, current_user.id))
    conn.commit()
    conn.close()
    
    flash('Snippet updated.', 'success')
    return redirect(url_for('home'))

@app.route('/delete/<int:snippet_id>', methods=['POST'])
@login_required
def delete_snippet(snippet_id):
    conn = get_db_conn()
    c = conn.cursor()
    c.execute("DELETE FROM snippets WHERE id = ? AND user_id = ?", (snippet_id, current_user.id))
    conn.commit()
    conn.close()
    
    flash('Snippet deleted.', 'info')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
