# profile.py

from flask import Blueprint, render_template, session, redirect, url_for, flash
from utils import get_db_connection

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile')
def profile():
    if 'user_id' not in session:
        flash('Please log in to access your profile.', 'error')
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    conn = get_db_connection()
    if conn is None:
        flash('Database connection error.', 'error')
        return redirect(url_for('auth.login'))

    try:
        cur = conn.cursor()
        cur.execute('SELECT name, email, phone FROM public."users" WHERE user_id = %s', (user_id,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user is None:
            flash('User not found.', 'error')
            return redirect(url_for('auth.login'))

        user_info = {
            'username': user[0],
            'email': user[1],
            'phone': user[2],
            'avatar_url': '/static/default-avatar.png'
        }

        return render_template('profile.html', user=user_info)

    except Exception as e:
        print(f"Error fetching user profile: {e}")
        flash('An error occurred while fetching your profile.', 'error')
        return redirect(url_for('auth.login'))