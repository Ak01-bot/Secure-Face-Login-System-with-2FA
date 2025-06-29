# 🧠  Secure Face Login System With 2FA

A secure, user-friendly login system using **face recognition**, **passwords**, and **OTP-based 2FA**, built with **Flask** and **face_recognition** library.

---

## Features

✅ Face Registration via Webcam
✅ Face Detection and Encoding using `face_recognition`
✅ Password-based Login
✅ Face-based Login (Biometric Authentication)
✅ OTP Verification via Email (2-Factor Authentication)
✅ Secure Password Hashing with `werkzeug.security`
✅ SQLite Database for User Management
✅ Real-time Face Capture using HTML5 & JavaScript
✅ Clean UI with Bootstrap

---

## Tech Stack

- **Frontend**: HTML, CSS (Bootstrap), JavaScript (Webcam API)
- **Backend**: Python, Flask
- **Libraries**:
  - `face_recognition` – for face detection & encoding
  - `OpenCV (cv2)` – for webcam access
  - `Werkzeug` – for password hashing
  - `smtplib` – for sending OTP via Gmail
  - `Pillow (PIL)` – for image processing
- **Database**: SQLite3 (`users.db`)
- **Storage**: Encoded faces in `encodings.npy`, images in `static/registered_faces/`

---

## Project Structure

face_login_system/

├── app/

│   ├── static/

│   │   ├── css/

│   │   ├── face_recognition_1.webp

│   │   └── styles.css

│   ├── templates/

│   │   ├── login.html

│   │   ├── register.html

│   │   ├── otp.html

│   │   └── dashboard.html

│   ├── face_utils.py

│   └── routes.py

├── database/

│   ├── users.db

│   └── encodings.npy

├── scripts/

│   ├── check_encodings.py

│   ├── generate_mock_encodings.py

│   ├── init_db.py

│   └── create_db.py

├── static/registered_faces/

│   └── `<username>`.jpg

├── register_face.py

├── main.py

├── requirements.txt

└── README.md

---

## How It Works

1. **Registration**:

   - User enters name, DOB, gender, email, username, password.
   - Face is captured from webcam and saved to `static/registered_faces/`.
   - Face encoding is generated and stored in `encodings.npy`.
   - All info is stored in `users.db`.
2. **Login (Password Mode)**:

   - User enters username and password.
   - If credentials are valid → OTP is sent to email for verification.
3. **Login (Face Mode)**:

   - Captures face from webcam.
   - Compares with stored encodings.
   - If matched → OTP sent to email for final verification.

---

## Security Features

- Passwords are securely hashed using `generate_password_hash`.
- OTPs are sent using Gmail SMTP (with app password).
- Session-based authentication with Flask sessions.
- Face recognition via reliable encoding and comparison.

---

## Installation

1. Clone the repo:

   ```bash
   git clone https://github.com/your-username/face_login_system.git
   cd face_login_system
   ```
2. Create virtual environment:

   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install dependencies:

   pip install -r requirements.txt
4. Run the app:

   python main.py

   ## Dependencies

   Add the following to your `requirements.txt`:

   blinker==1.9.0

   click==8.1.8

   colorama==0.4.6

   dlib==19.24.8

   face-recognition==1.3.0

   face_recognition_models==0.3.0

   Flask==3.1.0

   importlib_metadata==8.6.1

   itsdangerous==2.2.0

   Jinja2==3.1.6

   MarkupSafe==3.0.2

   numpy==2.0.2

   opencv-python==4.11.0.86

   pillow==11.2.1

   Werkzeug==3.1.3

   zipp==3.21.0

   ## 📬 Email OTP Setup


   * Use Gmail SMTP.
   * Enable **"App Passwords"** in your Gmail security settings.
   * Store credentials securely in environment variables or in code (for testing):

     from_email = 'your-email@gmail.com'
     app_password = 'your-app-password'

## 📸 Sample Face Registration UI

Captures user's face directly from the webcam:

<video id="video" autoplay></video>
<canvas id="canvas" style="display:none;"></canvas>

## Status

✔️ Working prototype completed

✔️ Face login and OTP verified

✔️ Fully functional on localhost

## Future Improvements

* Add multiple face samples per user
* Use cloud storage or database blob for images
* Add login attempt logging
* Add profile image preview after registration
* Deploy on cloud with HTTPS

## Author

**Chorotiya Akash** – 2025

Built for academic + practical learning use.

## Snapshots

### 🔐 Login Page

![Login Page](images/login_Page.png "first pic")

### ✅ Registration View

![Registration View](images/registration_interface.png "second pic")

### 📩 OTP Verification

![OTP Verification](images/OTP_verification_page.png "third pic")

### ✅ Dashboard View

![Dashboard View](images/Dashboard_view.png "fourth pic")

## 📄 License

Made by Akash.

MIT License – use freely with attribution.
