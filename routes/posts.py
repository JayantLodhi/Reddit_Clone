
from flask import Blueprint, request, render_template, session, redirect, url_for
from models import create_post, get_all_posts, get_post, get_comments, upvote_post, downvote_post, get_posts_by_author, delete_post

posts_bp = Blueprint('posts', __name__, url_prefix='/posts')

@posts_bp.route('/feed')
def feed():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    posts = get_all_posts()
    posts.sort(key=lambda x: x['created_at'], reverse=True)
    for post in posts:
        post['comment_count'] = len(get_comments(str(post['_id'])))
        post['upvoted'] = session['user'] in post.get('upvotes', [])
        post['downvoted'] = session['user'] in post.get('downvotes', [])
    return render_template('feed.html', posts=posts)

@posts_bp.route('/create', methods=['GET', 'POST'])
def create():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        create_post(title, content, session['user'])
        return redirect(url_for('posts.feed'))
    return render_template('create_post.html')

@posts_bp.route('/<post_id>')
def post_detail(post_id):
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    post = get_post(post_id, session['user'])  
    comments = get_comments(post_id)
    return render_template('post_detail.html', post=post, comments=comments)

@posts_bp.route('/upvote/<post_id>', methods=['POST'])
def upvote(post_id):
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    upvote_post(post_id, session['user'])
    return redirect(request.referrer or url_for('posts.feed'))

@posts_bp.route('/downvote/<post_id>', methods=['POST'])
def downvote(post_id):
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    post = get_post(post_id)
    if not (post.get('votes', 0) <= 0 and session['user'] not in post.get('downvotes', [])):
        downvote_post(post_id, session['user'])
    
    return redirect(request.referrer or url_for('posts.feed'))

@posts_bp.route('/profile')
def profile():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    user_posts = get_posts_by_author(session['user'])
    user_posts.sort(key=lambda x: x['created_at'], reverse=True)
    for post in user_posts:
        post['comment_count'] = len(get_comments(str(post['_id'])))
        post['upvoted'] = session['user'] in post.get('upvotes', [])
        post['downvoted'] = session['user'] in post.get('downvotes', [])
    return render_template('profile.html', username=session['user'], user_posts=user_posts)

@posts_bp.route('/delete/<post_id>', methods=['POST'])
def delete(post_id):
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    if delete_post(post_id, session['user']):
        return redirect(url_for('posts.profile'))
    else:
        return "Unable to delete post", 403
