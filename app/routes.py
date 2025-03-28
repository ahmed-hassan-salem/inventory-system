# app/routes.py
from flask import render_template, session, redirect, url_for
from app import app
from app.models import User, Location, Item

@app.route('/')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    # Query counts by user type
    admin_count = User.query.filter_by(user_role='admin').count()
    manager_count = User.query.filter_by(user_role='manager').count()
    normal_count = User.query.filter_by(user_role='normal').count()
    # Query totals for locations and items
    location_count = Location.query.count()
    item_count = Item.query.count()
    return render_template('home.html', 
                           admin_count=admin_count,
                           manager_count=manager_count, 
                           normal_count=normal_count,
                           location_count=location_count,
                           item_count=item_count)
