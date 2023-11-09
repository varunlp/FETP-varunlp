from flask import Flask, render_template, redirect, url_for, session
import datetime
import pytz  

app = Flask(__name__)
app.secret_key = '2001'

@app.route('/')
def home():
    user_info = session.get('user_info')
    current_time = get_indian_time()
    return render_template('index.html', user_info=user_info, current_time=current_time)

def get_indian_time():
    indian_timezone = pytz.timezone('Asia/Kolkata')
    indian_time = datetime.datetime.now(indian_timezone).strftime('%Y-%m-%d %H:%M:%S')
    return indian_time

@app.route('/login')
def login():
    
    user_info = {
        'name': 'Varun L P',
        'email': 'vkpleela@gmail.com',
        'profile_picture': 'varun1.jpg'  
    }

    session['user_info'] = user_info
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('user_info', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
