from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import requests

app = Flask(__name__)

# Load users and logs from CSV files
users_df = pd.read_csv('data/users.csv')
logs_df = pd.read_csv('data/logs.csv')

# Load malicious URLs from CSV file
malicious_urls = pd.read_csv('urls.csv')['url'].tolist()

def save_logs(username, url, result):
    logs_df = pd.read_csv('data/logs.csv')
    logs_df = logs_df.append({'Username': username, 'URL': url, 'Result': result}, ignore_index=True)
    logs_df.to_csv('data/logs.csv', index=False)

def detect_malicious(url):
    if url in malicious_urls:
        return "Malicious"
    else:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return "Safe"
            else:
                return "Malicious"
        except:
            return "The URL is not available in the list of Malicious URLs Provided. Seems to be a Safe URL"

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if check_credentials(username, password):
            return redirect(url_for('detect'))
        else:
            return render_template('login.html')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username not in users_df['Username'].values:
            users_df = users_df.append({'Username': username, 'Password': password}, ignore_index=True)
            users_df.to_csv('data/users.csv', index=False)
            return redirect(url_for('login'))
        else:
            return render_template('register.html')
    return render_template('register.html')

@app.route('/detect', methods=['GET', 'POST'])
def detect():
    if request.method == 'POST':
        url = request.form['url']
        result = detect_malicious(url)
        username = request.form['username'] if 'username' in request.form else 'Guest'
        save_logs(username, url, result)
        return render_template('results.html', url=url, result=result)
    # If it's a GET request or no username was found
    return render_template('detect.html', username='Guest')

def check_credentials(username, password):
    return (username in users_df['Username'].values) and \
           (password == users_df.loc[users_df['Username'] == username, 'Password'].values[0])

if __name__ == '__main__':
    app.run(debug=True)
