from flask import Flask, request, jsonify

app = Flask(__name__)

# Database of doctors
doctors = [
    {
        "id": 1,
        "name": "Dr. Gajanan",
        "specialty": "General medicine",
        "availability": [
            {
                "day": "Monday",
                "start_time": "17:00",
                "end_time": "20:00",
            },
            {
                "day": "Wednesday",
                "start_time": "17:00",
                "end_time": "20:00",
            },
            {
                "day": "Friday",
                "start_time": "17:00",
                "end_time": "20:00",
            },
        ],
    },
    {
        "id": 2,
        "name": "Dr. Rushikesh",
        "specialty": "Neurologist",
        "availability": [
            {
                "day": "Tuesday",
                "start_time": "17:00",
                "end_time": "20:00",
            },
            {
                "day": "Thursday",
                "start_time": "17:00",
                "end_time": "20:00",
            },
            {
                "day": "Saturday",
                "start_time": "17:00",
                "end_time": "20:00",
            },
        ],
    },
]
appointments=[]

# Get a list of all doctors
@app.route("/doctors", methods=["GET"])
def get_doctors():
    return jsonify(doctors)

# Get the details of a specific doctor
@app.route("/doctors/<int:doctor_id>", methods=["GET"])
def get_doctor(doctor_id):
    doctor = next((doctor for doctor in doctors if doctor["id"] == doctor_id), None)
    if doctor is None:
        return jsonify({"error": "Doctor not found"}), 404
    return jsonify(doctor)

# Book an appointment with a doctor
@app.route("/appointments", methods=["POST"])
def book_appointment():
    doctor_id = request.json.get("doctor_id")
    date = request.json.get("date")
    time = request.json.get("time")

    # Validate the doctor_id
    if doctor_id is None or doctor_id < 1 or doctor_id > len(doctors):
        return jsonify({"error": "Invalid doctor ID"}), 400

    # Find the doctor by ID
    doctor = next((d for d in doctors if d["id"] == doctor_id), None)
    if doctor is None:
        return jsonify({"error": "Doctor not found"}), 404

    # Check if the date is in the doctor's availability
    availability_on_date = next((availability for availability in doctor["availability"] if availability["day"] == date), None)
    if availability_on_date is None:
        return jsonify({"error": "Doctor not available on that date"}), 400

    # Check if the time slot is available
    if availability_on_date["start_time"] <= time <= availability_on_date["end_time"]:
        # Book the appointment
        appointment = {
            "doctor_id": doctor_id,
            "date": date,
            "time": time,
        }
        appointments.append(appointment)
        print(appointments)
        return jsonify(appointment), 201
    else:
        return jsonify({"error": "Time slot not available"}), 400


if __name__ == "__main__":
    app.run(debug=True)
