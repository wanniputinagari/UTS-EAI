const express = require('express');
const mysql = require('mysql');
const app = express();
app.use(express.json()); // Parse JSON bodies

// MySQL connection configuration
const connection = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: '',
    database: 'medical_consultation'
});

// Connect to MySQL
connection.connect(err => {
    if (err) {
        console.error('Error connecting to MySQL: ' + err.stack);
        return;
    }
    console.log('Connected to MySQL as id ' + connection.threadId);
});

// Get all consultations
app.get('/consultations', (req, res) => {
    const sql = 'SELECT * FROM consultations';

    connection.query(sql, (error, results, fields) => {
        if (error) {
            console.error('Error executing MySQL query: ' + error.stack);
            return res.status(500).json({ error: 'Database error' });
        }
        res.json(results);
    });
});

// Get all Doctors
app.get('/doctors', (req, res) => {
    const sql = 'SELECT * FROM doctors';

    connection.query(sql, (error, results, fields) => {
        if (error) {
            console.error('Error executing MySQL query: ' + error.stack);
            return res.status(500).json({ error: 'Database error' });
        }
        res.json(results);
    });
});

// Get all Patients
app.get('/patients', (req, res) => {
    const sql = 'SELECT * FROM patients';

    connection.query(sql, (error, results, fields) => {
        if (error) {
            console.error('Error executing MySQL query: ' + error.stack);
            return res.status(500).json({ error: 'Database error' });
        }
        res.json(results);
    });
});


// Get a single consultation by ID
app.get('/detailconsultation/:id', (req, res) => {
    const id = req.params.id;
    const sql = 'SELECT * FROM consultations WHERE patient_id = ?';

    connection.query(sql, [id], (error, results) => {
        if (error) {
            console.error('Error executing MySQL query:', error);
            return res.status(500).json({ error: 'Database error' });
        }

        if (results.length === 0) {
            return res.status(404).json({ error: 'Data not found' });
        }

        res.json(results[0]); // Return the first result (assuming ID is unique)
    });
});


// Create a new consultation
app.post('/postpatients', (req, res) => {
    const { name, dob, gender, address, phone, email } = req.body;
    const sql = 'INSERT INTO patients (name, dob, gender, address, phone, email) VALUES (?, ?, ?, ?, ?, ?)';

    connection.query(sql, [name, dob, gender, address, phone, email], (error, results) => {
        if (error) {
            console.error('Error executing MySQL query: ' + error.stack);
            return res.status(500).json({ error: 'Database error' });
        }
        if (results.affectedRows === 0) {
            return res.status(404).json({ error: 'Data not found' });
        }
        res.status(201).json({ message: 'Patient data created successfully', id: results.insertId });
    });
});

// Update an existing patients by ID
app.put('/putpatients/:id', (req, res) => {
    const patient_id = req.params.id;
    const { name, dob, gender, address, phone, email } = req.body;
    const sql = 'UPDATE patients SET name = ?, dob = ?, gender = ?, address = ?, phone = ?, email = ? WHERE patient_id = ?';

    connection.query(sql, [name, dob, gender, address, phone, email, patient_id], (error, results) => {
        if (error) {
            console.error('Error executing MySQL query: ' + error.stack);
            return res.status(500).json({ error: 'Database error' });
        }
        if (results.affectedRows === 0) {
            return res.status(404).json({ error: 'Patient not found' });
        }
        res.json({ message: 'Patients updated successfully' });
    });
});

// Delete a patients by ID
app.delete('/delpatients/:id', (req, res) => {
    const patient_id = req.params.id;
    const sql = 'DELETE FROM patients WHERE patient_id = ?';

    connection.query(sql, [patient_id], (error, results) => {
        if (error) {
            console.error('Error executing MySQL query: ' + error.stack);
            return res.status(500).json({ error: 'Database error' });
        }
        if (results.affectedRows === 0) {
            return res.status(404).json({ error: 'Patient not found' });
        }
        res.json({ message: 'Patient deleted successfully' });
    });
});

// Start the server
const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
