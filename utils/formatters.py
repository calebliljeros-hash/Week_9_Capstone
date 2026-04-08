#!/usr/bin/env python3
"""
Formatting Utilities
Output formatting functions for the budget tracker
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
    if amount is None:
        return f"{currency_symbol}0.00"
    try:
        amount = Decimal(str(amount))
    except Exception:
        return f"{currency_symbol}0.00"
    if amount < 0:
        return f"-{currency_symbol}{abs(amount):,.2f}"
    return f"{currency_symbol}{amount:,.2f}"

def format_date(date_obj, format_style="short"):
    """
    Format date for display
    
    Args:
        date_obj (date): Date to format
        format_style (str): 'short', 'medium', 'long'
        
    Returns:
        str: Formatted date string
    """
    if date_obj is None:
        return "N/A"
    if isinstance(date_obj, str):
        try:
            date_obj = datetime.strptime(date_obj, '%Y-%m-%d').date()
        except ValueError:
            return date_obj
    if format_style == "short":
        return date_obj.strftime('%m/%d/%Y')
    elif format_style == "medium":
        return date_obj.strftime('%b %d, %Y')
    elif format_style == "long":
        return date_obj.strftime('%B %d, %Y')
    return date_obj.strftime('%m/%d/%Y')

def format_transaction(transaction):
    """
    Format transaction for display
    
    Args:
        transaction (Transaction): Transaction object
        
    Returns:
        str: Formatted transaction string
    """
    if transaction is None:
        return "No transaction data"
    date_str = format_date(transaction.transaction_date) if transaction.transaction_date else "N/A"
    amount_str = format_currency(transaction.amount)
    type_indicator = "+" if transaction.type == "income" else "-"
    category = getattr(transaction, 'category_name', 'Uncategorized') or 'Uncategorized'
    desc = transaction.description or "No description"
    return f"{date_str} | {type_indicator}{amount_str} | {category} | {desc}"

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
    if not data and not headers:
        return "No data to display"
    if not column_widths:
        column_widths = []
        for i, header in enumerate(headers):
            max_width = len(str(header))
            for row in data:
                if i < len(row):
                    max_width = max(max_width, len(str(row[i])))
            column_widths.append(max_width + 2)
    lines = []
    header_line = " | ".join(str(h).ljust(column_widths[i]) for i, h in enumerate(headers))
    lines.append(header_line)
    lines.append("-+-".join("-" * w for w in column_widths))
    for row in data:
        row_line = " | ".join(
            str(row[i] if i < len(row) else "").ljust(column_widths[i])
            for i in range(len(headers))
        )
        lines.append(row_line)
    return "\n".join(lines)

def format_percentage(value, decimal_places=1):
    """
    Format number as percentage
    
    Args:
        value (float/Decimal): Value to format (0.15 = 15%)
        decimal_places (int): Number of decimal places
        
    Returns:
        str: Formatted percentage string
    """
    if value is None:
        return "0.0%"
    percentage = float(value) * 100
    return f"{percentage:.{decimal_places}f}%"

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
    if number is None:
        return "0"
    try:
        num = float(number)
    except (ValueError, TypeError):
        return str(number)
    if use_commas:
        return f"{num:,.{decimal_places}f}"
    return f"{num:.{decimal_places}f}"

def format_list_summary(items, max_items=5):
    """
    Format a list with summary if too long
    
    Args:
        items (list): Items to format
        max_items (int): Maximum items to show
        
    Returns:
        str: Formatted list summary
    """
    if not items:
        return "No items"
    items_str = [str(item) for item in items]
    if len(items_str) <= max_items:
        return "\n".join(f"  - {item}" for item in items_str)
    shown = "\n".join(f"  - {item}" for item in items_str[:max_items])
    remaining = len(items_str) - max_items
    return f"{shown}\n  ... and {remaining} more"

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
    if not data:
        return "No data for chart"
    positive_values = [v for v in data.values() if float(v) > 0]
    if not positive_values:
        return "No spending data to chart"
    max_value = max(positive_values)
    max_label = max(len(str(k)) for k in data.keys()) if data else 0
    lines = []
    for label, value in data.items():
        val = max(0, float(value))  # clamp negatives to zero for display
        bar_length = int((val / float(max_value)) * width) if max_value > 0 else 0
        bar = "█" * bar_length
        lines.append(f"{str(label).ljust(max_label)} | {bar} {format_currency(value)}")
    return "\n".join(lines)

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
    if not text:
        return ""
    text = str(text)
    if len(text) <= max_length:
        return text
    if max_length <= len(suffix):
        return text[:max_length]
    return text[:max_length - len(suffix)] + suffix

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
    if not text:
        return fill_char * width
    return str(text).center(width, fill_char)

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