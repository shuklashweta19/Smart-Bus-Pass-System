"""
db_helper.py
Smart Bus Pass Issuing System — Database Helper (CRUD)
Uses SQLite (stdlib, zero install needed).
"""

import sqlite3
import os
import random
import string
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), "bus_pass.db")


# ─────────────────────────────────────────
#  Connection
# ─────────────────────────────────────────
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row          # dict-like rows
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Create tables and seed data if DB doesn't exist."""
    conn = get_connection()
    cur  = conn.cursor()
    sql_file = os.path.join(os.path.dirname(__file__), "database.sql")
    with open(sql_file) as f:
        cur.executescript(f.read())
    conn.commit()
    conn.close()


# ─────────────────────────────────────────
#  Helper
# ─────────────────────────────────────────
def _gen_pass_number():
    return "BP-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=8))

def _gen_receipt_number():
    return "RCP-" + "".join(random.choices(string.digits, k=10))

def _expiry_date(pass_type: str) -> str:
    today = datetime.today()
    delta = {"Monthly": 30, "Quarterly": 90, "Annual": 365}
    return (today + timedelta(days=delta[pass_type])).strftime("%Y-%m-%d")


# ─────────────────────────────────────────
#  STUDENTS — CRUD
# ─────────────────────────────────────────
def add_student(name, roll, college, course, year, phone, email, address):
    conn = get_connection()
    try:
        conn.execute(
            """INSERT INTO students
               (name,roll_number,college_name,course,year_of_study,phone,email,address)
               VALUES (?,?,?,?,?,?,?,?)""",
            (name, roll, college, course, year, phone, email, address)
        )
        conn.commit()
        return True, "Student added successfully."
    except sqlite3.IntegrityError as e:
        return False, f"Error: {e}"
    finally:
        conn.close()


def get_all_students():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM students ORDER BY student_id DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_student_by_id(sid):
    conn = get_connection()
    row = conn.execute("SELECT * FROM students WHERE student_id=?", (sid,)).fetchone()
    conn.close()
    return dict(row) if row else None


def update_student(sid, name, roll, college, course, year, phone, email, address):
    conn = get_connection()
    try:
        conn.execute(
            """UPDATE students SET name=?,roll_number=?,college_name=?,course=?,
               year_of_study=?,phone=?,email=?,address=? WHERE student_id=?""",
            (name, roll, college, course, year, phone, email, address, sid)
        )
        conn.commit()
        return True, "Student updated."
    except sqlite3.IntegrityError as e:
        return False, f"Error: {e}"
    finally:
        conn.close()


def delete_student(sid):
    conn = get_connection()
    conn.execute("DELETE FROM students WHERE student_id=?", (sid,))
    conn.commit()
    conn.close()
    return True, "Student deleted."


def search_students(query):
    conn = get_connection()
    q = f"%{query}%"
    rows = conn.execute(
        "SELECT * FROM students WHERE name LIKE ? OR roll_number LIKE ? OR email LIKE ?",
        (q, q, q)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ─────────────────────────────────────────
#  ROUTES — Read only (seeded)
# ─────────────────────────────────────────
def get_all_routes():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM routes").fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ─────────────────────────────────────────
#  BUS PASSES — CRUD
# ─────────────────────────────────────────
def issue_pass(student_id, route_id, pass_type, amount_paid, payment_mode):
    conn = get_connection()
    pass_num    = _gen_pass_number()
    receipt_num = _gen_receipt_number()
    today       = datetime.today().strftime("%Y-%m-%d")
    expiry      = _expiry_date(pass_type)
    try:
        cur = conn.execute(
            """INSERT INTO bus_passes
               (student_id,route_id,pass_number,issue_date,expiry_date,pass_type,amount_paid)
               VALUES (?,?,?,?,?,?,?)""",
            (student_id, route_id, pass_num, today, expiry, pass_type, amount_paid)
        )
        pass_id = cur.lastrowid
        conn.execute(
            """INSERT INTO payments (pass_id,amount,payment_mode,receipt_number)
               VALUES (?,?,?,?)""",
            (pass_id, amount_paid, payment_mode, receipt_num)
        )
        conn.commit()
        return True, f"Pass issued: {pass_num} | Receipt: {receipt_num}"
    except sqlite3.IntegrityError as e:
        return False, f"Error: {e}"
    finally:
        conn.close()


def get_all_passes():
    conn = get_connection()
    rows = conn.execute(
        """SELECT bp.*, s.name AS student_name, s.roll_number,
                  r.route_number, r.source, r.destination
           FROM bus_passes bp
           JOIN students s ON bp.student_id = s.student_id
           JOIN routes   r ON bp.route_id   = r.route_id
           ORDER BY bp.pass_id DESC"""
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_pass_by_id(pid):
    conn = get_connection()
    row = conn.execute(
        """SELECT bp.*, s.name AS student_name, s.roll_number, s.phone,
                  r.route_number, r.source, r.destination
           FROM bus_passes bp
           JOIN students s ON bp.student_id = s.student_id
           JOIN routes   r ON bp.route_id   = r.route_id
           WHERE bp.pass_id=?""", (pid,)
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def update_pass_status(pid, status):
    conn = get_connection()
    conn.execute("UPDATE bus_passes SET status=? WHERE pass_id=?", (status, pid))
    conn.commit()
    conn.close()
    return True, f"Pass status updated to {status}."


def delete_pass(pid):
    conn = get_connection()
    conn.execute("DELETE FROM payments WHERE pass_id=?", (pid,))
    conn.execute("DELETE FROM bus_passes WHERE pass_id=?", (pid,))
    conn.commit()
    conn.close()
    return True, "Pass deleted."


def search_passes(query):
    conn = get_connection()
    q = f"%{query}%"
    rows = conn.execute(
        """SELECT bp.*, s.name AS student_name, s.roll_number,
                  r.route_number, r.source, r.destination
           FROM bus_passes bp
           JOIN students s ON bp.student_id = s.student_id
           JOIN routes   r ON bp.route_id   = r.route_id
           WHERE bp.pass_number LIKE ? OR s.name LIKE ? OR s.roll_number LIKE ?
           ORDER BY bp.pass_id DESC""",
        (q, q, q)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ─────────────────────────────────────────
#  PAYMENTS — Read
# ─────────────────────────────────────────
def get_all_payments():
    conn = get_connection()
    rows = conn.execute(
        """SELECT p.*, bp.pass_number, s.name AS student_name
           FROM payments p
           JOIN bus_passes bp ON p.pass_id   = bp.pass_id
           JOIN students   s  ON bp.student_id = s.student_id
           ORDER BY p.payment_id DESC"""
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ─────────────────────────────────────────
#  DASHBOARD STATS
# ─────────────────────────────────────────
def get_dashboard_stats():
    conn = get_connection()
    stats = {}
    stats["total_students"] = conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]
    stats["total_passes"]   = conn.execute("SELECT COUNT(*) FROM bus_passes").fetchone()[0]
    stats["active_passes"]  = conn.execute("SELECT COUNT(*) FROM bus_passes WHERE status='Active'").fetchone()[0]
    stats["expired_passes"] = conn.execute("SELECT COUNT(*) FROM bus_passes WHERE status='Expired'").fetchone()[0]
    stats["total_revenue"]  = conn.execute("SELECT COALESCE(SUM(amount),0) FROM payments").fetchone()[0]
    stats["monthly_revenue"]= conn.execute(
        "SELECT COALESCE(SUM(amount),0) FROM payments WHERE strftime('%Y-%m',payment_date)=strftime('%Y-%m','now')"
    ).fetchone()[0]
    conn.close()
    return stats
