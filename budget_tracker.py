#!/usr/bin/env python3
"""
Personal Budget Tracker - Main Application
A command-line interface for managing personal finances

A command-line interface for managing personal finances

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
from utils.validators import validate_amount, validate_date, validate_transaction_type, validate_positive_integer
from utils.formatters import format_currency, format_date, format_table

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
        dashboard = ReportService.generate_summary_dashboard()
        print(dashboard)
    
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
            # Get transaction type
            type_input = self.get_user_input(
                "Transaction type (income/expense): ",
                validate_transaction_type
            )
            # Get amount
            amount = self.get_user_input("Amount: $", validate_amount)
            # Get description
            from utils.validators import validate_description
            description = self.get_user_input("Description: ", validate_description)
            # Show categories and get selection
            if type_input == 'income':
                categories = Category.get_by_type('income')
            else:
                categories = Category.get_by_type('expense')

            if categories:
                print("\nAvailable categories:")
                for cat in categories:
                    print(f"  {cat.id}. {cat.name}")
                category_id = self.get_user_input("Category ID: ", validate_positive_integer)
            else:
                category_id = None

            # Get date (optional - defaults to today)
            transaction_date = self.get_user_input(
                "Date (YYYY-MM-DD, or press Enter for today): ",
                validate_date, required=False
            )
            if not transaction_date:
                transaction_date = date.today()

            # Save
            if TransactionService.add_transaction(amount, description, transaction_date, category_id, type_input):
                print("\nTransaction added successfully!")
            else:
                print("\nFailed to add transaction.")
        except Exception as e:
            print(f"Error adding transaction: {e}")
    
    def view_transactions(self):
        """
        Display transactions with filtering options
        """
        print("\n📋 VIEW TRANSACTIONS")
        print("-" * 20)
        
        print("1. All Transactions")
        print("2. Income Only")
        print("3. Expenses Only")
        print("4. By Date Range")

        choice = input("\nFilter option: ").strip()

        try:
            if choice == '2':
                transactions = TransactionService.get_transactions(transaction_type='income')
            elif choice == '3':
                transactions = TransactionService.get_transactions(transaction_type='expense')
            elif choice == '4':
                start = self.get_user_input("Start date (YYYY-MM-DD): ", validate_date)
                end = self.get_user_input("End date (YYYY-MM-DD): ", validate_date)
                transactions = TransactionService.get_transactions(start_date=start, end_date=end)
            else:
                transactions = TransactionService.get_transactions()

            if not transactions:
                print("\nNo transactions found.")
                return
            self.display_transactions_table(transactions)
        except Exception as e:
            print(f"Error viewing transactions: {e}")
    
    def edit_transaction(self):
        """
        Edit an existing transaction
        """
        print("\n✏️  EDIT TRANSACTION")
        print("-" * 18)
        
        transactions = TransactionService.get_transactions(limit=10)
        if not transactions:
            print("No transactions to edit.")
            return
        self.display_transactions_table(transactions)

        try:
            tid = self.get_user_input("\nTransaction ID to edit: ", validate_positive_integer)
            transaction = Transaction.get_by_id(tid)
            if not transaction:
                print(f"Transaction #{tid} not found.")
                return

            print(f"\nEditing: {transaction}")
            print("(Press Enter to keep current value)\n")

            new_amount = input(f"Amount [{transaction.amount}]: ").strip()
            new_desc = input(f"Description [{transaction.description}]: ").strip()
            new_date = input(f"Date [{transaction.transaction_date}]: ").strip()

            amount = validate_amount(new_amount) if new_amount else None
            desc = new_desc if new_desc else None
            trans_date = validate_date(new_date) if new_date else None

            if TransactionService.update_transaction(tid, amount=amount, description=desc, transaction_date=trans_date):
                print("Transaction updated successfully!")
            else:
                print("Failed to update transaction.")
        except Exception as e:
            print(f"Error: {e}")
    
    def delete_transaction(self):
        """
        Delete a transaction
        """
        print("\n🗑️  DELETE TRANSACTION")
        print("-" * 20)
        
        transactions = TransactionService.get_transactions(limit=10)
        if not transactions:
            print("No transactions to delete.")
            return
        self.display_transactions_table(transactions)

        try:
            tid = self.get_user_input("\nTransaction ID to delete: ", validate_positive_integer)
            transaction = Transaction.get_by_id(tid)
            if not transaction:
                print(f"Transaction #{tid} not found.")
                return

            print(f"\nAbout to delete: {transaction}")
            confirm = input("Are you sure? (y/N): ").strip().lower()
            if confirm == 'y':
                if TransactionService.delete_transaction(tid):
                    print("Transaction deleted successfully!")
                else:
                    print("Failed to delete transaction.")
            else:
                print("Delete cancelled.")
        except Exception as e:
            print(f"Error: {e}")
    
    def generate_reports(self):
        """
        Generate and display financial reports
        """
        print("\n  GENERATE REPORTS")
        print("-" * 18)

        print("Report Options:")
        print("1. Balance Summary")
        print("2. Expense by Category")
        print("3. Income by Category")
        print("4. Monthly Report")
        print("5. Trend Analysis (30 days)")
        print("6. Budget Health Score")
        print("7. Export Report to File")

        choice = input("\nReport choice: ").strip()

        try:
            if choice == '1':
                print(ReportService.generate_balance_report())
            elif choice == '2':
                print(ReportService.generate_category_report('expense'))
            elif choice == '3':
                print(ReportService.generate_category_report('income'))
            elif choice == '4':
                year_input = input("Year (Enter for current): ").strip()
                month_input = input("Month 1-12 (Enter for current): ").strip()
                year = int(year_input) if year_input else None
                month = int(month_input) if month_input else None
                print(ReportService.generate_monthly_report(year, month))
            elif choice == '5':
                print(ReportService.generate_trend_report(30))
            elif choice == '6':
                health = ReportService.generate_budget_health_score()
                print(f"\n  Budget Health Score: {health['score']}/100 (Grade: {health['grade']})")
                for rec in health['recommendations']:
                    print(f"    - {rec}")
            elif choice == '7':
                report = ReportService.generate_balance_report()
                filename = input("Filename (e.g., report.txt): ").strip() or "budget_report.txt"
                ReportService.export_report_to_file(report, filename)
            else:
                print("Invalid choice.")
        except ValueError as e:
            print(f"Invalid input: {e}")
    
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
        
        choice = input("\nChoice: ").strip()

        if choice == '1':
            categories = Category.get_all()
            if not categories:
                print("No categories found.")
                return
            print(f"\n{'ID':<5} {'Name':<20} {'Type':<10} {'Description'}")
            print("-" * 60)
            for cat in categories:
                count = cat.get_transaction_count()
                print(f"{cat.id:<5} {cat.name:<20} {cat.type:<10} {cat.description or ''} ({count} txns)")
        elif choice == '2':
            name = self.get_user_input("Category name: ")
            cat_type = self.get_user_input("Type (income/expense): ", validate_transaction_type)
            desc = input("Description (optional): ").strip() or None
            category = Category(name=name, category_type=cat_type, description=desc)
            if category.save():
                print(f"Category '{name}' created successfully!")
            else:
                print("Failed to create category.")
        elif choice == '3':
            print("Edit category is not yet implemented.")
        elif choice == '4':
            categories = Category.get_all()
            for cat in categories:
                print(f"  {cat.id}. {cat.name} ({cat.type})")
            cid = self.get_user_input("Category ID to delete: ", validate_positive_integer)
            category = Category.get_by_id(cid)
            if category:
                if category.delete():
                    print("Category deleted.")
            else:
                print("Category not found.")
        else:
            print("Invalid choice.")
    
    def search_transactions(self):
        """
        Search transactions by description or other criteria
        """
        print("\n🔍 SEARCH TRANSACTIONS")
        print("-" * 21)
        
        search_term = self.get_user_input("Search term: ")
        results = TransactionService.search_transactions(search_term)
        if results:
            self.display_transactions_table(results)
        else:
            print(f"No transactions matching '{search_term}'.")
    
    def show_settings(self):
        """
        Display and manage application settings
        """
        print("\n⚙️  SETTINGS")
        print("-" * 10)
        
        print("Settings Options:")
        print("1. View Database Info")
        print("2. Budget Health Score")

        choice = input("\nChoice: ").strip()

        if choice == '1':
            print(f"\n  Host: {self.db.host}")
            print(f"  Database: {self.db.database}")
            print(f"  User: {self.db.user}")
            print(f"  Port: {self.db.port}")
        elif choice == '2':
            health = ReportService.generate_budget_health_score()
            print(f"\n  Score: {health['score']}/100 ({health['grade']})")
        else:
            print("Invalid choice.")
    
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
        while True:
            user_input = input(prompt).strip()
            if not user_input and not required:
                return None
            if not user_input and required:
                print("This field is required. Please try again.")
                continue
            if validator:
                try:
                    return validator(user_input)
                except ValueError as e:
                    print(f"Invalid input: {e}")
                    continue
            return user_input
    
    def display_transactions_table(self, transactions, page_size=10):
        """
        Display transactions in a formatted table
        
        Args:
            transactions (list): List of Transaction objects
            page_size (int): Number of transactions per page
        """
        print(f"\nFound {len(transactions)} transaction(s):\n")
        headers = ["ID", "Date", "Type", "Amount", "Category", "Description"]
        data = []
        for t in transactions:
            cat_name = getattr(t, 'category_name', 'Uncategorized') or 'Uncategorized'
            data.append([
                t.id,
                format_date(t.transaction_date) if t.transaction_date else "N/A",
                t.type.title(),
                format_currency(t.amount),
                cat_name,
                (t.description[:30] + "...") if t.description and len(t.description) > 30 else t.description
            ])
        print(format_table(data, headers))

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