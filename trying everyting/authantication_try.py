from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_jwt_extended import JWTManager, create_access_token
from datetime import timedelta

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = "fdasgoniqher8913u2340235u0924je93jf02jf39fnjnw"  #random long string (dont know why it has to be long and random string)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)  #token expiry time 1 hour

jwt = JWTManager(app)

# dummy database instead of mangodb atlas just to try authentication
users = {
    "jayant": "lodhi123"
}

@app.route('/')   #homepage
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])   #login page handling get and post
def login():
    if request.method == 'POST':   #post
        username = request.form.get('username')
        password = request.form.get('password')

        if username in users and users[username] == password:
            access_token = create_access_token(identity=username)  #create token when authantication gets succesful
            return jsonify({"msg": "Login successful", "access_token": access_token})

        return jsonify({"msg": "Invalid credentials"}), 401

    return render_template('login_try.html')  #get

if __name__ == '__main__':
    app.run(debug=True)   #running in debug mode
