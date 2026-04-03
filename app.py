"""
app.py
Smart Bus Pass Issuing System — Main Dashboard (Tkinter)
Run:  python app.py
"""

import tkinter as tk
from tkinter import ttk, messagebox, font
import db_helper as db

# ─── Colour palette ───────────────────────────────────────────────────────────
BG       = "#0D1B2A"   # deep navy
CARD     = "#1B2A3B"   # dark card
ACCENT   = "#00C2A8"   # teal
ACCENT2  = "#F4A261"   # warm orange
TEXT     = "#E8EDF2"
SUBTEXT  = "#8899AA"
SUCCESS  = "#2ECC71"
DANGER   = "#E74C3C"
WARNING  = "#F39C12"
WHITE    = "#FFFFFF"


# ─── Base window ──────────────────────────────────────────────────────────────
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        db.init_db()
        self.title("Smart Bus Pass Issuing System")
        self.geometry("1280x780")
        self.configure(bg=BG)
        self.resizable(True, True)
        self._setup_style()
        self._build_layout()

    # ── ttk styles ────────────────────────────────────────────────────────────
    def _setup_style(self):
        s = ttk.Style(self)
        s.theme_use("clam")
        s.configure(".",           background=BG,    foreground=TEXT, font=("Segoe UI", 10))
        s.configure("TFrame",      background=BG)
        s.configure("Card.TFrame", background=CARD)
        s.configure("TLabel",      background=BG,    foreground=TEXT)
        s.configure("Card.TLabel", background=CARD,  foreground=TEXT)
        s.configure("Sub.TLabel",  background=CARD,  foreground=SUBTEXT, font=("Segoe UI", 9))
        s.configure("Head.TLabel", background=BG,    foreground=ACCENT,
                    font=("Segoe UI", 22, "bold"))
        s.configure("Accent.TButton", background=ACCENT, foreground=BG,
                    font=("Segoe UI", 10, "bold"), relief="flat", padding=6)
        s.map("Accent.TButton", background=[("active", "#009f8a")])
        s.configure("Danger.TButton", background=DANGER, foreground=WHITE,
                    font=("Segoe UI", 10, "bold"), relief="flat", padding=6)
        s.map("Danger.TButton", background=[("active", "#c0392b")])
        s.configure("Nav.TButton", background=CARD, foreground=TEXT,
                    font=("Segoe UI", 11), relief="flat", padding=10)
        s.map("Nav.TButton", background=[("active", ACCENT)],
                              foreground=[("active", BG)])
        # Treeview
        s.configure("Treeview",           background=CARD,  foreground=TEXT,
                    fieldbackground=CARD, rowheight=26,     font=("Segoe UI", 9))
        s.configure("Treeview.Heading",   background=BG,    foreground=ACCENT,
                    font=("Segoe UI", 9, "bold"), relief="flat")
        s.map("Treeview", background=[("selected", ACCENT)],
                          foreground=[("selected", BG)])
        # Entry / Combobox
        s.configure("TEntry",    fieldbackground="#1f3048", foreground=TEXT,
                    insertcolor=TEXT, relief="flat")
        s.configure("TCombobox", fieldbackground="#1f3048", foreground=TEXT,
                    selectbackground=ACCENT, relief="flat")

    # ── Layout skeleton ───────────────────────────────────────────────────────
    def _build_layout(self):
        # Sidebar
        self.sidebar = tk.Frame(self, bg=CARD, width=210)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        tk.Label(self.sidebar, text="🚌", bg=CARD, fg=ACCENT,
                 font=("Segoe UI", 30)).pack(pady=(20, 0))
        tk.Label(self.sidebar, text="BusPass\nSystem", bg=CARD, fg=TEXT,
                 font=("Segoe UI", 13, "bold"), justify="center").pack(pady=(4, 24))

        ttk.Separator(self.sidebar, orient="horizontal").pack(fill="x", padx=10)

        nav_items = [
            ("📊  Dashboard",  self.show_dashboard),
            ("👤  Students",   self.show_students),
            ("🎫  Bus Passes", self.show_passes),
            ("💳  Payments",   self.show_payments),
            ("🗺️   Routes",    self.show_routes),
        ]
        for label, cmd in nav_items:
            ttk.Button(self.sidebar, text=label, style="Nav.TButton",
                       command=cmd).pack(fill="x", padx=8, pady=3)

        # Main content area
        self.main = tk.Frame(self, bg=BG)
        self.main.pack(side="left", fill="both", expand=True)

        self.show_dashboard()

    def _clear_main(self):
        for w in self.main.winfo_children():
            w.destroy()

    # ══════════════════════════════════════════════════════════════════════════
    # DASHBOARD
    # ══════════════════════════════════════════════════════════════════════════
    def show_dashboard(self):
        self._clear_main()
        stats = db.get_dashboard_stats()

        tk.Label(self.main, text="Dashboard Overview",
                 style="Head.TLabel" if False else None,
                 bg=BG, fg=ACCENT, font=("Segoe UI", 22, "bold")).pack(
                 anchor="w", padx=30, pady=(28, 4))
        tk.Label(self.main, text="Welcome to Smart Bus Pass Issuing System",
                 bg=BG, fg=SUBTEXT, font=("Segoe UI", 10)).pack(
                 anchor="w", padx=30, pady=(0, 20))

        # Stat cards row
        cards_frame = tk.Frame(self.main, bg=BG)
        cards_frame.pack(fill="x", padx=24)

        card_data = [
            ("Total Students",  stats["total_students"],  "👤", ACCENT),
            ("Total Passes",    stats["total_passes"],    "🎫", ACCENT2),
            ("Active Passes",   stats["active_passes"],   "✅", SUCCESS),
            ("Expired Passes",  stats["expired_passes"],  "❌", DANGER),
            ("Total Revenue",   f"₹{stats['total_revenue']:.0f}", "💰", WARNING),
            ("This Month",      f"₹{stats['monthly_revenue']:.0f}", "📅", "#9B59B6"),
        ]
        for i, (label, val, icon, color) in enumerate(card_data):
            c = tk.Frame(cards_frame, bg=CARD, padx=18, pady=14,
                         highlightbackground=color, highlightthickness=2)
            c.grid(row=0, column=i, padx=6, sticky="ew")
            cards_frame.columnconfigure(i, weight=1)
            tk.Label(c, text=icon, bg=CARD, fg=color,
                     font=("Segoe UI", 22)).pack(anchor="w")
            tk.Label(c, text=str(val), bg=CARD, fg=WHITE,
                     font=("Segoe UI", 18, "bold")).pack(anchor="w")
            tk.Label(c, text=label, bg=CARD, fg=SUBTEXT,
                     font=("Segoe UI", 9)).pack(anchor="w")

        # Recent passes
        tk.Label(self.main, text="Recent Bus Passes",
                 bg=BG, fg=TEXT, font=("Segoe UI", 13, "bold")).pack(
                 anchor="w", padx=30, pady=(28, 8))

        cols = ("Pass No", "Student", "Route", "Type", "Expiry", "Status")
        tree = ttk.Treeview(self.main, columns=cols, show="headings", height=10)
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=140 if c == "Student" else 110, anchor="center")
        tree.pack(fill="both", expand=True, padx=24, pady=(0, 20))

        scrollbar = ttk.Scrollbar(tree, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        for p in db.get_all_passes()[:15]:
            status_icon = "🟢" if p["status"] == "Active" else ("🔴" if p["status"] == "Expired" else "⚪")
            tree.insert("", "end", values=(
                p["pass_number"], p["student_name"],
                f"{p['route_number']}: {p['source']}→{p['destination']}",
                p["pass_type"], p["expiry_date"],
                f"{status_icon} {p['status']}"
            ))

    # ══════════════════════════════════════════════════════════════════════════
    # STUDENTS
    # ══════════════════════════════════════════════════════════════════════════
    def show_students(self):
        self._clear_main()
        header_frame = tk.Frame(self.main, bg=BG)
        header_frame.pack(fill="x", padx=24, pady=(24, 8))
        tk.Label(header_frame, text="Student Management",
                 bg=BG, fg=ACCENT, font=("Segoe UI", 18, "bold")).pack(side="left")
        ttk.Button(header_frame, text="+ Add Student",
                   style="Accent.TButton",
                   command=self.open_add_student).pack(side="right")

        # Search bar
        sf = tk.Frame(self.main, bg=BG)
        sf.pack(fill="x", padx=24, pady=(0, 8))
        tk.Label(sf, text="Search:", bg=BG, fg=TEXT).pack(side="left")
        self.stu_search = ttk.Entry(sf, width=30)
        self.stu_search.pack(side="left", padx=6)
        ttk.Button(sf, text="🔍 Search", style="Accent.TButton",
                   command=self._search_students).pack(side="left")
        ttk.Button(sf, text="Show All", style="Nav.TButton",
                   command=self._load_students).pack(side="left", padx=4)

        cols = ("ID", "Name", "Roll No", "College", "Course", "Year", "Phone", "Email")
        self.stu_tree = ttk.Treeview(self.main, columns=cols, show="headings", height=16)
        for c in cols:
            self.stu_tree.heading(c, text=c)
            w = 60 if c == "ID" else (80 if c in ("Year","Phone") else 130)
            self.stu_tree.column(c, width=w, anchor="center")
        self.stu_tree.pack(fill="both", expand=True, padx=24)
        self.stu_tree.bind("<Double-1>", self._on_student_double_click)

        btn_row = tk.Frame(self.main, bg=BG)
        btn_row.pack(fill="x", padx=24, pady=8)
        ttk.Button(btn_row, text="✏️  Edit Selected", style="Accent.TButton",
                   command=self._edit_student).pack(side="left", padx=4)
        ttk.Button(btn_row, text="🗑️  Delete Selected", style="Danger.TButton",
                   command=self._delete_student).pack(side="left", padx=4)
        ttk.Button(btn_row, text="🎫  Issue Pass", style="Accent.TButton",
                   command=self._issue_pass_for_student).pack(side="left", padx=4)

        self._load_students()

    def _load_students(self, rows=None):
        self.stu_tree.delete(*self.stu_tree.get_children())
        for s in (rows or db.get_all_students()):
            self.stu_tree.insert("", "end", values=(
                s["student_id"], s["name"], s["roll_number"],
                s["college_name"], s["course"], s["year_of_study"],
                s["phone"], s["email"]
            ))

    def _search_students(self):
        q = self.stu_search.get().strip()
        if q:
            self._load_students(db.search_students(q))

    def _get_selected_student_id(self):
        sel = self.stu_tree.selection()
        if not sel:
            messagebox.showwarning("Select", "Please select a student first.")
            return None
        return self.stu_tree.item(sel[0])["values"][0]

    def _on_student_double_click(self, _event):
        self._edit_student()

    def _edit_student(self):
        sid = self._get_selected_student_id()
        if sid:
            s = db.get_student_by_id(sid)
            if s:
                StudentForm(self, s)

    def _delete_student(self):
        sid = self._get_selected_student_id()
        if sid and messagebox.askyesno("Confirm", "Delete this student?"):
            ok, msg = db.delete_student(sid)
            messagebox.showinfo("Done", msg)
            self._load_students()

    def _issue_pass_for_student(self):
        sid = self._get_selected_student_id()
        if sid:
            IssuePassForm(self, sid)

    def open_add_student(self):
        StudentForm(self)

    # ══════════════════════════════════════════════════════════════════════════
    # BUS PASSES
    # ══════════════════════════════════════════════════════════════════════════
    def show_passes(self):
        self._clear_main()
        header_frame = tk.Frame(self.main, bg=BG)
        header_frame.pack(fill="x", padx=24, pady=(24, 8))
        tk.Label(header_frame, text="Bus Pass Management",
                 bg=BG, fg=ACCENT, font=("Segoe UI", 18, "bold")).pack(side="left")
        ttk.Button(header_frame, text="+ Issue New Pass",
                   style="Accent.TButton",
                   command=lambda: IssuePassForm(self, None)).pack(side="right")

        sf = tk.Frame(self.main, bg=BG)
        sf.pack(fill="x", padx=24, pady=(0, 8))
        tk.Label(sf, text="Search:", bg=BG, fg=TEXT).pack(side="left")
        self.pass_search = ttk.Entry(sf, width=30)
        self.pass_search.pack(side="left", padx=6)
        ttk.Button(sf, text="🔍 Search", style="Accent.TButton",
                   command=self._search_passes).pack(side="left")
        ttk.Button(sf, text="Show All", style="Nav.TButton",
                   command=self._load_passes).pack(side="left", padx=4)

        cols = ("ID", "Pass No", "Student", "Roll", "Route", "Type", "Issued", "Expiry", "Amount", "Status")
        self.pass_tree = ttk.Treeview(self.main, columns=cols, show="headings", height=15)
        for c in cols:
            self.pass_tree.heading(c, text=c)
            w = {"ID": 40, "Pass No": 110, "Student": 130, "Roll": 90,
                 "Route": 130, "Type": 80, "Issued": 90, "Expiry": 90,
                 "Amount": 70, "Status": 80}.get(c, 90)
            self.pass_tree.column(c, width=w, anchor="center")

        sb = ttk.Scrollbar(self.main, orient="horizontal", command=self.pass_tree.xview)
        self.pass_tree.configure(xscrollcommand=sb.set)
        self.pass_tree.pack(fill="both", expand=True, padx=24)
        sb.pack(fill="x", padx=24)

        btn_row = tk.Frame(self.main, bg=BG)
        btn_row.pack(fill="x", padx=24, pady=8)
        for label, cmd in [
            ("✅ Set Active",    lambda: self._update_pass_status("Active")),
            ("❌ Set Expired",   lambda: self._update_pass_status("Expired")),
            ("⚪ Cancel Pass",   lambda: self._update_pass_status("Cancelled")),
            ("🗑️  Delete Pass",  self._delete_pass),
        ]:
            style = "Danger.TButton" if "Delete" in label or "Cancel" in label else "Accent.TButton"
            ttk.Button(btn_row, text=label, style=style, command=cmd).pack(side="left", padx=4)

        self._load_passes()

    def _load_passes(self, rows=None):
        self.pass_tree.delete(*self.pass_tree.get_children())
        for p in (rows or db.get_all_passes()):
            self.pass_tree.insert("", "end", values=(
                p["pass_id"], p["pass_number"], p["student_name"],
                p["roll_number"],
                f"{p['route_number']}: {p['source']}→{p['destination']}",
                p["pass_type"], p["issue_date"], p["expiry_date"],
                f"₹{p['amount_paid']}", p["status"]
            ))

    def _search_passes(self):
        q = self.pass_search.get().strip()
        if q:
            self._load_passes(db.search_passes(q))

    def _get_selected_pass_id(self):
        sel = self.pass_tree.selection()
        if not sel:
            messagebox.showwarning("Select", "Please select a pass first.")
            return None
        return self.pass_tree.item(sel[0])["values"][0]

    def _update_pass_status(self, status):
        pid = self._get_selected_pass_id()
        if pid:
            ok, msg = db.update_pass_status(pid, status)
            messagebox.showinfo("Done", msg)
            self._load_passes()

    def _delete_pass(self):
        pid = self._get_selected_pass_id()
        if pid and messagebox.askyesno("Confirm", "Delete this pass and its payment?"):
            ok, msg = db.delete_pass(pid)
            messagebox.showinfo("Done", msg)
            self._load_passes()

    # ══════════════════════════════════════════════════════════════════════════
    # PAYMENTS
    # ══════════════════════════════════════════════════════════════════════════
    def show_payments(self):
        self._clear_main()
        tk.Label(self.main, text="Payment Records",
                 bg=BG, fg=ACCENT, font=("Segoe UI", 18, "bold")).pack(
                 anchor="w", padx=24, pady=(24, 16))

        cols = ("Pay ID", "Pass No", "Student", "Amount", "Mode", "Receipt No", "Date")
        tree = ttk.Treeview(self.main, columns=cols, show="headings", height=20)
        for c in cols:
            tree.heading(c, text=c)
            w = {"Pay ID": 55, "Pass No": 120, "Student": 150, "Amount": 80,
                 "Mode": 80, "Receipt No": 140, "Date": 130}.get(c, 100)
            tree.column(c, width=w, anchor="center")
        tree.pack(fill="both", expand=True, padx=24, pady=(0, 16))

        total = 0
        for p in db.get_all_payments():
            tree.insert("", "end", values=(
                p["payment_id"], p["pass_number"], p["student_name"],
                f"₹{p['amount']}", p["payment_mode"],
                p["receipt_number"], p["payment_date"]
            ))
            total += p["amount"]

        tk.Label(self.main, text=f"Total Revenue Collected: ₹{total:.2f}",
                 bg=BG, fg=SUCCESS, font=("Segoe UI", 12, "bold")).pack(
                 anchor="e", padx=30, pady=8)

    # ══════════════════════════════════════════════════════════════════════════
    # ROUTES
    # ══════════════════════════════════════════════════════════════════════════
    def show_routes(self):
        self._clear_main()
        tk.Label(self.main, text="Available Routes",
                 bg=BG, fg=ACCENT, font=("Segoe UI", 18, "bold")).pack(
                 anchor="w", padx=24, pady=(24, 16))

        cols = ("Route No", "Source", "Destination", "Distance (km)", "Fare (₹)")
        tree = ttk.Treeview(self.main, columns=cols, show="headings", height=10)
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=180, anchor="center")
        tree.pack(padx=24, pady=8)

        for r in db.get_all_routes():
            tree.insert("", "end", values=(
                r["route_number"], r["source"], r["destination"],
                r["distance_km"], f"₹{r['fare']}"
            ))

        tk.Label(self.main,
                 text="Routes are pre-configured by administration.",
                 bg=BG, fg=SUBTEXT, font=("Segoe UI", 9)).pack(
                 anchor="w", padx=24, pady=4)


