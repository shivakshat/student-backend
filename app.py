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
@app.route('/delete_task', methods=['POST'])
def delete_task():
    data = request.json
    username = data['username']
    task_to_delete = data['task']
    time_to_delete = data['time']

    filename = f"{username}.csv"

    updated_tasks = []

    # Read existing data
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if not (row['task'] == task_to_delete and row['time'] == time_to_delete):
                updated_tasks.append(row)

    # Write back remaining data
    with open(filename, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['task', 'time'])
        writer.writeheader()
        writer.writerows(updated_tasks)

    return jsonify({"message": "Task deleted successfully"})
