from flask import Flask, render_template, request, redirect, session, url_for
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Patna@1234'
app.config['MYSQL_DB'] = 'job_portal'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        middle_name = request.form['middle_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        user_type = request.form['user_type']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO user_information (first_name, middle_name, last_name, email, password, user_type) VALUES (%s, %s, %s, %s, %s, %s)",
                    (first_name, middle_name, last_name, email, password, user_type))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM user_information WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()

        if user and check_password_hash(user[5], password):
            session['user_id'] = user[0]
            session['user_type'] = user[6]
            return redirect(url_for('dashboard'))

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_type = session['user_type']
    if user_type == 'job_seeker':
        return render_template('seeker_dashboard.html')
    elif user_type == 'employer':
        return render_template('employer_dashboard.html')
    else:
        return render_template('admin_dashboard.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
