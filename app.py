import csv
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# File paths for CSV data
USERS_CSV = 'users.csv'
MALICIOUS_URLS_CSV = 'malicious_urls.csv'
LOGS_CSV = 'logs.csv'

def write_to_csv(filename, data):
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

def read_csv(filename):
    with open(filename, mode='r', newline='') as file:
        reader = csv.reader(file)
        data = [row for row in reader]
    return data

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Check if username or email already exists
        users = read_csv(USERS_CSV)
        for user in users:
            if user[0] == username:
                flash('Username already exists! Please choose a different one.', 'error')
                return redirect(url_for('register'))
            if user[1] == email:
                flash('Email address already exists! Please use a different one.', 'error')
                return redirect(url_for('register'))

        new_user = [username, email, password]
        write_to_csv(USERS_CSV, new_user)
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        users = read_csv(USERS_CSV)
        for user in users:
            if user[0] == username and user[2] == password:
                flash('Login successful!', 'success')
                return redirect(url_for('home'))

        flash('Invalid username or password. Please try again.', 'error')
        return redirect(url_for('login'))

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
