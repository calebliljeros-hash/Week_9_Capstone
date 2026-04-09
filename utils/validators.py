#!/usr/bin/env python3
"""
Validation Utilities
Input validation functions for the budget tracker
"""

from datetime import date, datetime
from decimal import Decimal, InvalidOperation
import re

def validate_amount(amount_input):
    """
    Validate and convert amount input to Decimal
    
    Args:
        amount_input (str/float/int): Input amount
        
    Returns:
        Decimal: Validated amount
        
    Raises:
        ValueError: If amount is invalid
    """
    if amount_input is None:
        raise ValueError("Amount is required")
    amount_str = str(amount_input).strip().replace('$', '').replace(',', '')
    if not amount_str:
        raise ValueError("Amount cannot be empty")
    try:
        amount = Decimal(amount_str)
    except InvalidOperation:
        raise ValueError(f"Invalid amount: '{amount_input}'")
    if not amount.is_finite():
        raise ValueError(f"Invalid amount: '{amount_input}'")
    if amount <= 0:
        raise ValueError("Amount must be positive")
    # Round to 2 decimal places for currency
    amount = amount.quantize(Decimal('0.01'))
    return amount

def validate_date(date_input):
    """
    Validate and convert date input to date object
    
    Args:
        date_input (str/date): Input date
        
    Returns:
        date: Validated date object
        
    Raises:
        ValueError: If date is invalid
    """
    if isinstance(date_input, date) and not isinstance(date_input, datetime):
        return date_input
    if isinstance(date_input, datetime):
        return date_input.date()
    date_str = str(date_input).strip().lower()
    if date_str == 'today':
        return date.today()
    formats = ['%Y-%m-%d', '%m/%d/%Y', '%m-%d-%Y']
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    raise ValueError(f"Invalid date format: '{date_input}'. Use YYYY-MM-DD or MM/DD/YYYY")

def validate_transaction_type(transaction_type):
    """
    Validate transaction type
    
    Args:
        transaction_type (str): Transaction type input
        
    Returns:
        str: Validated transaction type ('income' or 'expense')
        
    Raises:
        ValueError: If type is invalid
    """
    if not transaction_type:
        raise ValueError("Transaction type is required")
    type_str = str(transaction_type).strip().lower()
    income_aliases = {'income', 'in', '+'}
    expense_aliases = {'expense', 'exp', 'out', '-'}
    if type_str in income_aliases:
        return 'income'
    if type_str in expense_aliases:
        return 'expense'
    raise ValueError(f"Invalid transaction type: '{transaction_type}'. Use 'income' or 'expense'")

def validate_description(description):
    """
    Validate transaction description
    
    Args:
        description (str): Description input
        
    Returns:
        str: Validated and cleaned description
        
    Raises:
        ValueError: If description is invalid
    """
    if not description:
        raise ValueError("Description is required")
    description = str(description).strip()
    description = ' '.join(description.split())  # collapse extra whitespace
    if len(description) < 3:
        raise ValueError("Description must be at least 3 characters")
    if len(description) > 200:
        raise ValueError("Description must be 200 characters or less")
    return description

def validate_category_name(name):
    """
    Validate category name
    
    Args:
        name (str): Category name input
        
    Returns:
        str: Validated category name
        
    Raises:
        ValueError: If name is invalid
    """
    if not name:
        raise ValueError("Category name is required")
    name = str(name).strip().title()
    if len(name) < 2:
        raise ValueError("Category name must be at least 2 characters")
    if len(name) > 50:
        raise ValueError("Category name must be 50 characters or less")
    if not re.match(r'^[a-zA-Z0-9\s&\-/]+$', name):
        raise ValueError("Category name can only contain letters, numbers, spaces, &, -, /")
    return name

def validate_positive_integer(value, field_name="value"):
    """
    Validate positive integer input
    
    Args:
        value (str/int): Input value
        field_name (str): Field name for error messages
        
    Returns:
        int: Validated integer
        
    Raises:
        ValueError: If value is invalid
    """
    try:
        int_val = int(value)
    except (ValueError, TypeError):
        raise ValueError(f"{field_name} must be a whole number")
    if int_val <= 0:
        raise ValueError(f"{field_name} must be positive")
    return int_val

def is_valid_email(email):
    """
    Basic email validation (optional feature)
    
    Args:
        email (str): Email address
        
    Returns:
        bool: True if valid format
    """
    if not email:
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, str(email).strip()))

def validate_date_range(start_date, end_date):
    """
    Validate a date range
    
    Args:
        start_date (date): Start date
        end_date (date): End date
        
    Returns:
        tuple: (start_date, end_date) validated
        
    Raises:
        ValueError: If date range is invalid
    """
    if not isinstance(start_date, date) or isinstance(start_date, datetime):
        start_date = validate_date(start_date)
    if not isinstance(end_date, date) or isinstance(end_date, datetime):
        end_date = validate_date(end_date)
    if start_date > end_date:
        raise ValueError("Start date must be before or equal to end date")
    return (start_date, end_date)

def sanitize_input(user_input, max_length=None):
    """
    Sanitize user input for security
    
    Args:
        user_input (str): Raw user input
        max_length (int, optional): Maximum length
        
    Returns:
        str: Sanitized input
    """
    if not isinstance(user_input, str):
        user_input = str(user_input)
    
    user_input = user_input.strip()
    if max_length is not None and len(user_input) > max_length:
        user_input = user_input[:max_length]
    return user_input

def main():
    """
    Test the validation functions
    """
    print("✓ Testing Validation Utilities")
    print("=" * 35)
    
    # Test amount validation
    print("\n💰 Testing amount validation:")
    test_amounts = ["25.50", "$1,234.56", "100", "-50", "abc", "0"]
    
    for amount in test_amounts:
        try:
            result = validate_amount(amount)
            print(f"  '{amount}' → {result} ✓")
        except Exception as e:
            print(f"  '{amount}' → Error: {e} ❌")
    
    # Test date validation
    print("\n📅 Testing date validation:")
    test_dates = ["2024-03-15", "03/15/2024", "today", "2030-01-01", "invalid"]
    
    for date_str in test_dates:
        try:
            result = validate_date(date_str)
            print(f"  '{date_str}' → {result} ✓")
        except Exception as e:
            print(f"  '{date_str}' → Error: {e} ❌")
    
    # Test transaction type validation
    print("\n🏷️  Testing transaction type validation:")
    test_types = ["income", "expense", "in", "out", "exp", "+", "-", "invalid"]
    
    for type_str in test_types:
        try:
            result = validate_transaction_type(type_str)
            print(f"  '{type_str}' → '{result}' ✓")
        except Exception as e:
            print(f"  '{type_str}' → Error: {e} ❌")
    
    print("\n💡 Complete the TODO sections to see full validation!")

if __name__ == "__main__":
    main()