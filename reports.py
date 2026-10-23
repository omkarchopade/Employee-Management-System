import csv
import os
from database import get_connection

def export_table_to_csv(filename, headers, rows):
    """Export list of dicts or tuples to CSV file."""
    os.makedirs("data", exist_ok=True)
    filepath = os.path.join("data", filename)
    try:
        with open(filepath, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)
        return True, f"Successfully exported to {filepath}"
    except Exception as e:
        return False, f"Export failed: {str(e)}"

def get_dashboard_stats(today_date):
    """Retrieve live statistics for the dashboard."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM employees")
    total_emp = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM employees WHERE status = 'Active'")
    active_emp = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM attendance WHERE date = ? AND status = 'Present'", (today_date,))
    present_today = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM attendance WHERE date = ? AND status = 'Absent'", (today_date,))
    absent_today = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(basic_salary) FROM employees WHERE status = 'Active'")
    total_payroll = cursor.fetchone()[0] or 0.0

    conn.close()
    return {
        "total_emp": total_emp,
        "active_emp": active_emp,
        "present_today": present_today,
        "absent_today": absent_today,
        "total_payroll": total_payroll
    }