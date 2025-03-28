# app/users.py
"""
Handles user management: listing users by type, deleting users,
resetting passwords, and creating new users.
"""

import random
import string
from datetime import datetime
from flask import render_template, request, redirect, url_for, flash, session, jsonify
from app import app, db
from app.models import User

def generate_random_password(length=8):
    """
    Generate a random password composed of letters and digits.
    """
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

@app.route('/manage_users')
def manage_users():
    """
    List all users segregated by type (admin, manager, normal).
    Only accessible to logged-in users.
    """
    if 'username' not in session:
        flash('Please log in to manage users.', 'warning')
        return redirect(url_for('login'))
    # Group users by role
    users_by_type = {
        'admin': User.query.filter_by(user_role='admin').all(),
        'manager': User.query.filter_by(user_role='manager').all(),
        'normal': User.query.filter_by(user_role='normal').all()
    }
    return render_template('manage_users.html', users_by_type=users_by_type)

@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    """
    Delete the user with the provided user_id.
    """
    if 'username' not in session:
        flash('Please log in to perform this action.', 'warning')
        return redirect(url_for('login'))
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully.', 'success')
    return redirect(url_for('manage_users'))

@app.route('/reset_password/<int:user_id>', methods=['POST'])
def reset_password(user_id):
    """
    Reset a user's password by generating a new random password.
    Marks the user to force a password change on next login.
    If the request is made via AJAX, return the new password in JSON.
    """
    if 'username' not in session:
        flash('Please log in to perform this action.', 'warning')
        return redirect(url_for('login'))
    user = User.query.get_or_404(user_id)
    new_password = generate_random_password()
    user.password = new_password
    user.must_change_password = True  # Force password change on next login
    user.last_password_change = datetime.now()
    db.session.commit()
    # Check if the request is AJAX by examining the header
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'new_password': new_password})
    flash(f"Password reset successfully. New password: {new_password}", 'success')
    return redirect(url_for('manage_users'))

@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    """
    Create a new user by providing the full name, username, and role.
    Generates a random password for the new user and marks the user to change it on first login.
    """
    if 'username' not in session:
        flash('Please log in to perform this action.', 'warning')
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('username')
        user_role = request.form.get('user_role')
        # Check if the username already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'danger')
            return redirect(url_for('create_user'))
        new_password = generate_random_password()
        new_user = User(
            name=name,
            username=username,
            password=new_password,
            user_role=user_role,
            must_change_password=True
        )
        db.session.add(new_user)
        db.session.commit()
        flash(f"User created successfully. The password is: {new_password}", 'success')
        return redirect(url_for('manage_users'))
    return render_template('create_user.html')
