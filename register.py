from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
import bcrypt
from utils import get_db_connection

register_bp = Blueprint('register', __name__)

@register_bp.route('/registration')
def registration_form():
    return render_template('register.html')

@register_bp.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    password = request.form['password']

    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Insert data into the database
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO public."users" (name, phone, email, password) VALUES (%s, %s, %s, %s)',
            (name, phone, email, hashed_password)
        )
        conn.commit()
        cur.close()
        conn.close()
        flash('Registration successful!', 'success')
    except Exception as e:
        flash(f'Error: {e}', 'error')

    return redirect(url_for('register.registration_form'))