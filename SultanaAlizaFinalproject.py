"""
# Author: Aliza Sultana
# Date written: 9/29/2024
# Assignment: Final project
"""
import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
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

        # Load background image
        self.background_image = tk.PhotoImage(file="Finance-Download-PNG-Image.png")  # Use a valid image file here
        self.background_label = tk.Label(self.root, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)  # Set the image to fill the entire window

        # Create a frame on top of the background image
        self.main_frame = tk.Frame(self.root, bg='grey', bd=5)  # You can change the bg color
        self.main_frame.place(relx=.5, rely=.5, anchor='center')

        self.expenses = []
        self.limit = None

        # Main window buttons
        self.add_expense_button = tk.Button(self.main_frame, text="Add Expense", command=self.open_add_expense_window)
        self.add_expense_button.grid(row=0, column=0, padx=10, pady=10)

        self.view_summary_button = tk.Button(self.main_frame, text="View Summary",
                                             command=self.open_view_summary_window)
        self.view_summary_button.grid(row=1, column=0, padx=10, pady=10)

        self.category_summary_button = tk.Button(self.main_frame, text="Category Summary",
                                                 command=self.open_category_summary_window)
        self.category_summary_button.grid(row=2, column=0, padx=10, pady=10)

        self.set_limit_button = tk.Button(self.main_frame, text="Set Expense Limit", command=self.open_set_limit_window)
        self.set_limit_button.grid(row=3, column=0, padx=10, pady=10)

        self.date_range_button = tk.Button(self.main_frame, text="View by Date Range",
                                           command=self.open_date_range_window)
        self.date_range_button.grid(row=4, column=0, padx=10, pady=10)

        self.save_data_button = tk.Button(self.main_frame, text="Save Data", command=self.save_data)
        self.save_data_button.grid(row=5, column=0, padx=10, pady=10)

        self.load_data_button = tk.Button(self.main_frame, text="Load Data", command=self.load_data)
        self.load_data_button.grid(row=6, column=0, padx=10, pady=10)

        self.show_chart_button = tk.Button(self.main_frame, text="Show Chart", command=self.show_chart)
        self.show_chart_button.grid(row=7, column=0, padx=10, pady=10)

        self.exit_button = tk.Button(self.main_frame, text="Exit", command=self.root.quit)
        self.exit_button.grid(row=8, column=0, padx=10, pady=10)

    # Add Expense Window
    def open_add_expense_window(self):
        self.add_expense_window = tk.Toplevel(self.root)
        self.add_expense_window.title("Add Expense")

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
        amount = self.amount_entry.get().strip()  # Ensure no leading/trailing spaces
        category = self.category_entry.get().strip()
        description = self.description_entry.get().strip()

        # Validate input fields
        if not amount or not category:
            messagebox.showerror("Input Error", "Amount and Category fields cannot be empty")
            return

        try:
            amount = float(amount)  # Convert the amount to float
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid number for amount")
            return

        # Use a default description if the user didn't provide one
        if not description:
            description = "No description provided"

        # Add the expense to the list
        self.expenses.append([current_date, amount, category, description])
        self.add_expense_window.destroy()
        messagebox.showinfo("Success", "Expense added successfully")

        # Check for expense limit
        if self.limit:
            self.check_limit()

    # View Summary Window
    def open_view_summary_window(self):
        self.view_summary_window = tk.Toplevel(self.root)
        self.view_summary_window.title("Expense Summary")

        tk.Label(self.view_summary_window, text="Date\t\tAmount\tCategory\tDescription").grid(row=0, column=0, sticky="w")
        for idx, expense in enumerate(self.expenses):
            tk.Label(self.view_summary_window, text=f"{expense[0]}\t{expense[1]}\t{expense[2]}\t{expense[3]}").grid(
                row=idx + 1, column=0, sticky="w")

        tk.Button(self.view_summary_window, text="Back", command=self.view_summary_window.destroy).grid(
            row=len(self.expenses) + 1, column=0, pady=5)

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

    # Category-Based Summary
    def open_category_summary_window(self):
        self.category_summary_window = tk.Toplevel(self.root)
        self.category_summary_window.title("Category-Based Summary")

        categories = set(expense[2] for expense in self.expenses)  # Collect all unique categories
        tk.Label(self.category_summary_window, text="Select Category:").grid(row=0, column=0)

        self.category_var = tk.StringVar()
        self.category_menu = tk.OptionMenu(self.category_summary_window, self.category_var, *categories)
        self.category_menu.grid(row=0, column=1)

        tk.Button(self.category_summary_window, text="Show", command=self.show_category_summary).grid(row=1, column=0,
                                                                                                      columnspan=2)

    def show_category_summary(self):
        selected_category = self.category_var.get()
        filtered_expenses = [exp for exp in self.expenses if exp[2] == selected_category]

        if not filtered_expenses:
            messagebox.showinfo("No Data", "No expenses found for this category.")
            return

        summary_window = tk.Toplevel(self.root)
        summary_window.title(f"Expenses for {selected_category}")
        tk.Label(summary_window, text="Date\t\tAmount\tCategory\tDescription").grid(row=0, column=0, sticky="w")
        for idx, expense in enumerate(filtered_expenses):
            tk.Label(summary_window, text=f"{expense[0]}\t{expense[1]}\t{expense[2]}\t{expense[3]}").grid(row=idx + 1, column=0, sticky="w")

        tk.Button(summary_window, text="Back", command=summary_window.destroy).grid(row=len(filtered_expenses) + 1, column=0, pady=5)

    # Set Expense Limit
    def open_set_limit_window(self):
        self.set_limit_window = tk.Toplevel(self.root)
        self.set_limit_window.title("Set Expense Limit")

        tk.Label(self.set_limit_window, text="Enter your expense limit:").grid(row=0, column=0)

        self.limit_entry = tk.Entry(self.set_limit_window)
        self.limit_entry.grid(row=0, column=1)

        tk.Button(self.set_limit_window, text="Set Limit", command=self.set_limit).grid(row=1, column=0, columnspan=2)

    def set_limit(self):
        limit_value = self.limit_entry.get().strip()

        if not limit_value:
            messagebox.showerror("Input Error", "Limit field cannot be empty")
            return

        try:
            self.limit = float(limit_value)
            messagebox.showinfo("Success", f"Expense limit set to {self.limit}")
            self.set_limit_window.destroy()
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid number for the limit")

    # Check if expenses exceed the limit
    def check_limit(self):
        total_expenses = sum(float(expense[1]) for expense in self.expenses)
        if total_expenses > self.limit:
            messagebox.showwarning("Limit Exceeded", f"Warning: Your expenses have exceeded the limit of {self.limit}!")

    # View by Date Range
    def open_date_range_window(self):
        self.date_range_window = tk.Toplevel(self.root)
        self.date_range_window.title("View Expenses by Date Range")

        tk.Label(self.date_range_window, text="Start Date:").grid(row=0, column=0)
        tk.Label(self.date_range_window, text="End Date:").grid(row=1, column=0)

        self.start_date_entry = DateEntry(self.date_range_window, date_pattern="dd/mm/yyyy")
        self.end_date_entry = DateEntry(self.date_range_window, date_pattern="dd/mm/yyyy")

        self.start_date_entry.grid(row=0, column=1)
        self.end_date_entry.grid(row=1, column=1)

        tk.Button(self.date_range_window, text="Show", command=self.show_expenses_by_date_range).grid(row=2, column=0, columnspan=2)

    def show_expenses_by_date_range(self):
        start_date = datetime.strptime(self.start_date_entry.get(), "%d/%m/%Y")
        end_date = datetime.strptime(self.end_date_entry.get(), "%d/%m/%Y")

        if start_date > end_date:
            messagebox.showerror("Date Error", "Start date cannot be later than end date")
            return

        filtered_expenses = [exp for exp in self.expenses if start_date <= datetime.strptime(exp[0], "%d/%m/%Y") <= end_date]

        if not filtered_expenses:
            messagebox.showinfo("No Data", "No expenses found in the selected date range.")
            return

        date_range_summary_window = tk.Toplevel(self.root)
        date_range_summary_window.title("Expenses by Date Range")
        tk.Label(date_range_summary_window, text="Date\t\tAmount\tCategory\tDescription").grid(row=0, column=0, sticky="w")
        for idx, expense in enumerate(filtered_expenses):
            tk.Label(date_range_summary_window, text=f"{expense[0]}\t{expense[1]}\t{expense[2]}\t{expense[3]}").grid(row=idx + 1, column=0, sticky="w")

        tk.Button(date_range_summary_window, text="Back", command=date_range_summary_window.destroy).grid(row=len(filtered_expenses) + 1, column=0, pady=5)

# Main application driver
if __name__ == "__main__":
    root = tk.Tk()
    app = PersonalExpenseTrackerApp(root)
    root.mainloop()



