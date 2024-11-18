from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db_connect import get_db
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

visualizations = Blueprint('visualizations', __name__)

@visualizations.route('/show_visualizations')
def show_visualizations():
    connection = get_db()
    query = "SELECT * FROM sales_data"
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
    df = pd.DataFrame(result)
    df.columns = [col.lower() for col in df.columns]  # Normalize column names to lowercase

    # Create a plot
    fig, ax = plt.subplots()
    df.groupby('region')['monthly_amount'].sum().plot(kind='bar', ax=ax)
    ax.set_title('Total Monthly Sales by Region')
    ax.set_xlabel('Region')
    ax.set_ylabel('Total Monthly Sales')

    # Save the plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return render_template("visualizations.html", plot_url=plot_url)

@visualizations.route('/add_visualization', methods=['GET', 'POST'])
def add_visualization():
    if request.method == 'POST':
        # Handle form submission for adding a new visualization
        pass

    return render_template("add_visualization.html")

@visualizations.route('/edit_visualization/<int:visualization_id>', methods=['GET', 'POST'])
def edit_visualization(visualization_id):
    if request.method == 'POST':
        # Handle form submission for editing an existing visualization
        pass

    return render_template("edit_visualization.html")

@visualizations.route('/delete_visualization/<int:visualization_id>', methods=['POST'])
def delete_visualization(visualization_id):
    # Handle deletion of a visualization
    pass

    return redirect(url_for('visualizations.show_visualizations'))