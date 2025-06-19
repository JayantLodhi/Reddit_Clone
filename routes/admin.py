# Create new file admin.py
from flask import Blueprint, render_template, session, redirect, url_for, request
from models import get_all_users, delete_user, get_posts_by_author, get_comments
from functools import wraps

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin', False):
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/')
@admin_required
def dashboard():
    return redirect(url_for('admin.users'))

@admin_bp.route('/users')
@admin_required
def users():
    all_users = get_all_users()
    return render_template('admin_users.html', users=all_users)

@admin_bp.route('/delete_user/<username>', methods=['POST'])
@admin_required
def delete_user_route(username):
    if username == "admin_rc":
        return "Cannot delete admin", 403
    if delete_user(username):
        return redirect(url_for('admin.users'))
    return "Failed to delete user", 400

@admin_bp.route('/user_posts/<username>')
@admin_required
def user_posts(username):
    posts = get_posts_by_author(username)
    posts.sort(key=lambda x: x['created_at'], reverse=True)
    for post in posts:
        post['comment_count'] = len(get_comments(str(post['_id'])))
        # Add voting status for each post
        post['upvoted'] = session['user'] in post.get('upvotes', [])
        post['downvoted'] = session['user'] in post.get('downvotes', [])
    return render_template('admin_user_posts.html', username=username, posts=posts)