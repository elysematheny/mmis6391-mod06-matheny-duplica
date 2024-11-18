from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db_connect import get_db
import pandas as pd

reports = Blueprint('reports', __name__)

@reports.route('/show_reports')
def show_reports():
    connection = get_db()
    query = "SELECT * FROM reports"
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
    df = pd.DataFrame(result)
    df.columns = [col.lower() for col in df.columns]  # Normalize column names to lowercase
    df['actions'] = df['report_id'].apply(lambda id:
                                          f'<a href="{url_for("reports.edit_report", report_id=id)}" class="btn btn-sm btn-info">Edit</a> '
                                          f'<form action="{url_for("reports.delete_report", report_id=id)}" method="post" style="display:inline;">'
                                          f'<button type="submit" class="btn btn-sm btn-danger">Delete</button></form>'
                                          )
    table_html = df.to_html(classes='dataframe table table-striped table-bordered', index=False, header=False,
                            escape=False)
    rows_only = table_html.split('<tbody>')[1].split('</tbody>')[0]

    return render_template("reports.html", table=rows_only)

@reports.route('/add_report', methods=['GET', 'POST'])
def add_report():
    if request.method == 'POST':
        report_name = request.form['report_name']
        report_data = request.form['report_data']

        connection = get_db()
        query = "INSERT INTO reports (report_name, report_data) VALUES (%s, %s)"
        with connection.cursor() as cursor:
            cursor.execute(query, (report_name, report_data))
        connection.commit()
        flash("New report added successfully!", "success")
        return redirect(url_for('reports.show_reports'))

    return render_template("add_report.html")

@reports.route('/edit_report/<int:report_id>', methods=['GET', 'POST'])
def edit_report(report_id):
    connection = get_db()
    if request.method == 'POST':
        report_name = request.form['report_name']
        report_data = request.form['report_data']

        query = "UPDATE reports SET report_name = %s, report_data = %s WHERE report_id = %s"
        with connection.cursor() as cursor:
            cursor.execute(query, (report_name, report_data, report_id))
        connection.commit()
        flash("Report updated successfully!", "success")
        return redirect(url_for('reports.show_reports'))

    query = "SELECT * FROM reports WHERE report_id = %s"
    with connection.cursor() as cursor:
        cursor.execute(query, (report_id,))
        report = cursor.fetchone()

    return render_template("edit_report.html", report=report)

@reports.route('/delete_report/<int:report_id>', methods=['POST'])
def delete_report(report_id):
    connection = get_db()
    query = "DELETE FROM reports WHERE report_id = %s"
    with connection.cursor() as cursor:
        cursor.execute(query, (report_id,))
    connection.commit()
    flash("Report deleted successfully!", "success")
    return redirect(url_for('reports.show_reports'))