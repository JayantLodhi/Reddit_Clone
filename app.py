
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from routes.auth import auth_bp
from routes.posts import posts_bp
from routes.comments import comments_bp
from routes.admin import admin_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key'
app.config['JWT_SECRET_KEY'] = 'my_jwt_secret_key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600

jwt = JWTManager(app)
CORS(app)

app.register_blueprint(auth_bp)
app.register_blueprint(posts_bp)
app.register_blueprint(comments_bp)
app.register_blueprint(admin_bp)

if __name__ == "__main__":
    app.run(debug=True)