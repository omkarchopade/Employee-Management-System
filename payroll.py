from database import get_connection

def calculate_payroll(basic_salary, allowances, deductions):
    """Calculate gross and net salary."""
    gross = basic_salary + allowances
    net = gross - deductions
    return gross, net

def save_payroll_record(emp_id, month, basic, allowances, deductions, net, payment_date):
    """Save payroll entry."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO payroll (emp_id, month, basic_salary, allowances, deductions, net_salary, payment_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (emp_id, month, basic, allowances, deductions, net, payment_date))
        conn.commit()
        return True, "Payroll record saved successfully."
    except Exception as e:
        return False, f"Error: {str(e)}"
    finally:
        conn.close()

def get_payroll_records():
    """Retrieve all payroll records with employee names."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.id, p.emp_id, e.full_name, e.department, p.month, p.basic_salary, p.allowances, p.deductions, p.net_salary, p.payment_date
        FROM payroll p JOIN employees e ON p.emp_id = e.emp_id
        ORDER BY p.id DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]