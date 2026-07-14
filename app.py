import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Helper function to ensure the database and table always exist automatically
def init_db_safely():
    conn = sqlite3.connect('website.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS photos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        file_path TEXT NOT NULL,
        alt_text TEXT,
        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    conn.commit()
    conn.close()


# Ensure the DB schema exists before any route attempts to read/write photos.
init_db_safely()

def get_db_photos():
    conn = sqlite3.connect('website.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT id, title, file_path, alt_text FROM photos ORDER BY id DESC')
    photos = cursor.fetchall()
    conn.close()
    return photos

@app.route('/')
def home():
    db_photos = get_db_photos()
    return render_template('index.html', photos=db_photos)

@app.route('/upload', methods=['GET'])
def upload_page():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def handle_upload():
    title = request.form['title']
    alt_text = request.form['alt_text']
    file = request.files['photo']
    
    if file and file.filename != '':
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        conn = sqlite3.connect('website.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO photos (title, file_path, alt_text) VALUES (?, ?, ?)', (title, file_path, alt_text))
        conn.commit()
        conn.close()
        
    return redirect(url_for('home'))


# Handles accidental POSTs to /delete and /delete/ without an id.
@app.route('/delete/', methods=['POST'])
@app.route('/delete', methods=['POST'])
def delete_fallback():
    return redirect(url_for('home'))


@app.route('/delete/<int:photo_id>', methods=['POST'])
def delete_photo(photo_id):
    conn = sqlite3.connect('website.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT file_path FROM photos WHERE id = ?', (photo_id,))
    photo = cursor.fetchone()
    if photo:
        file_path = photo['file_path']
        # Attempt deleting the image file from disk first, then remove DB row.
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except OSError:
                pass
        cursor.execute('DELETE FROM photos WHERE id = ?', (photo_id,))
        conn.commit()
    conn.close()
    return redirect(url_for('home'))


# Add this block right before "if __name__ == '__main__':"
@app.after_request
def add_header(response):
    # Prevents browsers from storing layout state and dead asset links
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)