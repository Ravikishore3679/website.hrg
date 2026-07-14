from flask import Flask, render_template
import sqlite3

app = Flask(__name__, template_folder='.')

def get_db_photos():
    # Connect to your SQLite database
    conn = sqlite3.connect('website.db')
    conn.row_factory = sqlite3.Row  # Allows accessing columns by name
    cursor = conn.cursor()
    
    # Fetch all photos
    cursor.execute('SELECT title, file_path, alt_text FROM photos')
    photos = cursor.fetchall()
    
    conn.close()
    return photos

@app.route('/')
def home():
    # Get photos from DB and pass them to the HTML page
    db_photos = get_db_photos()
    return render_template('index.html', photos=db_photos)

if __name__ == '__main__':
    app.run(debug=True)

