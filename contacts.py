from flask import Blueprint, render_template

contacts_bp = Blueprint('contacts', __name__)

@contacts_bp.route('/contacts')
def contacts():
    contacts_info = [
        {'department': 'Customer Support', 'phone': '+7 (000) 000-00-00', 'email': 'mail1@mail1'},
        {'department': 'Reception', 'phone': '+7 (000) 000-00-00', 'email': 'mail2@mail2'},
        {'department': 'Admin', 'phone': '+7 (000) 000-00-00', 'email': 'mail3@mail3'},
        {'department': 'Emergency', 'phone': '+7 (000) 000-00-00', 'email': 'mail4@mail4'},
    ]
    return render_template('contacts.html', contacts=contacts_info)