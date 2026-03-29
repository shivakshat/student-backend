from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
import os

app = Flask(__name__)

# ✅ THIS LINE IS CRITICAL
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def home():
    return "Backend Running"

@app.route('/add_task', methods=['POST'])
def add_task():
    data = request.json

    with open("data.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([data['username'], data['task'], data['time']])

    return jsonify({"message": "Task saved successfully"})

@app.route('/get_tasks/<username>')
def get_tasks(username):
    tasks = []

    try:
        with open("data.csv", "r") as f:
            reader = csv.reader(f)
            next(reader)

            for row in reader:
                if row[0] == username:
                    tasks.append({
                        "task": row[1],
                        "time": row[2]
                    })
    except:
        pass

    return jsonify(tasks)
