# 💰 Personal Budget Tracker - Python Foundations Capstone

## 🎯 Project Overview

Build a **command-line budget tracking application** that demonstrates your mastery of Python fundamentals while creating a real-world productivity tool. This project combines all the core Python concepts you've learned with professional database integration and CLI design patterns.

**What You'll Build:**
- A powerful CLI application for personal finance management
- PostgreSQL database integration for reliable data persistence
- Professional-grade code structure and error handling
- A portfolio-ready project that showcases your Python skills

## 🚀 Why This Project Will Accelerate Your Career

### 💼 **Real-World Skills You'll Gain**
- **Database Integration**: PostgreSQL is used by companies like Netflix, Instagram, and Spotify
- **CLI Development**: Essential for DevOps, automation, and backend development 
- **Data Processing**: Core skill for data analysis, ETL pipelines, and business intelligence
- **Error Handling**: Professional-grade exception management
- **Code Organization**: Modular design patterns used in enterprise applications

### 🏢 **How This Connects to Industry Roles**

**Backend Developer**: Database CRUD operations, API design patterns, data validation
**Data Analyst**: Data aggregation, reporting, financial modeling
**DevOps Engineer**: Command-line tools, automation scripts, database management
**Full-Stack Developer**: Complete application lifecycle, database design, user interface

### 📈 **Portfolio Value**
- Demonstrates **full-stack thinking** (data layer + application layer + user interface)
- Shows **practical problem-solving** with a real user need
- Exhibits **professional code standards** and documentation
- Proves **database competency** beyond simple tutorials

---

## 🔧 Technical Requirements

### **Technologies Used**
- **Python 3.8+**: Core application logic
- **PostgreSQL**: Production-grade database for data persistence  
- **psycopg2**: Python PostgreSQL adapter
- **datetime**: Date handling and validation
- **decimal**: Precise financial calculations

### **Core Features To Implement**
1. **Transaction Management**: Add, view, update, delete financial transactions
2. **Category System**: Organize spending with customizable categories
3. **Reporting Engine**: Generate balance summaries, spending reports, and trends
4. **Data Validation**: Ensure data integrity and user input validation
5. **CLI Interface**: Professional command-line user experience

---

## 🗄️ Database Setup Instructions

### Step 1: Install PostgreSQL

#### **Option A: macOS (Homebrew)**
```bash
# Install PostgreSQL
brew install postgresql

# Start PostgreSQL service
brew services start postgresql

# Create your database user
psql postgres
```

#### **Option B: Ubuntu/Linux**
```bash
# Update package list
sudo apt update

# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Start PostgreSQL service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Switch to postgres user
sudo -u postgres psql
```

