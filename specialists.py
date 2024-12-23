from flask import Blueprint, render_template
from utils import get_db_connection

specialists_bp = Blueprint('specialists', __name__)

def fetch_specialists():
    conn = get_db_connection()

    id = None
    name = None
    img = None
    description = None

    if conn is None:
        return []
    try:
        cur = conn.cursor()
        cur.execute('SELECT * FROM public."specialists"')
        doctors = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        doctors_dict = [dict(zip(columns, doctor)) for doctor in doctors]
        cur.close()
        conn.close()
        print(doctors_dict)
        return doctors_dict
    
    except Exception as e:
        print(f"Error fetching doctors: {e}")
        return []

@specialists_bp.route('/specialists')
def specialists():
    specialists_data = fetch_specialists()
    return render_template('specialists.html', specialists=specialists_data)