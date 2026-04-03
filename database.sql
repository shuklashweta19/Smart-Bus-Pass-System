-- ============================================
-- Smart Bus Pass Issuing System
-- Database Schema (MySQL / SQLite Compatible)
-- ============================================

CREATE TABLE IF NOT EXISTS students (
    student_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT NOT NULL,
    roll_number     TEXT UNIQUE NOT NULL,
    college_name    TEXT NOT NULL,
    course          TEXT NOT NULL,
    year_of_study   INTEGER NOT NULL,
    phone           TEXT NOT NULL,
    email           TEXT UNIQUE NOT NULL,
    address         TEXT NOT NULL,
    created_at      TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS routes (
    route_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    route_number    TEXT UNIQUE NOT NULL,
    source          TEXT NOT NULL,
    destination     TEXT NOT NULL,
    distance_km     REAL NOT NULL,
    fare            REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS bus_passes (
    pass_id         INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id      INTEGER NOT NULL,
    route_id        INTEGER NOT NULL,
    pass_number     TEXT UNIQUE NOT NULL,
    issue_date      TEXT NOT NULL,
    expiry_date     TEXT NOT NULL,
    pass_type       TEXT NOT NULL CHECK(pass_type IN ('Monthly','Quarterly','Annual')),
    amount_paid     REAL NOT NULL,
    status          TEXT DEFAULT 'Active' CHECK(status IN ('Active','Expired','Cancelled')),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (route_id)   REFERENCES routes(route_id)
);

CREATE TABLE IF NOT EXISTS payments (
    payment_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    pass_id         INTEGER NOT NULL,
    amount          REAL NOT NULL,
    payment_date    TEXT DEFAULT (datetime('now')),
    payment_mode    TEXT NOT NULL CHECK(payment_mode IN ('Cash','Online','Card')),
    receipt_number  TEXT UNIQUE NOT NULL,
    FOREIGN KEY (pass_id) REFERENCES bus_passes(pass_id)
);

-- Seed Routes
INSERT OR IGNORE INTO routes (route_number, source, destination, distance_km, fare)
VALUES
  ('R01','City Center','North Campus',12.5,150),
  ('R02','South Gate','East Terminal',18.0,200),
  ('R03','West Hub','Central Station',22.3,250),
  ('R04','Airport Road','University Gate',30.1,300),
  ('R05','Old Town','Tech Park',9.8,120);