#### **Option C: Windows**
1. Download PostgreSQL from [https://www.postgresql.org/download/windows/](https://www.postgresql.org/download/windows/)
2. Run installer and follow setup wizard
3. Remember your password for the `postgres` user
4. Open pgAdmin or use command line `psql`

### Step 2: Create Database and User

Connect to PostgreSQL and run:

```sql
-- Create database
CREATE DATABASE budget_tracker;

-- Create user with password
CREATE USER budget_user WITH ENCRYPTED PASSWORD 'secure_password123';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE budget_tracker TO budget_user;

-- Connect to the new database
\c budget_tracker

-- Grant schema privileges  
GRANT ALL ON SCHEMA public TO budget_user;
```

### Step 3: Test Connection

```bash
# Test connection with new user
psql -h localhost -d budget_tracker -U budget_user
```

---

## 📦 Python Environment Setup

### Step 1: Create Virtual Environment
```bash
# Navigate to your project directory
cd python_budget_tracker

# Create virtual environment
python -m venv venv

# Activate virtual environment
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\\Scripts\\activate
```

### Step 2: Install Dependencies
```bash
# Install required packages
pip install -r requirements.txt

# Or install individually:
pip install psycopg2-binary python-dotenv
```

### Step 3: Configure Environment Variables
Create a `.env` file in your project root:

```env
# Database Configuration
DB_HOST=localhost
DB_NAME=budget_tracker
DB_USER=budget_user
DB_PASSWORD=secure_password123
DB_PORT=5432

# Application Settings
DEBUG=True
DEFAULT_CURRENCY=USD
```

---

## 🏗️ Project Structure

Your final project should look like this:

```
python_budget_tracker/
├── README.md
├── requirements.txt
├── .env
├── .gitignore
├── budget_tracker.py          # Main application entry point
├── database/
│   ├── __init__.py
│   ├── connection.py          # Database connection management  
│   ├── schema.sql            # Database table definitions
│   └── seed_data.sql         # Sample data for testing
├── models/
│   ├── __init__.py
│   ├── transaction.py        # Transaction data model
│   └── category.py           # Category data model  
├── services/
│   ├── __init__.py
│   ├── transaction_service.py # Business logic for transactions
│   └── report_service.py     # Reporting and analytics
└── utils/
    ├── __init__.py
    ├── validators.py         # Input validation functions
    └── formatters.py         # Output formatting utilities
```

---

## 📝 5-Day Implementation Plan

### Day 1: Environment Setup & Database Foundation 
**Goal**: Get your development environment ready and database connected
1. ✅ Install and configure PostgreSQL database
2. ✅ Set up Python virtual environment and dependencies
3. ✅ Create database schema from `schema.sql` 
4. ✅ Test database connection with `connection.py`
5. ✅ Load sample data for testing and development

**Deliverable**: Working database connection and sample data loaded

### Day 2: Core Data Models
**Goal**: Build the foundation classes for your application
1. ✅ Implement `Transaction` model with basic CRUD operations
2. ✅ Implement `Category` model with validation  
3. ✅ Add input validation and error handling to models
4. ✅ Test your models by creating, reading, and updating sample data

**Deliverable**: Working Transaction and Category models with database integration

### Day 3: Application Logic & Services  
**Goal**: Create the business logic that powers your application
1. ✅ Build core application functionality in `budget_tracker.py`
2. ✅ Implement transaction management (add, view, update, delete)
3. ✅ Add basic reporting features (balance, summaries)
4. ✅ Focus on working features over perfect code

**Deliverable**: Functional CLI application with core features working

### Day 4: User Interface & Experience
**Goal**: Create a professional command-line interface
1. ✅ Build clean menu system and navigation
2. ✅ Add user input handling and validation
3. ✅ Implement formatted output and error messages
4. ✅ Test all user workflows thoroughly  

**Deliverable**: Complete CLI application with professional user experience

### Day 5: Integration & Polish
**Goal**: Finalize your project and prepare for demo
1. ✅ Integration testing - make sure everything works together
2. ✅ Add final error handling and edge case management
3. ✅ Clean up code formatting and add documentation
4. ✅ Prepare demo script showing key features  
5. ✅ Update README.md with final project information

**Deliverable**: Production-ready budget tracker application

---

## 🔍 Key Learning Objectives

By completing this project, you will demonstrate mastery of:

### **Python Fundamentals**
- ✅ Functions and modular code organization
- ✅ Classes and object-oriented programming  
- ✅ Exception handling and error management
- ✅ File I/O and environment configuration
- ✅ Data structures (lists, dictionaries, tuples)

### **Database Skills**
- ✅ SQL queries (SELECT, INSERT, UPDATE, DELETE)
- ✅ Database connection and transaction management
- ✅ Schema design and data relationships
- ✅ Data validation and integrity constraints

### **Software Engineering Practices**
- ✅ Project structure and code organization
- ✅ Environment management and configuration
- ✅ User interface design and experience
- ✅ Documentation and professional presentation

---

## 🛠️ Getting Started

### 1. Clone Starter Code
```bash
# The starter files are already provided in this folder
# Make sure you have all the template files before beginning
```

### 2. Follow Setup Instructions
- Complete PostgreSQL installation and database setup
- Set up Python virtual environment
- Install required dependencies
- Configure environment variables

### 3. Start with Database Layer
- Run `schema.sql` to create database tables
- Test connection with `python database/connection.py`
- Load sample data with `seed_data.sql`

### 4. Build Step by Step
Follow the implementation phases above. Each file has TODO comments guiding your implementation.

### 5. Test Frequently
Run your application after each major feature to ensure everything works correctly.

---

## 📚 Additional Resources

### **PostgreSQL Learning**
- [PostgreSQL Official Tutorial](https://www.postgresql.org/docs/current/tutorial.html)
- [PostgreSQL Python Tutorial](https://www.psycopg.org/docs/usage.html)
- [SQL for Beginners](https://sqlbolt.com/)

### **Python Best Practices**
- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [Real Python CLI Applications](https://realpython.com/command-line-interfaces-python-argparse/)
- [Python Error Handling Best Practices](https://realpython.com/python-exceptions-handling/)

### **Career Development**
- [Python Developer Roadmap](https://roadmap.sh/python)
- [Database Design Fundamentals](https://www.freecodecamp.org/news/database-design-course-for-beginners/)
- [Building a Programming Portfolio](https://realpython.com/effective-python-environment/#building-a-portfolio)

---

## 🏆 Success Criteria

### **Minimum Viable Product (MVP)**
- ✅ Add, view, edit, delete transactions
- ✅ Categorize transactions (income/expense)
- ✅ Generate basic balance summary
- ✅ Data persists in PostgreSQL database
- ✅ Clean CLI interface with error handling

### **Stretch Goals (Optional)**
- 📊 Advanced reporting (spending by category, monthly trends)
- 🔍 Search and filter transactions by date/category/amount
- 📈 Data visualization with simple ASCII charts
- 💾 Import/export functionality (CSV format)
- 🔒 Data validation and business logic constraints

---

## 🎯 Final Deliverables

1. **Working CLI Application**: Fully functional budget tracker
2. **Database Schema**: Well-designed PostgreSQL tables
3. **Clean Code**: Professional structure and documentation  
4. **Integration Testing**: Manual testing of all features
5. **User Documentation**: Clear instructions for running the application
6. **Demo Ready**: Prepared to demonstrate key features

---

## 💪 You've Got This!

This project brings together everything you've learned in Python Foundations:
- **Variables and Data Types** → Storing transaction information
- **Control Flow** → Menu systems and validation logic
- **Functions** → Modular, reusable code components
- **Data Structures** → Organizing financial data efficiently
- **File I/O & Context Managers** → Database connections and configuration
- **Error Handling** → Robust, user-friendly applications

**Remember**: This isn't just an assignment—it's the foundation of your professional portfolio. Take pride in building something that solves real problems and showcases your growing expertise as a Python developer!

🚀 **Ready to build something amazing? Let's get started!**