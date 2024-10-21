# Import necessary libraries
import pandas as pd  # For handling CSV data and dataframes
import csv  # To write data into CSV files
from datetime import datetime  # For handling date and time
from data_entry import get_amount, get_category, get_date, get_description  # Custom functions for input handling
import matplotlib.pyplot as plt  # For plotting graphs

# Define a class to handle CSV-related operations
class CSV:
    # Class variables for the CSV file name, column names, and date format
    CSV_FILE = "finance_data.csv"
    COLUMNS = ["date", "amount", "category", "description"]
    FORMAT = "%d-%m-%Y"  # Date format: day-month-year

    # Method to initialize the CSV file if it doesn't exist
    @classmethod
    def initialize_csv(cls):
        try:
            # Try reading the CSV file
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            # If file is not found, create a new CSV file with the specified columns
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)

    # Method to add a new transaction entry into the CSV file
    @classmethod
    def add_entry(cls, date, amount, category, description):
        # Create a dictionary for the new entry
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description,
        }
        # Append the new entry to the CSV file
        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        print("Entry added successfully")

    # Method to get transactions within a given date range
    @classmethod
    def get_transactions(cls, start_date, end_date):
        # Read the CSV file into a dataframe
        df = pd.read_csv(cls.CSV_FILE)
        # Convert the 'date' column to datetime objects
        df["date"] = pd.to_datetime(df["date"], format=CSV.FORMAT)
        # Convert the start and end dates from string to datetime objects
        start_date = datetime.strptime(start_date, CSV.FORMAT)
        end_date = datetime.strptime(end_date, CSV.FORMAT)

        # Create a mask to filter transactions within the date range
        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            # If no transactions are found, notify the user
            print("No transactions found in the given date range.")
        else:
            # Display the filtered transactions
            print(f"Transactions from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}")
            print(filtered_df.to_string(index=False, formatters={"date": lambda x: x.strftime(CSV.FORMAT)}))

            # Calculate and display the summary of income and expenses
            total_income = filtered_df[filtered_df["category"] == "Income"]["amount"].sum()
            total_expense = filtered_df[filtered_df["category"] == "Expense"]["amount"].sum()
            print("\nSummary:")
            print(f"Total Income: ${total_income:.2f}")
            print(f"Total Expense: ${total_expense:.2f}")
            print(f"Net Savings: ${(total_income - total_expense):.2f}")

        # Return the filtered dataframe
        return filtered_df

# Function to add a new transaction
def add():
    CSV.initialize_csv()  # Ensure the CSV file is initialized
    # Get the transaction details from the user using custom input functions
    date = get_date("Enter the date of the transaction (dd-mm-yyyy) or enter for today's date: ", allow_default=True)
    amount = get_amount()
    category = get_category()
    description = get_description()
    # Add the transaction to the CSV file
    CSV.add_entry(date, amount, category, description)

# Function to plot income and expenses over time
def plot_transactions(df):
    df.set_index("date", inplace=True)  # Set the date column as the dataframe index

    # Filter and resample income and expense data
    income_df = (
        df[df["category"] == "Income"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    )
    expense_df = (
        df[df["category"] == "Expense"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    )

    # Plot the income and expenses over time
    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df["amount"], label="Income", color="g")
    plt.plot(expense_df.index, expense_df["amount"], label="Expense", color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expenses Over Time")
    plt.legend()
    plt.grid(True)
    plt.show()

# Main function to handle the program flow
def main():
    while True:
        # Display menu options
        print("\n1. Add a new transaction")
        print("2. View transactions and summary within a date range")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            # Add a new transaction
            add()
        elif choice == "2":
            # Get the start and end dates for transaction filtering
            start_date = get_date("Enter the start date (dd-mm-yyyy): ")
            end_date = get_date("Enter the end date (dd-mm-yyyy): ")
            # Get transactions within the date range and plot if requested
            df = CSV.get_transactions(start_date, end_date)
            if input("Do you want to see a plot? (y/n) ").lower() == "y":
                plot_transactions(df)
        elif choice == "3":
            # Exit the program
            print("Exiting...")
            break
        else:
            # Handle invalid menu choice
            print("Invalid choice. Enter 1, 2 or 3.")

# Run the program if this script is executed directly
if __name__ == "__main__":
    main()
