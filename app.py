from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'

# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Sample User Model (Replace with your database model)
class User(UserMixin):
    def __init__(self, username):
        self.username = username

    @staticmethod
    def get(username):
        # Replace this with your database query to get user by username
        return users.get(username)

# Sample dictionary acting as a database for users (Replace with database)
users = {'user1': User('user1')}
malicious_urls = set()
with open('malicious_urls.txt', 'r') as f:
    for line in f:
        malicious_urls.add(line.strip())

@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

# Sample login form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    submit = SubmitField('Login')

# Sample registration form
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    submit = SubmitField('Register')

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        url = request.form['url']
        result = check_malicious(url)
        return render_template('index.html', result=result, url=url)
    return render_template('index.html', result=None, url=None)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = users.get(form.username.data)
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password.', 'error')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        if username in users:
            flash('Username already taken.', 'error')
        else:
            hashed_password = generate_password_hash(form.password.data, method='sha256')
            users[username] = User(username, hashed_password)
            flash('Registration successful. Please log in.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('home'))

@login_manager.unauthorized_handler
def unauthorized():
    flash('You must be logged in to access this page.', 'error')
    return redirect(url_for('login'))

def check_malicious(url):
    if url in malicious_urls:
        return f"The URL '{url}' is detected as malicious."
    else:
        return f"The URL '{url}' is safe."

if __name__ == '__main__':
    app.run(debug=True)
