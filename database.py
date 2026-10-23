import sqlite3
import os
import hashlib

DB_PATH = os.path.join("data", "ems.db")

def get_connection():
    """Ensure data directory exists and return SQLite connection."""
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize SQLite database tables if they do not exist."""
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Admin Users Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)

    # 2. Employees Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            emp_id TEXT PRIMARY KEY,
            full_name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT NOT NULL,
            address TEXT NOT NULL,
            department TEXT NOT NULL,
            designation TEXT NOT NULL,
            joining_date TEXT NOT NULL,
            basic_salary REAL NOT NULL,
            status TEXT NOT NULL
        )
    """)

    # 3. Attendance Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            emp_id TEXT NOT NULL,
            date TEXT NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (emp_id) REFERENCES employees(emp_id) ON DELETE CASCADE,
            UNIQUE(emp_id, date)
        )
    """)

    # 4. Payroll Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS payroll (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            emp_id TEXT NOT NULL,
            month TEXT NOT NULL,
            basic_salary REAL NOT NULL,
            allowances REAL NOT NULL,
            deductions REAL NOT NULL,
            net_salary REAL NOT NULL,
            payment_date TEXT NOT NULL,
            FOREIGN KEY (emp_id) REFERENCES employees(emp_id) ON DELETE CASCADE
        )
    """)

    # Create default admin if none exists (username: admin, password: admin123)
    cursor.execute("SELECT COUNT(*) FROM admins")
    if cursor.fetchone()[0] == 0:
        default_pass = hashlib.sha256("admin123".encode()).hexdigest()
        cursor.execute("INSERT INTO admins (username, password_hash) VALUES (?, ?)", ("admin", default_pass))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")