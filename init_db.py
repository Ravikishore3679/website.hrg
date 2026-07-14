import sqlite3

# Connects to database (creates 'website.db' file if it doesn't exist)
connection = sqlite3.connect('website.db')
cursor = connection.cursor()

# Create the photos table
cursor.execute('''
CREATE TABLE IF NOT EXISTS photos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    file_path TEXT NOT NULL,
    alt_text TEXT,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# Insert sample data to test it
cursor.execute('''
INSERT INTO photos (title, file_path, alt_text) 
VALUES ('Beach Sunset', 'images/sunset.jpg', 'A beautiful orange sunset over the ocean')
''')

# Save changes and close
connection.commit()
connection.close()

print("Database and table created successfully with sample data!")
