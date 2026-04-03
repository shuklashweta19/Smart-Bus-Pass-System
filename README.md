# Smart Bus Pass Issuing System
## Python + SQL Mini Project

---

## 📁 Project Structure

```
SmartBusPass/
├── app.py          ← Main dashboard (Tkinter GUI)
├── db_helper.py    ← All CRUD operations (Python + SQLite)
├── database.sql    ← SQL schema + seed data
├── bus_pass.db     ← Auto-created SQLite database (after first run)
└── README.md       ← This file
```

---

## 🚀 How to Run

### Step 1 — Install Python (if not already)
- Python 3.8 or above required
- Download from: https://www.python.org/downloads/

### Step 2 — No extra packages needed!
This project uses only Python standard libraries:
- `tkinter` (GUI)
- `sqlite3` (Database)

### Step 3 — Run the application
```bash
cd SmartBusPass
python app.py
```

---

## 📋 Features

### Dashboard
- Live stats: Total Students, Passes, Revenue
- Recent bus pass table

### Student Management (CRUD)
- ✅ **Create** — Add new student with all details
- ✅ **Read**   — View all students, search by name/roll/email
- ✅ **Update** — Edit student details via double-click
- ✅ **Delete** — Remove student records

### Bus Pass Management (CRUD)
- ✅ **Create** — Issue new pass (Monthly / Quarterly / Annual)
- ✅ **Read**   — View all passes with student & route info
- ✅ **Update** — Change pass status (Active / Expired / Cancelled)
- ✅ **Delete** — Remove pass + payment record

### Payment Records
- View all payment history with receipt numbers

### Route Management
- Pre-configured 5 routes with fares

---

## 🗃️ Database Tables

| Table       | Purpose                          |
|-------------|----------------------------------|
| `students`  | Student registration details     |
| `routes`    | Bus route info and fares         |
| `bus_passes`| Issued pass records              |
| `payments`  | Payment transactions             |

---

## 🔗 SQL Concepts Used
- DDL: `CREATE TABLE`, `PRIMARY KEY`, `FOREIGN KEY`, `AUTOINCREMENT`
- DML: `INSERT`, `SELECT`, `UPDATE`, `DELETE`
- Constraints: `UNIQUE`, `CHECK`, `NOT NULL`, `DEFAULT`
- Joins: `INNER JOIN` across 3 tables
- Aggregates: `COUNT`, `SUM`, `COALESCE`
- Date functions: `strftime`, `datetime`

---

## 📦 Evaluation Checklist
- [x] Python + SQL integration
- [x] SQLite database with 4 tables
- [x] Full CRUD operations
- [x] Dashboard with stats
- [x] Search functionality
- [x] Foreign key relationships
- [x] Clean GUI (Tkinter)
- [x] No external libraries needed

---

*Project developed for college evaluation — Smart Bus Pass Issuing System*
