# app/routes.py
from flask import Blueprint, jsonify,request, render_template
from .db import get_db_connection

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('base.html')

@main.route('/about')
def about():
    return render_template('about.html')


@main.route('/api/data', methods=['GET'])
def get_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM data')
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(rows), 200

@main.route('/api/data', methods=['POST'])
def add_data():
    first_name = request.json.get('first_name')
    surname = request.json.get('surname')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO data (first_name, surname) VALUES (%s, %s)', (first_name,surname))
    conn.commit()
    cursor.close()
    conn.close()
    print('Data added')
    return jsonify({'message': 'Data added!'}), 201

@main.route('/api/data/<int:id>', methods=['PUT'])
def update_data(id):
    new_data = request.json  # Assuming JSON data is sent in the request body
    print("Received new data:", new_data)  # Debugging line to show new data

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if the record with the given id exists
    cursor.execute('SELECT first_name FROM data WHERE id = %s', (id,))
    record = cursor.fetchone()
    print("Fetched record:", record)  # Debugging line to show fetched data
    
    if record is None:
        cursor.close()
        conn.close()
        return jsonify({'message': 'No such record found.'}), 404

    # Extract the existing data from the record tuple
    existing_data = record[0]
    print("Existing data:", existing_data)  # Debugging line to show existing data

    # Check if the new data is the same as the existing data
    if existing_data == new_data['first_name']:
        print("No update needed; data is already the same.")  # Debug message
        cursor.close()
        conn.close()
        return jsonify({'message': 'No update needed; data is already the same.'}), 200

    # Update the data in the database if it is different
    cursor.execute('UPDATE data SET first_name = %s WHERE id = %s',
                   (new_data['first_name'], id))
    
    conn.commit()  # Commit the changes
    cursor.close()
    conn.close()

    print("Data updated successfully.")  # Debug message
    return jsonify({'message': 'Data updated successfully'}), 200

