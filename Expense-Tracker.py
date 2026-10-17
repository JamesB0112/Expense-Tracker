
import tkinter as tk
from tkinter import messagebox
import datetime
import csv
import os
import psycopg
from decimal import Decimal, InvalidOperation


def get_connection():
    return psycopg.connect(
        host="localhost",
        port=5432,
        dbname="postgres",
        user="postgres"
    )


def test_database():
    try:
        conn = get_connection()
        conn.close()
        messagebox.showinfo(
            "Database Test",
            "Connected to PostgreSQL successfully!"
        )
    except Exception as e:
        messagebox.showerror("Database Error", str(e))


# Main application window
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("500x500")
root.config(bg="#ffed46")

# Global list to store expenses in memory (optional)
expenses = []

# Create input fields
tk.Label(root, text="Amount:", bg="#9e914a").pack()
amount_entry = tk.Entry(root, width=30)
amount_entry.pack()

tk.Label(root, text="Category:", bg="#9e914a").pack()
category_entry = tk.Entry(root, width=30)
category_entry.pack()

tk.Label(root, text="Date (YYYY-MM-DD):", bg="#9e914a").pack()
date_entry = tk.Entry(root, width=30)
date_entry.pack()

tk.Label(root, text="Description:", bg="#9e914a").pack()
description_entry = tk.Entry(root, width=30)
description_entry.pack()

# Output Text Widget (for displaying all expenses)
output_text = tk.Text(root, height=10, width=50)
output_text.pack()


# Function to submit an expense
def submit_expense():
    amount_text = amount_entry.get().strip()
    category = category_entry.get().strip()
    date_text = date_entry.get().strip()
    description = description_entry.get().strip()

    # Validate inputs
    try:
        if date_text:
            expense_date = datetime.datetime.strptime(
                date_text, "%Y-%m-%d"
            ).date()
        else:
            expense_date = datetime.date.today()

        try:
            amount = Decimal(amount_text)
        except InvalidOperation:
            raise ValueError("Amount must be a valid number.")

        if not amount.is_finite():
            raise ValueError("Amount must be a finite number.")

        if amount <= 0:
            raise ValueError("Amount must be positive.")

        if amount.as_tuple().exponent < -2:
            raise ValueError(
                "Amount cannot have more than two decimal places."
            )

        if not category:
            raise ValueError("Category cannot be empty.")

        if not description:
            raise ValueError("Description cannot be empty.")

    except ValueError as e:
        messagebox.showerror("Input Error", str(e))
        return

    # Save to PostgreSQL first
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO expenses
                        (amount, category, expense_date, description)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (amount, category, expense_date, description)
                )
    except Exception as e:
        messagebox.showerror(
            "Database Error",
            f"Expense was not saved to PostgreSQL:\n{e}"
        )
        return

    # Keep a CSV backup after the database save succeeds
    file_exists = os.path.isfile("expenses.csv")

    try:
        with open(
            "expenses.csv", "a", newline="", encoding="utf-8"
        ) as file:
            writer = csv.writer(file)

            if not file_exists:
                writer.writerow(
                    ["Date", "Category", "Description", "Amount"]
                )

            writer.writerow([
                expense_date.strftime("%Y-%m-%d"),
                category,
                description,
                str(amount)
            ])

    except OSError as e:
        messagebox.showwarning(
            "CSV Backup Warning",
            f"Saved to PostgreSQL, but the CSV backup failed:\n{e}"
        )

    messagebox.showinfo("Success", "Expense saved to PostgreSQL!")

    # Clear input fields
    date_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)


# Function to display spending by category
def show_category_summary():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT
                        category,
                        COUNT(*) AS total_transactions,
                        SUM(amount) AS total_spending
                    FROM expenses
                    GROUP BY category
                    ORDER BY total_spending DESC;
                """)

                rows = cur.fetchall()

        if not rows:
            messagebox.showinfo(
                "Category Summary",
                "No expenses recorded yet."
            )
            return

        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, "SPENDING BY CATEGORY\n\n")

        for category, total_transactions, total_spending in rows:
            output_text.insert(
                tk.END,
                f"{category}\n"
                f"  Transactions: {total_transactions}\n"
                f"  Total: ${total_spending:.2f}\n\n"
            )

    except Exception as e:
        messagebox.showerror("Database Error", str(e))


# Function to display spending summary
def show_summary():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT
                        COUNT(*) AS total_transactions,
                        COALESCE(SUM(amount), 0) AS total_spending,
                        COALESCE(AVG(amount), 0) AS average_expense
                    FROM expenses;
                """)

                total_transactions, total_spending, average_expense = cur.fetchone()

        messagebox.showinfo(
            "Spending Summary",
            f"Total Transactions: {total_transactions}\n"
            f"Total Spending: ${total_spending:.2f}\n"
            f"Average Expense: ${average_expense:.2f}"
        )

    except Exception as e:
        messagebox.showerror("Database Error", str(e))


# Function to display all expenses
def show_expenses():
    output_text.delete("1.0", tk.END)

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT expense_id, expense_date, category,
                           description, amount
                    FROM expenses
                    ORDER BY expense_date DESC, expense_id DESC;
                """)

                rows = cur.fetchall()

        if not rows:
            output_text.insert(tk.END, "No expenses recorded yet.\n")
            return

        for row in rows:
            expense_id, date, category, description, amount = row

            output_text.insert(
                tk.END,
                f"ID: {expense_id} | {date} | {category} | "
                f"{description} | ${amount:.2f}\n"
            )

    except Exception as e:
        messagebox.showerror("Database Error", str(e))


# Submit and View buttons
tk.Button(root, text="Submit Expense", command=submit_expense).pack()
tk.Button(root, text="View All Expenses", command=show_expenses).pack()
tk.Button(root, text="Test Database", command=test_database).pack()
tk.Button(root, text="Spending Summary", command=show_summary).pack()
tk.Button(root, text="Spending by Category", command=show_category_summary).pack()

# Run the GUI event loop
root.mainloop()
