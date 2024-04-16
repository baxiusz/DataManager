# Flask SQLite Database Manager

This Flask application serves as a simple SQLite database manager. It provides a web interface to create, view, and manipulate SQLite databases and their tables.

## Prerequisites

Make sure you have Python installed on your system. You can download it from [python.org](https://www.python.org/).

Install Flask and tabulate libraries using pip:

```bash
pip install flask tabulate
```

## Usage

1. Clone or download the repository to your local machine.
2. Navigate to the directory containing the code.
3. Run the Flask application:

```bash
python DataManager.py
```

4. Access the web interface by visiting [http://localhost:5000/](http://localhost:5000/) in your web browser.

## Features

### Create Table

- Click on the "Create Table" option to create a new table in an existing SQLite database.
- Select the database and provide the table name along with column names and types.
- Click "Create" to create the table.

### Insert Data

- Use the "Insert Data" option to insert data into an existing table.
- Select the database and table to insert data into.
- Enter comma-separated values for each column and click "Insert".

### View Data

- View the data stored in a table using the "View Data" option.
- Select the database and table to view data from.
- The data will be displayed in tabular format.

### Delete Table (Work in Progress)

- Delete a table from the database using the "Delete Table" option.
- Select the database and table to delete.
- Click "Delete" to remove the table.

### Add Column (Work in Progress)

- Add a new column to an existing table with the "Add Column" option.
- Select the database, table, and provide the column name and type.
- Click "Add" to add the column to the table.

### Delete Column (Work in Progress)

- Delete a column from an existing table using the "Delete Column" option.
- Select the database, table, and column to delete.
- Click "Delete" to remove the column from the table.

## Structure

- `DataManager.py`: Contains the Flask application with routes for handling database operations.
- `base_manager.py`: Defines the `DatabaseManager` class responsible for managing SQLite databases and tables.

## Note

- Ensure that the `databases` directory exists in the root directory. This is where SQLite databases will be stored.
- This application assumes the usage of SQLite databases.
- Error handling is minimal in this application. Modify and enhance error handling as per your requirements.
