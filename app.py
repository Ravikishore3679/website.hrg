import os
import sqlite3
from flask import Flask, render_template_string, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# HTML templates directly coded into the python server so directories never fail you again
UPLOAD_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Admin Dashboard - The Heaven Rock</title>
    <style>
        body { font-family: sans-serif; background-color: #f4f6f4; margin: 40px; text-align: center; }
        .form-container { background: white; padding: 30px; border-radius: 8px; max-width: 400px; margin: 0 auto; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
        .form-group { margin-bottom: 15px; text-align: left; }
        label { display: block; font-weight: bold; margin-bottom: 5px; }
        input[type="text"], input[type="file"] { width: 100%; padding: 8px; box-sizing: border-box; }
        button { background: #1b3d2f; color: white; border: none; padding: 10px; width: 100%; font-weight: bold; cursor: pointer; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="form-container">
        <h2>Upload New Photo to Gallery</h2>
        <form action="/upload" method="POST" enctype="multipart/form-data">
            <div class="form-group">
                <label>Photo Title</label>
                <input type="text" name="title" required placeholder="e.g., Luxury Suite View">
            </div>
            <div class="form-group">
                <label>Description (Alt Text)</label>
                <input type="text" name="alt_text" required placeholder="e.g., Garden view farmhouse entrance">
            </div>
            <div class="form-group">
                <label>Select Image</label>
                <input type="file" name="photo" accept="image/*" required>
            </div>
            <button type="submit">Upload to Gallery</button>
        </form>
        <br><a href="/" style="color: #c5a880; text-decoration: none;">← Back to Home View</a>
    </div>
</body>
</html>
"""

def get_db_photos():
    conn = sqlite3.connect('website.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT title, file_path, alt_text FROM photos ORDER BY id DESC')
    photos = cursor.fetchall()
    conn.close()
    return photos

@app.route('/')
def home():
    # Looks for index.html folder automatically
    db_photos = get_db_photos()
    try:
        return render_template('index.html', photos=db_photos)
    except:
        # Fallback if folder structure template is misplaced
        return render_template_string("<h1>Server Active!</h1><p>Move your index.html into a folder named 'templates' inside your workspace directory to see the resort design framework.</p>")

@app.route('/upload', methods=['GET'])
def upload_page():
    # Bypasses local folder issues to guarantee form rendering
    return render_template_string(UPLOAD_TEMPLATE)

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

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
