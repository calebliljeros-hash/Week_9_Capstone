#!/usr/bin/env python3
"""
Report Service
Generates financial reports and analytics
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
        print("Generating Balance Report...")
        
        summary = TransactionService.get_transaction_summary()
        report = []
        report.append("\n" + "=" * 50)
        report.append("  PERSONAL BUDGET BALANCE REPORT")
        report.append("=" * 50)
        report.append(f"  Total Income:    {format_currency(summary['total_income'])}")
        report.append(f"  Total Expenses:  {format_currency(summary['total_expenses'])}")
        report.append("-" * 50)
        report.append(f"  Net Balance:     {format_currency(summary['net_balance'])}")
        report.append("")
        report.append(f"  Transactions:    {summary['transaction_count']}")
        report.append(f"    Income:        {summary['income_count']}")
        report.append(f"    Expenses:      {summary['expense_count']}")
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
        print(f"Generating {transaction_type.title()} by Category Report...")
        
        report = []
        report.append("\n" + "=" * 50)
        report.append(f"  {transaction_type.upper()} BY CATEGORY REPORT")
        report.append("=" * 50)
        
        category_data = TransactionService.get_spending_by_category(transaction_type)
        total = sum(category_data.values()) if category_data else Decimal('0')
        for i, (category, amount) in enumerate(category_data.items()):
            if i >= top_n:
                break
            pct = float(amount / total) if total > 0 else 0
            bar_len = int(pct * 30)
            bar = "=" * bar_len
            report.append(f"  {category:<20} {format_currency(amount):>12}  ({pct:.1%})  {bar}")
        report.append("-" * 50)
        report.append(f"  {'TOTAL':<20} {format_currency(total):>12}")
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
        
        print(f"Generating {month_names[month-1]} {year} Report...")
        
        report = []
        report.append("\n" + "=" * 50)
        report.append(f"  MONTHLY REPORT - {month_names[month-1].upper()} {year}")
        report.append("=" * 50)
        
        monthly_data = TransactionService.get_monthly_summary(year, month)
        report.append(f"  Income:      {format_currency(monthly_data['total_income'])}")
        report.append(f"  Expenses:    {format_currency(monthly_data['total_expenses'])}")
        report.append(f"  Net Change:  {format_currency(monthly_data['net'])}")
        report.append(f"  Transactions: {monthly_data['transaction_count']}")
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
        print(f"Generating {days}-Day Trend Report...")
        
        end_date = date.today()
        start_date = end_date - timedelta(days=days)
        
        report = []
        report.append("\n" + "=" * 50)
        report.append(f"  FINANCIAL TREND REPORT ({days} DAYS)")
        report.append("=" * 50)
        report.append(f"Period: {format_date(start_date)} to {format_date(end_date)}")
        report.append("")
        
        transactions = Transaction.get_by_date_range(start_date, end_date)
        income = sum(Decimal(str(t.amount)) for t in transactions if t.type == 'income')
        expenses = sum(Decimal(str(t.amount)) for t in transactions if t.type == 'expense')
        if days > 0:
            report.append(f"  Daily Avg Income:   {format_currency(income / days)}")
            report.append(f"  Daily Avg Expenses: {format_currency(expenses / days)}")
        report.append(f"  Total Income:       {format_currency(income)}")
        report.append(f"  Total Expenses:     {format_currency(expenses)}")
        report.append(f"  Net:                {format_currency(income - expenses)}")
        report.append(f"  Transactions:       {len(transactions)}")
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
        print("Generating Financial Dashboard...")
        
        dashboard = []
        dashboard.append("\n" + "=" * 60)
        dashboard.append("  PERSONAL BUDGET TRACKER DASHBOARD")
        dashboard.append("=" * 60)
        
        summary = TransactionService.get_transaction_summary()
        expense_categories = TransactionService.get_spending_by_category('expense')

        dashboard.append(f"\n  BALANCE OVERVIEW")
        dashboard.append(f"  Income:    {format_currency(summary['total_income'])}")
        dashboard.append(f"  Expenses:  {format_currency(summary['total_expenses'])}")
        dashboard.append(f"  Balance:   {format_currency(summary['net_balance'])}")
        dashboard.append(f"\n  TOP SPENDING CATEGORIES")
        for i, (cat, amt) in enumerate(expense_categories.items()):
            if i >= 5:
                break
            dashboard.append(f"    {cat:<20} {format_currency(amt)}")
        dashboard.append("\n  QUICK ACTIONS:")
        dashboard.append("    1. Add New Transaction")
        dashboard.append("    2. View Recent Transactions")
        dashboard.append("    3. Generate Detailed Reports")
        dashboard.append("    4. Manage Categories")
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
        summary = TransactionService.get_transaction_summary()
        income = float(summary['total_income'])
        expenses = float(summary['total_expenses'])

        score = 50  # baseline
        if income > 0:
            savings_rate = (income - expenses) / income
            score += int(savings_rate * 40)  # up to +40 for good savings
        if expenses > 0 and income > expenses:
            score += 10  # bonus for positive balance
        score = max(0, min(100, score))

        if score >= 90: grade = 'A'
        elif score >= 80: grade = 'B'
        elif score >= 70: grade = 'C'
        elif score >= 60: grade = 'D'
        else: grade = 'F'

        recommendations = []
        if income <= expenses:
            recommendations.append("Reduce expenses or increase income to build savings")
        if income == 0:
            recommendations.append("Add income transactions to track your earnings")

        return {
            'score': score, 'grade': grade,
            'factors': {
                'income_stability': min(100, int(income / 100)) if income > 0 else 0,
                'expense_control': max(0, 100 - int((expenses / max(income, 1)) * 100)),
                'savings_rate': max(0, int(((income - expenses) / max(income, 1)) * 100)),
                'budget_balance': score
            },
            'recommendations': recommendations
        }
    
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
            with open(filename, 'w') as f:
                f.write(report_content)
            print(f"Report exported to {filename}")
            return True
        except Exception as e:
            print(f"Error exporting report: {e}")
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