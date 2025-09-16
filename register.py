from flask import *
import psycopg2
from flask_jwt_extended import JWTManager, create_access_token

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret-key"
jwt = JWTManager(app)

@app.route("/register", methods=['POST'])
def data():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    year_of_passing = data.get('year_of_passing')
    studying_year = data.get('studying_year')
    enter_password = data.get('password')
    confirm_password = data.get('password1')

    # Check for missing fields
    if not all([name, email, year_of_passing, studying_year, enter_password, confirm_password]):
        return "Missing required fields", 400

    if enter_password != confirm_password:
        return "Enter your correct password", 400
    else:
        conn = psycopg2.connect(
            dbname="ecommerce",
            user="postgres",
            password="Thamizh@123",
            host="localhost",
            port="5432"
        )
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO user1(name,email,year_of_passing,studying_year,enter_password,confirm_password) VALUES (%s, %s, %s, %s, %s, %s)",
            (name, email, year_of_passing, studying_year, enter_password, confirm_password)
        )
        conn.commit()
        cur.close()
        conn.close()
        return "User inserted successfully", 200

@app.route("/login", methods=['POST'])
def login():
    data=request.get_json()
    emails=data.get('email')
    password=data.get('password')
    if not emails or not password:
        return "Missing email or password", 400
    conn = psycopg2.connect(
        dbname="ecommerce",
        user="postgres",
        password="Thamizh@123",
        host="localhost",
        port="5432"
    )
    cur=conn.cursor()
    cur.execute("SELECT email,enter_password FROM user1 WHERE email=%s", (emails,))
    user=cur.fetchone()
    cur.close()
    conn.close()
    if user:
        email, enter_password=user
    else:
        return "user not found"

    if enter_password==password:
        access_token = create_access_token(identity=email)
        return jsonify({"message": "login successful", "access_token": access_token}), 200
    else:
        return "enter correct password"

if __name__ == "__main__":
    app.run(debug=True, port=5000)