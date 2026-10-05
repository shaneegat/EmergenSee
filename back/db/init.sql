-- Local demo data only. This file runs once for a new Docker database volume.
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL,
    role INTEGER NOT NULL CHECK (role IN (1, 2)),
    imagePath TEXT,
    isActive BOOLEAN NOT NULL DEFAULT TRUE
);
CREATE TABLE patients (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    phone_number VARCHAR(30),
    full_name VARCHAR(100) NOT NULL,
    age INTEGER NOT NULL,
    photo TEXT,
    doctor_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE
);
CREATE TABLE doctors (
    user_id INTEGER PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    rank TEXT DEFAULT '',
    phoneNumber TEXT DEFAULT '',
    numberOfPatients INTEGER DEFAULT 0,
    active BOOLEAN DEFAULT TRUE,
    dateOfBirth TEXT DEFAULT ''
);
CREATE TABLE admins (
    user_id INTEGER PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE
);
CREATE TABLE datasets (id SERIAL PRIMARY KEY, name TEXT NOT NULL, description TEXT);
CREATE TABLE models (id SERIAL PRIMARY KEY, name TEXT NOT NULL, labeled BOOLEAN NOT NULL);
CREATE TABLE algorithms (
    id SERIAL PRIMARY KEY,
    algorithm_name TEXT NOT NULL,
    success_rank DOUBLE PRECISION DEFAULT 0,
    num_uses INTEGER DEFAULT 0
);
INSERT INTO users (email, name, password, role) VALUES
    ('admin1@example.com', 'Demo Admin', 'password1', 2),
    ('doctor1@example.com', 'Demo Doctor', 'password1', 1);
INSERT INTO admins (user_id) SELECT id FROM users WHERE role = 2;
INSERT INTO doctors (user_id) SELECT id FROM users WHERE role = 1;
INSERT INTO patients (email, phone_number, full_name, age, photo, doctor_id)
SELECT 'demo.patient@example.com', '0500000000', 'Demo Patient', 30, '', id
FROM users WHERE email = 'doctor1@example.com';
