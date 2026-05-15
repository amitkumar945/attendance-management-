from flask import Flask, render_template, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

# Replace with your MongoDB URI
app.config["MONGO_URI"] = "mongodb://localhost:27017/AttendanceDB"
mongo = PyMongo(app)

# --- Routes ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/attendance', methods=['GET', 'POST'])
def handle_attendance():
    if request.method == 'POST':
        data = request.json
        attendance_id = mongo.db.attendance.insert_one({
            "name": data['name'],
            "date": data['date'],
            "subject": data['subject'],
            "status": data['status']
        }).inserted_id
        return jsonify({"msg": "Record Added", "id": str(attendance_id)}), 201
    
    # GET: Retrieve all records
    records = list(mongo.db.attendance.find())
    for record in records:
        record['_id'] = str(record['_id'])
    return jsonify(records)

@app.route('/api/attendance/<id>', methods=['PUT', 'DELETE'])
def modify_attendance(id):
    if request.method == 'PUT':
        data = request.json
        mongo.db.attendance.update_one(
            {'_id': ObjectId(id)},
            {'$set': data}
        )
        return jsonify({"msg": "Updated successfully"})
    
    if request.method == 'DELETE':
        mongo.db.attendance.delete_one({'_id': ObjectId(id)})
        return jsonify({"msg": "Deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True)