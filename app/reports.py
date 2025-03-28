# app/reports.py
import csv
import io
from flask import render_template, request, redirect, url_for, flash, session, Response
from app import app, db
from app.models import User, Location, Item

@app.route('/reports')
def reports():
    """
    Render a page to choose which report to generate.
    """
    if 'username' not in session:
        flash('Please log in to access reports.', 'warning')
        return redirect(url_for('login'))
    return render_template('reports.html')

@app.route('/generate_report', methods=['POST'])
def generate_report():
    """
    Generate a CSV report for the selected data type.
    """
    if 'username' not in session:
        flash('Please log in to access reports.', 'warning')
        return redirect(url_for('login'))
    
    report_type = request.form.get('report_type')
    si = io.StringIO()
    cw = csv.writer(si)
    
    if report_type == 'users':
        cw.writerow(['ID', 'Name', 'Username', 'Last Login', 'Last Password Change', 'Last Failed Login', 'User Role'])
        for user in User.query.all():
            cw.writerow([
                user.id,
                user.name,
                user.username,
                user.last_login,
                user.last_password_change,
                user.last_failed_login,
                user.user_role
            ])
        filename = 'users_report.csv'
    
    elif report_type == 'locations':
        cw.writerow(['ID', 'Name', 'Address', 'Created By'])
        for loc in Location.query.all():
            cw.writerow([
                loc.id,
                loc.name,
                loc.address,
                loc.created_by
            ])
        filename = 'locations_report.csv'
    
    elif report_type == 'items':
        cw.writerow(['ID', 'Name', 'Category', 'Created By', 'Item User', 'Item Location', 'Price'])
        for item in Item.query.all():
            location_name = item.location.name if item.location else 'N/A'
            cw.writerow([
                item.id,
                item.name,
                item.category,
                item.created_by,
                item.item_user,
                location_name,
                item.price
            ])
        filename = 'items_report.csv'
    
    else:
        flash("Invalid report type selected", "danger")
        return redirect(url_for('reports'))
    
    output = si.getvalue()
    response = Response(output, mimetype="text/csv")
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    return response
