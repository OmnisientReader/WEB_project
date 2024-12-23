from flask import Flask, render_template, request, redirect, url_for, flash
from utils import get_db_connection
from auth import auth_bp
from specialists import specialists_bp
from register import register_bp
from contacts import contacts_bp
from reviews import reviews_bp
from services import services_bp
from cart import cart_bp
from uprofile import profile_bp

app = Flask(__name__)
app.secret_key = 'secret'


app.register_blueprint(cart_bp)
app.register_blueprint(services_bp)
app.register_blueprint(reviews_bp)
app.register_blueprint(contacts_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(specialists_bp)
app.register_blueprint(register_bp)
app.register_blueprint(profile_bp)
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)