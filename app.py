from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect, text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/viraj/AppData/Roaming/TIPP10/tipp10v2.db'  # Make sure this points to your actual database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route('/')
def home():
    # Get the list of all table names
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()

    table_data = {}

    # Open a connection to execute raw SQL queries
    with db.engine.connect() as connection:
        # For each table, get the column names and the first 3 rows of data
        for table in tables:
            # open_analysis
            if table not in ['keyboard_grids', "keyboard_layouts", "lesson_analysis", "language_layouts", "db_version", "lesson_chars", "language_lessons", "language_interfaces", "lesson_content", "lesson_list", "numboard_grids", "numboard_layouts", "open_analysis", "open_content", "open_list", "open_themes", "own_content", "own_list"]:
                columns = inspector.get_columns(table)

                # Extract column headers (names)
                column_headers = [column['name'] for column in columns]

                # Query to get the first 3 rows of the table
                result = connection.execute(text(f"SELECT * FROM {table}")).fetchall()

                # Store the data along with column headers
                table_data[table] = {
                    'headers': column_headers,
                    'rows': result
                }
            else:
                columns = inspector.get_columns(table)

                # Extract column headers (names)
                column_headers = [column['name'] for column in columns]

                # Query to get the first 3 rows of the table
                result = connection.execute(text(f"SELECT * FROM {table} LIMIT 3")).fetchall()

                # Store the data along with column headers
                table_data[table] = {
                    'headers': column_headers,
                    'rows': result
                }

    return render_template('tables.html', table_data=table_data)

if __name__ == '__main__':
    app.run(debug=True)