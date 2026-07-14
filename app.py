import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder='.')

# Configuration for file uploads
UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def get_db_photos():
    conn = sqlite3.connect('website.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT title, file_path, alt_text FROM photos ORDER BY id DESC')
    photos = cursor.fetchall()
    conn.close()
    return photos

# Route: Home Page Gallery
@app.route('/')
def home():
    db_photos = get_db_photos()
    return render_template('index.html', photos=db_photos)

# Route: View the Admin Upload Form Page
@app.route('/upload', methods=['GET'])
def upload_page():
    return render_template('upload.html')

# Route: Handle Form Submission Processing
@app.route('/upload', methods=['POST'])
def handle_upload():
    title = request.form['title']
    alt_text = request.form['alt_text']
    file = request.files['photo']
    
    if file and file.filename != '':
        # Sanitize filename for system safety
        filename = secure_filename(file.filename)
        # Construct path where file is physically stored on disk
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Save relative file path string into database records
        conn = sqlite3.connect('website.db')
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO photos (title, file_path, alt_text) VALUES (?, ?, ?)',
            (title, file_path, alt_text)
        )
        conn.commit()
        conn.close()
        
    return redirect(url_for('home'))

if __name__ == '__main__':
    # Ensure the static folder structurally exists prior to execution
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
