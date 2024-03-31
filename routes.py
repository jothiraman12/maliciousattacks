from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm
from app.models import User

main = Blueprint('main', __name__)

# Your routes here

def read_csv(file_path):
    with open(file_path, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        return [row for row in reader]

def write_csv(file_path, fieldnames, data):
    with open(file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        users = read_csv('app/users.csv')
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = {
            'username': form.username.data,
            'email': form.email.data,
            'password': hashed_password
        }
        users.append(new_user)
        write_csv('app/users.csv', ['username', 'email', 'password'], users)
        flash('Your account has been created! You are now able to log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        users = read_csv('app/users.csv')
        user = next((u for u in users if u['email'] == form.email.data), None)
        if user and bcrypt.check_password_hash(user['password'], form.password.data):
            user_obj = User(user['email'], user['password'])  # Create a user object
            login_user(user_obj)
            flash('Login successful!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password.', 'danger')

    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

# Example of logging to a CSV file
def log_action(action):
    with open('app/logs.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([current_user.username, action])

# Example of using the log_action function
@app.route('/some-protected-route')
@login_required
def protected_route():
    log_action('Accessed protected route')
    return "You've accessed a protected route!"
