from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
import os

app = Flask(__name__)

# Enable CORS
CORS(app, resources={r"/*": {"origins": "*"}})

# 🔹 Create CSV if not exists (with header)
if not os.path.exists("data.csv"):
    with open("data.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["username", "task", "time"])

@app.route('/')
def home():
    return "Backend Running"

# 🔹 ADD TASK
@app.route('/add_task', methods=['POST'])
def add_task():
    data = request.json

    with open("data.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([data['username'], data['task'], data['time']])

    return jsonify({"message": "Task saved successfully"})

# 🔹 GET TASKS
@app.route('/get_tasks/<username>')
def get_tasks(username):
    tasks = []

    try:
        with open("data.csv", "r") as f:
            reader = csv.reader(f)
            next(reader)  # skip header

            for row in reader:
                if row[0] == username:
                    tasks.append({
                        "task": row[1],
                        "time": row[2]
                    })
    except:
        pass

    return jsonify(tasks)

# 🔹 DELETE TASK
@app.route('/delete_task', methods=['POST'])
def delete_task():
    data = request.json
    username = data['username']
    task_to_delete = data['task']
    time_to_delete = data['time']

    updated_tasks = []

    # Read existing data
    with open("data.csv", "r") as file:
        reader = csv.reader(file)
        header = next(reader)

        for row in reader:
            # Keep rows NOT matching delete condition
            if not (row[0] == username and row[1] == task_to_delete and row[2] == time_to_delete):
                updated_tasks.append(row)

    # Write updated data back
    with open("data.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(updated_tasks)

    return jsonify({"message": "Task deleted successfully"})

if __name__ == "__main__":
    app.run()
