CopyPasteSaver - simple Flask + SQLite snippet saver
---------------------------------------------------
Contents:
- app.py                : Flask application
- snippets.db           : created automatically when app runs
- templates/index.html  : main template
- static/styles.css     : CSS (modern)
- static/script.js      : copy-to-clipboard logic
- requirements.txt

To run:
1. Create a venv (optional):
   python -m venv venv
   venv\Scripts\activate   (Windows)
   source venv/bin/activate  (macOS/Linux)

2. Install requirements:
   pip install -r requirements.txt

3. Run:
   python app.py

Open http://127.0.0.1:5000
