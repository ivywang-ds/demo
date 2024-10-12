from flask import Flask, render_template, request, redirect
import sqlite3

# Initialize the Flask application
app = Flask(__name__)

# Function to create a database and a table (run once)
def create_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Create a table called 'items'
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT NOT NULL
    )
    ''')
    
    # Insert sample data
    cursor.execute('INSERT INTO items (name, description) VALUES (?, ?)', 
                   ('Apple', 'A sweet red fruit'))
    cursor.execute('INSERT INTO items (name, description) VALUES (?, ?)', 
                   ('Banana', 'A long yellow fruit'))
    cursor.execute('INSERT INTO items (name, description) VALUES (?, ?)', 
                   ('Carrot', 'An orange vegetable'))
    cursor.execute('INSERT INTO items (name, description) VALUES (?, ?)', 
                   ('Kiwi', 'A sweet green fruit'))
    cursor.execute('INSERT INTO items (name, description) VALUES (?, ?)', 
                   ('Mango', 'A sweet tropical fruit'))
    cursor.execute('INSERT INTO items (name, description) VALUES (?, ?)', 
                   ('Potato', 'An vegetable'))
    conn.commit()
    conn.close()

# Route for the home page
@app.route('/', methods=['GET', 'POST'])
def search():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    if request.method == 'POST':
        search_query = request.form['query']
        
        # Search in the database using LIKE for partial matching
        cursor.execute("SELECT * FROM items WHERE name LIKE ?", ('%' + search_query + '%',))
        results = cursor.fetchall()
        
        return render_template('search.html', results=results)
    
    # On GET, simply show an empty form
    return render_template('search.html', results=None)

if __name__ == '__main__':
    create_db()  # Create the database and populate with sample data
    app.run(host='0.0.0.0', port=5000, debug=True)
