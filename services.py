from flask import Blueprint, render_template, request
from utils import get_db_connection

services_bp = Blueprint('services', __name__)

# services.py

def fetch_services(search_query=None):
    conn = get_db_connection()
    if conn is None:
        return []
    try:
        cur = conn.cursor()
        if search_query:
            query = """
            SELECT service_id, service_name, img, service_description, price
            FROM public."services"
            WHERE service_name ILIKE %s
            """
            cur.execute(query, ('%' + search_query + '%',))
        else:
            query = """
            SELECT service_id, service_name, img, service_description, price
            FROM public."services"
            """
            cur.execute(query)
        services = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        services_dict = [dict(zip(columns, service)) for service in services]
        cur.close()
        conn.close()
        return services_dict
    except Exception as e:
        print(f"Error fetching services: {e}")
        return []

@services_bp.route('/services')
def services():
    search_query = request.args.get('search', '')
    services_data = fetch_services(search_query)
    return render_template('services.html', services=services_data, search_query=search_query)