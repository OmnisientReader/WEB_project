# auth.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
import bcrypt
from utils import get_db_connection

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login')
def login():
    return render_template('authorize.html')

@auth_bp.route('/login_submit', methods=['POST'])
def login_submit():
    # Check if the request is an AJAX request
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        flash('Invalid request format.', 'error')
        return redirect(url_for('auth.login'))

    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'success': False, 'message': 'Email and password are required.'}), 400

    conn = get_db_connection()
    if conn is None:
        flash('Database connection error.', 'error')
        return jsonify({'success': False, 'message': 'Database connection error.'}), 500

    try:
        cur = conn.cursor()
        cur.execute('SELECT * FROM public."users" WHERE email = %s', (email,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user is None:
            return jsonify({'success': False, 'message': 'Wrong email or password.'}), 401

        stored_password = user[4]

        # Handle different storage formats
        if isinstance(stored_password, str):
            stored_password = stored_password.encode('utf-8')

        # Remove possible hexadecimal encoding if applicable
        if stored_password.startswith(b'\\x'):
            stored_password = bytes.fromhex(stored_password.decode('utf-8').replace('\\x', ''))

        if bcrypt.checkpw(password.encode('utf-8'), stored_password):
            # Assuming the user table has an 'avatar_url' column
            user_avatar = user[5] if len(user) > 5 and user[5] else '/static/default-avatar.png'

            session['user_id'] = user[0]
            session['email'] = user[3]
            session['user_avatar'] = user_avatar 
            flash('Login successful.', 'success')
            return jsonify({
                'success': True,
                'message': 'Login successful.',
                'redirect_url': url_for('index')
            }), 200
        else:
            return jsonify({'success': False, 'message': 'Wrong email or password.'}), 401

    except Exception as e:
        print(f"Error during login: {e}")
        return jsonify({'success': False, 'message': 'An error occurred.'}), 500

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.login'))