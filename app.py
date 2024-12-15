from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'some_secret_key'  # Required for flashing error messages

# MySQL connection setup
def create_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',  # replace with your MySQL username
        password='ROOT75',  # replace with your MySQL password
        database='my_flask_app_db'  # replace with your MySQL database name
    )

@app.route('/')
def home():
    return render_template('index.html')

# --- Flight Management ---
@app.route('/flights')
def flights():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM flights")
    flights = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('flights.html', flights=flights)

@app.route('/flight_details/<int:flight_id>', methods=['GET'])
def flight_details(flight_id):
    try:
        connection = create_connection()
        cursor = connection.cursor()
        
        # Call the MySQL function 'get_flight_details'
        cursor.execute("SELECT get_flight_details(%s)", (flight_id,))
        flight_details = cursor.fetchone()[0]
        
        cursor.close()
        connection.close()

        return jsonify({'flight_details': flight_details})
    except Error as e:
        return jsonify({'error': str(e)})
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred: ' + str(e)})

# --- Ticket Management ---
@app.route('/tickets')
def tickets():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM tickets")
    tickets = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('tickets.html', tickets=tickets)

@app.route('/add_ticket', methods=['POST'])
def add_ticket():
    passenger_name = request.form['passenger_name']
    flight_no = request.form['flight_no']
    seat_no = request.form['seat_no']
    price = request.form['price']

    try:
        # Ensure price is a float
        price = float(price)

        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO tickets (passenger_name, flight_no, seat_no, price) VALUES (%s, %s, %s, %s)",
                       (passenger_name, flight_no, seat_no, price))
        connection.commit()
        cursor.close()
        connection.close()

        flash("Ticket added successfully!", "success")
    except Error as e:
        flash(f"Error adding ticket: {str(e)}", "danger")
    except Exception as e:
        flash(f"An unexpected error occurred: {str(e)}", "danger")

    return redirect(url_for('tickets'))

# --- Customer Management ---
@app.route('/customers')
def customers():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM customers")
    customers = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('customers.html', customers=customers)

@app.route('/add_customer', methods=['POST'])
def add_customer():
    customer_name = request.form['customer_name']
    customer_email = request.form['customer_email']
    customer_phone = request.form['customer_phone']

    try:
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO customers (customer_name, customer_email, customer_phone) VALUES (%s, %s, %s)",
                       (customer_name, customer_email, customer_phone))
        connection.commit()
        cursor.close()
        connection.close()
        flash("Customer added successfully!", "success")
    except Error as e:
        flash(f"Error adding customer: {str(e)}", "danger")
    except Exception as e:
        flash(f"An unexpected error occurred: {str(e)}", "danger")

    return redirect(url_for('customers'))

# --- Call MySQL Stored Procedure to Get All Tickets ---
@app.route('/get_all_tickets', methods=['GET'])
def get_all_tickets():
    try:
        connection = create_connection()
        cursor = connection.cursor()

        # Call the stored procedure 'get_all_tickets'
        cursor.callproc('get_all_tickets')

        ticket_info_list = []
        for result in cursor.stored_results():
            ticket_info_list.extend(result.fetchall())

        cursor.close()
        connection.close()

        # Return the ticket information as JSON
        return jsonify({'tickets': ticket_info_list})
    except Error as e:
        return jsonify({'error': str(e)})
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred: ' + str(e)})


# --- Home Page Redirect ---
@app.route('/index')
def index():
    return redirect(url_for('flights'))

if __name__ == '__main__':
    app.run(debug=True)
