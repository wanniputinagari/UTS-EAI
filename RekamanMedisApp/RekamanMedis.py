from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from datetime import datetime

app = Flask(__name__)

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'medical_record_management'

mysql = MySQL(app)

def generate_response(status_code, message, data=None):
    response = {'status_code': status_code, 'message': message, 'timestamp': datetime.now().isoformat()}
    if data:
        response['data'] = data
    return jsonify(response), status_code

@app.route('/')
def root():
    return 'Welcome to Medical Records'

@app.route('/add_record', methods=['POST'])
def add_record():
    data = request.get_json()
    name = data['name']
    dob = data['dob']
    gender= data['gender']
    address = data['address']
    phone = data['phone']
    email = data['email']
    
    cursor = mysql.connection.cursor()
    sql = "INSERT INTO patients (name, dob, gender, address, phone, email) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (name, dob, gender, address, phone, email)
    cursor.execute(sql, val)
    mysql.connection.commit()
    cursor.close()

    return generate_response(201, 'Record added successfully')

@app.route('/medical_records', methods=['GET'])
def medical_records():
    if request.method == 'GET':
        # Get query parameters
        query_params = request.args.to_dict()

        # Constructing the query based on parameters
        query = "SELECT * FROM medical_history WHERE 1=1"
        params = []
        for key, value in query_params.items():
            query += f" AND {key} = %s"
            params.append(value)

        # Fetching data from the database
        cursor = mysql.connection.cursor()
        cursor.execute(query, tuple(params))
        column_names = [i[0] for i in cursor.description]
        data = [dict(zip(column_names, row)) for row in cursor.fetchall()]
        cursor.close()

        return generate_response(200, 'Medical records fetched successfully', data)
    
    else:
        return generate_response(400, 'data not provided')

@app.route('/detailrecords/')
def detailrecords():
    if 'id' in request.args:
        cursor = mysql.connection.cursor()
        sql = "SELECT * FROM medical_history WHERE patient_id = %s"
        val = (request.args['id'],)
        cursor.execute(sql, val)

        #get column names from cursor.decription
        column_names = [i[0] for i in cursor.description]

        #fetch data and format into list of dictionaries
        data = []
        for row in cursor.fetchall():
            data.append(dict(zip(column_names, row)))
            
        return jsonify(data)
        cursor.close()

@app.route('/update_record', methods=['PUT'])
def update_record():
    if 'id' in request.args:
        data = request.get_json()

        cursor = mysql.connection.cursor()
        sql = "UPDATE medical_history SET patient_id=%s, doctor_name=%s, visit_date=%s, diagnosis=%s, prescrription=%s WHERE history_id=%s"
        val = (data['patient_id'], data['doctor_name'], data['visit_date'], data['diagnosis'], data['prescrription'], request.args['id'])
        cursor.execute(sql, val)
        mysql.connection.commit()
        cursor.close()

        return generate_response(200, 'Record updated successfully')
    else:
        return generate_response(400, 'history ID not provided')

@app.route('/delete_record', methods=['DELETE'])
def delete_record():
    if 'id' in request.args:
        cursor = mysql.connection.cursor()
        sql = "DELETE FROM patients WHERE patient_id=%s"
        val = (request.args['id'],)
        cursor.execute(sql, val)
        mysql.connection.commit()
        cursor.close()

        return generate_response(200, 'Record deleted successfully')
    else:
        return generate_response(400, 'Patient ID is not provided')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)
