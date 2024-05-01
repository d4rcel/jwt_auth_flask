from flask import Flask, request, jsonify, make_response, render_template, session
import jwt
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = '1c3ad9f5ae786035019b4aea'


def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'Alert': 'Token is missing'})
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'Alert': 'Invalid Token:'})   
    return decorated


# Home


@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return 'Logged in currently'
    

# For Public    
    

@app.route('/public')
def public():
    return 'For Public'
    

# For Authenticated   


@app.route('/auth')
@token_required
def auth():
    return 'JWT is verififed. Welcome to your dashboaard!'


# Login


@app.route('/login', methods=['POST'])
def login():
    if request.form['username'] and request.form['password'] == '123456':
        session['logged_in'] = True
        token = jwt.encode({
            'user': request.form['username'],
            'expiration': str(datetime.utcnow() + timedelta(seconds=120))
        },
            app.config['SECRET_KEY'])
        return jsonify({'token': token})
    else:
        return make_response('Unable, to verify', 403, {'WWW-Authenticate': 'Basic realm:Authentification Failed!'})

if __name__ == '__main__':
    app.run(debug=True)