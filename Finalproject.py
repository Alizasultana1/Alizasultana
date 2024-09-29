"""
# Author: Aliza Sultana
# Date written: 9/29/2024
# Assignment:Final project
"""
import tkinter as tk
from tkinter import messagebox
import csv
import os
from datetime import datetime
import matplotlib.pyplot as plt
from collections import defaultdict

# Main application class
class PersonalExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Expense Tracker")
        self.expenses = []

        # Main window buttons
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(padx=10, pady=10)

        self.add_expense_button = tk.Button(self.main_frame, text="Add Expense", command=self.open_add_expense_window)
        self.add_expense_button.grid(row=0, column=0, padx=5, pady=5)

        self.view_summary_button = tk.Button(self.main_frame, text="View Summary", command=self.open_view_summary_window)
        self.view_summary_button.grid(row=1, column=0, padx=5, pady=5)

        self.save_data_button = tk.Button(self.main_frame, text="Save Data", command=self.save_data)
        self.save_data_button.grid(row=2, column=0, padx=5, pady=5)

        self.load_data_button = tk.Button(self.main_frame, text="Load Data", command=self.load_data)
        self.load_data_button.grid(row=3, column=0, padx=5, pady=5)

        self.show_chart_button = tk.Button(self.main_frame, text="Show Chart", command=self.show_chart)
        self.show_chart_button.grid(row=4, column=0, padx=5, pady=5)

        self.exit_button = tk.Button(self.main_frame, text="Exit", command=self.root.quit)
        self.exit_button.grid(row=5, column=0, padx=5, pady=5)

    # Add Expense Window
    def open_add_expense_window(self):
        self.add_expense_window = tk.Toplevel(self.root)
        self.add_expense_window.title("Add Expense")

        # Automatically fetch current system date
        current_date = datetime.now().strftime("%d/%m/%Y")

        tk.Label(self.add_expense_window, text=f"Date (Auto-filled): {current_date}").grid(row=0, column=0, columnspan=2)
        tk.Label(self.add_expense_window, text="Amount:").grid(row=1, column=0)
        tk.Label(self.add_expense_window, text="Category:").grid(row=2, column=0)
        tk.Label(self.add_expense_window, text="Description:").grid(row=3, column=0)

        self.amount_entry = tk.Entry(self.add_expense_window)
        self.category_entry = tk.Entry(self.add_expense_window)
        self.description_entry = tk.Entry(self.add_expense_window)

        self.amount_entry.grid(row=1, column=1)
        self.category_entry.grid(row=2, column=1)
        self.description_entry.grid(row=3, column=1)

        tk.Button(self.add_expense_window, text="Add", command=lambda: self.add_expense(current_date)).grid(row=4, column=0, pady=5)
        tk.Button(self.add_expense_window, text="Cancel", command=self.add_expense_window.destroy).grid(row=4, column=1, pady=5)

    def add_expense(self, current_date):
        amount = self.amount_entry.get()
        category = self.category_entry.get()
        description = self.description_entry.get()

        # Validate input
        if not amount or not category:
            messagebox.showerror("Input Error", "Please fill in all fields")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid number for amount")
            return

        self.expenses.append([current_date, amount, category, description])
        self.add_expense_window.destroy()
        messagebox.showinfo("Success", "Expense added successfully")

    # View Summary Window
    def open_view_summary_window(self):
        self.view_summary_window = tk.Toplevel(self.root)
        self.view_summary_window.title("Expense Summary")

        tk.Label(self.view_summary_window, text="Date\t\tAmount\tCategory\tDescription").grid(row=0, column=0, sticky="w")
        for idx, expense in enumerate(self.expenses):
            tk.Label(self.view_summary_window, text=f"{expense[0]}\t{expense[1]}\t{expense[2]}\t{expense[3]}").grid(row=idx + 1, column=0, sticky="w")

        tk.Button(self.view_summary_window, text="Back", command=self.view_summary_window.destroy).grid(row=len(self.expenses) + 1, column=0, pady=5)

    # Save Data to CSV
    def save_data(self):
        with open("expenses.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Amount", "Category", "Description"])
            writer.writerows(self.expenses)
        messagebox.showinfo("Success", "Data saved to expenses.csv")

    # Load Data from CSV
    def load_data(self):
        if not os.path.exists("expenses.csv"):
            messagebox.showerror("File Error", "No data file found")
            return

        with open("expenses.csv", "r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            self.expenses = [row for row in reader]
        messagebox.showinfo("Success", "Data loaded from expenses.csv")

    # Show Daily Expense Chart
    def show_chart(self):
        if not self.expenses:
            messagebox.showerror("No Data", "No expenses to show in the chart.")
            return

        # Group expenses by date
        expense_by_date = defaultdict(float)
        for expense in self.expenses:
            date, amount = expense[0], float(expense[1])
            expense_by_date[date] += amount

        dates = list(expense_by_date.keys())
        amounts = list(expense_by_date.values())

        # Plotting the bar chart
        plt.figure(figsize=(10, 6))
        plt.bar(dates, amounts, color='skyblue')
        plt.xlabel("Date")
        plt.ylabel("Total Expenses")
        plt.title("Daily Expenses")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

# Running the application
if __name__ == "__main__":
    root = tk.Tk()
    app = PersonalExpenseTrackerApp(root)
    root.mainloop()



