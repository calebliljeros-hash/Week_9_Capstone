#!/usr/bin/env python3
"""
Category Model
Handles category data operations for organizing transactions

Handles category data operations for organizing transactions
"""

from database.connection import DatabaseConnection

class Category:
    """
    Represents a transaction category (e.g., Food, Transportation)
    """
    
    def __init__(self, name=None, category_type=None, description=None, category_id=None):
        """
        Initialize a category
        
        Args:
            name (str): Category name
            category_type (str): 'income' or 'expense'
            description (str): Category description
            category_id (int): Database ID (for existing categories)
        """
        self.id = category_id
        self.name = name
        self.type = category_type
        self.description = description
        self.db = DatabaseConnection()
    
    def save(self):
        """
        Save category to database
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.validate():
            return False
            
        self.db.connect()
        
        try:
            if self.id:
                query = "UPDATE categories SET name = %s, type = %s, description = %s WHERE id = %s"
                success = self.db.execute_update(query, (self.name, self.type, self.description, self.id))
                if not success:
                    return False
            else:
                query = "INSERT INTO categories (name, type, description) VALUES (%s, %s, %s) RETURNING id"
                result = self.db.execute_query(query, (self.name, self.type, self.description))
                if result:
                    self.id = result[0]['id']
                    self.db.connection.commit()
                else:
                    return False
                
        except Exception as e:
            print(f"Error saving category: {e}")
            if self.db.connection:
                self.db.connection.rollback()
            return False
        finally:
            self.db.disconnect()
        
        return True
    
    def validate(self):
        """
        Validate category data
        
        Returns:
            bool: True if valid, False otherwise
        """
        if not self.name or len(str(self.name).strip()) < 2:
            print("Category name must be at least 2 characters")
            return False
        if self.type not in ('income', 'expense'):
            print("Category type must be 'income' or 'expense'")
            return False
        if self.name and len(self.name) > 50:
            print("Category name must be 50 characters or less")
            return False
        return True
    
    @staticmethod
    def get_all():
        """
        Get all categories from database
        
        Returns:
            list: List of Category objects
        """
        db = DatabaseConnection()
        db.connect()
        
        query = "SELECT id, name, type, description FROM categories ORDER BY type, name"
        try:
            results = db.execute_query(query)
            categories = []
            for row in results:
                categories.append(Category(
                    name=row['name'], category_type=row['type'],
                    description=row.get('description'), category_id=row['id']
                ))
            return categories
        finally:
            db.disconnect()
    
    @staticmethod
    def get_by_type(category_type):
        """
        Get categories by type
        
        Args:
            category_type (str): 'income' or 'expense'
            
        Returns:
            list: List of Category objects
        """
        db = DatabaseConnection()
        db.connect()
        query = "SELECT id, name, type, description FROM categories WHERE type = %s ORDER BY name"
        try:
            results = db.execute_query(query, (category_type,))
            return [Category(name=r['name'], category_type=r['type'],
                             description=r.get('description'), category_id=r['id']) for r in results]
        finally:
            db.disconnect()
    
    @staticmethod
    def get_by_id(category_id):
        """
        Get category by ID
        
        Args:
            category_id (int): Category ID
            
        Returns:
            Category: Category object or None if not found
        """
        db = DatabaseConnection()
        db.connect()
        query = "SELECT id, name, type, description FROM categories WHERE id = %s"
        try:
            results = db.execute_query(query, (category_id,))
            if results:
                r = results[0]
                return Category(name=r['name'], category_type=r['type'],
                                description=r.get('description'), category_id=r['id'])
            return None
        finally:
            db.disconnect()
    
    def get_transaction_count(self):
        """
        Get number of transactions in this category
        
        Returns:
            int: Number of transactions
        """
        if not self.id:
            return 0
            
        self.db.connect()
        try:
            query = "SELECT COUNT(*) as count FROM transactions WHERE category_id = %s"
            result = self.db.execute_query(query, (self.id,))
            return result[0]['count'] if result else 0
        finally:
            self.db.disconnect()
    
    def delete(self):
        """
        Delete category from database
        Note: This will set category_id to NULL in related transactions
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.id:
            print("❌ Cannot delete category without ID")
            return False
            
        # Check if category is in use
        transaction_count = self.get_transaction_count()
        if transaction_count > 0:
            print(f"⚠️  Category has {transaction_count} transactions. They will be uncategorized.")
            response = input("Continue? (y/N): ")
            if response.lower() != 'y':
                print("❌ Delete cancelled")
                return False
        
        self.db.connect()
        try:
            return self.db.execute_update("DELETE FROM categories WHERE id = %s", (self.id,))
        finally:
            self.db.disconnect()
    
    def __str__(self):
        """
        String representation of category
        """
        return f"{self.name} ({self.type})"
    
    def __repr__(self):
        """
        Developer-friendly representation  
        """
        return f"Category(id={self.id}, name='{self.name}', type='{self.type}')"

def main():
    """
    Test the Category model
    """
    print("🏷️  Testing Category Model")
    print("=" * 30)
    
    # Test getting all categories
    print("📋 All categories:")
    all_categories = Category.get_all()
    
    for category in all_categories:
        count = category.get_transaction_count()
        print(f"  {category} - {count} transactions")
    
    print(f"\n📊 Found {len(all_categories)} total categories")
    
    # Test getting categories by type
    print("\n💰 Income categories:")
    income_categories = Category.get_by_type('income')
    for cat in income_categories:
        print(f"  {cat}")
    
    print("\n💸 Expense categories:")
    expense_categories = Category.get_by_type('expense')
    for cat in expense_categories:
        print(f"  {cat}")

if __name__ == "__main__":
    main()