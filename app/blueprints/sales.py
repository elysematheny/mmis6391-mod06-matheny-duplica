from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db_connect import get_db
import pandas as pd

sales = Blueprint('sales', __name__)

@sales.route('/show_sales', methods=['GET'])
def show_sales():
    db = get_db()  # Get the DB connection from g
    with db.cursor() as cursor:  # Correct cursor usage
        cursor.execute('SELECT * FROM sales')
        result = cursor.fetchall()

        if not result:
            print("No sales records found!")

        # Create a DataFrame from the fetched data
        df = pd.DataFrame(result)
        table_html = df.to_html(classes="table table-striped table-bordered", escape=False, index=False)
        rows_only = table_html.split('<tbody>')[1].split('</tbody>')[0]

        return render_template('sales_data.html', sales_table=rows_only)



# Route to add new sales data
@sales.route('/add_sales_data', methods=['GET', 'POST'])
def add_sales_data():
    if request.method == 'POST':
        # Retrieve form data
        monthly_amount = request.form['monthly_amount']
        region = request.form['region']
        date = request.form['date']

        # Insert new sale record into the database
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            'INSERT INTO sales (monthly_amount, region, date) VALUES (%s, %s, %s)',
            (monthly_amount, region, date)
        )
        db.commit()

        flash("Sale added successfully!", "success")
        return redirect(url_for('sales.show_sales'))

    return render_template('add_sales_data.html')

# Route to edit existing sales data
@sales.route('/edit_sales_data/<int:sales_id>', methods=['GET', 'POST'])
def edit_sales_data(sales_id):
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        # Handle form submission and update the record
        monthly_amount = request.form['monthly_amount']
        region = request.form['region']
        date = request.form['date']

        cursor.execute(
            'UPDATE sales SET monthly_amount = %s, region = %s, date = %s WHERE sales_id = %s',
            (monthly_amount, region, date, sales_id)
        )
        db.commit()
        flash("Sale updated successfully!", "success")
        return redirect(url_for('sales.show_sales'))

    # GET request: Fetch the current data to pre-populate the form
    cursor.execute('SELECT * FROM sales WHERE sales_id = %s', (sales_id,))
    current_sale = cursor.fetchone()

    return render_template('edit_sales_data.html', current_sale=current_sale)


# Route to delete a specific sales record
@sales.route('/delete_sales_data/<int:sales_id>', methods=['POST'])
def delete_sales_data(sales_id):
    db = get_db()
    cursor = db.cursor()

    # Delete the specified sale record from the database
    cursor.execute('DELETE FROM sales WHERE sales_id = %s', (sales_id,))
    db.commit()

    flash("Sale deleted successfully!", "success")
    return redirect(url_for('sales.show_sales'))










