from flask import Blueprint, render_template, request, url_for, redirect
from app.db_connect import get_db
import pandas as pd

sales = Blueprint('sales', __name__)


@sales.route('/show_sales', methods=['GET'])
def show_sales():
    # Connect to the database
    db = get_db()
    cursor = db.cursor()

    # Query all sales data
    cursor.execute('SELECT * FROM sales')
    data = cursor.fetchall()

    # Convert data to DataFrame
    df = pd.DataFrame(data, columns=['sales_id', 'monthly_amount', 'region', 'date'])

    # Render HTML table using Pandas' DataFrame to_html() method
    sales_table = df.to_html(index=False, classes="table table-striped table-bordered")
    return render_template('sales_data.html', sales_table=sales_table)


@sales.route('/add_sales_data', methods=['GET', 'POST'])
def add_sales_data():
    if request.method == 'POST':
        # Get data from form
        monthly_amount = request.form['monthly_amount']
        region = request.form['region']
        date = request.form['date']

        # Connect to database and insert new record
        db = get_db()
        cursor = db.cursor()
        cursor.execute('INSERT INTO sales (monthly_amount, region, date) VALUES (%s, %s, %s)',
                       (monthly_amount, region, date))
        db.commit()

        return redirect(url_for('sales.show_sales'))

    return render_template('add_sales_data.html')


@sales.route('/edit_sales_data/<int:sales_data_id>', methods=['GET', 'POST'])
def edit_sales_data(sales_data_id):
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        # Get updated data from form
        monthly_amount = request.form['monthly_amount']
        region = request.form['region']
        date = request.form['date']

        # Update the record in the database
        cursor.execute('UPDATE sales SET monthly_amount = %s, region = %s, date = %s WHERE sales_id = %s',
                       (monthly_amount, region, date, sales_data_id))
        db.commit()

        return redirect(url_for('sales.show_sales'))

    # GET method: fetch current data for the specified sales_data_id
    cursor.execute('SELECT * FROM sales WHERE sales_id = %s', (sales_data_id,))
    current_sale = cursor.fetchone()

    # Convert data to DataFrame to simplify data manipulation
    df = pd.DataFrame([current_sale], columns=['sales_id', 'monthly_amount', 'region', 'date'])

    # Pass data to the form pre-populated with current details
    return render_template('edit_sales_data.html', sale=df.iloc[0])


@sales.route('/delete_sales/<int:sales_id>', methods=['POST'])
def delete_sales(sales_id):
    # Connect to database and delete the specified record
    db = get_db()
    cursor = db.cursor()
    cursor.execute('DELETE FROM sales WHERE sales_id = %s', (sales_id,))
    db.commit()

    return redirect(url_for('sales.show_sales'))








