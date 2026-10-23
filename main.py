import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from database import init_db
from auth import verify_admin, change_password
from employees import generate_emp_id, add_employee, get_all_employees, update_employee, delete_employee
from attendance import mark_attendance, get_attendance_records
from payroll import calculate_payroll, save_payroll_record, get_payroll_records
from reports import export_table_to_csv, get_dashboard_stats

class EMSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Employee Management System - By OM_XCORE")
        self.root.geometry("1150x700")
        self.root.minsize(1000, 600)
        
        # Color Theme (Dark Navy & Blue)
        self.bg_dark = "#1e293b"
        self.bg_light = "#f8fafc"
        self.sidebar_bg = "#0f172a"
        self.accent_blue = "#2563eb"
        self.text_dark = "#0f172a"
        self.text_light = "#ffffff"
        
        self.current_user = "admin"
        init_db()
        self.show_login_screen()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # ==================== LOGIN SCREEN ====================
    def show_login_screen(self):
        self.clear_window()
        
        main_frame = tk.Frame(self.root, bg=self.bg_dark)
        main_frame.pack(fill=tk.BOTH, expand=True)

        card = tk.Frame(main_frame, bg="#ffffff", bd=2, relief=tk.GROOVE)
        card.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=400, height=380)

        tk.Label(card, text="Admin Portal", font=("Arial", 20, "bold"), bg="#ffffff", fg=self.text_dark).pack(pady=20)
        tk.Label(card, text="Employee Management System", font=("Arial", 10), bg="#ffffff", fg="#64748b").pack(pady=(0, 20))

        tk.Label(card, text="Username", font=("Arial", 10, "bold"), bg="#ffffff", fg=self.text_dark).pack(anchor="w", padx=40)
        self.user_entry = tk.Entry(card, font=("Arial", 11), bd=1, relief=tk.SOLID)
        self.user_entry.pack(fill=tk.X, padx=40, pady=5)
        self.user_entry.insert(0, "admin")

        tk.Label(card, text="Password", font=("Arial", 10, "bold"), bg="#ffffff", fg=self.text_dark).pack(anchor="w", padx=40, pady=(10, 0))
        self.pass_entry = tk.Entry(card, font=("Arial", 11), show="*", bd=1, relief=tk.SOLID)
        self.pass_entry.pack(fill=tk.X, padx=40, pady=5)
        self.pass_entry.insert(0, "admin123")

        btn = tk.Button(card, text="Login", font=("Arial", 11, "bold"), bg=self.accent_blue, fg=self.text_light, bd=0, cursor="hand2", command=self.handle_login)
        btn.pack(fill=tk.X, padx=40, pady=25, ipady=6)
        

    def handle_login(self):
        user = self.user_entry.get().strip()
        pwd = self.pass_entry.get().strip()
        if verify_admin(user, pwd):
            self.current_user = user
            self.show_dashboard_screen()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    # ==================== MAIN DASHBOARD LAYOUT ====================
    def show_dashboard_screen(self):
        self.clear_window()

        # Container Frame
        container = tk.Frame(self.root, bg=self.bg_light)
        container.pack(fill=tk.BOTH, expand=True)

        # Sidebar
        sidebar = tk.Frame(container, bg=self.sidebar_bg, width=220)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="EMS Portal", font=("Arial", 16, "bold"), bg=self.sidebar_bg, fg=self.text_light).pack(pady=25)

        nav_buttons = [
            ("Dashboard", self.load_dashboard_tab),
            ("Employees", self.load_employees_tab),
            ("Attendance", self.load_attendance_tab),
            ("Payroll", self.load_payroll_tab),
            ("Analytics & Graphs", self.load_analytics_tab),
            ("Reports & Export", self.load_reports_tab),
            ("Change Password", self.load_change_password_tab),
            ("Logout", self.show_login_screen)
        ]

        for text, cmd in nav_buttons:
            btn = tk.Button(sidebar, text=text, font=("Arial", 11), bg=self.sidebar_bg, fg="#cbd5e1", activebackground=self.accent_blue, activeforeground=self.text_light, bd=0, anchor="w", padx=25, command=cmd)
            btn.pack(fill=tk.X, pady=4, ipady=8)

        # Content Area
        self.content_area = tk.Frame(container, bg=self.bg_light)
        self.content_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.load_dashboard_tab()

    # ==================== TAB 1: DASHBOARD ====================
    def load_dashboard_tab(self):
        for w in self.content_area.winfo_children(): w.destroy()

        today_str = datetime.now().strftime("%Y-%m-%d")
        stats = get_dashboard_stats(today_str)

        header = tk.Label(self.content_area, text="Dashboard Overview", font=("Arial", 18, "bold"), bg=self.bg_light, fg=self.text_dark)
        header.pack(anchor="w", padx=30, pady=25)

        cards_frame = tk.Frame(self.content_area, bg=self.bg_light)
        cards_frame.pack(fill=tk.X, padx=30)

        card_data = [
            ("Total Employees", str(stats["total_emp"]), "#3b82f6"),
            ("Active Employees", str(stats["active_emp"]), "#10b981"),
            ("Present Today", str(stats["present_today"]), "#6366f1"),
            ("Absent Today", str(stats["absent_today"]), "#ef4444"),
            ("Monthly Payroll", f"₹{stats['total_payroll']:,.2f}", "#f59e0b")
        ]

        for title, val, color in card_data:
            frm = tk.Frame(cards_frame, bg="#ffffff", bd=1, relief=tk.SOLID)
            frm.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5, ipady=15)
            
            tk.Label(frm, text=title, font=("Arial", 10), bg="#ffffff", fg="#64748b").pack(pady=(10, 0))
            tk.Label(frm, text=val, font=("Arial", 16, "bold"), bg="#ffffff", fg=color).pack(pady=(5, 10))

    # ==================== TAB 2: EMPLOYEES ====================
    def load_employees_tab(self):
        for w in self.content_area.winfo_children(): w.destroy()

        top_frame = tk.Frame(self.content_area, bg=self.bg_light)
        top_frame.pack(fill=tk.X, padx=30, pady=20)

        tk.Label(top_frame, text="Employee Management", font=("Arial", 18, "bold"), bg=self.bg_light, fg=self.text_dark).pack(side=tk.LEFT)
        tk.Button(top_frame, text="+ Add Employee", font=("Arial", 10, "bold"), bg=self.accent_blue, fg=self.text_light, bd=0, padx=15, pady=8, command=self.open_add_employee_window).pack(side=tk.RIGHT)

        # Search & Filter
        filter_frame = tk.Frame(self.content_area, bg=self.bg_light)
        filter_frame.pack(fill=tk.X, padx=30, pady=5)

        tk.Label(filter_frame, text="Search (ID/Name):", bg=self.bg_light, font=("Arial", 10)).pack(side=tk.LEFT)
        self.emp_search_entry = tk.Entry(filter_frame, font=("Arial", 10), width=20)
        self.emp_search_entry.pack(side=tk.LEFT, padx=10)

        tk.Label(filter_frame, text="Department:", bg=self.bg_light, font=("Arial", 10)).pack(side=tk.LEFT, padx=(10,0))
        self.dept_combo = ttk.Combobox(filter_frame, values=["All Departments", "IT", "HR", "Finance", "Sales", "Operations"], state="readonly", width=15)
        self.dept_combo.set("All Departments")
        self.dept_combo.pack(side=tk.LEFT, padx=10)

        tk.Button(filter_frame, text="Filter", bg="#334155", fg="white", bd=0, padx=10, command=self.populate_employee_table).pack(side=tk.LEFT, padx=10)

        # Table
        table_frame = tk.Frame(self.content_area, bg=self.bg_light)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=15)

        columns = ("ID", "Name", "Dept", "Designation", "Phone", "Email", "Salary", "Status")
        self.emp_tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")
        
        for col in columns:
            self.emp_tree.heading(col, text=col)
            self.emp_tree.column(col, width=100)

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.emp_tree.yview)
        self.emp_tree.configure(yscrollcommand=scrollbar.set)

        self.emp_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.populate_employee_table()

    def populate_employee_table(self):
        for row in self.emp_tree.get_children():
            self.emp_tree.delete(row)

        search = self.emp_search_entry.get().strip() if hasattr(self, 'emp_search_entry') else None
        dept = self.dept_combo.get() if hasattr(self, 'dept_combo') else None

        employees = get_all_employees(search=search if search else None, department=dept)
        for emp in employees:
            self.emp_tree.insert("", tk.END, values=(
                emp['emp_id'], emp['full_name'], emp['department'], emp['designation'],
                emp['phone'], emp['email'], f"₹{emp['basic_salary']}", emp['status']
            ))

    def open_add_employee_window(self):
        win = tk.Toplevel(self.root)
        win.title("Add New Employee")
        win.geometry("500x600")

        fields = [
            ("Full Name", tk.Entry), ("Age", tk.Entry), ("Gender", ttk.Combobox),
            ("Phone", tk.Entry), ("Email", tk.Entry), ("Address", tk.Entry),
            ("Department", ttk.Combobox), ("Designation", tk.Entry),
            ("Joining Date (YYYY-MM-DD)", tk.Entry), ("Basic Salary", tk.Entry),
            ("Status", ttk.Combobox)
        ]

        entries = {}
        for i, (label, widget_type) in enumerate(fields):
            tk.Label(win, text=label, font=("Arial", 10)).grid(row=i, column=0, sticky="w", padx=30, pady=5)
            if widget_type == ttk.Combobox:
                w = widget_type(win, state="readonly")
                if label == "Gender": w['values'] = ["Male", "Female", "Other"]
                elif label == "Department": w['values'] = ["IT", "HR", "Finance", "Sales", "Operations"]
                elif label == "Status": w['values'] = ["Active", "Inactive"]
            else:
                w = widget_type(win, font=("Arial", 10))
                if label == "Joining Date (YYYY-MM-DD)":
                    w.insert(0, datetime.now().strftime("%Y-%m-%d"))
            w.grid(row=i, column=1, padx=30, pady=5, sticky="ew")
            entries[label] = w

        def save():
            try:
                data = {
                    'emp_id': generate_emp_id(),
                    'full_name': entries["Full Name"].get(),
                    'age': int(entries["Age"].get()),
                    'gender': entries["Gender"].get(),
                    'phone': entries["Phone"].get(),
                    'email': entries["Email"].get(),
                    'address': entries["Address"].get(),
                    'department': entries["Department"].get(),
                    'designation': entries["Designation"].get(),
                    'joining_date': entries["Joining Date (YYYY-MM-DD)"].get(),
                    'basic_salary': float(entries["Basic Salary"].get()),
                    'status': entries["Status"].get()
                }
                success, msg = add_employee(data)
                if success:
                    messagebox.showinfo("Success", msg)
                    win.destroy()
                    self.populate_employee_table()
                else:
                    messagebox.showerror("Error", msg)
            except ValueError:
                messagebox.showerror("Validation Error", "Please enter valid numeric values for Age and Salary.")

        tk.Button(win, text="Save Employee", bg=self.accent_blue, fg="white", font=("Arial", 10, "bold"), command=save).grid(row=len(fields), column=0, columnspan=2, pady=20, ipadx=20, ipady=5)

    # ==================== TAB 3: ATTENDANCE ====================
    def load_attendance_tab(self):
        for w in self.content_area.winfo_children(): w.destroy()

        tk.Label(self.content_area, text="Attendance Management", font=("Arial", 18, "bold"), bg=self.bg_light, fg=self.text_dark).pack(anchor="w", padx=30, pady=25)

        form_frame = tk.Frame(self.content_area, bg=self.bg_light)
        form_frame.pack(fill=tk.X, padx=30)

        tk.Label(form_frame, text="Employee ID:", font=("Arial", 10)).pack(side=tk.LEFT)
        self.att_emp_id = tk.Entry(form_frame, font=("Arial", 10), width=15)
        self.att_emp_id.pack(side=tk.LEFT, padx=10)

        tk.Label(form_frame, text="Status:", font=("Arial", 10)).pack(side=tk.LEFT, padx=(10, 0))
        self.att_status = ttk.Combobox(form_frame, values=["Present", "Absent", "Leave"], state="readonly", width=12)
        self.att_status.set("Present")
        self.att_status.pack(side=tk.LEFT, padx=10)

        tk.Button(form_frame, text="Mark Attendance", bg=self.accent_blue, fg="white", bd=0, padx=15, pady=5, command=self.submit_attendance).pack(side=tk.LEFT, padx=15)

        # Attendance Table
        table_frame = tk.Frame(self.content_area, bg=self.bg_light)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=25)

        columns = ("ID", "Emp ID", "Name", "Department", "Date", "Status")
        self.att_tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        for col in columns:
            self.att_tree.heading(col, text=col)
            self.att_tree.column(col, width=120)

        self.att_tree.pack(fill=tk.BOTH, expand=True)
        self.populate_attendance_table()

    def submit_attendance(self):
        emp_id = self.att_emp_id.get().strip()
        status = self.att_status.get()
        date_str = datetime.now().strftime("%Y-%m-%d")

        if not emp_id:
            messagebox.showerror("Error", "Please enter Employee ID.")
            return

        success, msg = mark_attendance(emp_id, date_str, status)
        if success:
            messagebox.showinfo("Success", msg)
            self.populate_attendance_table()
        else:
            messagebox.showerror("Error", msg)

    def populate_attendance_table(self):
        for row in self.att_tree.get_children():
            self.att_tree.delete(row)
        records = get_attendance_records()
        for r in records:
            self.att_tree.insert("", tk.END, values=(r['id'], r['emp_id'], r['full_name'], r['department'], r['date'], r['status']))

    # ==================== TAB 4: PAYROLL ====================
    def load_payroll_tab(self):
        for w in self.content_area.winfo_children(): w.destroy()

        tk.Label(self.content_area, text="Salary & Payroll Management", font=("Arial", 18, "bold"), bg=self.bg_light, fg=self.text_dark).pack(anchor="w", padx=30, pady=25)

        form_frame = tk.Frame(self.content_area, bg=self.bg_light)
        form_frame.pack(fill=tk.X, padx=30)

        tk.Label(form_frame, text="Emp ID:", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=5)
        self.pay_emp_id = tk.Entry(form_frame, font=("Arial", 10))
        self.pay_emp_id.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Month (e.g., Oct 2026):", font=("Arial", 10)).grid(row=0, column=2, sticky="w", pady=5)
        self.pay_month = tk.Entry(form_frame, font=("Arial", 10))
        self.pay_month.insert(0, datetime.now().strftime("%b %Y"))
        self.pay_month.grid(row=0, column=3, padx=10, pady=5)

        tk.Label(form_frame, text="Basic Salary (₹):", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=5)
        self.pay_basic = tk.Entry(form_frame, font=("Arial", 10))
        self.pay_basic.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Allowances (₹):", font=("Arial", 10)).grid(row=1, column=2, sticky="w", pady=5)
        self.pay_allow = tk.Entry(form_frame, font=("Arial", 10))
        self.pay_allow.insert(0, "2000")
        self.pay_allow.grid(row=1, column=3, padx=10, pady=5)

        tk.Label(form_frame, text="Deductions (₹):", font=("Arial", 10)).grid(row=2, column=0, sticky="w", pady=5)
        self.pay_deduct = tk.Entry(form_frame, font=("Arial", 10))
        self.pay_deduct.insert(0, "500")
        self.pay_deduct.grid(row=2, column=1, padx=10, pady=5)

        tk.Button(form_frame, text="Process Payroll", bg=self.accent_blue, fg="white", bd=0, padx=15, pady=5, command=self.process_payroll).grid(row=2, column=3, pady=10, sticky="e")

        # Table
        table_frame = tk.Frame(self.content_area, bg=self.bg_light)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)

        columns = ("ID", "Emp ID", "Name", "Month", "Basic", "Allowances", "Deductions", "Net Salary")
        self.pay_tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        for col in columns:
            self.pay_tree.heading(col, text=col)
            self.pay_tree.column(col, width=100)

        self.pay_tree.pack(fill=tk.BOTH, expand=True)
        self.populate_payroll_table()

    def process_payroll(self):
        try:
            emp_id = self.pay_emp_id.get().strip()
            month = self.pay_month.get().strip()
            basic = float(self.pay_basic.get())
            allow = float(self.pay_allow.get())
            deduct = float(self.pay_deduct.get())

            _, net = calculate_payroll(basic, allow, deduct)
            date_str = datetime.now().strftime("%Y-%m-%d")

            success, msg = save_payroll_record(emp_id, month, basic, allow, deduct, net, date_str)
            if success:
                messagebox.showinfo("Success", f"{msg}\nNet Salary Calculated: ₹{net:,.2f}")
                self.populate_payroll_table()
            else:
                messagebox.showerror("Error", msg)
        except ValueError:
            messagebox.showerror("Validation Error", "Please enter valid numeric values for salary components.")

    def populate_payroll_table(self):
        for row in self.pay_tree.get_children():
            self.pay_tree.delete(row)
        records = get_payroll_records()
        for r in records:
            self.pay_tree.insert("", tk.END, values=(
                r['id'], r['emp_id'], r['full_name'], r['month'],
                f"₹{r['basic_salary']}", f"₹{r['allowances']}", f"₹{r['deductions']}", f"₹{r['net_salary']}"
            ))

    # ==================== TAB 5: ANALYTICS & GRAPHS ====================
    def load_analytics_tab(self):
        for w in self.content_area.winfo_children(): w.destroy()

        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        from database import get_connection

        tk.Label(self.content_area, text="Department & Payroll Analytics", font=("Arial", 18, "bold"), bg=self.bg_light, fg=self.text_dark).pack(anchor="w", padx=30, pady=20)

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT department, COUNT(*) FROM employees GROUP BY department")
        dept_data = cursor.fetchall()
        cursor.execute("SELECT department, SUM(basic_salary) FROM employees GROUP BY department")
        sal_data = cursor.fetchall()
        conn.close()

        depts = [row[0] for row in dept_data] if dept_data else ["No Data"]
        counts = [row[1] for row in dept_data] if dept_data else [0]
        sal_depts = [row[0] for row in sal_data] if sal_data else ["No Data"]
        salaries = [row[1] for row in sal_data] if sal_data else [0]

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5))
        fig.patch.set_facecolor('#f8fafc')

        ax1.bar(depts, counts, color='#2563eb', width=0.5)
        ax1.set_title("Employees per Department", fontsize=11, fontweight='bold', color='#0f172a')
        ax1.set_ylabel("Count", fontsize=10)
        ax1.tick_params(axis='x', rotation=15)
        ax1.set_facecolor('#ffffff')

        ax2.pie(salaries, labels=sal_depts, autopct='%1.1f%%', startangle=140, colors=['#3b82f6', '#10b981', '#f59e0b', '#6366f1', '#ef4444'])
        ax2.set_title("Payroll Budget Share by Dept", fontsize=11, fontweight='bold', color='#0f172a')

        fig.tight_layout()

        canvas_frame = tk.Frame(self.content_area, bg=self.bg_light)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)

        canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # ==================== TAB 6: REPORTS & EXPORT ====================
    def load_reports_tab(self):
        for w in self.content_area.winfo_children(): w.destroy()

        tk.Label(self.content_area, text="Reports & CSV Export", font=("Arial", 18, "bold"), bg=self.bg_light, fg=self.text_dark).pack(anchor="w", padx=30, pady=25)

        btn_frame = tk.Frame(self.content_area, bg=self.bg_light)
        btn_frame.pack(fill=tk.X, padx=30)

        tk.Button(btn_frame, text="Export Employees CSV", bg="#10b981", fg="white", font=("Arial", 10, "bold"), bd=0, padx=15, pady=10, command=self.export_employees).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Export Attendance CSV", bg="#3b82f6", fg="white", font=("Arial", 10, "bold"), bd=0, padx=15, pady=10, command=self.export_attendance).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Export Payroll CSV", bg="#f59e0b", fg="white", font=("Arial", 10, "bold"), bd=0, padx=15, pady=10, command=self.export_payroll).pack(side=tk.LEFT, padx=10)

    def export_employees(self):
        emps = get_all_employees()
        headers = ["Emp ID", "Full Name", "Age", "Gender", "Phone", "Email", "Department", "Designation", "Joining Date", "Basic Salary", "Status"]
        rows = [[e['emp_id'], e['full_name'], e['age'], e['gender'], e['phone'], e['email'], e['department'], e['designation'], e['joining_date'], e['basic_salary'], e['status']] for e in emps]
        success, msg = export_table_to_csv("employees_report.csv", headers, rows)
        if success: messagebox.showinfo("Success", msg)
        else: messagebox.showerror("Error", msg)

    def export_attendance(self):
        atts = get_attendance_records()
        headers = ["ID", "Emp ID", "Full Name", "Department", "Date", "Status"]
        rows = [[a['id'], a['emp_id'], a['full_name'], a['department'], a['date'], a['status']] for a in atts]
        success, msg = export_table_to_csv("attendance_report.csv", headers, rows)
        if success: messagebox.showinfo("Success", msg)
        else: messagebox.showerror("Error", msg)

    def export_payroll(self):
        pays = get_payroll_records()
        headers = ["ID", "Emp ID", "Full Name", "Department", "Month", "Basic", "Allowances", "Deductions", "Net Salary", "Payment Date"]
        rows = [[p['id'], p['emp_id'], p['full_name'], p['department'], p['month'], p['basic_salary'], p['allowances'], p['deductions'], p['net_salary'], p['payment_date']] for p in pays]
        success, msg = export_table_to_csv("payroll_report.csv", headers, rows)
        if success: messagebox.showinfo("Success", msg)
        else: messagebox.showerror("Error", msg)

    # ==================== TAB 7: CHANGE PASSWORD ====================
    def load_change_password_tab(self):
        for w in self.content_area.winfo_children(): w.destroy()

        tk.Label(self.content_area, text="Change Admin Password", font=("Arial", 18, "bold"), bg=self.bg_light, fg=self.text_dark).pack(anchor="w", padx=30, pady=25)

        card = tk.Frame(self.content_area, bg="#ffffff", bd=1, relief=tk.SOLID)
        card.pack(anchor="w", padx=30, pady=10, ipadx=20, ipady=20)

        tk.Label(card, text="Current Password", font=("Arial", 10, "bold"), bg="#ffffff", fg=self.text_dark).pack(anchor="w", padx=20, pady=(10, 0))
        self.old_pass_entry = tk.Entry(card, font=("Arial", 11), show="*", width=30, bd=1, relief=tk.SOLID)
        self.old_pass_entry.pack(anchor="w", padx=20, pady=5)

        tk.Label(card, text="New Password", font=("Arial", 10, "bold"), bg="#ffffff", fg=self.text_dark).pack(anchor="w", padx=20, pady=(10, 0))
        self.new_pass_entry = tk.Entry(card, font=("Arial", 11), show="*", width=30, bd=1, relief=tk.SOLID)
        self.new_pass_entry.pack(anchor="w", padx=20, pady=5)

        tk.Label(card, text="Confirm New Password", font=("Arial", 10, "bold"), bg="#ffffff", fg=self.text_dark).pack(anchor="w", padx=20, pady=(10, 0))
        self.confirm_pass_entry = tk.Entry(card, font=("Arial", 11), show="*", width=30, bd=1, relief=tk.SOLID)
        self.confirm_pass_entry.pack(anchor="w", padx=20, pady=5)

        tk.Button(card, text="Update Password", font=("Arial", 10, "bold"), bg=self.accent_blue, fg="white", bd=0, padx=15, pady=8, command=self.submit_password_change).pack(anchor="w", padx=20, pady=20)

    def submit_password_change(self):
        old_pwd = self.old_pass_entry.get()
        new_pwd = self.new_pass_entry.get()
        confirm_pwd = self.confirm_pass_entry.get()

        if not old_pwd or not new_pwd or not confirm_pwd:
            messagebox.showerror("Error", "All fields are required.")
            return

        if new_pwd != confirm_pwd:
            messagebox.showerror("Error", "New passwords do not match.")
            return

        success, msg = change_password(self.current_user, old_pwd, new_pwd)
        if success:
            messagebox.showinfo("Success", msg)
            self.load_dashboard_tab()
        else:
            messagebox.showerror("Error", msg)

if __name__ == "__main__":
    root = tk.Tk()
    app = EMSApp(root)
    root.mainloop()