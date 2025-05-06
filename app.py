from flask import Flask, render_template, request, redirect, url_for, session
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Dummy credentials
USERNAME = os.getenv('ADMIN_USERNAME')
PASSWORD = os.getenv('ADMIN_PASSWORD')


@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == USERNAME and password == PASSWORD:
            session['user'] = username
            return redirect(url_for('fastag_history'))
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/transaction_details')
def transaction_details():
    if 'user' not in session:
        return redirect(url_for('login'))
    date = request.args.get('date')
    plaza = request.args.get('plaza')
    amount = request.args.get('amount')
    status = request.args.get('status')
    return render_template('transaction_details.html', date=date, plaza=plaza, amount=amount, status=status)

@app.route('/fastag_history')
def fastag_history():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('fastag_history.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=False)
    
