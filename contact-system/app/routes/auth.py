from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_mail import Message
from app import mongo, mail
import secrets
from bson import ObjectId

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = mongo.db.users.find_one({
            'username': username,
            'password': password
        })
        if user:
            session['user_id'] = str(user['_id'])
            flash('Login successful!', 'success')
            return redirect(url_for('auth.contact_form'))
        else:
            flash('Invalid username or password', 'error')
            return redirect(url_for('auth.login'))
    return render_template('auth/login.html')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username').strip()
        email = request.form.get('email').strip()
        password = request.form.get('password').strip()
        
        if not (username and email and password):
            flash('All fields are required!', 'error')
            return redirect(url_for('auth.register'))
        
        # Check if user already exists
        if mongo.db.users.find_one({'username': username}):
            flash('Username already exists! Please choose another.', 'error')
            return redirect(url_for('auth.register'))
        
        # Insert new user (for production, remember to hash the password)
        user = {
            'username': username,
            'email': email,
            'password': password
        }
        mongo.db.users.insert_one(user)
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html')


@bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = mongo.db.users.find_one({'email': email})
        if user:
            # Generate a secure token and store it in the user document.
            token = secrets.token_urlsafe(32)
            mongo.db.users.update_one({'email': email}, {'$set': {'reset_token': token}})
            # Build a password reset URL that points to the reset_password route
            reset_url = url_for('auth.reset_password', token=token, _external=True)
            try:
                msg = Message('Password Reset Request',
                                recipients=[email],
                                body=(f"To reset your password, click on the following link:\n\n"
                                    f"{reset_url}\n\n"
                                    "If you did not request this reset, please ignore this email."))
                mail.send(msg)
                flash('Password reset instructions have been sent to your email.', 'success')
            except Exception as e:
                flash(f'Failed to send email: {str(e)}', 'error')
        else:
            flash('No account found with that email address.', 'error')
        return redirect(url_for('auth.login'))
    return render_template('auth/forgot_password.html')

@bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    # Look for a user with this reset token
    user = mongo.db.users.find_one({'reset_token': token})
    if not user:
        flash('Invalid or expired reset token.', 'error')
        return redirect(url_for('auth.forgot_password'))
    if request.method == 'POST':
        new_password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        if new_password != confirm_password:
            flash('Passwords do not match!', 'error')
            return redirect(url_for('auth.reset_password', token=token))
        # Update the password (hash the password in production) and remove the reset token
        mongo.db.users.update_one(
            {'_id': user['_id']},
            {'$set': {'password': new_password}, '$unset': {'reset_token': ""}}
        )
        flash('Your password has been updated. Please log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', token=token)

@bp.route('/contact-form', methods=['GET', 'POST'])
def contact_form():
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('auth.login'))
    if request.method == 'POST':
        mobile = request.form.get('mobile')
        email = request.form.get('email')
        address = request.form.get('address')
        registration_number = request.form.get('registration_number')
        
        if not (mobile and email and address and registration_number):
            flash('All fields are required!', 'error')
            return redirect(url_for('auth.contact_form'))
        
        # Convert the session user_id (which is a string) to an ObjectId
        try:
            user_object_id = ObjectId(session['user_id'])
        except Exception:
            flash('Invalid user session. Please log in again.', 'error')
            return redirect(url_for('auth.login'))
        
        contact = {
            'mobile': mobile,
            'email': email,
            'address': address,
            'registration_number': registration_number,
            'user_id': user_object_id
        }
        mongo.db.contacts.insert_one(contact)
        flash('Contact added successfully!', 'success')
        return redirect(url_for('auth.search'))
    return render_template('auth/contact_form.html')

@bp.route('/search', methods=['GET'])
def search():
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('auth.login'))
    reg_number = request.args.get('registration_number')
    contact = None
    if reg_number:
        contact = mongo.db.contacts.find_one({'registration_number': reg_number})
    return render_template('auth/search.html', contact=contact)