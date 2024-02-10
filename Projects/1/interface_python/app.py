from flask import Flask, request, jsonify
from flask import render_template
import sqlite3

app = Flask(__name__)

DATABASE = 'address.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with app.app_context():
        db = get_db_connection()
        db.execute('''CREATE TABLE IF NOT EXISTS AddressBook (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL UNIQUE,
                        address TEXT NOT NULL
                      );''')
        db.commit()

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/addresses', methods=['GET'])
def get_bikes():
    conn = get_db_connection()
    addressbook = conn.execute('SELECT * FROM AddressBook').fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in addressbook])

@app.route('/add_address', methods=['POST'])
def add_address():
    new_address = request.json
    conn = get_db_connection()
    conn.execute('INSERT OR IGNORE INTO AddressBook (name, address) VALUES (?, ?)',
                 (new_address['name'], new_address['address']))
    conn.commit()
    conn.close()
    return {'message': 'Address added successfully'}, 200

@app.route('/update_address/<int:id>', methods=['PUT'])
def update_address(id):
    update_details = request.json
    conn = get_db_connection()
    conn.execute('UPDATE AddressBook SET name = ?, address = ? WHERE id = ?',
                 (update_details['name'], update_details['address'], id))
    conn.commit()
    conn.close()
    return {'message': 'Address updated successfully'}, 200

@app.route('/delete_address/<int:id>', methods=['DELETE'])
def delete_address(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM AddressBook WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return {'message': 'Address deleted successfully'}, 200

@app.route('/delete_address_book', methods=['DELETE'])
def delete_address_book():
    conn = get_db_connection()
    conn.execute('DELETE FROM AddressBook')
    conn.commit()
    conn.close()
    return {'message': 'Address book deleted successfully'}, 200

if __name__ == '__main__':
    init_db()  # Initialize the database, create table if not exists, and add bikes
    app.run(debug=True)