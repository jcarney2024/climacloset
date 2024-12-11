import os  # Added import
from weakref import ref
from flask import Blueprint, render_template, redirect, url_for, request, flash, get_flashed_messages, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .models import User
from . import db, mail
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature

auth = Blueprint('auth', __name__)

# Configure the serializer
serializer = URLSafeTimedSerializer(os.environ.get('SECRET_KEY'))

@auth.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.profile'))    
    r = request.args.get('r')
    
    if r == 'signup':
        flash('Account created successfully. Please log in.', 'green')
    elif r == 'logout':
        flash('Logged out successfully.', 'green')
    elif r == 'timeout':
        flash('Session timed out. Please log in again.', 'blue')
        
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()
    
    next = request.args.get('next')

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.', 'red')
        return redirect(url_for('auth.login'))
    
    login_user(user, remember=remember)
    session.permanent = remember  # Set session.permanent based on 'remember'

    return redirect(next or url_for('main.profile'))

@auth.route('/signup')
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.profile'))
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    confirmation = request.form.get('confirmation')
    code = request.form.get('code')

    if code != 'test':
        flash('Invalid invite code.', 'red')
        return redirect(url_for('auth.signup'))
    
    if confirmation != password:
        flash('Passwords do not match.', 'red')
        return redirect(url_for('auth.signup'))

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash(f'Email address already exists. <a href="{url_for("auth.login", email=email)}">Sign in</a>', 'blue')
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='pbkdf2:sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    # con.close()
    return redirect(url_for('auth.login') + '?r=signup')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login') + '?r=logout')

@auth.route('/is_authenticated')
def is_authenticated():
    auth_status = current_user.is_authenticated
    session.modified = False  # Prevent session from being extended
    return jsonify({'authenticated': auth_status})

@auth.route('/forgot', methods=['GET', 'POST'])
def forgot():
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect(url_for('main.profile'))
        return render_template('forgot.html')
    else:
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            token = serializer.dumps(user.email, salt='password-reset-salt')
            reference = os.urandom(8).hex()
            msg = Message(
                subject='Reset Your Password!',
                sender='noreply@climacloset.com',
                recipients=[email]
            )
            msg.html = render_template('reset_password_email.html', user=user, token=token, reference=reference)
            try:
                mail.send(msg)
                flash('Password reset email sent.')
            except Exception as e:
                flash(f'Failed to send password reset email. {e}')
        else:
            flash('Email not found.', 'red')
        return redirect(url_for('auth.login'))

@auth.route('/reset_password/<token>')
def reset_password(token):
    try:
        email = serializer.loads(token, salt='password-reset-salt', max_age=3600)
    except (SignatureExpired, BadSignature):
        flash('The password reset link is invalid or has expired.', 'red')
        return redirect(url_for('auth.forgot'))
    return render_template('reset_password.html', token=token)
    
@auth.route('/reset_password/<token>', methods=['POST'])
def reset_password_post(token):
    try:
        email = serializer.loads(token, salt='password-reset-salt', max_age=3600)
    except (SignatureExpired, BadSignature):
        flash('The password reset link is invalid or has expired.', 'red')
        return redirect(url_for('auth.forgot'))
    
    password = request.form.get('password')
    confirmation = request.form.get('confirmation')
    
    if password != confirmation:
        flash('Passwords do not match.', 'red')
        return redirect(url_for('auth.reset_password', token=token))
    
    user = User.query.filter_by(email=email).first()
    if user:
        user.password = generate_password_hash(password, method='pbkdf2:sha256')
        db.session.commit()
        flash('Your password has been updated.', 'green')
        return redirect(url_for('auth.login'))
    else:
        flash('User not found.', 'red')
        return redirect(url_for('auth.forgot'))