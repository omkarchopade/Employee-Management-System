import sqlite3
import random
from datetime import datetime, timedelta
import os

def seed_database():
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    db_path = os.path.join("data", "ems.db")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 1. Ensure tables exist
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

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            emp_id TEXT NOT NULL,
            date TEXT NOT NULL,
            status TEXT NOT NULL,
            UNIQUE(emp_id, date)
        )
    """)

    # 2. Lists for realistic Indian context generation
    first_names_male = ["Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Sai", "Reyansh", "Ayaan", "Krishna", "Ishaan", "Dhruv", "Kian", "Ritvik", "Kabir", "Aarush", "Aniket", "Rohan", "Rahul", "Amit", "Alok"]
    first_names_female = ["Aadhya", "Diya", "Saanvi", "Ananya", "Pari", "Anika", "Navya", "Angel", "Aarohi", "Riya", "Pooja", "Neha", "Priyanka", "Sneha", "Kavya", "Tanvi", "Swati", "Puja", "Meera", "Divya"]
    last_names = ["Sharma", "Verma", "Gupta", "Malhotra", "Mehra", "Sen", "Bose", "Mukherjee", "Chatterjee", "Iyer", "Nair", "Pillai", "Menon", "Reddy", "Rao", "Patil", "Deshmukh", "Kulkarni", "Joshi", "Patel", "Shah", "Mehta", "Singh", "Kumar", "Yadav", "Mishra", "Tiwari"]

    departments = ["IT", "HR", "Finance", "Sales", "Operations"]
    designations = {
        "IT": ["Software Engineer", "Senior Developer", "DevOps Engineer", "QA Tester", "UI/UX Designer"],
        "HR": ["HR Executive", "Talent Acquisition Lead", "HR Manager", "Payroll Specialist"],
        "Finance": ["Accountant", "Financial Analyst", "Tax Consultant", "Finance Manager"],
        "Sales": ["Sales Executive", "Business Development Manager", "Account Executive", "Sales Representative"],
        "Operations": ["Operations Associate", "Logistics Coordinator", "Project Coordinator", "Operations Manager"]
    }
    cities = ["Mumbai, Maharashtra", "Bengaluru, Karnataka", "New Delhi, Delhi", "Hyderabad, Telangana", "Chennai, Tamil Nadu", "Pune, Maharashtra", "Kolkata, West Bengal", "Ahmedabad, Gujarat"]

    employees = []
    start_date = datetime(2022, 1, 1)

    # 3. Generate 50 Employees
    for i in range(1, 51):
        emp_id = f"EMP{i:03d}"
        gender = random.choice(["Male", "Female"])
        fname = random.choice(first_names_male if gender == "Male" else first_names_female)
        lname = random.choice(last_names)
        full_name = f"{fname} {lname}"
        
        age = random.randint(22, 58)
        phone = f"+91 {random.randint(70000, 99999)} {random.randint(10000, 99999)}"
        email = f"{fname.lower()}.{lname.lower()}{random.randint(10,99)}@company.in"
        address = f"Flat {random.randint(101, 904)}, {random.choice(cities)}"
        
        dept = random.choice(departments)
        desig = random.choice(designations[dept])
        
        days_offset = random.randint(0, 1000)
        joining_date = (start_date + timedelta(days=days_offset)).strftime("%Y-%m-%d")
        
        base_salaries = {"IT": 75000, "Finance": 60000, "HR": 50000, "Sales": 45000, "Operations": 40000}
        basic_salary = float(base_salaries[dept] + random.randint(-5000, 30000))
        status = "Active" if random.random() > 0.1 else "Inactive"
        
        employees.append((emp_id, full_name, age, gender, phone, email, address, dept, desig, joining_date, basic_salary, status))

    cursor.executemany("""
        INSERT OR REPLACE INTO employees (emp_id, full_name, age, gender, phone, email, address, department, designation, joining_date, basic_salary, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, employees)

    # 4. Generate Attendance for Today
    today_str = datetime.now().strftime("%Y-%m-%d")
    attendance_records = []
    for emp in employees:
        status_att = random.choices(["Present", "Absent", "Leave"], weights=[82, 13, 5])[0]
        attendance_records.append((emp[0], today_str, status_att))

    cursor.executemany("""
        INSERT OR REPLACE INTO attendance (emp_id, date, status)
        VALUES (?, ?, ?)
    """, attendance_records)

    conn.commit()
    conn.close()
    print("✅ Successfully seeded 50 Indian employee records and attendance data!")

if __name__ == "__main__":
    seed_database()