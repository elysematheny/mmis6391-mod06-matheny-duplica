from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db_connect import get_db
import pandas as pd
import plotly.express as px
import plotly.io as pio
from app.functions import total_sales_by_region, monthly_sales_trend, top_performing_region

sales = Blueprint('sales', __name__)


# Route to show sales data with Edit and Delete buttons
@sales.route('/show_sales')
def show_sales():
    connection = get_db()
    query = "SELECT * FROM sales_data"
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()

    # Create a Pandas DataFrame for better formatting
    df = pd.DataFrame(result, columns=['sales_data_id', 'monthly_amount', 'date', 'region'])

    # Add the action buttons to the DataFrame
    df['Actions'] = df['sales_data_id'].apply(lambda
                                                  id: f'<a href="{url_for("sales.edit_sales_data", sales_data_id=id)}" class="btn btn-sm btn-info">Edit</a> '
                                                      f'<form action="{url_for("sales.delete_sales_data", sales_data_id=id)}" method="post" style="display:inline;">'
                                                      f'<button type="submit" class="btn btn-sm btn-danger">Delete</button></form>')

    # Convert DataFrame to HTML table
    table_html = df.to_html(classes='dataframe table table-striped table-bordered', index=False, escape=False)

    return render_template("sales_data.html", table=table_html)


# Route to render the add sales data form
@sales.route('/add_sales_data', methods=['GET', 'POST'])
def add_sales_data():
    if request.method == 'POST':
        monthly_amount = request.form['monthly_amount']
        date = request.form['date']
        region = request.form['region']

        if not monthly_amount or not date or not region:
            flash("All fields are required!", "danger")
            return redirect(url_for('sales.add_sales_data'))

        connection = get_db()
        try:
            query = "INSERT INTO sales_data (monthly_amount, date, region) VALUES (%s, %s, %s)"
            with connection.cursor() as cursor:
                cursor.execute(query, (monthly_amount, date, region))
            connection.commit()
            flash("New sales data added successfully!", "success")
        except Exception as e:
            flash(f"Error: {str(e)}", "danger")
        return redirect(url_for('sales.show_sales'))

    return render_template("add_sales_data.html")


# Route to handle editing a row
@sales.route('/edit_sales_data/<int:sales_data_id>', methods=['GET', 'POST'])
def edit_sales_data(sales_data_id):
    connection = get_db()
    if request.method == 'POST':
        monthly_amount = request.form['monthly_amount']
        date = request.form['date']
        region = request.form['region']

        if not monthly_amount or not date or not region:
            flash("All fields are required!", "danger")
            return redirect(url_for('sales.edit_sales_data', sales_data_id=sales_data_id))

        try:
            query = "UPDATE sales_data SET monthly_amount = %s, date = %s, region = %s WHERE sales_data_id = %s"
            with connection.cursor() as cursor:
                cursor.execute(query, (monthly_amount, date, region, sales_data_id))
            connection.commit()
            flash("Sales data updated successfully!", "success")
        except Exception as e:
            flash(f"Error: {str(e)}", "danger")
        return redirect(url_for('sales.show_sales'))

    # Fetch the current data to pre-populate the form
    query = "SELECT * FROM sales_data WHERE sales_data_id = %s"
    with connection.cursor() as cursor:
        cursor.execute(query, (sales_data_id,))
        sales_data = cursor.fetchone()

    return render_template("edit_sales_data.html", sales_data=sales_data)


# Route to handle deleting a row
@sales.route('/delete_sales_data/<int:sales_data_id>', methods=['POST'])
def delete_sales_data(sales_data_id):
    connection = get_db()
    try:
        query = "DELETE FROM sales_data WHERE sales_data_id = %s"
        with connection.cursor() as cursor:
            cursor.execute(query, (sales_data_id,))
        connection.commit()
        flash("Sales data deleted successfully!", "success")
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")
    return redirect(url_for('sales.show_sales'))


# Route to show sales data with analysis
@sales.route('/reports')
def reports():
    connection = get_db()
    query = "SELECT * FROM sales_data"
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()

    # Create a DataFrame from the sales data
    df = pd.DataFrame(result, columns=['sales_data_id', 'monthly_amount', 'date', 'region'])

    # 1. Total Sales by Region
    total_sales_by_region_df = total_sales_by_region(df)

    # 2. Monthly Sales Trend (group by year and month)
    monthly_sales_trend_df = monthly_sales_trend(df)

    # 3. Top-Performing Region based on total sales
    top_performing_region_df = top_performing_region(df)

    # Render the template and pass the analysis results to the HTML
    return render_template(
        'reports.html',
        total_sales_by_region=total_sales_by_region_df.to_html(classes='table table-bordered table-striped',
                                                               index=False, escape=False),
        monthly_sales_trend=monthly_sales_trend_df.to_html(classes='table table-bordered table-striped', index=False,
                                                           escape=False),
        top_performing_region=top_performing_region_df.to_html(classes='table table-bordered table-striped',
                                                               index=False, escape=False)
    )


# Route for visualization
@sales.route('/visualization')
def visualization():
    connection = get_db()
    query = "SELECT * FROM sales_data"
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()

    # Create a DataFrame from the sales data
    df = pd.DataFrame(result, columns=['sales_data_id', 'monthly_amount', 'date', 'region'])

    # 1. Generate Total Sales by Region Bar Chart using Plotly
    total_sales_by_region = df.groupby('region')['monthly_amount'].sum().reset_index()
    total_sales_by_region = total_sales_by_region.rename(columns={'monthly_amount': 'total_sales'})

    fig = px.bar(total_sales_by_region, x='region', y='total_sales', title="Total Sales by Region")

    # Convert the Plotly figure to HTML and pass it to the template
    graph_html = pio.to_html(fig, full_html=False)

    return render_template('visualization.html', graph_html=graph_html)













