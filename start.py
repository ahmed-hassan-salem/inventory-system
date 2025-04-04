# start.py
import os
from app import app, db
from app.models import User

if __name__ == '__main__':
    # Define path to the SQLite database file
    db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'inventory.db')
    # If the database doesn't exist, create it and add the default admin user
    if not os.path.exists(db_path):
        with app.app_context():
            db.create_all()
            admin = User(
                name="Administrator",
                username="admin",
                password="password",       # For demo only. Use hashed passwords in production.
                user_role="admin",
                must_change_password=True  # Force password change on first login
            )
            db.session.add(admin)
            db.session.commit()
    app.run(debug=True, host='0.0.0.0', port= 8080)
