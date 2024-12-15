from flask import Flask
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Database configuration
db_config = {
    'user': 'root',         # Replace with your MySQL username
    'password': 'ROOT75',      # Replace with your MySQL password
    'host': 'localhost',              # Usually localhost
    'database': 'my_flask_app_db'  # Replace with your database name
}

@app.route('/')
def check_connection():
    connection = None  # Initialize the connection variable
    try:
        # Attempt to connect to the database
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            return "Connection to MySQL database was successful!"
    except Error as e:
        return f"Error while connecting to MySQL: {e}"
    finally:
        # Close the connection if it was established
        if connection and connection.is_connected():
            connection.close()

if __name__ == '__main__':
    app.run(debug=True)
