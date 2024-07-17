from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEM_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)

@app.route('/')
def home():
    return "Hello from Flask!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)