from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import json
import os
from pau.services import ai_engine

# Define Blueprint
auth_bp = Blueprint('auth', __name__, template_folder='templates')

# Path to user credentials file
USER_FILE = 'data/user.json'

def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, 'r') as file:
        return json.load(file)

def save_users(users):
    with open(USER_FILE, 'w') as file:
        json.dump(users, file, indent=4)

def login_checker(username, password):
    users = load_users()
    if username in users and users[username]['password'] == password:
        return True, "Login successful"
    return False, "Invalid username or password."

@auth_bp.route('/')
def home():
    return render_template('auth.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        users = load_users()

        if password != confirm_password:
            flash("Passwords do not match!", 'danger')
            return redirect(url_for('auth.register'))

        if username in users:
            flash("Username already taken!", 'danger')
            return redirect(url_for('auth.register'))

        users[username] = {"password": password}
        save_users(users)

        flash("Account created successfully! Please log in.", 'success')
        return redirect(url_for('auth.home'))

    return render_template('signup.html')  # ✅ Serve the signup page

@auth_bp.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    print(f"🔹 Received login request: {username} / {password}")  # Debug log

    success, message = login_checker(username, password)
    
    if success:
        session['user'] = username
        print(f"✅ Login successful for {username}")  # Debug log
        return redirect(url_for('auth.dashboard'))
    else:
        print(f"❌ Login failed for {username}: {message}")  # Debug log
        flash(message, 'danger')
        return redirect(url_for('auth.home'))

@auth_bp.route('/dashboard')
def dashboard():
    if 'user' not in session:
        flash("Please log in first.", 'warning')
        return redirect(url_for('auth.home'))
    
    return render_template("chat.html", username=session['user'])
    
@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        users = load_users()

        # Check if email exists in database
        if email in users:
            # Send password reset email
            flash(f"A password reset link has been sent to {email}", "success")
            return redirect(url_for('auth.home'))
        else:
            flash("Email not found. Please check and try again.", "danger")

    return render_template('forget_password.html')

@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    flash("Logged out successfully.", 'info')
    return redirect(url_for('auth.home'))