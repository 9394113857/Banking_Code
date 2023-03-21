import sqlite3

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect('bank_registration.db')

# Create a cursor to execute SQL statements
cursor = conn.cursor()

# Create a table
cursor.execute('''CREATE TABLE IF NOT EXISTS users
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   username TEXT UNIQUE NOT NULL,
                   password TEXT NOT NULL,
                   balance REAL NOT NULL)''')

# Insert some data
cursor.execute("INSERT INTO users (username, password, balance) VALUES (?, ?, ?)", ('Alice', 'password123', 1000.00))
cursor.execute("INSERT INTO users (username, password, balance) VALUES (?, ?, ?)", ('Bob', 'secret', 500.00))

# Commit the changes to the database
conn.commit()

# Retrieve data from the database
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()
for row in rows:
    print(row)

# Update data in the database
cursor.execute("UPDATE users SET balance = ? WHERE username = ?", (1500.00, 'Alice'))
conn.commit()

# Delete data from the database
cursor.execute("DELETE FROM users WHERE username = ?", ('Bob',))
conn.commit()

# Close the database connection
conn.close()
