from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# DB Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="tcet",
    database="bus_pass_"
)

cursor = db.cursor()

# Home Page (Form)
@app.route('/')
def form():
    return render_template('form.html')


# Submit Form
@app.route('/apply', methods=['POST'])
def apply():
    data = (
        request.form['name'],
        request.form['age'],
        request.form['gender'],
        request.form['phone'],
        request.form['email'],
        request.form['user_type'],
        request.form['source'],
        request.form['destination'],
        request.form['pass_type']
    )

    cursor.execute("""
        INSERT INTO Users(name, age, gender, phone, email, user_type)
        VALUES (%s,%s,%s,%s,%s,%s)
    """, data[:6])

    user_id = cursor.lastrowid

    cursor.execute("""
        INSERT INTO Routes(source, destination, distance, fare)
        VALUES (%s,%s,0,0)
    """, data[6:8])

    route_id = cursor.lastrowid

    cursor.execute("""
        INSERT INTO Passes(user_id, route_id, issue_date, expiry_date, pass_type, status)
        VALUES (%s,%s,CURDATE(), DATE_ADD(CURDATE(), INTERVAL 30 DAY), %s, 'active')
    """, (user_id, route_id, data[8]))

    db.commit()

    return render_template('success.html')


if __name__ == '__main__':
    app.run(debug=True)
