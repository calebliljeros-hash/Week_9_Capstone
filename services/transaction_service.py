#!/usr/bin/env python3
"""
Transaction Service
Business logic for managing transactions
"""

from datetime import date, datetime
from decimal import Decimal
from models.transaction import Transaction
from models.category import Category
from utils.validators import validate_amount, validate_date, validate_description, validate_transaction_type
from utils.formatters import format_currency
import calendar

class TransactionService:
    """
    Service class for transaction operations
    """
    
    @staticmethod
    def add_transaction(amount, description, transaction_date, category_id, transaction_type):
        """
        Add a new transaction
        
        Args:
            amount (str/float): Transaction amount
            description (str): Transaction description
            transaction_date (str/date): Transaction date
            category_id (int): Category ID
            transaction_type (str): 'income' or 'expense'
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            validated_amount = validate_amount(amount)
            validated_date = validate_date(transaction_date)
            validated_desc = validate_description(description)
            validated_type = validate_transaction_type(transaction_type)
            transaction = Transaction(
                amount=validated_amount, description=validated_desc,
                transaction_date=validated_date, category_id=category_id,
                transaction_type=validated_type
            )
            return transaction.save()
        except Exception as e:
            print(f"Error adding transaction: {e}")
            return False
    
    @staticmethod
    def update_transaction(transaction_id, amount=None, description=None, 
                         transaction_date=None, category_id=None):
        """
        Update an existing transaction
        
        Args:
            transaction_id (int): Transaction ID to update
            amount (str/float, optional): New amount
            description (str, optional): New description
            transaction_date (str/date, optional): New date
            category_id (int, optional): New category ID
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            transaction = Transaction.get_by_id(transaction_id)
            if not transaction:
                print(f"Transaction #{transaction_id} not found")
                return False
            if amount is not None:
                transaction.amount = validate_amount(amount)
            if description is not None:
                transaction.description = validate_description(description)
            if transaction_date is not None:
                transaction.transaction_date = validate_date(transaction_date)
            if category_id is not None:
                transaction.category_id = category_id
            return transaction.save()
        except Exception as e:
            print(f"Error updating transaction: {e}")
            return False
    
    @staticmethod
    def delete_transaction(transaction_id):
        """
        Delete a transaction
        
        Args:
            transaction_id (int): Transaction ID to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        transaction = Transaction.get_by_id(transaction_id)
        if not transaction:
            print(f"Transaction #{transaction_id} not found")
            return False
        return transaction.delete()
    
    @staticmethod
    def get_transactions(limit=None, transaction_type=None, category_id=None,
                        start_date=None, end_date=None):
        """
        Get transactions with optional filtering
        
        Args:
            limit (int, optional): Maximum number to return
            transaction_type (str, optional): 'income' or 'expense'
            category_id (int, optional): Category ID filter
            start_date (date, optional): Start date filter
            end_date (date, optional): End date filter
            
        Returns:
            list: List of Transaction objects
        """
        if start_date and end_date:
            transactions = Transaction.get_by_date_range(start_date, end_date)
        elif transaction_type:
            transactions = Transaction.get_by_type(transaction_type)
        else:
            transactions = Transaction.get_all()
        if category_id:
            transactions = [t for t in transactions if t.category_id == category_id]
        if limit:
            transactions = transactions[:limit]
        return transactions
    
    @staticmethod
    def search_transactions(search_term):
        """
        Search transactions by description
        
        Args:
            search_term (str): Term to search for
            
        Returns:
            list: List of matching Transaction objects
        """
        if not search_term:
            return []
        all_transactions = Transaction.get_all()
        search_lower = search_term.lower()
        return [t for t in all_transactions if search_lower in (t.description or '').lower()]
    
    @staticmethod
    def get_transaction_summary():
        """
        Get summary of all transactions
        
        Returns:
            dict: Summary with totals, counts, etc.
        """
        transactions = Transaction.get_all()
        
        summary = {
            'total_income': Decimal('0'),
            'total_expenses': Decimal('0'),
            'net_balance': Decimal('0'),
            'transaction_count': len(transactions),
            'income_count': 0,
            'expense_count': 0
        }
        
        for t in transactions:
            if t.type == 'income':
                summary['total_income'] += Decimal(str(t.amount))
                summary['income_count'] += 1
            elif t.type == 'expense':
                summary['total_expenses'] += Decimal(str(t.amount))
                summary['expense_count'] += 1
        summary['net_balance'] = summary['total_income'] - summary['total_expenses']
        return summary
    
    @staticmethod
    def get_spending_by_category(transaction_type='expense'):
        """
        Get spending/income totals by category
        
        Args:
            transaction_type (str): 'income' or 'expense'
            
        Returns:
            dict: Category names mapped to total amounts
        """
        transactions = Transaction.get_by_type(transaction_type)
        category_totals = {}
        for t in transactions:
            cat_name = getattr(t, 'category_name', 'Uncategorized') or 'Uncategorized'
            if cat_name not in category_totals:
                category_totals[cat_name] = Decimal('0')
            category_totals[cat_name] += Decimal(str(t.amount))
        return dict(sorted(category_totals.items(), key=lambda x: x[1], reverse=True))
    
    @staticmethod
    def get_monthly_summary(year=None, month=None):
        """
        Get summary for a specific month
        
        Args:
            year (int, optional): Year (default: current year)
            month (int, optional): Month (default: current month)
            
        Returns:
            dict: Monthly summary data
        """
        if not year:
            year = date.today().year
        if not month:
            month = date.today().month
            
        _, last_day = calendar.monthrange(year, month)
        start_date = date(year, month, 1)
        end_date = date(year, month, last_day)
        transactions = Transaction.get_by_date_range(start_date, end_date)
        income = sum(Decimal(str(t.amount)) for t in transactions if t.type == 'income')
        expenses = sum(Decimal(str(t.amount)) for t in transactions if t.type == 'expense')
        return {
            'year': year, 'month': month,
            'total_income': income, 'total_expenses': expenses,
            'net': income - expenses, 'transaction_count': len(transactions),
            'transactions': transactions
        }

def main():
    """
    Test the TransactionService
    """
    print("💼 Testing Transaction Service")
    print("=" * 35)
    
    # Test getting transaction summary
    print("📊 Transaction Summary:")
    summary = TransactionService.get_transaction_summary()
    
    print(f"  Total Income: {format_currency(summary['total_income'])}")
    print(f"  Total Expenses: {format_currency(summary['total_expenses'])}")
    print(f"  Net Balance: {format_currency(summary['net_balance'])}")
    print(f"  Transaction Count: {summary['transaction_count']}")
    
    # Test spending by category
    print("\n📋 Spending by Category:")
    category_spending = TransactionService.get_spending_by_category()
    
    for category, amount in category_spending.items():
        print(f"  {category}: {format_currency(amount)}")
    
    print("\n💡 Complete the TODO sections to see full functionality!")

if __name__ == "__main__":
    main()