#!/usr/bin/env python3
"""
Report Service
Generates financial reports and analytics

TODO: Complete the report generation methods
"""

from datetime import date, datetime, timedelta
from decimal import Decimal
from models.transaction import Transaction
from models.category import Category
from services.transaction_service import TransactionService
from utils.formatters import format_currency, format_date

class ReportService:
    """
    Service class for generating financial reports
    """
    
    @staticmethod
    def generate_balance_report():
        """
        Generate a balance report showing current financial status
        
        Returns:
            str: Formatted balance report
        """
        print("📊 Generating Balance Report...")
        
        # TODO: Get transaction summary
        # summary = TransactionService.get_transaction_summary()
        
        report = []
        report.append("\n" + "=" * 50)
        report.append("💰 PERSONAL BUDGET BALANCE REPORT")
        report.append("=" * 50)
        
        # TODO: Add balance information to report
        # Format currency amounts nicely
        # Show income, expenses, and net balance
        
        report.append("\nGenerated: " + format_date(date.today()))
        report.append("=" * 50)
        
        return "\n".join(report)
    
    @staticmethod
    def generate_category_report(transaction_type='expense', top_n=10):
        """
        Generate a report showing spending/income by category
        
        Args:
            transaction_type (str): 'income' or 'expense'
            top_n (int): Number of top categories to show
            
        Returns:
            str: Formatted category report
        """
        print(f"🏷️  Generating {transaction_type.title()} by Category Report...")
        
        report = []
        report.append("\n" + "=" * 50)
        report.append(f"📋 {transaction_type.upper()} BY CATEGORY REPORT")
        report.append("=" * 50)
        
        # TODO: Get category spending data
        # category_data = TransactionService.get_spending_by_category(transaction_type)
        
        # TODO: Sort categories by amount (highest first)
        # Show top N categories with percentages
        
        report.append("\nGenerated: " + format_date(date.today()))
        report.append("=" * 50)
        
        return "\n".join(report)
    
    @staticmethod
    def generate_monthly_report(year=None, month=None):
        """
        Generate a monthly financial report
        
        Args:
            year (int, optional): Year (default: current)
            month (int, optional): Month (default: current)
            
        Returns:
            str: Formatted monthly report
        """
        if not year:
            year = date.today().year
        if not month:
            month = date.today().month
            
        month_names = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]
        
        print(f"📅 Generating {month_names[month-1]} {year} Report...")
        
        report = []
        report.append("\n" + "=" * 50)
        report.append(f"📅 MONTHLY REPORT - {month_names[month-1].upper()} {year}")
        report.append("=" * 50)
        
        # TODO: Get monthly data
        # monthly_data = TransactionService.get_monthly_summary(year, month)
        
        # TODO: Add monthly statistics
        # - Total income for month
        # - Total expenses for month
        # - Net change
        # - Number of transactions
        # - Average transaction size
        # - Top spending categories
        
        report.append("\nGenerated: " + format_date(date.today()))
        report.append("=" * 50)
        
        return "\n".join(report)
    
    @staticmethod
    def generate_trend_report(days=30):
        """
        Generate a trend report for recent activity
        
        Args:
            days (int): Number of days to analyze
            
        Returns:
            str: Formatted trend report
        """
        print(f"📈 Generating {days}-Day Trend Report...")
        
        end_date = date.today()
        start_date = end_date - timedelta(days=days)
        
        report = []
        report.append("\n" + "=" * 50)
        report.append(f"📈 FINANCIAL TREND REPORT ({days} DAYS)")
        report.append("=" * 50)
        report.append(f"Period: {format_date(start_date)} to {format_date(end_date)}")
        report.append("")
        
        # TODO: Get transactions for date range
        # Use Transaction.get_by_date_range()
        
        # TODO: Calculate trends
        # - Daily average spending
        # - Most active spending days
        # - Trend direction (spending increasing/decreasing)
        
        report.append("\nGenerated: " + format_date(date.today()))
        report.append("=" * 50)
        
        return "\n".join(report)
    
    @staticmethod
    def generate_summary_dashboard():
        """
        Generate a comprehensive dashboard with key metrics
        
        Returns:
            str: Formatted dashboard
        """
        print("📊 Generating Financial Dashboard...")
        
        dashboard = []
        dashboard.append("\n" + "=" * 60)
        dashboard.append("📊 PERSONAL BUDGET TRACKER DASHBOARD")
        dashboard.append("=" * 60)
        
        # TODO: Get comprehensive data
        # summary = TransactionService.get_transaction_summary()
        # expense_categories = TransactionService.get_spending_by_category('expense')
        # income_categories = TransactionService.get_spending_by_category('income')
        
        # TODO: Create dashboard sections:
        # 1. Current Balance Overview
        # 2. Recent Activity (last 7 days)
        # 3. Top Spending Categories
        # 4. Budget Health Indicators
        
        dashboard.append("\n📝 QUICK ACTIONS:")
        dashboard.append("   1. Add New Transaction")
        dashboard.append("   2. View Recent Transactions")
        dashboard.append("   3. Generate Detailed Reports")
        dashboard.append("   4. Manage Categories")
        
        dashboard.append("\nGenerated: " + format_date(date.today()))
        dashboard.append("=" * 60)
        
        return "\n".join(dashboard)
    
    @staticmethod
    def generate_budget_health_score():
        """
        Calculate and return a budget health score (0-100)
        
        Returns:
            dict: Health score and breakdown
        """
        # TODO: Implement budget health calculation
        # Consider factors like:
        # - Income vs expenses ratio
        # - Savings rate (if income > expenses)
        # - Spending consistency
        # - Emergency fund equivalent
        
        health_data = {
            'score': 0,  # 0-100
            'grade': 'F',  # A, B, C, D, F
            'factors': {
                'income_stability': 0,
                'expense_control': 0,
                'savings_rate': 0,
                'budget_balance': 0
            },
            'recommendations': []
        }
        
        # TODO: Calculate actual score based on financial data
        
        return health_data
    
    @staticmethod
    def export_report_to_file(report_content, filename):
        """
        Export report content to a text file
        
        Args:
            report_content (str): Report content
            filename (str): Output filename
            
        Returns:
            bool: True if successful
        """
        try:
            # TODO: Write report to file
            # Use context managers for file operations
            
            pass
            
        except Exception as e:
            print(f"❌ Error exporting report: {e}")
            return False

def main():
    """
    Test the ReportService
    """
    print("📈 Testing Report Service")
    print("=" * 30)
    
    # Test dashboard generation
    dashboard = ReportService.generate_summary_dashboard()
    print(dashboard)
    
    # Test balance report
    balance_report = ReportService.generate_balance_report()
    print(balance_report)
    
    print("\n💡 Complete the TODO sections to see full reports!")

if __name__ == "__main__":
    main()