# ══════════════════════════════════════════════════════════════════════════════
# STUDENT FORM (Add / Edit)
# ══════════════════════════════════════════════════════════════════════════════
class StudentForm(tk.Toplevel):
    def __init__(self, parent, data=None):
        super().__init__(parent)
        self.parent = parent
        self.data   = data
        self.title("Edit Student" if data else "Add Student")
        self.configure(bg=BG)
        self.geometry("480x520")
        self.grab_set()
        self._build()
        if data:
            self._fill(data)

    def _build(self):
        tk.Label(self, text="Student Details",
                 bg=BG, fg=ACCENT, font=("Segoe UI", 14, "bold")).pack(pady=(18, 10))
        f = tk.Frame(self, bg=BG, padx=30)
        f.pack(fill="both", expand=True)

        fields = [
            ("Full Name",       "name"),
            ("Roll Number",     "roll"),
            ("College Name",    "college"),
            ("Course",          "course"),
            ("Year of Study",   "year"),
            ("Phone",           "phone"),
            ("Email",           "email"),
            ("Address",         "address"),
        ]
        self.vars = {}
        for i, (label, key) in enumerate(fields):
            tk.Label(f, text=label, bg=BG, fg=TEXT,
                     font=("Segoe UI", 10)).grid(row=i, column=0, sticky="w", pady=4)
            v = tk.StringVar()
            ttk.Entry(f, textvariable=v, width=30).grid(row=i, column=1, padx=10, pady=4)
            self.vars[key] = v

        ttk.Button(self, text="💾  Save", style="Accent.TButton",
                   command=self._save).pack(pady=16)

    def _fill(self, d):
        self.vars["name"].set(d["name"])
        self.vars["roll"].set(d["roll_number"])
        self.vars["college"].set(d["college_name"])
        self.vars["course"].set(d["course"])
        self.vars["year"].set(d["year_of_study"])
        self.vars["phone"].set(d["phone"])
        self.vars["email"].set(d["email"])
        self.vars["address"].set(d["address"])

    def _save(self):
        v = {k: var.get().strip() for k, var in self.vars.items()}
        if not all(v.values()):
            messagebox.showwarning("Validation", "All fields are required.", parent=self)
            return
        try:
            year = int(v["year"])
        except ValueError:
            messagebox.showwarning("Validation", "Year must be a number.", parent=self)
            return
        if self.data:
            ok, msg = db.update_student(
                self.data["student_id"],
                v["name"], v["roll"], v["college"], v["course"],
                year, v["phone"], v["email"], v["address"]
            )
        else:
            ok, msg = db.add_student(
                v["name"], v["roll"], v["college"], v["course"],
                year, v["phone"], v["email"], v["address"]
            )
        if ok:
            messagebox.showinfo("Success", msg, parent=self)
            self.parent.show_students()
            self.destroy()
        else:
            messagebox.showerror("Error", msg, parent=self)


