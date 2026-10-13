import psycopg

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
import tkinter as tk
from tkinter import messagebox
import datetime
import csv
import os

# Main application window
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("500x500")  # Set the window size
root.config(bg="#ffed46") #setting colors

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

    # Validate and convert the date
    try:
        if date_text:
            expense_date = datetime.datetime.strptime(
                date_text, "%Y-%m-%d"
            ).date()
        else:
            expense_date = datetime.date.today()

        amount = float(amount_text)

        if amount <= 0:
            raise ValueError("Amount must be positive.")

        if not category:
            raise ValueError("Category cannot be empty.")

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
        with open("expenses.csv", "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Date", "Category", "Description", "Amount"])

            writer.writerow([
                expense_date.strftime("%m-%d-%Y"),
                category,
                description,
                amount
            ])
    except OSError as e:
        messagebox.showwarning(
            "CSV Backup Warning",
            f"Saved to PostgreSQL, but the CSV backup failed:\n{e}"
        )

    messagebox.showinfo("Success", "Expense saved to PostgreSQL!")

    date_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)


# Function to display all expenses
def show_expenses():
    output_text.delete("1.0", tk.END)  # Clear previous output
    if not os.path.isfile("expenses.csv"):
        output_text.insert(tk.END, "No expenses recorded yet.\n")
        return

    # Read expenses from the CSV file
    with open("expenses.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            output_text.insert(tk.END, f"{' | '.join(row)}\n")

# Submit and View buttons
tk.Button(root, text="Submit Expense", command=submit_expense).pack()
tk.Button(root, text="View All Expenses", command=show_expenses).pack()
tk.Button(
    root,
    text="Test Database",
    command=test_database
).pack()

# Run the GUI event loop
root.mainloop()
