# app/locations.py
"""
Handles location management: listing locations, deleting, updating, and creating new locations.
"""

from flask import render_template, request, redirect, url_for, flash, session
from app import app, db
from app.models import Location

@app.route('/manage_locations')
def manage_locations():
    """
    List all locations.
    """
    if 'username' not in session:
        flash('Please log in to manage locations.', 'warning')
        return redirect(url_for('login'))
    locations = Location.query.all()
    return render_template('manage_locations.html', locations=locations)

@app.route('/delete_location/<int:location_id>', methods=['POST'])
def delete_location(location_id):
    """
    Delete the location with the given ID.
    """
    if 'username' not in session:
        flash('Please log in to perform this action.', 'warning')
        return redirect(url_for('login'))
    location = Location.query.get_or_404(location_id)
    db.session.delete(location)
    db.session.commit()
    flash('Location deleted successfully.', 'success')
    return redirect(url_for('manage_locations'))

@app.route('/update_location/<int:location_id>', methods=['GET', 'POST'])
def update_location(location_id):
    """
    Display a form with the location details ready for update.
    On POST, save changes and redirect to the locations management page.
    """
    if 'username' not in session:
        flash('Please log in to perform this action.', 'warning')
        return redirect(url_for('login'))
    location = Location.query.get_or_404(location_id)
    if request.method == 'POST':
        location.name = request.form.get('name')
        location.address = request.form.get('address')
        location.created_by = request.form.get('created_by')
        db.session.commit()
        flash('Location updated successfully.', 'success')
        return redirect(url_for('manage_locations'))
    return render_template('update_location.html', location=location)

@app.route('/create_location', methods=['GET', 'POST'])
def create_location():
    """
    Create a new location. The form requires the location name and address.
    The 'created_by' field is set from the current session's username.
    """
    if 'username' not in session:
        flash('Please log in to perform this action.', 'warning')
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form.get('name')
        address = request.form.get('address')
        # Use the logged in user's username as the creator
        created_by = session.get('username')
        new_location = Location(name=name, address=address, created_by=created_by)
        db.session.add(new_location)
        db.session.commit()
        flash('Location created successfully.', 'success')
        return redirect(url_for('manage_locations'))
    return render_template('create_location.html')
