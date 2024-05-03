from flask import Flask, jsonify, render_template
import requests

app = Flask(__name__)

@app.route('/')
def index():
    # Sample data (replace this with actual data from your application)
    info = {
        'name': 'Medical Service Name',
        'patients_info': 'Information about patients',
        'records_info': 'Data records details'
    }
    return render_template('index.html', info=info)

# Layanan Konsultasi
def get_patients(patient_id):
    response = requests.get(f'http://localhost:3000/detailpatient/{patient_id}')
    return response.json()

# Layanan Pasien
def get_records(patient_id):
    response = requests.get(f'http://localhost:4000/detailrecords?id={patient_id}')
    return response.json()

@app.route('/patientrecords/<int:patient_id>')
def get_patient_info(patient_id):
    # Get layanan konsultasi
    patients_info = get_patients(patient_id)
    records_info = get_records(patient_id)

    return render_template('index.html', info=patients_info, records=records_info)

if __name__ == "__main__":
    app.run(debug=True, port=5004)