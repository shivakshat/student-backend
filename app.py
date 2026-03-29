from flask import Flask, request, jsonify
import csv
import os

app = Flask(__name__)

# Create CSV if not exists
if not os.path.exists("data.csv"):
    with open("data.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["username", "task", "time"])

@app.route('/')
def home():
    return "Backend Running"

@app.route('/add_task', methods=['POST'])
def add_task():
    data = request.json
    username = data['username']
    task = data['task']
    time = data['time']

    with open("data.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([username, task, time])

    return jsonify({"message": "Task saved successfully"})

@app.route('/get_tasks/<username>')
def get_tasks(username):
    user_tasks = []

    with open("data.csv", "r") as f:
        reader = csv.reader(f)
        next(reader)

        for row in reader:
            if row[0] == username:
                user_tasks.append({
                    "task": row[1],
                    "time": row[2]
                })

    return jsonify(user_tasks)

if __name__ == "__main__":
    app.run()