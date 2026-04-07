-- Sample data for testing the budget tracker
-- Run this after creating the schema

-- Insert default categories
INSERT INTO categories (name, type, description) VALUES
('Salary', 'income', 'Regular employment income'),
('Freelance', 'income', 'Freelance work and consulting'),
('Investment', 'income', 'Investment returns and dividends'),
('Food', 'expense', 'Groceries and dining out'),
('Transportation', 'expense', 'Gas, public transport, car maintenance'),
('Utilities', 'expense', 'Electricity, water, internet, phone'),
('Entertainment', 'expense', 'Movies, games, hobbies'),
('Healthcare', 'expense', 'Medical bills and insurance'),
('Education', 'expense', 'Books, courses, training'),
('Shopping', 'expense', 'Clothing, electronics, miscellaneous')
ON CONFLICT (name) DO NOTHING;

-- Insert sample transactions for testing
INSERT INTO transactions (amount, description, transaction_date, category_id, type) VALUES
(3000.00, 'Monthly salary', '2024-03-01', (SELECT id FROM categories WHERE name = 'Salary'), 'income'),
(500.00, 'Freelance project payment', '2024-03-05', (SELECT id FROM categories WHERE name = 'Freelance'), 'income'),
(120.50, 'Grocery shopping at Whole Foods', '2024-03-02', (SELECT id FROM categories WHERE name = 'Food'), 'expense'),
(45.00, 'Gas station fill-up', '2024-03-03', (SELECT id FROM categories WHERE name = 'Transportation'), 'expense'),
(89.99, 'Monthly internet bill', '2024-03-01', (SELECT id FROM categories WHERE name = 'Utilities'), 'expense'),
(25.00, 'Movie tickets', '2024-03-06', (SELECT id FROM categories WHERE name = 'Entertainment'), 'expense'),
(75.30, 'Dinner at restaurant', '2024-03-07', (SELECT id FROM categories WHERE name = 'Food'), 'expense'),
(200.00, 'Programming course', '2024-03-08', (SELECT id FROM categories WHERE name = 'Education'), 'expense'),
(150.00, 'Doctor visit copay', '2024-03-09', (SELECT id FROM categories WHERE name = 'Healthcare'), 'expense'),
(80.00, 'New coding book', '2024-03-10', (SELECT id FROM categories WHERE name = 'Education'), 'expense');

-- Verify the data was inserted
SELECT 'Categories' as table_name, COUNT(*) as count FROM categories
UNION ALL
SELECT 'Transactions' as table_name, COUNT(*) as count FROM transactions;