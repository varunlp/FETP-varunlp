from flask import Flask, render_template, redirect, url_for, session, request
import datetime
import pytz

app = Flask(__name__)
app.secret_key = 'varun'

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'user_info' in session:
        user_info = session['user_info']
        current_time = get_indian_time()

        if request.method == 'POST':
            num_lines = int(request.form.get('num_lines', 0))
            design_output = generate_design(num_lines)
            return render_template('home.html', user_info=user_info, current_time=current_time, design_output=design_output)

        return render_template('home.html', user_info=user_info, current_time=current_time)

    return redirect(url_for('login_page'))

@app.route('/login')
def login():
    # Simulate Gmail authentication
    user_info = {
        'name': 'Varun L P',
        'email': 'vkpleela@gmail.com',
        'profile_picture': 'varun1.jpg'  # Optional
    }

    session['user_info'] = user_info
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('user_info', None)
    return redirect(url_for('login_page'))

def get_indian_time():
    indian_timezone = pytz.timezone('Asia/Kolkata')
    indian_time = datetime.datetime.now(indian_timezone).strftime('%Y-%m-%d %H:%M:%S')
    return indian_time


import random


def generate_design(num_lines):
    design = ""
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    for i in range(0, num_lines):
        spaces = " " * (num_lines - i - 1)
        random_letters = ''.join(random.choice(letters) for _ in range(2 * i + 1))
        design += spaces + random_letters + "\n"

    for i in range(num_lines - 2, -1, -1):
        spaces = " " * (num_lines - i - 1)
        random_letters = ''.join(random.choice(letters) for _ in range(2 * i + 1))
        design += spaces + random_letters + "\n"

    return design











if __name__ == '__main__':
    app.run(debug=True)
