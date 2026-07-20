from flask import Flask, render_template, request
from db import get_connection
import boto3
import json

app = Flask(__name__)

lambda_client = boto3.client("lambda", region_name="ap-south-1")


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/apply', methods=['POST'])
def apply():

    name = request.form['name']
    days = int(request.form['days'])

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO leaves (employee_name, leave_days, status) VALUES (%s, %s, %s)",
        (name, days, "Submitted")
    )

    connection.commit()

    cursor.close()
    connection.close()

    # Invoke Lambda asynchronously
    lambda_client.invoke(
        FunctionName="EmployeLeave",
        InvocationType="Event",
        Payload=json.dumps({}).encode("utf-8")
    )

    return render_template("success.html")


if __name__ == "__main__":
    app.run(debug=True)