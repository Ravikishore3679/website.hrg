import os
import sqlite3
from flask import Flask, render_template_string, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ----------------------------------------------------
# 1. THE MAIN GALLERY, AMENITIES, MAP & DELETE TEMPLATE
# ----------------------------------------------------
INDEX_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The Heaven Rock Guest House</title>
    <style>
        :root {
            --primary-color: #1b3d2f; 
            --accent-color: #c5a880;  
            --text-dark: #222222;
            --text-light: #666666;
            --bg-light: #fdfdfd;
            --white: #ffffff;
            --danger-color: #dc3545;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
            margin: 0; padding: 0; background-color: var(--bg-light); color: var(--text-dark); line-height: 1.6;
        }
        .top-banner {
            background-color: var(--primary-color); color: var(--white); text-align: center; padding: 10px 20px; font-size: 0.9rem; letter-spacing: 1px; font-weight: 600;
        }
        header { background-color: var(--white); box-shadow: 0 2px 15px rgba(0, 0, 0, 0.04); position: sticky; top: 0; z-index: 1000; }
        nav { max-width: 1200px; margin: 0 auto; padding: 20px; display: flex; justify-content: space-between; align-items: center; }
        .logo { font-size: 1.5rem; font-weight: 700; color: var(--primary-color); text-decoration: none; }
        nav ul { list-style: none; display: flex; gap: 30px; margin: 0; padding: 0; align-items: center; }
        nav a { text-decoration: none; color: var(--text-light); font-weight: 500; transition: color 0.3s ease; }
        nav a:hover { color: var(--primary-color); }
        .upload-link { color: #007bff !important; font-weight: 600; }
        .book-btn { background-color: var(--accent-color); color: var(--white) !important; padding: 10px 22px; border-radius: 4px; font-weight: 600; }
        
        .hero { text-align: center; padding: 80px 20px 40px 20px; max-width: 900px; margin: 0 auto; }
        .hero h1 { font-size: 3.5rem; color: var(--primary-color); margin: 0 0 20px 0; font-weight: 800; }
        .hero p { font-size: 1.25rem; color: var(--text-light); max-width: 700px; margin: 0 auto 35px auto; }
        .contact-box { background-color: #f4f6f4; border-left: 4px solid var(--accent-color); padding: 20px; border-radius: 0 8px 8px 0; display: inline-block; margin-bottom: 20px; }
        .contact-box p { margin: 0 0 10px 0; font-weight: bold; color: var(--primary-color); }
        .phone-links a { color: var(--primary-color); text-decoration: none; font-size: 1.2rem; font-weight: 700; margin: 0 15px; border-bottom: 2px solid var(--accent-color); }
        
        .map-btn { display: inline-block; background-color: #007bff; color: white !important; font-weight: 600; text-decoration: none; padding: 10px 20px; border-radius: 6px; box-shadow: 0 4px 10px rgba(0,123,255,0.2); transition: background 0.2s; margin-top: 10px; }
        .map-btn:hover { background-color: #0056b3; }

        .section-header { text-align: center; margin-top: 80px; margin-bottom: 40px; }
        .section-header h2 { font-size: 2.2rem; color: var(--primary-color); margin: 0; font-weight: 700; position: relative; display: inline-block; }
        .section-header h2::after { content: ''; display: block; width: 50px; height: 3px; background-color: var(--accent-color); margin: 10px auto 0 auto; border-radius: 2px; }
        
        .amenities-container { max-width: 1100px; margin: 0 auto 40px auto; padding: 0 20px; }
        .amenities-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 20px; }
        .amenity-card { background-color: var(--white); border: 1px solid #ebebeb; border-radius: 8px; padding: 24px; display: flex; align-items: center; gap: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.02); transition: transform 0.2s ease; }
        .amenity-card:hover { transform: translateY(-3px); border-color: var(--accent-color); }
        .amenity-icon { font-size: 2rem; min-width: 40px; display: inline-flex; justify-content: center; }
        .amenity-info h4 { margin: 0; font-size: 1.05rem; color: var(--primary-color); font-weight: 600; }

        .photo-gallery { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 30px; padding: 0 20px; max-width: 1200px; margin: 0 auto 100px auto; }
        .photo-item { background-color: var(--white); border-radius: 8px; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05); overflow: hidden; display: flex; flex-direction: column; position: relative; }
        .photo-item img { width: 100%; height: 260px; object-fit: cover; display: block; }
        .photo-text { padding: 20px; text-align: center; display: flex; flex-direction: column; justify-content: space-between; flex-grow: 1; }
        .photo-text h3 { margin: 0 0 15px 0; font-size: 1.2rem; color: var(--primary-color); }
        
        /* New Delete Button Style */
        .delete-btn { background-color: var(--white); color: var(--danger-color); border: 1px solid var(--danger-color); padding: 6px 12px; border-radius: 4px; font-weight: 600; cursor: pointer; font-size: 0.85rem; transition: all 0.2s ease; align-self: center; }
        .delete-btn:hover { background-color: var(--danger-color); color: var(--white); }
    </style>
</head>
<body>
    <div class="top-banner">✦ BOOKINGS OPEN FOR YOUR NEXT GETAWAY ✦</div>
    <header>
        <nav>
            <a href="/" class="logo">The Heaven Rock</a>
            <ul>
                <li><a href="/">Home</a></li>
                <li><a href="/upload" class="upload-link">➕ Add Photos</a></li>
                <li><a href="tel:9666332255" class="book-btn">Book Now</a></li>
            </ul>
        </nav>
    </header>
    
    <div class="hero">
        <h1>Escape to Heaven Rock</h1>
        <p>A private luxury farmhouse designed beautifully for family getaways, private gatherings, and life's major milestones.</p>
        <div class="contact-box">
            <p>📍 KONDAMADUGU, BIBINAGAR MDL, YADADRI - 508126</p>
            <div class="phone-links">
                <a href="tel:9666332255">Call 9666332255</a>
                <a href="tel:9949214746">Call 9949214746</a>
            </div>
        </div>
        <div>
            <!-- Google Maps Web Navigation Shortcut Link -->
            <a href="https://google.com" target="_blank" class="map-btn">📍 Open in Google Maps</a>
        </div>
    </div>

    <div class="section-header">
        <h2>Premium Amenities</h2>
    </div>
    <div class="amenities-container">
        <div class="amenities-grid">
            <div class="amenity-card">
                <div class="amenity-icon">🏊‍♂️</div>
                <div class="amenity-info"><h4>Swimming Pool</h4></div>
            </div>
            <div class="amenity-card">
                <div class="amenity-icon">🏡</div>
                <div class="amenity-info"><h4>Spacious Lawn</h4></div>
            </div>
            <div class="amenity-card">
                <div class="amenity-icon">📺</div>
                <div class="amenity-info"><h4>Living Room with 65" TV</h4></div>
            </div>
            <div class="amenity-card">
                <div class="amenity-icon">🛏️</div>
                <div class="amenity-info"><h4>3BHK with Attached Bath & AC</h4></div>
            </div>
            <div class="amenity-card">
                <div class="amenity-icon">⛱️</div>
                <div class="amenity-info"><h4>Pergola in the Lawn to Hangout</h4></div>
            </div>
            <div class="amenity-card">
                <div class="amenity-icon">🎏</div>
                <div class="amenity-info"><h4>Exclusive Small Pond with Koi</h4></div>
            </div>
            <div class="amenity-card">
                <div class="amenity-icon">🔥</div>
                <div class="amenity-info"><h4>Barbecue & Bonfire Area</h4></div>
            </div>
            <div class="amenity-card">
                <div class="amenity-icon">🍳</div>
                <div class="amenity-info"><h4>Fully Equipped Kitchen</h4></div>
            </div>
        </div>
    </div>

    <div class="section-header">
        <h2>Your Private Oasis</h2>
    </div>
    <div class="photo-gallery">
        {% for photo in photos %}
            <div class="photo-item">
                <img src="{{ photo['file_path'] }}" alt="{{ photo['alt_text'] }}">
                <div class="photo-text">
                    <h3>{{ photo['title'] }}</h3>
                    <!-- Dynamic form triggering the deletion of this photo card item by ID -->
                    <form action="/delete/{{ photo['id'] }}" method="POST" onsubmit="return confirm('Are you sure you want to delete this photo?');">
                        <button type="submit" class="delete-btn">🗑️ Delete Photo</button>
                    </form>
                </div>
            </div>
        {% endfor %}
    </div>
</body>
</html>
"""

# ----------------------------------------------------
# 2. THE UPLOAD DASHBOARD TEMPLATE (upload.html)
# ----------------------------------------------------
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
        <h2>Upload New Photo</h2>
        <form action="/upload" method="POST" enctype="multipart/form-data">
            <div class="form-group">
                <label>Photo Title</label>
                <input type="text" name="title" required placeholder="e.g., Luxury Suite View">
            </div>
            <div class="form-group">
                <label>Description (Alt Text)</label>
                <input type="text" name="alt_text" required placeholder="e.g., Garden view entry">
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
    db_photos = get_db_photos()
    return render_template_string(INDEX_TEMPLATE, photos=db_photos)

@app.route('/upload', methods=['GET'])
def upload_page():
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
# Add this fallback route right above your existing delete function block
@app.route('/delete/', methods=['POST'])
@app.route('/delete', methods=['POST'])
def delete_fallback():
    # If a blank or broken ID is sent, ignore it and safely refresh the home gallery
    return redirect(url_for('home'))

@app.route('/delete/int:photo_id', methods=['POST'])
def delete_photo(photo_id):
    conn = sqlite3.connect('website.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    # Retrieve file path to remove the file from your computer disk storage
    cursor.execute('SELECT file_path FROM photos WHERE id = ?', (photo_id,))
    photo = cursor.fetchone()
    if photo:
        file_path = photo['file_path']
        # Safely attempt removing the local physical image asset file if it exists
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass
            # Wipe data record row from SQLite tables
            cursor.execute('DELETE FROM photos WHERE id = ?', (photo_id,))
            conn.commit()
    conn.close()
    return redirect(url_for('home'))

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)