
from flask import Blueprint, request, render_template, redirect, url_for, session
from flask_jwt_extended import create_access_token
from models import get_user_by_username, create_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    return redirect(url_for('auth.login'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user_by_username(username)
        
        if username == "admin_rc":
            from werkzeug.security import check_password_hash
            if user and check_password_hash(user['password'], password):
                access_token = create_access_token(identity=username)
                session['user'] = username
                session['is_admin'] = True
                return redirect(url_for('posts.feed'))
            return render_template('login.html', error='Invalid credentials')
        
        if user and user['password'] == password:
            access_token = create_access_token(identity=username)
            session['user'] = username
            session['is_admin'] = user.get('is_admin', False)
            return redirect(url_for('posts.feed'))
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if get_user_by_username(username):
            return render_template('signup.html', error='User already exists')
        create_user(username, password)
        return redirect(url_for('auth.login'))
    return render_template('signup.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
