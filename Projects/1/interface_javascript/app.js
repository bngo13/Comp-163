/* Imports for web page and sqlite */
const express = require('express');
const sqlite3 = require('sqlite3').verbose();

/* Constants */
const app = express();
const PORT = process.env.PORT || 3000;
const DATABASE = 'address.db';

app.use(express.static('public'));

function getDBConnection() {
  return new sqlite3.Database(DATABASE);
}

function initDB() {
  const db = getDBConnection();
  db.serialize(() => {
    db.run(`CREATE TABLE IF NOT EXISTS AddressBook (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL UNIQUE,
      address TEXT NOT NULL
    )`);
  });
  db.close();
}

function bindApp() {
  // Set input type to json
  app.use(express.json());

  // Route to get all bikes
  app.get('/addressbook', (req, res) => {
    const db = getDBConnection();
    db.all('SELECT * FROM AddressBook', (err, rows) => {
      if (err) {
        console.error('Error fetching addresses:', err);
        res.status(500).json({ error: 'Internal Server Error' });
      } else {
        res.json(rows);
      }
    });
    db.close();
  });

  // Route to add a new bike
  app.post('/add_address', (req, res) => {
    const newBike = req.body;
    const db = getDBConnection();
    db.run('INSERT OR IGNORE INTO AddressBook (name, address) VALUES (?, ?)', [newBike.name, newBike.address], function(err) {
      if (err) {
        console.error('Error adding Address:', err);
        res.status(500).json({ error: 'Internal Server Error' });
      } else {
        res.json({ message: 'Address added successfully', id: this.lastID });
      }
    });
    db.close();
  });

  // Route to update a bike
  app.put('/update_address/:id', (req, res) => {
    const { id } = req.params;
    const updateDetails = req.body;
    const db = getDBConnection();
    db.run('UPDATE AddressBook SET name = ?, address = ? WHERE id = ?', [updateDetails.name, updateDetails.address, id], function(err) {
      if (err) {
        console.error('Error updating address:', err);
        res.status(500).json({ error: 'Internal Server Error' });
      } else {
        res.json({ message: 'Address updated successfully', changes: this.changes });
      }
    });
    db.close();
  });

  // Route to delete a bike
  app.delete('/delete_address/:id', (req, res) => {
    const { id } = req.params;
    const db = getDBConnection();
    db.run('DELETE FROM AddressBook WHERE id = ?', id, function(err) {
      if (err) {
        console.error('Error deleting address:', err);
        res.status(500).json({ error: 'Internal Server Error' });
      } else {
        res.json({ message: 'Address deleted successfully', changes: this.changes });
      }
    });
    db.close();
  });

  // Route to delete all bikes
  app.delete('/clear_address_book', (req, res) => {
    const db = getDBConnection();
    db.run('DELETE FROM AddressBook', function(err) {
      if (err) {
        console.error('Error deleting all bikes:', err);
        res.status(500).json({ error: 'Internal Server Error' });
      } else {
        res.json({ message: 'All addresses deleted successfully', changes: this.changes });
      }
    });
    db.close();
  }); 
}

function initApp() {
  // Initializations
  initDB();
  bindApp();

  // Start App
  app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
  });
}

initApp();
