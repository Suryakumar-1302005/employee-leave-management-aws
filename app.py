from flask import Flask, render_template, request
from db import get_connection

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/apply', methods=['POST'])
def apply():
    name = request.form['name']
    days = request.form['days']

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO leaves (employee_name, leave_days) VALUES (%s, %s)",
        (name, days)
    )

    connection.commit()
    cursor.close()
    connection.close()

    return "Leave Applied Successfully"

if __name__ == "__main__":
    app.run(debug=True)