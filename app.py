from flask import Flask, render_template, request, redirect, url_for, jsonify 
from transformers import TFMarianMTModel, MarianTokenizer
# from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
# from flask_login import current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session
from flask_session import Session
from flask import request
import mysql.connector



app = Flask(__name__)

token = "<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>"  # Your Hugging Face token;
app.secret_key = 'super secret key'
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'WafulaNas23.'
app.config['MYSQL_DB'] = 'translation'
 
mysql = MySQL(app)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'  # Use filesystem-based session storage
Session(app)


# class User:
#     def __init__(self, username, password):
#         self.username = username
#         self.password_hash = generate_password_hash(password)

# Within the context of the Flask application
# with app.app_context():
#     # Create a MySQL cursor
#     cursor = mysql.connection.cursor()

# # Define function to create database tables
# def create_tables():
#     # Create User table
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS User (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             username VARCHAR(80) UNIQUE NOT NULL,
#             email VARCHAR(120) UNIQUE NOT NULL,
#             password_hash VARCHAR(128) NOT NULL
#         )
#     """)
#     mysql.connection.commit()

    # Other tables can be created similarly
    
# Call create_tables function to create tables
# create_tables()

def translate_kiswahili_to_english(text):
    model_name = "Helsinki-NLP/opus-mt-swc-en"
    tokenizer = MarianTokenizer.from_pretrained(model_name, revision="main", use_auth_token=token)
    model = TFMarianMTModel.from_pretrained(model_name, revision="main", use_auth_token=token)

    inputs = tokenizer.encode(text, return_tensors="tf")
    outputs = model.generate(inputs, max_length=128, num_beams=4, early_stopping=True)
    translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return translated_text

def translate_english_to_kiswahili(text):
    model_name = "Helsinki-NLP/opus-mt-en-sw"
    tokenizer = MarianTokenizer.from_pretrained(model_name, revision="main", use_auth_token=token)
    model = TFMarianMTModel.from_pretrained(model_name, revision="main", use_auth_token=token)

    inputs = tokenizer.encode(text, return_tensors="tf")
    outputs = model.generate(inputs, max_length=128, num_beams=4, early_stopping=True)
    translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return translated_text

# Sign-up route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return render_template('signup.html', error='Passwords do not match')

        # Create cursor
        cur = mysql.connection.cursor()

        # Check if username already exists
        cur.execute("SELECT * FROM User WHERE username = %s", (username,))
        user = cur.fetchone()

        if user:
            return render_template('signup.html', error='Username already exists')

        # Hash password
        # password = generate_password_hash(password)

        # Insert new user into database
        cur.execute("INSERT INTO User (username,email, password) VALUES (%s, %s,%s)", (username,email, password))
        mysql.connection.commit()
        cur.close()

        # Redirect to login page after successful sign-up
        return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor()  # Create cursor object
        cursor.execute('SELECT * FROM User WHERE username = %s AND password=%s', (username, password))  
        record = cursor.fetchone()  # Fetch the record
        if record:
            session['loggedin'] = True
            session['username'] = record[1]
            return redirect(url_for('dashboard'))
        else:
            msg = 'Incorrect username/password!Try again!'
    return render_template('login.html', msg=msg)


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html',username=session['username'])

@app.route('/usertranslation')
def usertranslation():
    return render_template('usertranslation.html',username=session['username'])


def insert_translation(user_id, source_language, target_language, input_text, translated_text):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO history (user_id, source_language, target_language, input_text, translated_text) VALUES (%s, %s, %s, %s, %s)",
            (user_id, source_language, target_language, input_text, translated_text)
        )
        mysql.connection.commit()
        cursor.close()
    except Exception as e:
        print("Error inserting translation into history table:", e)


@app.route('/profile')
def profile():
    return render_template('profile.html',username=session['username'])

@app.route('/history')
def history():
    return render_template('history.html',username=session['username'])

@app.route('/engkiuk')
def engkiuk():
    return render_template('eng_kiuk.html',username=session['username'])

@app.route('/engkisw')
def engkisw():
    # Fetch translations saved by the logged-in user from the database
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT h.input_text, h.translated_text FROM history h INNER JOIN user u ON h.user_id = u.id WHERE u.username = %s", (session['username'],))
    user_translations = cursor.fetchall()
    cursor.close()
    
    # Fetch English to Kiswahili translations from the database
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT input_text, translated_text FROM history WHERE source_language = 'English' AND target_language = 'Kiswahili'")
    eng_kisw_translations = cursor.fetchall()
    cursor.close()

    return render_template('eng_kisw.html', user_translations=user_translations, eng_kisw_translations=eng_kisw_translations, username=session['username'])

# @app.route('/update_profile', methods=['GET', 'POST'])
# def update_profile():
#     if request.method == 'POST':
#         username = request.form['username']
#         email = request.form['email']
#         password = request.form['password']
#         confirm_password = request.form['confirm_password']

#         if password != confirm_password:
#             return render_template('update_profile.html', error='Passwords do not match')

#         # Create cursor
#         cur = mysql.connection.cursor()

#         # Update user's profile
#         cur.execute("UPDATE User SET email = %s, password = %s WHERE username = %s", (email, password, username))
#         mysql.connection.commit()
#         cur.close()

#         # Redirect to profile page after successful update
#         return redirect(url_for('profile'))

#     return render_template('update_profile.html')


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

# Logout route
@app.route('/logout')
def logout():
    # Clear the session
    session.clear()
    return redirect(url_for('login'))

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/translation')
def translation():
    return render_template('translation.html')

@app.route("/translate", methods=["POST"])
def translate():
    data = request.get_json()
    input_text = data.get("text")
    direction = data.get("direction")

    source_language = "english" if direction == "kiswahili" else "kiswahili"
    target_language = "kiswahili" if direction == "kiswahili" else "english"

    # Perform translation
    if direction == "kiswahili":
        translated_text = translate_english_to_kiswahili(input_text)
    elif direction == "english":
        translated_text = translate_kiswahili_to_english(input_text)
    else:
        return jsonify({"error": "Unsupported translation direction"})

    return jsonify({"translation": translated_text})

@app.route("/save_translation", methods=["POST"])
def save_translation():
    # Get data from the request JSON
    data = request.json
    if not data or "input_text" not in data or "translated_text" not in data \
            or "source_language" not in data or "target_language" not in data:
        return jsonify({"error": "Missing required data fields"}), 400

    input_text = data["input_text"]
    translated_text = data["translated_text"]
    source_language = data["source_language"]
    target_language = data["target_language"]

    # Get the username from the session
    username = session.get("username")
    if not username:
        return jsonify({"error": "User not authenticated"}), 401

    # Fetch the user ID from the database based on the username
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id FROM user WHERE username = %s", (username,))
        user = cursor.fetchone()
        if not user:
            return jsonify({"error": "User not found"}), 404
        user_id = user["id"]
    except Exception as e:
        return jsonify({"error": f"Failed to fetch user ID: {str(e)}"}), 500
    finally:
        cursor.close()

    # Insert the translation into the history table
    try:
        insert_translation(user_id, source_language, target_language, input_text, translated_text)
        return jsonify({"message": "Translation saved successfully"}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to save translation: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
