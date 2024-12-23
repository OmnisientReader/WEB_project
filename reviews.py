from flask import Blueprint, render_template, request, redirect, url_for, flash
from utils import get_db_connection

reviews_bp = Blueprint('reviews', __name__)

def fetch_reviews():
    conn = get_db_connection()
    if conn is None:
        return []
    try:
        cur = conn.cursor()
        cur.execute('''
            SELECT r.review_id, r.user_id, r.review_text, u.name
            FROM public."reviews" r
            JOIN public."users" u ON r.user_id = u.user_id
        ''')
        reviews = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        reviews_dict = [dict(zip(columns, review)) for review in reviews]
        cur.close()
        conn.close()
        print(reviews_dict)
        return reviews_dict
    except Exception as e:
        print(f"Error fetching reviews: {e}")
        return []
    
@reviews_bp.route('/add_review', methods=['POST'])
def add_review():
    name = request.form['name']
    comment = request.form['comment']
    conn = get_db_connection()
    if conn is None:
        flash('Ошибка соединения с базой данных.')
        return redirect(url_for('reviews.reviews'))
    try:
        cur = conn.cursor()
        # Assuming user_id is obtained from the current user's session
        user_id = 1  # Replace with actual user ID retrieval logic
        cur.execute("""
            INSERT INTO public."reviews" (user_id, review_text)
            VALUES (%s, %s)
        """, (user_id, comment))
        conn.commit()
        cur.close()
        conn.close()
        flash('Комментарий успешно добавлен!')
    except Exception as e:
        print(f"Error adding review: {e}")
        flash('Ошибка при добавлении комментария.')
    return redirect(url_for('reviews.reviews'))

@reviews_bp.route('/reviews')
def reviews():
    reviews_data = fetch_reviews()
    return render_template('reviews.html', reviews=reviews_data)