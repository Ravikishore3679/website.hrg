import sqlite3
conn = sqlite3.connect('website.db')
cursor = conn.cursor()

# Rebuild table cleanly if broken
cursor.execute('''
CREATE TABLE IF NOT EXISTS photos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    file_path TEXT NOT NULL,
    alt_text TEXT,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# Clear bad test data strings
cursor.execute('DELETE FROM photos')

# Insert absolute fallback safe variables
cursor.execute('''
INSERT INTO photos (title, file_path, alt_text) 
VALUES ('The Heaven Rock Oasis', 'https://unsplash.com', 'Luxury resort grounds overview')
''')
conn.commit()
conn.close()
print("Database initialized cleanly with online fallback photo placeholder data!")
