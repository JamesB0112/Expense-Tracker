import tkinter as tk
from tkinter import messagebox
import datetime
import csv
import os

# Main application window
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("400x400")  # Set the window size

# Global list to store expenses in memory (optional)
expenses = []

# Create input fields
tk.Label(root, text="Date (YYYY-MM-DD):").pack()
date_entry = tk.Entry(root, width=30)
date_entry.pack()

tk.Label(root, text="Category:").pack()
category_entry = tk.Entry(root, width=30)
category_entry.pack()

tk.Label(root, text="Description:").pack()
description_entry = tk.Entry(root, width=30)
description_entry.pack()

tk.Label(root, text="Amount:").pack()
amount_entry = tk.Entry(root, width=30)
amount_entry.pack()

# Output Text Widget (for displaying all expenses)
output_text = tk.Text(root, height=10, width=50)
output_text.pack()

# Function to submit an expense
def submit_expense():
    # Retrieve input values
    date = date_entry.get()
    category = category_entry.get()
    description = description_entry.get()
    amount = amount_entry.get()

    # Validate inputs
    try:
        if not date:
            date = str(datetime.date.today())  # Default to today's date
        str(amount)  # Check if amount is numeric
        if float(amount) <= 0:
            raise ValueError("Amount must be positive.")
    except ValueError as e:
        messagebox.showerror("Input Error", f"Invalid input: {e}")
        return

    # Save expense to a CSV file
    file_exists = os.path.isfile("expenses.csv")
    with open("expenses.csv", "a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Date", "Category", "Description", "Amount"])  # Write header if new file
        writer.writerow([date, category, description, amount])

    # Add to in-memory list (optional)
    expenses.append({"date": date, "category": category, "description": description, "amount": amount})

    # Provide feedback to the user
    messagebox.showinfo("Success", "Expense added successfully!")

    # Clear input fields
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

# Run the GUI event loop
root.mainloop()
