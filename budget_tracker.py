#!/usr/bin/env python3
"""
Personal Budget Tracker - Main Application
A command-line interface for managing personal finances

TODO: Complete the CLI interface and menu system

Author: [Your Name Here]
Date: [Date]
"""

import os
import sys
from datetime import date, datetime
from decimal import Decimal

# Import our modules
from database.connection import DatabaseConnection
from models.transaction import Transaction
from models.category import Category
from services.transaction_service import TransactionService
from services.report_service import ReportService
from utils.validators import validate_amount, validate_date, validate_transaction_type
from utils.formatters import format_currency, format_date

class BudgetTracker:
    """
    Main application class for the Budget Tracker CLI
    """
    
    def __init__(self):
        """
        Initialize the budget tracker application
        """
        self.db = DatabaseConnection()
        self.running = True
    
    def start(self):
        """
        Start the budget tracker application
        """
        # Check database connection
        print("💰 Personal Budget Tracker")
        print("=" * 30)
        
        if not self.db.test_connection():
            print("❌ Cannot connect to database. Please check your setup.")
            print("💡 Make sure PostgreSQL is running and .env is configured.")
            return
        
        print("✅ Database connection successful!")
        
        # Show welcome dashboard
        self.show_dashboard()
        
        # Main application loop
        while self.running:
            self.show_main_menu()
            choice = input("\nEnter your choice: ").strip()
            self.handle_menu_choice(choice)
    
    def show_dashboard(self):
        """
        Display the main dashboard with key information
        """
        # TODO: Implement dashboard display
        # Use ReportService.generate_summary_dashboard()
        
        pass  # Remove when implemented
    
    def show_main_menu(self):
        """
        Display the main menu options
        """
        print("\n" + "=" * 40)
        print("💰 BUDGET TRACKER - MAIN MENU")
        print("=" * 40)
        print("1. 💵 Add Transaction")
        print("2. 📋 View Transactions")
        print("3. ✏️  Edit Transaction")
        print("4. 🗑️  Delete Transaction")
        print("5. 📈 Generate Reports")
        print("6. 🏷️  Manage Categories")
        print("7. 🔍 Search Transactions")
        print("8. ⚙️  Settings")
        print("9. 🚪 Exit")
        print("=" * 40)
    
    def handle_menu_choice(self, choice):
        """
        Handle user menu selection
        
        Args:
            choice (str): User's menu choice
        """
        # TODO: Implement menu choice handling
        # Route to appropriate methods based on choice
        
        if choice == '1':
            self.add_transaction()
        elif choice == '2':
            self.view_transactions()
        elif choice == '3':
            self.edit_transaction()
        elif choice == '4':
            self.delete_transaction()
        elif choice == '5':
            self.generate_reports()
        elif choice == '6':
            self.manage_categories()
        elif choice == '7':
            self.search_transactions()
        elif choice == '8':
            self.show_settings()
        elif choice == '9':
            self.exit_application()
        else:
            print("❌ Invalid choice. Please try again.")
    
    def add_transaction(self):
        """
        Add a new transaction through user input
        """
        print("\n➕ ADD NEW TRANSACTION")
        print("-" * 25)
        
        try:
            # TODO: Implement transaction input
            # 1. Get transaction type (income/expense)
            # 2. Get amount with validation
            # 3. Get description
            # 4. Get category (show list to choose from)
            # 5. Get date (default to today)
            # 6. Create and save transaction
            
            # Example implementation structure:
            # transaction_type = input("Transaction type (income/expense): ")
            # amount_input = input("Amount: $")
            # description = input("Description: ")
            # ... get other inputs ...
            
            # Use TransactionService.add_transaction() to save
            
            pass  # Remove when implemented
            
        except Exception as e:
            print(f"❌ Error adding transaction: {e}")
    
    def view_transactions(self):
        """
        Display transactions with filtering options
        """
        print("\n📋 VIEW TRANSACTIONS")
        print("-" * 20)
        
        # TODO: Implement transaction viewing
        # 1. Ask for filter options (all, recent, by type, by category)
        # 2. Get transactions using appropriate service method
        # 3. Display in formatted table
        # 4. Show pagination if many transactions
        
        pass  # Remove when implemented
    
    def edit_transaction(self):
        """
        Edit an existing transaction
        """
        print("\n✏️  EDIT TRANSACTION")
        print("-" * 18)
        
        # TODO: Implement transaction editing
        # 1. Show recent transactions for selection
        # 2. Ask for transaction ID to edit
        # 3. Load existing transaction
        # 4. Allow editing individual fields
        # 5. Save changes
        
        pass  # Remove when implemented
    
    def delete_transaction(self):
        """
        Delete a transaction
        """
        print("\n🗑️  DELETE TRANSACTION")
        print("-" * 20)
        
        # TODO: Implement transaction deletion
        # 1. Show recent transactions
        # 2. Ask for transaction ID
        # 3. Confirm deletion
        # 4. Delete using service
        
        pass  # Remove when implemented
    
    def generate_reports(self):
        """
        Generate and display financial reports
        """
        print("\n📈 GENERATE REPORTS")
        print("-" * 18)
        
        print("Report Options:")
        print("1. Balance Summary")
        print("2. Category Report")
        print("3. Monthly Report")
        print("4. Trend Analysis")
        print("5. Export Report to File")
        
        # TODO: Implement report generation
        # Use ReportService methods to generate different reports
        # Allow user to choose report type and parameters
        
        pass  # Remove when implemented
    
    def manage_categories(self):
        """
        Manage transaction categories
        """
        print("\n🏷️  MANAGE CATEGORIES")
        print("-" * 19)
        
        print("Category Options:")
        print("1. View All Categories")
        print("2. Add New Category")
        print("3. Edit Category")
        print("4. Delete Category")
        
        # TODO: Implement category management
        # CRUD operations for categories
        
        pass  # Remove when implemented
    
    def search_transactions(self):
        """
        Search transactions by description or other criteria
        """
        print("\n🔍 SEARCH TRANSACTIONS")
        print("-" * 21)
        
        # TODO: Implement transaction search
        # 1. Get search term from user
        # 2. Use TransactionService.search_transactions()
        # 3. Display matching results
        
        pass  # Remove when implemented
    
    def show_settings(self):
        """
        Display and manage application settings
        """
        print("\n⚙️  SETTINGS")
        print("-" * 10)
        
        print("Settings Options:")
        print("1. View Database Info")
        print("2. Export All Data")
        print("3. Import Data")
        print("4. Reset Application")
        
        # TODO: Implement settings management
        # Database info, backup/restore, etc.
        
        pass  # Remove when implemented
    
    def exit_application(self):
        """
        Exit the application gracefully
        """
        print("\n👋 Thank you for using Budget Tracker!")
        print("Your financial data has been saved.")
        self.running = False
    
    def get_user_input(self, prompt, validator=None, required=True):
        """
        Get validated user input
        
        Args:
            prompt (str): input prompt
            validator (function): Validation function
            required (bool): Whether input is required
            
        Returns:
            str: Validated user input
        """
        # TODO: Implement robust user input handling
        # 1. Display prompt
        # 2. Get input
        # 3. Validate if validator provided
        # 4. Retry on validation error
        # 5. Handle empty input based on required flag
        
        pass  # Remove when implemented
    
    def display_transactions_table(self, transactions, page_size=10):
        """
        Display transactions in a formatted table
        
        Args:
            transactions (list): List of Transaction objects
            page_size (int): Number of transactions per page
        """
        # TODO: Implement transaction table display
        # Use utils.formatters for proper formatting
        # Include pagination for large lists
        
        pass  # Remove when implemented

def check_environment():
    """
    Check if the environment is properly set up
    
    Returns:
        bool: True if environment is ready
    """
    # TODO: Implement environment checks
    # 1. Check if .env file exists
    # 2. Check required environment variables
    # 3. Check database connectivity
    # 4. Provide helpful error messages
    
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        print("💡 Copy .env.example to .env and configure your database settings")
        return False
    
    return True

def main():
    """
    Main application entry point
    """
    try:
        # Check environment setup
        if not check_environment():
            print("\n⚠️  Please set up your environment before running the application.")
            print("\n📌 Setup steps:")
            print("   1. Copy .env.example to .env")
            print("   2. Configure database settings in .env")
            print("   3. Run schema.sql to create database tables")
            print("   4. Run seed_data.sql to add sample data (optional)")
            return
        
        # Create and start the application
        app = BudgetTracker()
        app.start()
        
    except KeyboardInterrupt:
        print("\n\n👋 Application terminated by user.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("🐞 Please report this issue if it persists.")

if __name__ == "__main__":
    main()