#!/usr/bin/env python3
"""
Database Connection Module
Handles PostgreSQL database connections and basic operations

Handles PostgreSQL database connections and basic operations
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DatabaseConnection:
    """
    Manages database connections and provides query methods
    """
    
    def __init__(self):
        """
        Initialize database connection parameters from environment variables
        """
        self.host = os.getenv('DB_HOST', 'localhost')
        self.database = os.getenv('DB_NAME', 'budget_tracker')
        self.user = os.getenv('DB_USER', 'budget_user')
        self.password = os.getenv('DB_PASSWORD', '')
        self.port = os.getenv('DB_PORT', '5432')
        self.connection = None
    
    def connect(self):
        """
        Establish connection to the PostgreSQL database
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port,
                cursor_factory=RealDictCursor
            )
            return True
        except Exception as e:
            print(f"Database connection failed: {e}")
            return False
    
    def disconnect(self):
        """
        Close the database connection
        """
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def execute_query(self, query, params=None):
        """
        Execute a SQL query and return results
        
        Args:
            query (str): SQL query to execute
            params (tuple, optional): Query parameters
            
        Returns:
            list: Query results as list of dictionaries
        """
        try:
            cursor = self.connection.cursor()
            try:
                cursor.execute(query, params)
                results = cursor.fetchall()
                return results
            finally:
                cursor.close()
        except Exception as e:
            print(f"Query execution failed: {e}")
            return []
    
    def execute_update(self, query, params=None):
        """
        Execute an INSERT, UPDATE, or DELETE query
        
        Args:
            query (str): SQL query to execute
            params (tuple, optional): Query parameters
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            cursor = self.connection.cursor()
            try:
                cursor.execute(query, params)
                self.connection.commit()
                return True
            finally:
                cursor.close()
        except Exception as e:
            print(f"Update query failed: {e}")
            if self.connection:
                self.connection.rollback()
            return False
    
    def test_connection(self):
        """
        Test database connection and print status
        """
        print("🔍 Testing database connection...")
        
        if self.connect():
            # Test with a simple query
            result = self.execute_query("SELECT version()")
            if result:
                print(f"✅ Database connection successful!")
                print(f"📊 PostgreSQL version: {result[0]['version'][:50]}...")
                
                # Test if our tables exist
                tables_query = """
                SELECT table_name FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
                """
                tables = self.execute_query(tables_query)
                if tables:
                    print(f"📋 Found {len(tables)} tables: {', '.join([t['table_name'] for t in tables])}")
                else:
                    print("⚠️  No tables found. Run schema.sql to create tables.")
                
                self.disconnect()
                return True
            else:
                print("❌ Connection established but query failed")
                self.disconnect()
                return False
        else:
            print("❌ Could not connect to database")
            print("💡 Make sure PostgreSQL is running and .env file is configured")
            return False

def main():
    """
    Test the database connection
    """
    print("🗄️  Budget Tracker Database Connection Test")
    print("=" * 50)
    
    db = DatabaseConnection()
    db.test_connection()
    
    print("\n💡 Next steps:")
    print("   1. If connection failed, check your .env file and PostgreSQL setup")
    print("   2. Run schema.sql to create database tables")
    print("   3. Run seed_data.sql to add sample data")
    print("   4. Start building your budget tracker application!")

if __name__ == "__main__":
    main()