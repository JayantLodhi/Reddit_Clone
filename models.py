from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash

client = MongoClient("link")
db = client['RedditClone']

users_col = db['users']
posts_col = db['posts']
comments_col = db['comments']

def get_user_by_username(username):
    user = users_col.find_one({"username": username})
    if user:
        user['is_admin'] = user.get('is_admin', False)
    return user

def create_user(username, password):
    users_col.insert_one({
        "username": username,
        "password": password,
        "created_at": datetime.now(timezone.utc)
    })

def ensure_admin_exists():
    admin = users_col.find_one({"username": "admin_username"})
    if not admin:
        users_col.insert_one({
            "username": "admin_rc",
            "password": generate_password_hash("admin_password"),
            "created_at": datetime.now(timezone.utc),
            "is_admin": True
        })

ensure_admin_exists()

def get_all_users():
    return list(users_col.find({}, {'password': 0}))

def delete_user(username):
    result = users_col.delete_one({"username": username})
    if result.deleted_count > 0:
        posts_col.delete_many({"author": username})
        comments_col.delete_many({"author": username})
        return True
    return False

def create_post(title, content, author):
    posts_col.insert_one({
        "title": title,
        "content": content,
        "author": author,
        "created_at": datetime.now(timezone.utc),
        "votes": 0,
        "upvotes": [],
        "downvotes": []
    })

def get_all_posts():
    return list(posts_col.find())

def get_post(post_id, username=None):
    post = posts_col.find_one({"_id": ObjectId(post_id)})
    if post and username:
        post['upvoted'] = username in post.get('upvotes', [])
        post['downvoted'] = username in post.get('downvotes', [])
    return post

def add_comment(post_id, author, text):
    comments_col.insert_one({
        "post_id": ObjectId(post_id),
        "author": author,
        "text": text,
        "created_at": datetime.now(timezone.utc),
        "votes": 0
    })

def get_comments(post_id):
    return list(comments_col.find({"post_id": ObjectId(post_id)}))

def upvote_post(post_id, username):
    post = posts_col.find_one({"_id": ObjectId(post_id)})
    if not post:
        return

    if username in post.get("upvotes", []):
        # Remove upvote: 10 → 9
        posts_col.update_one(
            {"_id": ObjectId(post_id)},
            {"$inc": {"votes": -1}, "$pull": {"upvotes": username}}
        )
    elif username in post.get("downvotes", []):
        # Switch from downvote to upvote: 10 → 11 (+2)
        posts_col.update_one(
            {"_id": ObjectId(post_id)},
            {
                "$inc": {"votes": 2},
                "$pull": {"downvotes": username},
                "$addToSet": {"upvotes": username}
            }
        )
    else:
        # Add new upvote: 10 → 11
        posts_col.update_one(
            {"_id": ObjectId(post_id)},
            {"$inc": {"votes": 1}, "$addToSet": {"upvotes": username}}
        )

def downvote_post(post_id, username):
    post = posts_col.find_one({"_id": ObjectId(post_id)})
    if not post:
        return

    # Prevent downvote if votes are 0 and user hasn't already downvoted
    if post.get("votes", 0) <= 0 and username not in post.get("downvotes", []):
        return

    if username in post.get("downvotes", []):
        # Remove downvote: 10 → 11
        posts_col.update_one(
            {"_id": ObjectId(post_id)},
            {"$inc": {"votes": 1}, "$pull": {"downvotes": username}}
        )
    elif username in post.get("upvotes", []):
        # Switch from upvote to downvote: 10 → 9 (-2)
        posts_col.update_one(
            {"_id": ObjectId(post_id)},
            {
                "$inc": {"votes": -2},
                "$pull": {"upvotes": username},
                "$addToSet": {"downvotes": username}
            }
        )
    else:
        # Add new downvote: 10 → 9
        posts_col.update_one(
            {"_id": ObjectId(post_id)},
            {"$inc": {"votes": -1}, "$addToSet": {"downvotes": username}}
        )

def get_posts_by_author(author):
    posts = list(posts_col.find({"author": author}))
    for post in posts:
        post['upvotes'] = post.get('upvotes', [])
        post['downvotes'] = post.get('downvotes', [])
    return posts

def delete_post(post_id, username):
    post = posts_col.find_one({"_id": ObjectId(post_id)})
    if post and (post['author'] == username or get_user_by_username(username).get('is_admin', False)):
        posts_col.delete_one({"_id": ObjectId(post_id)})
        comments_col.delete_many({"post_id": ObjectId(post_id)})
        return True
    return False