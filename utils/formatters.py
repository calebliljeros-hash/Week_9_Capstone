#!/usr/bin/env python3
"""
Formatting Utilities
Output formatting functions for the budget tracker

TODO: Complete the formatting functions
"""

from datetime import date, datetime
from decimal import Decimal

def format_currency(amount, currency_symbol="$"):
    """
    Format amount as currency
    
    Args:
        amount (Decimal/float): Amount to format
        currency_symbol (str): Currency symbol to use
        
    Returns:
        str: Formatted currency string
    """
    # TODO: Implement currency formatting
    # 1. Convert to Decimal if needed
    # 2. Format with 2 decimal places
    # 3. Add thousands separators (commas)
    # 4. Add currency symbol
    # 5. Handle negative amounts with parentheses or minus sign
    
    pass  # Remove when implemented

def format_date(date_obj, format_style="short"):
    """
    Format date for display
    
    Args:
        date_obj (date): Date to format
        format_style (str): 'short', 'medium', 'long'
        
    Returns:
        str: Formatted date string
    """
    # TODO: Implement date formatting
    # short: 03/15/2024
    # medium: Mar 15, 2024
    # long: March 15, 2024
    
    pass  # Remove when implemented

def format_transaction(transaction):
    """
    Format transaction for display
    
    Args:
        transaction (Transaction): Transaction object
        
    Returns:
        str: Formatted transaction string
    """
    # TODO: Implement transaction formatting
    # Format: "2024-03-15 | $25.50 | Food | Coffee and pastry"
    # Include: date, amount, category, description
    # Different formatting for income vs expense
    
    pass  # Remove when implemented

def format_table(data, headers, column_widths=None):
    """
    Format data as a table
    
    Args:
        data (list): List of rows (each row is a list)
        headers (list): Column headers
        column_widths (list, optional): Width for each column
        
    Returns:
        str: Formatted table string
    """
    # TODO: Implement table formatting
    # 1. Calculate column widths if not provided
    # 2. Create header row with separators
    # 3. Format each data row
    # 4. Handle text alignment (left/right/center)
    
    pass  # Remove when implemented

def format_percentage(value, decimal_places=1):
    """
    Format number as percentage
    
    Args:
        value (float/Decimal): Value to format (0.15 = 15%)
        decimal_places (int): Number of decimal places
        
    Returns:
        str: Formatted percentage string
    """
    # TODO: Implement percentage formatting
    # Convert decimal to percentage and add % symbol
    
    pass  # Remove when implemented

def format_number(number, decimal_places=2, use_commas=True):
    """
    Format number with specified decimal places and commas
    
    Args:
        number (float/Decimal/int): Number to format
        decimal_places (int): Number of decimal places
        use_commas (bool): Whether to use thousands separators
        
    Returns:
        str: Formatted number string
    """
    # TODO: Implement number formatting
    # 1. Convert to appropriate type
    # 2. Round to specified decimal places
    # 3. Add commas if requested
    
    pass  # Remove when implemented

def format_list_summary(items, max_items=5):
    """
    Format a list with summary if too long
    
    Args:
        items (list): Items to format
        max_items (int): Maximum items to show
        
    Returns:
        str: Formatted list summary
    """
    # TODO: Implement list summary formatting
    # Show first max_items, then "... and X more" if longer
    
    pass  # Remove when implemented

def colorize_text(text, color="white"):
    """
    Add color codes to text (optional advanced feature)
    
    Args:
        text (str): Text to colorize
        color (str): Color name
        
    Returns:
        str: Text with color codes
    """
    # TODO: Implement text colorization (optional)
    # Use ANSI color codes for terminal colors
    # Colors: red, green, yellow, blue, magenta, cyan, white
    
    # For now, just return the text unchanged
    return text

def format_bar_chart(data, width=50):
    """
    Create simple ASCII bar chart
    
    Args:
        data (dict): Label -> value mapping
        width (int): Chart width in characters
        
    Returns:
        str: ASCII bar chart
    """
    # TODO: Implement ASCII bar chart
    # Create horizontal bars using characters like █
    # Scale bars based on maximum value
    
    pass  # Remove when implemented

def truncate_text(text, max_length, suffix="..."):
    """
    Truncate text to specified length
    
    Args:
        text (str): Text to truncate
        max_length (int): Maximum length
        suffix (str): Suffix to add if truncated
        
    Returns:
        str: Truncated text
    """
    # TODO: Implement text truncation
    # Add suffix only if text was actually truncated
    
    pass  # Remove when implemented

def center_text(text, width, fill_char=" "):
    """
    Center text within specified width
    
    Args:
        text (str): Text to center
        width (int): Total width
        fill_char (str): Character to use for padding
        
    Returns:
        str: Centered text
    """
    # TODO: Implement text centering
    
    pass  # Remove when implemented

def main():
    """
    Test the formatting functions
    """
    print("🎨 Testing Formatting Utilities")
    print("=" * 35)
    
    # Test currency formatting
    print("\n💰 Testing currency formatting:")
    test_amounts = [Decimal('1234.56'), Decimal('-25.50'), Decimal('0'), Decimal('1000000')]
    
    for amount in test_amounts:
        try:
            result = format_currency(amount)
            print(f"  {amount} → '{result}'")
        except Exception as e:
            print(f"  {amount} → Error: {e}")
    
    # Test date formatting
    print("\n📅 Testing date formatting:")
    test_date = date.today()
    
    for style in ['short', 'medium', 'long']:
        try:
            result = format_date(test_date, style)
            print(f"  {style}: '{result}'")
        except Exception as e:
            print(f"  {style}: Error: {e}")
    
    # Test percentage formatting
    print("\n📈 Testing percentage formatting:")
    test_percentages = [0.15, 0.888, 1.25, 0.0]
    
    for pct in test_percentages:
        try:
            result = format_percentage(pct)
            print(f"  {pct} → '{result}'")
        except Exception as e:
            print(f"  {pct} → Error: {e}")
    
    print("\n💡 Complete the TODO sections to see full formatting!")

if __name__ == "__main__":
    main()