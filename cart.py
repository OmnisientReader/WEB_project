# cart.py

from flask import Blueprint, render_template, session, redirect, url_for, request
from utils import get_db_connection

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/cart')
def cart():
    cart_items = session.get('cart', {})
    total_price = sum(item['price'] * item['quantity'] for item in cart_items.values())
    return render_template('cart.html', cart_items=cart_items, total_price=total_price)

@cart_bp.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    service_id = request.form.get('service_id')
    quantity = int(request.form.get('quantity', 1))
    if not service_id:
        return redirect(url_for('services.services'))
    
    conn = get_db_connection()
    if conn is None:
        # Handle the error appropriately, perhaps flash a message
        return redirect(url_for('services.services'))
    
    try:
        cur = conn.cursor()
        query = """
            SELECT service_id, service_name, img, service_description, price
            FROM public."services"
            WHERE service_id = %s
        """
        cur.execute(query, (service_id,))
        service = cur.fetchone()
        columns = [desc[0] for desc in cur.description] if service else []
        cur.close()
        conn.close()
        
        if not service:
            # Service not found, handle appropriately
            return redirect(url_for('services.services'))
        
        # Convert service to a dict
        service_dict = dict(zip(columns, service))
        
        cart = session.get('cart', {})
        if service_id in cart:
            cart[service_id]['quantity'] += quantity
        else:
            cart[service_id] = {
                'service_id': service_dict['service_id'],
                'service_name': service_dict['service_name'],
                'img': service_dict['img'],
                'service_description': service_dict['service_description'],
                'price': float(service_dict['price']),
                'quantity': quantity
            }
        session['cart'] = cart
        return redirect(url_for('services.services'))
        
    except Exception as e:
        print(f"Error adding to cart: {e}")
        return redirect(url_for('services.services'))

@cart_bp.route('/update_cart', methods=['POST'])
def update_cart():
    service_id = request.form.get('service_id')
    quantity = int(request.form.get('quantity', 1))
    if not service_id:
        return redirect(url_for('cart.cart'))
    
    cart = session.get('cart', {})
    if service_id in cart:
        if quantity > 0:
            cart[service_id]['quantity'] = quantity
        else:
            del cart[service_id]
        session['cart'] = cart
    return redirect(url_for('cart.cart'))

@cart_bp.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    service_id = request.form.get('service_id')
    if not service_id:
        return redirect(url_for('cart.cart'))
    
    cart = session.get('cart', {})
    if service_id in cart:
        del cart[service_id]
        session['cart'] = cart
    return redirect(url_for('cart.cart'))