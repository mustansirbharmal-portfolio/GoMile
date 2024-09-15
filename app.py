from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
from flask_session import Session
from werkzeug.utils import secure_filename
import secrets
import os

app = Flask(__name__)
CORS(app)

# Ensure a folder for uploaded images
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def generate_secret_key():
    return secrets.token_hex(16)  # Generates a 32-character hexadecimal string

# Configure session
app.config['SECRET_KEY'] = generate_secret_key()  # Change this to a secret key
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/GOMILE")
db = client['cab_booking_platform']
customer_collection = db['customers']
agency_collection = db['agency']
driver_collection = db['driver']

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/loginAgain')
def loginAgain():
     return render_template('login.html')


@app.route('/agency')
def agency():
    return render_template('Agency_Registration_Page.html')

@app.route('/driver')
def driver():
    return render_template('Driver_Registration_Page copy.html')

@app.route('/customer')
def customer():
    return render_template('Customer_Registration_Page copy.html')

@app.route('/customerHome')
def customerHome():
    if 'user' in session and session['role'] == 'customer':
        return render_template('customerHome.html')
    return redirect(url_for('home'))

@app.route('/agencyHome')
def agencyHome():
    if 'user' in session and session['role'] == 'agency':
        return render_template('agencyHome.html')
    return redirect(url_for('home'))

@app.route('/driverHome')
def driverHome():
    if 'user' in session and session['role'] == 'driver':
        return render_template('driverHome.html')
    return redirect(url_for('home'))

@app.route('/agencyCars')
def agencyCars():
    if 'user' in session and session['role'] == 'agency':
        return render_template('agencyCars.html')
    return redirect(url_for('loginAgain'))

@app.route('/login', methods=['POST'])
def loginIndividual():
    data = request.get_json()
    role = data.get('role')
    email = data.get('email')
    password = data.get('password')

    collection = None
    if role == 'customer':
        collection = customer_collection
        redirect_url = url_for('customerHome')
    elif role == 'driver':
        collection = driver_collection
        redirect_url = url_for('driverHome')
    elif role == 'agency':
        collection = agency_collection
        redirect_url = url_for('agencyHome')
    else:
        return jsonify({"success": False, "message": "Invalid role"})

    user = collection.find_one({'email': email})
    if user and check_password_hash(user['password'], password):
        session['user'] = email
        session['role'] = role
        return jsonify({"success": True, "redirect_url": redirect_url})
    else:
        return jsonify({"success": False, "message": "Invalid email or password"})



# Customer registration API
@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        city = data.get('city')
        address = data.get('address')
        password = generate_password_hash(data.get('password'))

        if customer_collection.find_one({"email": email}):
            return jsonify({"success": False, "message": "Email already exists, please choose another one."})

        customer_collection.insert_one({
            "name": name,
            "email": email,
            "phone": phone,
            "city": city,
            "address": address,
            "password": password
        })

        return redirect(url_for('home'))
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

# Agency registration API
@app.route('/registerAgency', methods=['POST'])
def registerAgency():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        city = data.get('city')
        address = data.get('address')
        password = generate_password_hash(data.get('password'))

        if agency_collection.find_one({"email": email}):
            return jsonify({"success": False, "message": "Email already exists, please choose another one."})

        agency_collection.insert_one({
            "name": name,
            "email": email,
            "phone": phone,
            "city": city,
            "address": address,
            "password": password
        })

        return jsonify({"success": True, "message": "Registration successful!"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

# Register Driver
@app.route('/registerDriver', methods=['POST'])
def registerDriver():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        city = data.get('city')
        address = data.get('address')
        password = generate_password_hash(data.get('password'))

        if driver_collection.find_one({"email": email}):
            return jsonify({"success": False, "message": "Email already exists, please choose another one."})

        driver_collection.insert_one({
            "name": name,
            "email": email,
            "phone": phone,
            "city": city,
            "address": address,
            "password": password
        })

        return jsonify({"success": True, "message": "Registration successful!"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})
    
@app.route('/addCar', methods=['POST'])
def addCar():
    try:
        if 'user' not in session or session['role'] != 'agency':
            return jsonify({"success": False, "message": "Unauthorized"}), 401

        # Retrieve form data
        car_name = request.form['carName']
        car_model = request.form['carModel']
        car_mode = request.form['carMode']
        car_price_ac = request.form['carPriceAc']
        car_price = request.form['carPrice']
        car_image = request.files['carImage']

        # Save the image to the upload folder
        filename = secure_filename(car_image.filename)
        car_image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        car_image.save(car_image_path)

        # Get the logged-in agency's email
        agency_email = session['user']

        # Insert car details into MongoDB
        agency_collection.update_one(
            {'email': agency_email},
            {'$push': {
                'cars': {
                    'name': car_name,
                    'model': car_model,
                    'mode': car_mode,
                    'price_ac': car_price_ac,
                    'price': car_price,
                    'image_url': f"/{car_image_path}"
                }
            }}
        )

        return jsonify({"success": True, "message": "Car added successfully!"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

@app.route('/getCars', methods=['GET'])
def getCars():
    if 'user' not in session or session['role'] != 'agency':
        return jsonify({"success": False, "message": "Unauthorized"}), 401

    # Get the logged-in agency's email
    agency_email = session['user']
    
    # Fetch the cars from the agency collection
    agency = agency_collection.find_one({'email': agency_email})
    cars = agency.get('cars', [])

    return jsonify({"success": True, "cars": cars})

    
@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('role', None)
    return redirect(url_for('loginAgain'))

if __name__ == '__main__':
    app.run(debug=True, port=5002)
