
from flask import Blueprint, request, redirect, session, url_for
from models import add_comment

comments_bp = Blueprint('comments', __name__, url_prefix='/comments')

@comments_bp.route('/add/<post_id>', methods=['POST'])
def add(post_id):
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    text = request.form['comment']
    add_comment(post_id, session['user'], text)
    return redirect(url_for('posts.post_detail', post_id=post_id))
