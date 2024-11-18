from flask import Flask, g
from .app_factory import create_app
from .db_connect import close_db, get_db

# Create the app
app = create_app()
app.secret_key = 'your-secret'  # Replace with an environment variable for security

# Register Blueprints
from app.blueprints.sales import sales
from app.blueprints.regions import regions


app.register_blueprint(sales)
app.register_blueprint(regions)


# Import additional routes, if any
from . import routes

@app.before_request
def before_request():
    g.db = get_db()

@app.teardown_appcontext
def teardown_db(exception=None):
    close_db(exception)

if __name__ == '__main__':
    app.run(debug=True)

