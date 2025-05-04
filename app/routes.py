from flask import render_template, redirect, url_for, flash, request, session, send_from_directory
from app import app, mysql, bcrypt
import os

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        middle_name = request.form['middle_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        user_type = request.form['user_type']

        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO user_information (first_name, middle_name, last_name, email, password, user_type) VALUES (%s, %s, %s, %s, %s, %s)",
                    (first_name, middle_name, last_name, email, hashed_pw, user_type))
        mysql.connection.commit()

        user_id = cur.lastrowid

        if user_type == 'job_seeker':
            cur.execute("INSERT INTO job_seeker (user_id) VALUES (%s)", (user_id,))
        elif user_type == 'employer':
            company = request.form['company_name']
            website = request.form['company_website']
            cur.execute("INSERT INTO employer (user_id, company_name, company_website) VALUES (%s, %s, %s)", (user_id, company, website))
        mysql.connection.commit()
        cur.close()
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT user_id, password, user_type FROM user_information WHERE email = %s", (email,))
        user = cur.fetchone()
        if user and bcrypt.check_password_hash(user[1], password):
            session['user_id'] = user[0]
            session['user_type'] = user[2]
            return redirect(url_for('dashboard'))
        else:
            flash('Login Failed. Check email/password.', 'danger')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_type = session['user_type']
    if user_type == 'job_seeker':
        cur = mysql.connection.cursor()
        cur.execute("SELECT job_id, title, location FROM job")
        jobs = cur.fetchall()
        return render_template('dashboard_seeker.html', jobs=jobs)
    elif user_type == 'employer':
        cur = mysql.connection.cursor()
        cur.execute("SELECT employer_id FROM employer WHERE user_id = %s", (session['user_id'],))
        employer_id = cur.fetchone()[0]
        cur.execute("SELECT * FROM job WHERE employer_id = %s", (employer_id,))
        jobs = cur.fetchall()
        return render_template('dashboard_employer.html', jobs=jobs)
    else:
        return 'Admin dashboard coming soon.'

@app.route('/post_job', methods=['GET', 'POST'])
def post_job():
    if session.get('user_type') != 'employer':
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        title = request.form['title']
        location = request.form['location']
        salary_range = request.form['salary_range']
        description = request.form['description']
        requirements = request.form['requirements']
        cur = mysql.connection.cursor()
        cur.execute("SELECT employer_id FROM employer WHERE user_id = %s", (session['user_id'],))
        employer_id = cur.fetchone()[0]
        cur.execute("INSERT INTO job (employer_id, title, location, salary_range, description, requirements) VALUES (%s, %s, %s, %s, %s, %s)",
                    (employer_id, title, location, salary_range, description, requirements))
        mysql.connection.commit()
        cur.close()
        flash('Job posted successfully!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('post_job.html')

@app.route('/apply/<int:job_id>', methods=['GET', 'POST'])
def apply(job_id):
    if session.get('user_type') != 'job_seeker':
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        cover_letter = request.form['cover_letter']
        cur = mysql.connection.cursor()
        cur.execute("SELECT seeker_id FROM job_seeker WHERE user_id = %s", (session['user_id'],))
        seeker_id = cur.fetchone()[0]
        cur.execute("INSERT INTO application (job_id, seeker_id, cover_letter) VALUES (%s, %s, %s)", (job_id, seeker_id, cover_letter))
        mysql.connection.commit()
        flash('Application submitted!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('apply.html', job_id=job_id)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))
