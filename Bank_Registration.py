from flask import Flask, render_template, request, session, redirect
import sqlite3

app = Flask(__name__)
app.secret_key = "secret_key"

# SQLite Database Configuration
conn = sqlite3.connect('bank_registration.db')
print("Opened database successfully")
conn.execute(
    'CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT, balance REAL)')
print("Table created successfully")
conn.close()


# Route for home page
@app.route('/')
def home():
    return render_template('home.html')


# Route for user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        balance = request.form['balance']

        conn = sqlite3.connect('bank.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password, balance) VALUES (?, ?, ?)",
                       (username, password, balance))
        conn.commit()
        conn.close()

        return redirect('/login')

    return render_template('register.html')


# Route for user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user', None)

        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('bank.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['user'] = user[1]
            return redirect('/dashboard')

        return redirect('/login')

    return render_template('login.html')


# Route for user logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


# Route for user dashboard
@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        username = session['user']

        conn = sqlite3.connect('bank.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()

        return render_template('dashboard.html', user=user)

    return redirect('/login')


# Route for deposit functionality
@app.route('/deposit', methods=['GET', 'POST'])
def deposit():
    if request.method == 'POST':
        amount = float(request.form['amount'])
        username = session['user']

        conn = sqlite3.connect('bank.db')
        cursor = conn.cursor()
        cursor.execute("SELECT balance FROM users WHERE username = ?", (username,))
        balance = cursor.fetchone()[0]
        new_balance = balance + amount
        cursor.execute("UPDATE users SET balance = ? WHERE username = ?", (new_balance, username))
        conn.commit()
        conn.close()

        return redirect('/dashboard')

    return render_template('deposit.html')


# Route for withdrawal functionality
@app.route('/withdraw', methods=['GET', 'POST'])
def withdraw():
    if request.method == 'POST':
        amount = float(request.form['amount'])
        username = session['user']

        conn = sqlite3.connect('bank.db')
        cursor = conn.cursor()
        cursor.execute("SELECT balance FROM users WHERE username = ?", (username,))
        balance = cursor.fetchone()[0]

        if amount > balance:
            error = "Insufficient balance"
            return render_template('withdraw.html', error=error)

        new_balance = balance - amount
        cursor.execute("UPDATE users SET balance = ? WHERE username = ?", (new_balance, username))
        conn.commit()
        conn.close()

        return redirect('/dashboard')

    return render_template('withdraw.html')


if __name__ == '__main__':
    app.run(debug=True)
