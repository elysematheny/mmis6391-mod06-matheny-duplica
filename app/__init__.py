from flask import Flask, g
from .app_factory import create_app
from .db_connect import close_db, get_db

# Create the app
app = create_app()
app.secret_key = 'your-secret'  # Replace with an environment variable for security

# Register Blueprints
from app.blueprints.sales import sales  # Import the sales blueprint


app.register_blueprint(sales)  # Register the sales blueprint

# Import additional routes, if any
from . import routes

@app.before_request
def before_request():
    # Setup database connection for each request
    g.db = get_db()

# Teardown database connection after each request
@app.teardown_appcontext
def teardown_db(exception=None):
    close_db(exception)


