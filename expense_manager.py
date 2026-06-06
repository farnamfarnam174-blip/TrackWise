import json
import hashlib
import os
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

USERS_FILE = "users.json"

# ─── Auth Functions ───────────────────────────────────────

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=4)

def get_user_file(username):
    return f"expenses_{username}.json"

# ─── Data Functions ───────────────────────────────────────

def load_expenses(username):
    try:
        with open(get_user_file(username), "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def save_expenses(username, expenses):
    with open(get_user_file(username), "w", encoding="utf-8") as f:
        json.dump(expenses, f, ensure_ascii=False, indent=4)

# ─── Login Window ─────────────────────────────────────────

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login - Expense Manager")
        self.root.geometry("400x480")
        self.root.configure(bg="#1e1e2e")
        self.root.resizable(False, False)
        self.mode = "login"
        self.build_ui()

    def build_ui(self):
        # Title
        tk.Label(self.root, text="💰 Expense Manager",
                 font=("Segoe UI", 20, "bold"),
                 bg="#1e1e2e", fg="#cdd6f4").pack(pady=(40, 5))

        self.subtitle = tk.Label(self.root, text="Sign in to your account",
                                  font=("Segoe UI", 11),
                                  bg="#1e1e2e", fg="#6c7086")
        self.subtitle.pack(pady=(0, 30))

        # Card
        card = tk.Frame(self.root, bg="#313244", padx=30, pady=30)
        card.pack(padx=30, fill="x")

        # Username
        tk.Label(card, text="Username", bg="#313244",
                 fg="#cdd6f4", font=("Segoe UI", 10)).pack(anchor="w")
        self.username_entry = tk.Entry(card, font=("Segoe UI", 11),
                                       bg="#45475a", fg="#cdd6f4",
                                       insertbackground="white",
                                       relief="flat", bd=5)
        self.username_entry.pack(fill="x", pady=(3, 15))

        # Password
        tk.Label(card, text="Password", bg="#313244",
                 fg="#cdd6f4", font=("Segoe UI", 10)).pack(anchor="w")
        self.password_entry = tk.Entry(card, font=("Segoe UI", 11),
                                       bg="#45475a", fg="#cdd6f4",
                                       insertbackground="white",
                                       show="●", relief="flat", bd=5)
        self.password_entry.pack(fill="x", pady=(3, 20))

        # Action Button
        self.action_btn = tk.Button(card, text="Login",
                                     command=self.handle_action,
                                     bg="#89b4fa", fg="#1e1e2e",
                                     font=("Segoe UI", 11, "bold"),
                                     relief="flat", cursor="hand2",
                                     pady=8)
        self.action_btn.pack(fill="x")

        # Switch mode
        switch_frame = tk.Frame(self.root, bg="#1e1e2e")
        switch_frame.pack(pady=15)

        self.switch_label = tk.Label(switch_frame, text="Don't have an account?",
                                      bg="#1e1e2e", fg="#6c7086",
                                      font=("Segoe UI", 10))
        self.switch_label.pack(side="left")

        self.switch_btn = tk.Button(switch_frame, text=" Register",
                                     command=self.toggle_mode,
                                     bg="#1e1e2e", fg="#89b4fa",
                                     font=("Segoe UI", 10, "bold"),
                                     relief="flat", cursor="hand2",
                                     bd=0)
        self.switch_btn.pack(side="left")

        # Enter key
        self.root.bind("<Return>", lambda e: self.handle_action())

    def toggle_mode(self):
        if self.mode == "login":
            self.mode = "register"
            self.root.title("Register - Expense Manager")
            self.subtitle.config(text="Create a new account")
            self.action_btn.config(text="Register")
            self.switch_label.config(text="Already have an account?")
            self.switch_btn.config(text=" Login")
        else:
            self.mode = "login"
            self.root.title("Login - Expense Manager")
            self.subtitle.config(text="Sign in to your account")
            self.action_btn.config(text="Login")
            self.switch_label.config(text="Don't have an account?")
            self.switch_btn.config(text=" Register")

    def handle_action(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        users = load_users()

        if self.mode == "login":
            if username not in users:
                messagebox.showerror("Error", "Username not found.")
                return
            if users[username] != hash_password(password):
                messagebox.showerror("Error", "Incorrect password.")
                return
            self.open_app(username)

        else:  # register
            if username in users:
                messagebox.showerror("Error", "Username already exists.")
                return
            if len(password) < 4:
                messagebox.showerror("Error", "Password must be at least 4 characters.")
                return
            users[username] = hash_password(password)
            save_users(users)
            messagebox.showinfo("Success", f"Account created! Welcome, {username}!")
            self.toggle_mode()

    def open_app(self, username):
        self.root.destroy()
        new_root = tk.Tk()
        ExpenseApp(new_root, username)
        new_root.mainloop()

# ─── Main App ─────────────────────────────────────────────

class ExpenseApp:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.root.title(f"Expense Manager — {username}")
        self.root.geometry("750x570")
        self.root.configure(bg="#1e1e2e")
        self.root.resizable(False, False)
        self.build_ui()
        self.refresh_table()

    def build_ui(self):
        # ── Header ──
        header = tk.Frame(self.root, bg="#1e1e2e")
        header.pack(fill="x", padx=20, pady=(15, 5))

        tk.Label(header, text="💰 Personal Expense Manager",
                 font=("Segoe UI", 16, "bold"),
                 bg="#1e1e2e", fg="#cdd6f4").pack(side="left")

        tk.Label(header, text=f"👤 {self.username}",
                 font=("Segoe UI", 10),
                 bg="#1e1e2e", fg="#6c7086").pack(side="right", pady=5)

        logout_btn = tk.Button(header, text="Logout",
                               command=self.logout,
                               bg="#45475a", fg="#cdd6f4",
                               font=("Segoe UI", 9),
                               relief="flat", cursor="hand2", padx=8)
        logout_btn.pack(side="right", padx=10)

        # ── Input Frame ──
        input_frame = tk.Frame(self.root, bg="#313244", padx=15, pady=15)
        input_frame.pack(fill="x", padx=20, pady=5)

        tk.Label(input_frame, text="Amount (Toman):", bg="#313244",
                 fg="#cdd6f4", font=("Segoe UI", 10)).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.amount_entry = tk.Entry(input_frame, font=("Segoe UI", 10),
                                     bg="#45475a", fg="#cdd6f4",
                                     insertbackground="white", width=20)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Category:", bg="#313244",
                 fg="#cdd6f4", font=("Segoe UI", 10)).grid(row=0, column=2, sticky="w", padx=5)
        self.category_var = tk.StringVar()
        categories = ["Food", "Transport", "Shopping", "Health", "Entertainment", "Other"]
        self.category_menu = ttk.Combobox(input_frame, textvariable=self.category_var,
                                           values=categories, width=15,
                                           font=("Segoe UI", 10), state="readonly")
        self.category_menu.current(0)
        self.category_menu.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(input_frame, text="Description:", bg="#313244",
                 fg="#cdd6f4", font=("Segoe UI", 10)).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.desc_entry = tk.Entry(input_frame, font=("Segoe UI", 10),
                                   bg="#45475a", fg="#cdd6f4",
                                   insertbackground="white", width=50)
        self.desc_entry.grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky="ew")

        add_btn = tk.Button(input_frame, text="➕ Add Expense",
                            command=self.add_expense,
                            bg="#89b4fa", fg="#1e1e2e",
                            font=("Segoe UI", 10, "bold"),
                            relief="flat", cursor="hand2", padx=10)
        add_btn.grid(row=2, column=0, columnspan=4, pady=10)

        # ── Table ──
        table_frame = tk.Frame(self.root, bg="#1e1e2e")
        table_frame.pack(fill="both", expand=True, padx=20, pady=5)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#313244", foreground="#cdd6f4",
                         rowheight=28, fieldbackground="#313244", font=("Segoe UI", 10))
        style.configure("Treeview.Heading", background="#45475a",
                         foreground="#89b4fa", font=("Segoe UI", 10, "bold"))
        style.map("Treeview", background=[("selected", "#45475a")])

        columns = ("Date", "Amount", "Category", "Description")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
        self.tree.column("Date", width=140)
        self.tree.column("Amount", width=130)
        self.tree.column("Category", width=110)
        self.tree.column("Description", width=250)
        for col in columns:
            self.tree.heading(col, text=col)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # ── Bottom Bar ──
        bottom = tk.Frame(self.root, bg="#313244", padx=15, pady=10)
        bottom.pack(fill="x", padx=20, pady=(5, 15))

        self.total_label = tk.Label(bottom, text="Total: 0 Toman",
                                     font=("Segoe UI", 12, "bold"),
                                     bg="#313244", fg="#a6e3a1")
        self.total_label.pack(side="left")

        tk.Button(bottom, text="📊 Monthly Report",
                  command=self.show_monthly_report,
                  bg="#a6e3a1", fg="#1e1e2e",
                  font=("Segoe UI", 10, "bold"),
                  relief="flat", cursor="hand2", padx=10).pack(side="right", padx=5)

        tk.Button(bottom, text="🗑 Delete Selected",
                  command=self.delete_expense,
                  bg="#f38ba8", fg="#1e1e2e",
                  font=("Segoe UI", 10, "bold"),
                  relief="flat", cursor="hand2", padx=10).pack(side="right", padx=5)

    # ─── Actions ──────────────────────────────────────────

    def add_expense(self):
        try:
            amount = float(self.amount_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for amount.")
            return

        description = self.desc_entry.get().strip()
        if not description:
            messagebox.showerror("Error", "Please enter a description.")
            return

        expense = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "amount": amount,
            "category": self.category_var.get(),
            "description": description
        }

        expenses = load_expenses(self.username)
        expenses.append(expense)
        save_expenses(self.username, expenses)

        self.amount_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.refresh_table()
        messagebox.showinfo("Success", "Expense added successfully!")

    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        expenses = load_expenses(self.username)
        total = 0
        for exp in expenses:
            self.tree.insert("", "end", values=(
                exp['date'], f"{exp['amount']:,.0f} T",
                exp['category'], exp['description']
            ))
            total += exp['amount']

        self.total_label.config(text=f"Total: {total:,.0f} Toman")

    def delete_expense(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an expense to delete.")
            return
        if not messagebox.askyesno("Confirm", "Delete selected expense(s)?"):
            return

        indexes = sorted([self.tree.index(s) for s in selected], reverse=True)
        expenses = load_expenses(self.username)
        for i in indexes:
            expenses.pop(i)
        save_expenses(self.username, expenses)
        self.refresh_table()

    def show_monthly_report(self):
        expenses = load_expenses(self.username)
        if not expenses:
            messagebox.showinfo("Report", "No expenses recorded yet.")
            return

        monthly = {}
        for exp in expenses:
            month = exp['date'][:7]
            if month not in monthly:
                monthly[month] = {"total": 0, "categories": {}}
            monthly[month]["total"] += exp['amount']
            cat = exp['category']
            monthly[month]["categories"][cat] = \
                monthly[month]["categories"].get(cat, 0) + exp['amount']

        win = tk.Toplevel(self.root)
        win.title("Monthly Report")
        win.geometry("400x450")
        win.configure(bg="#1e1e2e")

        tk.Label(win, text="📊 Monthly Report",
                 font=("Segoe UI", 14, "bold"),
                 bg="#1e1e2e", fg="#cdd6f4").pack(pady=15)

        text = tk.Text(win, bg="#313244", fg="#cdd6f4",
                       font=("Consolas", 10), relief="flat", padx=10, pady=10)
        text.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        for month, data in sorted(monthly.items()):
            text.insert("end", f"{'='*35}\n")
            text.insert("end", f"  📅 {month}\n")
            text.insert("end", f"{'='*35}\n")
            for cat, amt in sorted(data["categories"].items(),
                                    key=lambda x: x[1], reverse=True):
                text.insert("end", f"  {cat:<18} {amt:>10,.0f} T\n")
            text.insert("end", f"  {'-'*33}\n")
            text.insert("end", f"  {'Total':<18} {data['total']:>10,.0f} T\n\n")

        text.config(state="disabled")

    def logout(self):
        self.root.destroy()
        new_root = tk.Tk()
        LoginWindow(new_root)
        new_root.mainloop()

# ─── Run ──────────────────────────────────────────────────

if __name__ == "__main__":
    root = tk.Tk()
    LoginWindow(root)
    root.mainloop()
