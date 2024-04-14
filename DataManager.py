from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, session
from tabulate import tabulate
import os
from base_manager import DatabaseManager

app = Flask(__name__)
app.secret_key = 'randomcrapgo'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_table')
def create_table():
    try:
        databases = os.listdir('databases')
        flash('Table creation page loaded successfully!', 'info')
        return render_template('create_table.html', databases=databases)
    except OSError as e:
        flash(f'Error: {e}', 'error')
        return f"Error: {e}"

@app.route('/insert_data')
def insert_data():
    try:
        databases = os.listdir('databases')
        flash('Data insertion page loaded successfully!', 'info')
        return render_template('insert_data.html', databases=databases)
    except OSError as e:
        flash(f'Error: {e}', 'error')
        return f"Error: {e}"

@app.route('/view_data')
def view_data():
    try:
        databases = os.listdir('databases')
        flash('Data viewing page loaded successfully!', 'info')
        return render_template('view_data.html', databases=databases)
    except OSError as e:
        flash(f'Error: {e}', 'error')
        return f"Error: {e}"

@app.route('/process_create_table', methods=['POST'])
def process_create_table():
    try:
        db_name = request.form['db_name']
        table_name = request.form['table_name']
        columns = request.form.getlist('columns')
        db_manager = DatabaseManager(db_name)
        db_manager.create_table(table_name, columns)
        db_manager.close()
        flash('Table created successfully!', 'success')
        return redirect(url_for('index'))
    except Exception as e:
        flash(f'Error: {e}', 'error')
        return f"Error: {e}"

@app.route('/process_insert_data', methods=['POST'])
def process_insert_data():
    try:
        db_name = request.form['db_name']
        table_name = request.form['table_name']
        data = tuple(request.form['data'].split(','))
        db_manager = DatabaseManager(db_name)
        db_manager.insert_data(table_name, data)
        db_manager.close()
        flash('Data inserted successfully!', 'success')
        return redirect(url_for('index'))
    except Exception as e:
        flash(f'Error: {e}', 'error')
        return f"Error: {e}"

@app.route('/process_view_data', methods=['POST'])
def process_view_data():
    try:
        db_name = request.form['db_name']
        table_name = request.form['table_name']
        db_manager = DatabaseManager(db_name)
        columns = db_manager.cursor.execute(f"PRAGMA table_info({table_name})").fetchall()
        headers = [column[1] for column in columns]  # Extract column names
        data = db_manager.select_data(table_name, limit=200)  # Limit to first 200 values
        
        # Check if there is any data in the table
        if len(data) <= 1:
            flash.clear()
            flash('No data found in the table!', 'info')
            return redirect(url_for('view_data'))
        
        table = tabulate(data, headers=headers, tablefmt='html')
        db_manager.close()
        flash('Table found and data viewed successfully!', 'success')
        return render_template('view_data.html', table=table)
    except Exception as e:
        flash(f'Error: {e}', 'error')
        return f"Error: {e}"

@app.route('/get_tables', methods=['POST'])
def get_tables():
    try:
        data = request.json
        db_name = data.get('db_name')
        db_manager = DatabaseManager(db_name)
        tables = db_manager.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        tables = [table[0] for table in tables]
        db_manager.close()

        # Print the tables found
        print("Tables found in database '{}':".format(db_name))
        for table in tables:
            print(table)

        flash('Tables retrieved successfully!', 'success')
        return jsonify(tables)
    except Exception as e:
        flash(f'Error: {e}', 'error')
        return f"Error: {e}"

@app.route('/get_columns', methods=['POST'])
def get_columns():
    try:
        data = request.json
        table_name = data.get('table_name')
        db_name = data.get('db_name')  # Get the database name

        # Assuming you're using SQLite
        db_manager = DatabaseManager(db_name)  # You need to define db_name
        columns_query = "PRAGMA table_info('{}');".format(table_name)
        columns = db_manager.cursor.execute(columns_query).fetchall()
        columns = [column[1] for column in columns]  # Extract column names
        db_manager.close()

        # Print the columns found
        print("Columns found in table '{}':".format(table_name))
        for column in columns:
            print(column)

        flash('Columns retrieved successfully!', 'success')
        return jsonify(columns)
    except Exception as e:
        flash(f'Error: {e}', 'error')
        return f"Error: {e}"

@app.route('/delete_table', methods=['POST'])
def delete_table():
    db_name = request.form['db_name']
    table_name = request.form['table_name']
    db_manager = DatabaseManager(db_name)
    db_manager.delete_table(table_name)
    db_manager.close()
    flash('Table deleted successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/add_column', methods=['POST'])
def add_column():
    db_name = request.form['db_name']
    table_name = request.form['table_name']
    column_name = request.form['column_name']
    column_type = request.form['column_type']
    db_manager = DatabaseManager(db_name)
    db_manager.add_column(table_name, column_name, column_type)
    db_manager.close()
    flash('Column added successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/delete_column', methods=['POST'])
def delete_column():
    db_name = request.form['db_name']
    table_name = request.form['table_name']
    column_name = request.form['column_name']
    db_manager = DatabaseManager(db_name)
    db_manager.delete_column(table_name, column_name)
    db_manager.close()
    flash('Column deleted successfully!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
