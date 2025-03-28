# app/items.py
"""
Handles item management: listing items, deleting, updating, and creating new items.
"""

from flask import render_template, request, redirect, url_for, flash, session
from app import app, db
from app.models import Item, Location, User

@app.route('/manage_items')
def manage_items():
    """
    List all items.
    """
    if 'username' not in session:
        flash("Please log in to manage items.", "warning")
        return redirect(url_for('login'))
    items = Item.query.all()
    return render_template("manage_items.html", items=items)

@app.route('/delete_item/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    """
    Delete the item with the provided ID.
    """
    if 'username' not in session:
        flash("Please log in to perform this action.", "warning")
        return redirect(url_for('login'))
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash("Item deleted successfully.", "success")
    return redirect(url_for("manage_items"))

@app.route('/update_item/<int:item_id>', methods=['GET', 'POST'])
def update_item(item_id):
    """
    Display a form with the item details for update.
    On POST, save changes and redirect to the items management page.
    """
    if 'username' not in session:
        flash("Please log in to perform this action.", "warning")
        return redirect(url_for('login'))
    item = Item.query.get_or_404(item_id)
    # Get lists for dropdowns
    locations = Location.query.all()
    users = User.query.all()
    if request.method == 'POST':
        item.name = request.form.get("name")
        item.category = request.form.get("category")
        item.item_user = request.form.get("item_user")
        # Convert selected location to integer
        item.item_location = int(request.form.get("item_location"))
        item.price = float(request.form.get("price"))
        db.session.commit()
        flash("Item updated successfully.", "success")
        return redirect(url_for("manage_items"))
    return render_template("update_item.html", item=item, locations=locations, users=users)

@app.route('/create_item', methods=['GET', 'POST'])
def create_item():
    """
    Create a new item. The form includes item name, category, assigned user,
    location, and price. 'Created by' is set to the current session's username.
    """
    if 'username' not in session:
        flash("Please log in to perform this action.", "warning")
        return redirect(url_for('login'))
    locations = Location.query.all()
    users = User.query.all()
    if request.method == 'POST':
        name = request.form.get("name")
        category = request.form.get("category")
        item_user = request.form.get("item_user")
        item_location = int(request.form.get("item_location"))
        price = float(request.form.get("price"))
        created_by = session.get("username")
        new_item = Item(name=name, category=category, created_by=created_by,
                        item_user=item_user, item_location=item_location, price=price)
        db.session.add(new_item)
        db.session.commit()
        flash("Item created successfully.", "success")
        return redirect(url_for("manage_items"))
    return render_template("create_item.html", locations=locations, users=users)
