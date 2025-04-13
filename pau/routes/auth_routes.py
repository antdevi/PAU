from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from pau.models.models import db, User
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

#def save_users(users):
    #with open(USER_FILE, 'w') as file:
        #json.dump(users, file, indent=4)

#def login_checker(username, password):
    #users = load_users()
    #if username in users and check_password_hash(users[username]['password'], password):
        #return True, "Login successful"
    #return False, "Invalid username or password."

@auth_bp.route('/')
def home():
    return render_template('auth.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash("Passwords do not match!", 'danger')
            return redirect(url_for('auth.register'))

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already taken!", 'danger')
            return redirect(url_for('auth.register'))
        
        hashed_password = generate_password_hash(password, method = "pbkdf2:sha256", salt_length=16)
        new_user = User(username=username, password=hashed_password)
        
        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully! Please log in.", 'success')
        return redirect(url_for('auth.home'))

    return render_template('signup.html')  # ✅ Serve the signup page

@auth_bp.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    print(f"🔹 Received login request: {username} / {password}")  # Debug log

    user = User.query.filter_by(username=username).first()
    
    if user and check_password_hash(user.password, password):
        session['user'] = username
        print(f"Login Successful for {username}")  # Debug log
        return redirect(url_for('auth.dashboard'))
    else:
        print(f"Login Failed for {username}")  # Debug log
        flash("Invalid username or password.", 'danger')
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
        username = request.form['username']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        user = User.query.filter_by(username=username).first()
        if not user:
            flash("Username does not exist.", "danger")
            return redirect(url_for('auth.reset_password'))

        if new_password != confirm_password:
            flash("Passwords do not match!", "warning")
            return redirect(url_for('auth.reset_password'))
        
        # ✅ Hash the new password and update it in the DB
        user.password = generate_password_hash(new_password, method="pbkdf2:sha256", salt_length=16)
        db.session.commit()

        flash("Password has been reset. Please log in.", "success")
        return redirect(url_for('auth.home'))
    
    return render_template('forget_password.html')

@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    flash("Logged out successfully.", 'info')
    return redirect(url_for('auth.home'))