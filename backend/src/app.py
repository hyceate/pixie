from flask import Flask, request, jsonify, session
from flask_migrate import Migrate
from ariadne import graphql_sync
from ariadne.explorer import ExplorerGraphiQL
from ariadne.asgi import GraphQL
from asgiref.wsgi import WsgiToAsgi
from dotenv import load_dotenv
from db import db
from sql_models.user import User
from gql.schema import schema
import os

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.secret_key = os.getenv('SECRET_KEY', 'your_secret_key')
db.init_app(app)
migrate = Migrate(app, db)
schema = schema

explorer_html = ExplorerGraphiQL().html(None)

@app.route('/')
def home():
    return "Hello from Flask!"

@app.route("/graphql", methods=["GET"])
def graphql_explorer():
    return explorer_html, 200

@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(
        schema,
        data.get('query'),
        context_value={"request": request},
        debug=app.debug
    )
    status_code = 200 if success else 400
    return jsonify(result), status_code

# Wrap the Flask app with WsgiToAsgi to make it ASGI-compatible
asgi_app = WsgiToAsgi(app)
# Create Ariadne GraphQL app with Playground enabled
graphql_app = GraphQL(schema, debug=True)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'username and password required'}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'user already exists'}), 400
    
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error':'username and password required'}), 400
    
    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    session['user_id'] = user.id
    return jsonify({'message': 'login successful'}), 200

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({"message": "Logout successful"}), 200

if __name__ == '__main__':
    port = int(os.getenv('PORT', 3000))
    app.run(host='0.0.0.0', port=port)
