# app/auth.py
"""
This module handles authentication: login and password change.
"""

from flask import render_template, request, redirect, url_for, session, flash
from datetime import datetime
from app import app, db
from app.models import User

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            # Update last login time and commit changes
            user.last_login = datetime.now()
            db.session.commit()
            session['username'] = username
            flash('Login successful', 'success')
            # If the user must change password, redirect to change password page
            if user.must_change_password:
                return redirect(url_for('change_password'))
            return redirect(url_for('home'))
        else:
            if user:
                user.last_failed_login = datetime.now()
                db.session.commit()
            flash('Invalid username or password', 'danger')
    return render_template('login.html')

# Change password route
@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if 'username' not in session:
        flash('Please log in to change your password.', 'warning')
        return redirect(url_for('login'))

    username = session['username']
    user = User.query.filter_by(username=username).first()

    if request.method == 'POST':
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        if new_password != confirm_password:
            flash('Passwords do not match', 'danger')
        elif not new_password:
            flash('Password cannot be empty', 'danger')
        else:
            user.password = new_password
            user.must_change_password = False
            user.last_password_change = datetime.now()
            db.session.commit()
            flash('Password updated successfully', 'success')
            return redirect(url_for('home'))
    return render_template('change_password.html')

@app.route('/logout')
def logout():
    # Remove the username from session if it exists
    session.pop('username', None)
    flash("You have been logged out.", "success")
    return redirect(url_for('login'))