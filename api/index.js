const express = require('express');
const { Pool } = require('pg');

const app = express();
const port = 3000;

// PostgreSQL connection
const pool = new Pool({
  user: 'flowuser',
  host: 'postgres-flowdb',   // PostgreSQL container name
  database: 'flowdb',
  password: 'flowpass',
  port: 5432,
});

// Endpoint: returns all flow_records
app.get('/getHttpsRecords', async (req, res) => {
  try {
    const result = await pool.query('SELECT * FROM flow_records');
    res.json(result.rows);
  } catch (err) {
    console.error('Database query failed', err);
    res.status(500).json({ error: 'Database query failed' });
  }
});

app.listen(port, () => {
  console.log(`FlowDB API listening at http://localhost:${port}`);
});
