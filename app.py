from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'tajny_klucz'

def get_db_connection():
    conn = sqlite3.connect('coupons.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    coupons = conn.execute("SELECT * FROM coupons WHERE expiration_date >= DATE('now')").fetchall()
    conn.close()
    return render_template('index.html', coupons=coupons)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin123':
            session['admin'] = True
            return redirect('/admin')
    return render_template('login.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session.get('admin'):
        return redirect('/login')
    conn = get_db_connection()
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        code = request.form['code']
        expiration_date = request.form['expiration_date']
        conn.execute("INSERT INTO coupons (title, description, code, expiration_date) VALUES (?, ?, ?, ?)", 
                     (title, description, code, expiration_date))
        conn.commit()
    coupons = conn.execute("SELECT * FROM coupons").fetchall()
    conn.close()
    return render_template('admin.html', coupons=coupons)

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
