from flask import Flask, render_template, request, redirect, session
import mysql.connector
from datetime import date

app = Flask(__name__)
app.secret_key = 'secretkey'

# Update with your RDS info
conn = mysql.connector.connect(
    host='attendance-db.cjmk404s6ldp.ap-south-1.rds.amazonaws.com',
    user='admin',
    password='password',
    database='attendance_db'
)
cursor = conn.cursor(dictionary=True)

@app.route('/')
def home():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        return redirect('/login')
    except:
        return "User already exists. <a href='/login'>Go to Login</a>"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    username = request.form['username']
    password = request.form['password']
    
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()
    
    if user:
        session['user_id'] = user['id']
        return redirect('/dashboard')
    else:
        return "Invalid credentials. <a href='/login'>Try again</a>"

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')

    return render_template('dashboard.html')

@app.route('/mark_attendance', methods=['POST'])
def mark_attendance():
    user_id = session['user_id']
    today = date.today()

    cursor.execute("SELECT * FROM attendance WHERE user_id=%s AND date=%s", (user_id, today))
    if cursor.fetchone():
        return "Attendance already marked today. <a href='/dashboard'>Back</a>"

    cursor.execute("INSERT INTO attendance (user_id, date, status) VALUES (%s, %s, %s)", (user_id, today, 'Present'))
    conn.commit()
    return "Attendance marked. <a href='/dashboard'>Back</a>"

@app.route('/report')
def report():
    user_id = session['user_id']
    cursor.execute("SELECT date, status FROM attendance WHERE user_id=%s", (user_id,))
    data = cursor.fetchall()
    return render_template('report.html', attendance=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

