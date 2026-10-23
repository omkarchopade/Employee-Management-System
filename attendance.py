import sqlite3
from database import get_connection

def mark_attendance(emp_id, date, status):
    """Mark attendance avoiding duplicate entries for same date."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO attendance (emp_id, date, status)
            VALUES (?, ?, ?)
        """, (emp_id, date, status))
        conn.commit()
        return True, "Attendance marked successfully."
    except sqlite3.IntegrityError:
        return False, "Error: Attendance already marked for this employee on this date."
    except Exception as e:
        return False, f"Error: {str(e)}"
    finally:
        conn.close()

def get_attendance_records(date=None):
    """Get attendance records for a specific date or all records."""
    conn = get_connection()
    cursor = conn.cursor()
    if date:
        cursor.execute("""
            SELECT a.id, a.emp_id, e.full_name, e.department, a.date, a.status
            FROM attendance a JOIN employees e ON a.emp_id = e.emp_id
            WHERE a.date = ?
        """, (date,))
    else:
        cursor.execute("""
            SELECT a.id, a.emp_id, e.full_name, e.department, a.date, a.status
            FROM attendance a JOIN employees e ON a.emp_id = e.emp_id
            ORDER BY a.date DESC
        """)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]