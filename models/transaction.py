#!/usr/bin/env python3
"""
Transaction Model
Handles transaction data operations and validation
"""

from datetime import date, datetime
from decimal import Decimal
from database.connection import DatabaseConnection

class Transaction:
    """
    Represents a financial transaction (income or expense)
    """
    
    def __init__(self, amount=None, description=None, transaction_date=None, 
                 category_id=None, transaction_type=None, transaction_id=None):
        """
        Initialize a transaction
        
        Args:
            amount (Decimal): Transaction amount
            description (str): Transaction description
            transaction_date (date): Date of transaction
            category_id (int): Category ID
            transaction_type (str): 'income' or 'expense'
            transaction_id (int): Database ID (for existing transactions)
        """
        self.id = transaction_id
        self.amount = amount
        self.description = description
        self.transaction_date = transaction_date
        self.category_id = category_id
        self.type = transaction_type
        self.db = DatabaseConnection()
    
    def save(self):
        """
        Save transaction to database (INSERT or UPDATE)
        
        Returns:
            bool: True if successful, False otherwise
        """
        # TODO: Implement save method
        # If self.id exists, UPDATE existing transaction
        # If self.id is None, INSERT new transaction
        
        if not self.validate():
            return False
            
        self.db.connect()
        
        try:
            if self.id:
                query = """UPDATE transactions
                           SET amount = %s, description = %s, transaction_date = %s,
                               category_id = %s, type = %s
                           WHERE id = %s"""
                success = self.db.execute_update(query, (
                    self.amount, self.description, self.transaction_date,
                    self.category_id, self.type, self.id
                ))
                if not success:
                    return False
            else:
                query = """INSERT INTO transactions (amount, description, transaction_date, category_id, type)
                           VALUES (%s, %s, %s, %s, %s) RETURNING id"""
                result = self.db.execute_query(query, (
                    self.amount, self.description, self.transaction_date,
                    self.category_id, self.type
                ))
                if result:
                    self.id = result[0]['id']
                    self.db.connection.commit()
                else:
                    if self.db.connection:
                        self.db.connection.rollback()
                    return False
        except Exception as e:
            print(f"Error saving transaction: {e}")
            if self.db.connection:
                self.db.connection.rollback()
            return False
        finally:
            self.db.disconnect()
        
        return True
    
    def delete(self):
        """
        Delete transaction from database
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.id:
            print("❌ Cannot delete transaction without ID")
            return False
            
        self.db.connect()
        try:
            return self.db.execute_update("DELETE FROM transactions WHERE id = %s", (self.id,))
        finally:
            self.db.disconnect()
    
    def validate(self):
        """
        Validate transaction data
        
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            if self.amount is None or Decimal(str(self.amount)) <= 0:
                print("Amount must be a positive number")
                return False
        except Exception:
            print("Amount must be a valid positive number")
            return False
        if not self.description or len(str(self.description).strip()) < 1:
            print("Description is required")
            return False
        if self.type not in ('income', 'expense'):
            print("Transaction type must be 'income' or 'expense'")
            return False
        if not self.transaction_date:
            print("Transaction date is required")
            return False
        return True
    
    @staticmethod
    def get_all():
        """
        Get all transactions from database
        
        Returns:
            list: List of Transaction objects
        """
        db = DatabaseConnection()
        if not db.connect():
            return []
        query = """SELECT t.id, t.amount, t.description, t.transaction_date, t.type,
                          t.category_id, c.name as category_name
                   FROM transactions t
                   LEFT JOIN categories c ON t.category_id = c.id
                   ORDER BY t.transaction_date DESC"""
        try:
            results = db.execute_query(query)
            transactions = []
            for row in results:
                t = Transaction(
                    amount=row['amount'], description=row['description'],
                    transaction_date=row['transaction_date'], category_id=row['category_id'],
                    transaction_type=row['type'], transaction_id=row['id']
                )
                t.category_name = row.get('category_name', 'Uncategorized')
                transactions.append(t)
            return transactions
        finally:
            db.disconnect()
    
    @staticmethod
    def get_by_id(transaction_id):
        """
        Get transaction by ID
        
        Args:
            transaction_id (int): Transaction ID
            
        Returns:
            Transaction: Transaction object or None if not found
        """
        db = DatabaseConnection()
        if not db.connect():
            return None
        query = """SELECT t.id, t.amount, t.description, t.transaction_date, t.type,
                          t.category_id, c.name as category_name
                   FROM transactions t
                   LEFT JOIN categories c ON t.category_id = c.id
                   WHERE t.id = %s"""
        try:
            results = db.execute_query(query, (transaction_id,))
            if results:
                row = results[0]
                t = Transaction(
                    amount=row['amount'], description=row['description'],
                    transaction_date=row['transaction_date'], category_id=row['category_id'],
                    transaction_type=row['type'], transaction_id=row['id']
                )
                t.category_name = row.get('category_name', 'Uncategorized')
                return t
            return None
        finally:
            db.disconnect()
    
    @staticmethod
    def get_by_type(transaction_type):
        """
        Get transactions by type (income or expense)
        
        Args:
            transaction_type (str): 'income' or 'expense'
            
        Returns:
            list: List of Transaction objects
        """
        db = DatabaseConnection()
        if not db.connect():
            return []
        query = """SELECT t.id, t.amount, t.description, t.transaction_date, t.type,
                          t.category_id, c.name as category_name
                   FROM transactions t
                   LEFT JOIN categories c ON t.category_id = c.id
                   WHERE t.type = %s
                   ORDER BY t.transaction_date DESC"""
        try:
            results = db.execute_query(query, (transaction_type,))
            transactions = []
            for row in results:
                t = Transaction(
                    amount=row['amount'], description=row['description'],
                    transaction_date=row['transaction_date'], category_id=row['category_id'],
                    transaction_type=row['type'], transaction_id=row['id']
                )
                t.category_name = row.get('category_name', 'Uncategorized')
                transactions.append(t)
            return transactions
        finally:
            db.disconnect()
    
    @staticmethod
    def get_by_date_range(start_date, end_date):
        """
        Get transactions within date range
        
        Args:
            start_date (date): Start date
            end_date (date): End date
            
        Returns:
            list: List of Transaction objects
        """
        db = DatabaseConnection()
        if not db.connect():
            return []
        query = """SELECT t.id, t.amount, t.description, t.transaction_date, t.type,
                          t.category_id, c.name as category_name
                   FROM transactions t
                   LEFT JOIN categories c ON t.category_id = c.id
                   WHERE t.transaction_date BETWEEN %s AND %s
                   ORDER BY t.transaction_date DESC"""
        try:
            results = db.execute_query(query, (start_date, end_date))
            transactions = []
            for row in results:
                t = Transaction(
                    amount=row['amount'], description=row['description'],
                    transaction_date=row['transaction_date'], category_id=row['category_id'],
                    transaction_type=row['type'], transaction_id=row['id']
                )
                t.category_name = row.get('category_name', 'Uncategorized')
                transactions.append(t)
            return transactions
        finally:
            db.disconnect()
    
    def __str__(self):
        """
        String representation of transaction
        """
        return f"{self.type.title()}: ${self.amount} - {self.description} ({self.transaction_date})"
    
    def __repr__(self):
        """
        Developer-friendly representation
        """
        return f"Transaction(id={self.id}, amount={self.amount}, type='{self.type}', date='{self.transaction_date}')"

def main():
    """
    Test the Transaction model
    """
    print("💰 Testing Transaction Model")
    print("=" * 30)
    
    # Test creating a new transaction
    transaction = Transaction(
        amount=Decimal('25.50'),
        description="Coffee and pastry",
        transaction_date=date.today(),
        category_id=4,  # Food category from seed data
        transaction_type="expense"
    )
    
    print(f"Created transaction: {transaction}")
    
    # Test validation (when implemented)
    if transaction.validate():
        print("✅ Transaction is valid")
    else:
        print("❌ Transaction validation failed")
    
    # Test getting all transactions  
    print("\n📋 All transactions:")
    all_transactions = Transaction.get_all()
    for t in all_transactions[:5]:  # Show first 5
        print(f"  {t}")
    
    print(f"\n📊 Found {len(all_transactions)} total transactions")

if __name__ == "__main__":
    main()