# Import necessary libraries and modules
from flask import Flask, request, jsonify  # Import Flask for web framework, request for handling HTTP requests, and jsonify for JSON responses
import pymysql  # Import pymysql for working with MySQL databases
from flask_cors import CORS  # Import CORS to handle Cross-Origin Resource Sharing (CORS) issues
import datetime  # Import datetime for handling date and time

# Create a database connection using pymysql
conn = pymysql.connect(
    host='localhost',  # Database host (usually 'localhost' for a local MySQL server)
    port=3306,  # Port for MySQL server
    user='root',  # Username to connect to the database
    password='422322',  # Password for the database user
    database='calculator'  # Database name to connect to
)

# Create a Flask web application
app = Flask(__name__)

# Enable Cross-Origin Resource Sharing (CORS) for the Flask app
CORS(app)

# Create a cursor object for executing SQL queries on the database
cursor = conn.cursor()

# Define a route for the '/post_history' endpoint with a POST request method
@app.route('/post_history', methods=['POST'])
def post_history():  # Function for storing calculation expressions and results
    try:
        # Get JSON data from the POST request
        data = request.get_json()
        expression = data.get('expression')  # Extract 'expression' from the JSON data
        result = data.get('result')  # Extract 'result' from the JSON data

        # Get the current timestamp
        time = datetime.datetime.now()

        # Create a tuple containing the timestamp, expression, and result
        data = (time, expression, result)

        # Define an SQL INSERT statement
        insert = "INSERT INTO calculation VALUES (%s, %s, %s)"

        # Execute the SQL INSERT statement with the data
        cursor.execute(insert, data)

        # Commit the changes to the database
        conn.commit()

        # Prepare a success response message
        response_message = "ok"

        # Return a JSON response with the success message
        return jsonify({"message": response_message})

    except Exception as e:
        # If an exception occurs, capture the error message
        error_message = str(e)
        print(error_message)  # Print the error message to the console

        # Return a JSON response with the error message and HTTP status code 500 (Internal Server Error)
        return jsonify({"error": error_message}), 500

# Define a route for the '/get_calculation_data' endpoint with a GET request method
@app.route('/get_calculation_data', methods=['GET'])
def get_calculation_data():  # Function for retrieving historical data
    try:
        # Execute an SQL SELECT query to fetch the expression and result from the 'calculation' table
        # The data is ordered by time in descending order and limited to the top 10 records
        cursor.execute("SELECT expression, result FROM calculation ORDER BY time DESC LIMIT 10")

        # Fetch all the records as a list of tuples
        data = cursor.fetchall()

        # Return a JSON response containing the retrieved data
        return jsonify({"data": data})

    except Exception as e:
        # If an exception occurs, capture the error message
        error_message = str(e)

        # Return a JSON response with the error message and HTTP status code 500 (Internal Server Error)
        return jsonify({"error": error_message}), 500

# Define a route for the '/send_clear' endpoint with a POST request method
@app.route('/send_clear', methods=['POST'])
def send_clear():  # Function for clearing the database
    try:
        # Define an SQL DELETE statement to clear all records from the 'calculation' table
        insert = "DELETE FROM calculation"

        # Execute the SQL DELETE statement to clear the table
        cursor.execute(insert)

        # Commit the changes to the database
        conn.commit()

        # Prepare a success response message
        response_message = "ok"

        # Return a JSON response with the success message
        return jsonify({"message": response_message})

    except Exception as e:
        # If an exception occurs, capture the error message
        error_message = str(e)

        # Return a JSON response with the error message and HTTP status code 500 (Internal Server Error)
        return jsonify({"error": error_message}), 500

# Run the Flask application with debugging enabled
if __name__ == '__main__':
    app.run(debug=True)
