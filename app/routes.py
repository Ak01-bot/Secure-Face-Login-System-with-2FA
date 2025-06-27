# app/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import cv2
import face_recognition
from werkzeug.security import generate_password_hash, check_password_hash
import numpy as np
import os
import sqlite3
import smtplib
import random
from PIL import Image
from io import BytesIO
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import uuid
import base64
from PIL import Image
from PIL import ImageEnhance
from io import BytesIO

main = Blueprint('main', __name__)  # only ONE blueprint!

@main.route('/')
def index():
    return render_template('login.html')

@main.route('/login', methods=['GET','POST'])
def login():
    
    username = request.form.get('username')
    password = request.form.get('password')

    # If username/password provided → Password Login flow
    if username and password:
        conn = sqlite3.connect('database/users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
        result = cursor.fetchone()
        conn.close()

        if result and check_password_hash(result[0], password):
            session['username'] = username
            flash('Login successful!', 'success')
            # After successful password login:
            session['username'] = username

            # 1. Generate OTP
            otp_code = str(random.randint(100000, 999999))
            session['otp_code'] = otp_code

            # 2. Get user email from DB
            conn = sqlite3.connect('database/users.db')
            cursor = conn.cursor()
            cursor.execute('SELECT email FROM users WHERE username = ?', (username,))
            user_email = cursor.fetchone()
            conn.close()

            if user_email:
                send_otp_email(user_email[0], otp_code)
                flash('OTP has been sent to your email.', 'info')
                return redirect(url_for('main.otp_verify'))
            else:
                flash('Email not found for user.', 'danger')
                return redirect(url_for('main.index'))  
        else:
            flash('Invalid username or password.', 'danger')
            return redirect(url_for('main.index'))
        
        
    # ---------- FACE LOGIN ----------
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    cam.release()

    if not ret:
        flash('Camera Error. Try again.', 'danger')
        return redirect(url_for('main.index'))

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    if not face_encodings:
        flash('No face detected. Try again.', 'danger')
        return redirect(url_for('main.index'))

    user_encoding = face_encodings[0]

    # Load known encodings
    known_data = np.load('database/encodings.npy', allow_pickle=True).item() 
    known_encodings = known_data['encodings']
    known_names = known_data['names']

    matches = face_recognition.compare_faces(known_encodings, user_encoding)
    face_distances = face_recognition.face_distance(known_encodings, user_encoding)

    if True in matches:
        index = face_distances.argmin()
        matched_username = known_names[index]

        session['username'] = matched_username
        flash(f'Welcome {matched_username}!', 'success')

        # Generate OTP
        otp_code = str(random.randint(100000, 999999))
        session['otp_code'] = otp_code

        # Get user email
        conn = sqlite3.connect('database/users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT email FROM users WHERE username = ?', (matched_username,))
        user_email = cursor.fetchone()
        conn.close()

        if user_email:
            send_otp_email(user_email[0], otp_code)
            flash('OTP has been sent to your email.', 'info')
            return redirect(url_for('main.otp_verify'))
        else:
            flash('Email not found for user.', 'danger')
            return redirect(url_for('main.index'))
    else:
        flash('Face not recognized.', 'danger')
        return redirect(url_for('main.index'))    
    
@main.route('/otp', methods=['GET', 'POST'])
def otp_verify():
    if request.method == 'POST':
        entered_otp = request.form.get('otp')

        if entered_otp == session.get('otp_code'):
            session.pop('otp_code', None)  # Remove OTP after successful login
            flash('OTP verified successfully!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid OTP. Please try again.', 'danger')
            return redirect(url_for('main.otp_verify'))

    return render_template('otp.html')
       
def send_otp_email(to_email, otp_code):
    from_email = 'your-email@gmail.com'
    app_password = 'your-app-password'  # <-- not your normal password!

    subject = 'Your OTP Code'
    body = f'Your OTP code is {otp_code}'

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(from_email, app_password)
            smtp.send_message(msg)
        print('Email sent successfully!')
    except Exception as e:
        print(f'Failed to send email: {e}')
        
@main.route('/dashboard')
def dashboard():
    if 'username' not in session:
        flash('Please log in to access the dashboard.', 'warning')
        return redirect(url_for('main.index'))
    return render_template('dashboard.html', username=session['username'])


# Logout route
@main.route('/logout')
def logout():
    session.pop('username', None)  # Remove username from session
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('main.index'))

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Collect form data
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        full_name = request.form['full_name']
        gender = request.form['gender']
        dob = request.form['dob']
        face_data = request.form.get('face_image') 
        print("Captured face image:", face_data[:100])  # Print first 100 chars
        print("Received form data:")
        print(f"Name: {full_name}, DOB: {dob}, Gender: {gender}, Email: {email}, Username: {username}")
        print(f"Password: {password[:10]}..., Face image length: {len(face_data) if face_data else 'None'}")
  
        # Process face image from browser
        if face_data:
            try:
                os.makedirs('database', exist_ok=True)
                image_data = face_data.split(',' )[1]
                image_bytes = base64.b64decode(image_data)
                image = Image.open(BytesIO(image_bytes))
                image_path = f'static/registered_faces/{username}.jpg'
                image.save(image_path)
                
                # Generate and save face encoding
                img = face_recognition.load_image_file(image_path)
                face_locations = face_recognition.face_locations(img)
                face_encodings = face_recognition.face_encodings(img, face_locations)
                
                 
                # Ensure face is detected
                if not face_encodings:
                    os.remove(image_path)  # Remove image if no face detected
                    flash("No face detected in the image. Please try again.", "danger")
                    return redirect(url_for('main.register'))

                encoding = face_encodings[0]  # Save the encoding for use later

                # Save encoding to encodings.npy
                if os.path.exists('database/encodings.npy'):
                    data = np.load('database/encodings.npy', allow_pickle=True).item()
                    data['encodings'].append(encoding)
                    data['names'].append(username)
                else:
                    data = {'encodings': [encoding], 'names': [username]}
                np.save('database/encodings.npy', data)
            
            except Exception as e:
                flash(f"Error handling face image: {e}", 'danger')
                return redirect(url_for('main.register'))
             
        # ---------- Step 2: Store user in database ----------
        try:
            conn = sqlite3.connect('database/users.db')
            print("Using DB path:", os.path.abspath("database/users.db"))

            cursor = conn.cursor()

            # Check if username already exists
            cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
            if cursor.fetchone():
                flash('Username already exists. Choose another one.', 'danger')
                return redirect(url_for('main.register'))

            # Check if email already exists
            cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
            if cursor.fetchone():
                flash('Email already registered. Try logging in or use a different email.', 'danger')
                return redirect(url_for('main.register'))

            # If all good, insert the user
            cursor.execute('''
                INSERT INTO users (full_name, dob, gender, email, username, password, face_image)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (full_name, dob, gender, email, username, generate_password_hash(password), face_data))

            conn.commit()
            print(" User successfully inserted.")
            flash('Registration successful!', 'success')
            return redirect(url_for("main.login"))  # Adjust blueprint if needed
        except Exception as e:
            print(" DB insertion error:", e)
            return "Database error occurred", 500

        except Exception as e:
            flash('Database error: ' + str(e), 'danger')
            return redirect(url_for('main.register'))
        finally:
            conn.close()


        #return redirect(url_for('main.index'))

    return render_template('register.html')