# ══════════════════════════════════════════════════════════════════════════════
# ISSUE PASS FORM
# ══════════════════════════════════════════════════════════════════════════════
class IssuePassForm(tk.Toplevel):
    def __init__(self, parent, student_id=None):
        super().__init__(parent)
        self.parent     = parent
        self.pre_sid    = student_id
        self.title("Issue Bus Pass")
        self.configure(bg=BG)
        self.geometry("460x420")
        self.grab_set()
        self._build()

    def _build(self):
        tk.Label(self, text="Issue Bus Pass",
                 bg=BG, fg=ACCENT, font=("Segoe UI", 14, "bold")).pack(pady=(18, 10))
        f = tk.Frame(self, bg=BG, padx=30)
        f.pack(fill="both", expand=True)

        # Student
        tk.Label(f, text="Student ID", bg=BG, fg=TEXT).grid(row=0, column=0, sticky="w", pady=6)
        self.sid_var = tk.StringVar(value=str(self.pre_sid) if self.pre_sid else "")
        ttk.Entry(f, textvariable=self.sid_var, width=28).grid(row=0, column=1, padx=10, pady=6)

        # Route
        routes = db.get_all_routes()
        self.route_map = {f"{r['route_number']}: {r['source']} → {r['destination']} (₹{r['fare']})": r
                          for r in routes}
        route_labels = list(self.route_map.keys())
        tk.Label(f, text="Route", bg=BG, fg=TEXT).grid(row=1, column=0, sticky="w", pady=6)
        self.route_var = tk.StringVar()
        ttk.Combobox(f, textvariable=self.route_var,
                     values=route_labels, width=30, state="readonly").grid(
                     row=1, column=1, padx=10, pady=6)

        # Pass Type
        tk.Label(f, text="Pass Type", bg=BG, fg=TEXT).grid(row=2, column=0, sticky="w", pady=6)
        self.type_var = tk.StringVar(value="Monthly")
        ttk.Combobox(f, textvariable=self.type_var,
                     values=["Monthly", "Quarterly", "Annual"],
                     width=28, state="readonly").grid(row=2, column=1, padx=10, pady=6)

        # Amount
        tk.Label(f, text="Amount (₹)", bg=BG, fg=TEXT).grid(row=3, column=0, sticky="w", pady=6)
        self.amount_var = tk.StringVar()
        ttk.Entry(f, textvariable=self.amount_var, width=28).grid(row=3, column=1, padx=10, pady=6)

        # Payment Mode
        tk.Label(f, text="Payment Mode", bg=BG, fg=TEXT).grid(row=4, column=0, sticky="w", pady=6)
        self.mode_var = tk.StringVar(value="Cash")
        ttk.Combobox(f, textvariable=self.mode_var,
                     values=["Cash", "Online", "Card"],
                     width=28, state="readonly").grid(row=4, column=1, padx=10, pady=6)

        # Auto-fill amount when route selected
        self.route_var.trace_add("write", self._fill_amount)

        ttk.Button(self, text="🎫  Issue Pass", style="Accent.TButton",
                   command=self._issue).pack(pady=18)

    def _fill_amount(self, *_):
        sel = self.route_var.get()
        if sel in self.route_map:
            fare = self.route_map[sel]["fare"]
            pt   = self.type_var.get()
            mult = {"Monthly": 1, "Quarterly": 2.5, "Annual": 9}.get(pt, 1)
            self.amount_var.set(str(int(fare * mult)))

    def _issue(self):
        sid_str  = self.sid_var.get().strip()
        route_lbl = self.route_var.get()
        pt       = self.type_var.get()
        amt_str  = self.amount_var.get().strip()
        mode     = self.mode_var.get()

        if not all([sid_str, route_lbl, pt, amt_str, mode]):
            messagebox.showwarning("Validation", "All fields are required.", parent=self)
            return
        try:
            sid = int(sid_str)
            amt = float(amt_str)
        except ValueError:
            messagebox.showwarning("Validation", "Student ID and Amount must be numbers.", parent=self)
            return

        if route_lbl not in self.route_map:
            messagebox.showwarning("Validation", "Please select a valid route.", parent=self)
            return

        route_id = self.route_map[route_lbl]["route_id"]
        ok, msg  = db.issue_pass(sid, route_id, pt, amt, mode)
        if ok:
            messagebox.showinfo("✅ Pass Issued", msg, parent=self)
            self.parent.show_passes()
            self.destroy()
        else:
            messagebox.showerror("Error", msg, parent=self)


# ─────────────────────────────────────────
if __name__ == "__main__":
    App().mainloop()
