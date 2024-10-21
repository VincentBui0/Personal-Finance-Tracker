# Import necessary library to work with dates
from datetime import datetime

# Define the date format to be used for input and output
date_format = "%d-%m-%Y"

# Define a dictionary for categorizing transactions as 'Income' or 'Expense'
CATEGORIES = {"I": "Income", "E": "Expense"}


# Function to get a valid date from the user
def get_date(prompt, allow_default=False):
    # Prompt the user for a date input
    date_str = input(prompt)

    # If default date is allowed and user provides no input, return today's date
    if allow_default and not date_str:
        return datetime.today().strftime(date_format)

    try:
        # Try converting the input string into a valid date based on the defined format
        valid_date = datetime.strptime(date_str, date_format)
        return valid_date.strftime(date_format)  # Return the formatted date
    except ValueError:
        # If the input is invalid, print an error message and ask again
        print("Invalid date format. Please enter the date in dd-mm-yyyy format")
        return get_date(prompt, allow_default)  # Recursively call to get valid input


# Function to get a valid transaction amount from the user
def get_amount():
    try:
        # Prompt the user for an amount and convert it to a floating-point number
        amount = float(input("Enter the amount: "))
        # Ensure that the amount is positive and non-zero
        if amount <= 0:
            raise ValueError("Amount must be a non-negative non-zero value.")
        return amount
    except ValueError as e:
        # If the input is invalid or negative, print the error and ask again
        print(e)
        return get_amount()  # Recursively call to get valid input


# Function to get a transaction category from the user ('I' for Income, 'E' for Expense)
def get_category():
    # Prompt the user to enter a category
    category = input("Enter the category ('I' for Income or 'E' for Expense): ").upper()

    # Check if the input is valid (i.e., 'I' or 'E')
    if category in CATEGORIES:
        return CATEGORIES[category]  # Return the corresponding category

    # If input is invalid, print an error message and ask again
    print("Invalid category. Please enter 'I' for Income or 'E' for Expense.")
    return get_category()  # Recursively call to get valid input


# Function to get an optional description of the transaction from the user
def get_description():
    return input("Enter a description (optional): ")  # Return the description input (can be empty)
