import sqlite3
from database import get_connection

def generate_emp_id():
    """Generate next unique employee ID like EMP001."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT emp_id FROM employees ORDER BY emp_id DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()

    if row:
        last_id = row["emp_id"]  # e.g., 'EMP005'
        num = int(last_id.replace("EMP", "")) + 1
        return f"EMP{num:03d}"
    return "EMP001"

def add_employee(data):
    """Add a new employee to the database."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO employees (emp_id, full_name, age, gender, phone, email, address, department, designation, joining_date, basic_salary, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data['emp_id'], data['full_name'], data['age'], data['gender'],
            data['phone'], data['email'], data['address'], data['department'],
            data['designation'], data['joining_date'], data['basic_salary'], data['status']
        ))
        conn.commit()
        return True, "Employee added successfully."
    except sqlite3.IntegrityError:
        return False, "Error: Employee ID already exists."
    except Exception as e:
        return False, f"Error: {str(e)}"
    finally:
        conn.close()

def get_all_employees(search=None, department=None):
    """Retrieve employees with optional search and department filter."""
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM employees WHERE 1=1"
    params = []

    if search:
        query += " AND (emp_id LIKE ? OR full_name LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%"])

    if department and department != "All Departments":
        query += " AND department = ?"
        params.append(department)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def update_employee(data):
    """Update existing employee details."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE employees SET full_name=?, age=?, gender=?, phone=?, email=?, address=?, department=?, designation=?, joining_date=?, basic_salary=?, status=?
            WHERE emp_id=?
        """, (
            data['full_name'], data['age'], data['gender'], data['phone'],
            data['email'], data['address'], data['department'], data['designation'],
            data['joining_date'], data['basic_salary'], data['status'], data['emp_id']
        ))
        conn.commit()
        return True, "Employee updated successfully."
    except Exception as e:
        return False, f"Error: {str(e)}"
    finally:
        conn.close()

def delete_employee(emp_id):
    """Delete employee by ID."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM employees WHERE emp_id = ?", (emp_id,))
        conn.commit()
        return True, "Employee deleted successfully."
    except Exception as e:
        return False, f"Error: {str(e)}"
    finally:
        conn.close()