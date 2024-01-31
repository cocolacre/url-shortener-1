from flask import Flask, request, redirect
from flask_sqlalchemy import SQLAlchemy
import string
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String, nullable=False)
    short_url = db.Column(db.String, unique=True, nullable=False)

    def __init__(self, original_url):
        self.original_url = original_url
        self.short_url = self.generate_short_link()

    def generate_short_link(self):
        characters = string.digits + string.ascii_letters
        short_url = ''.join(random.choice(characters) for _ in range(6))

        link = self.query.filter_by(short_url=short_url).first()

        if link:
            return self.generate_short_link()
        else:
            return short_url

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/<short_url>')
def redirect_to_url(short_url):
    link = URL.query.filter_by(short_url=short_url).first_or_404()
    return redirect(link.original_url)

@app.route('/')
def index():
    return 'Welcome to the URL Shortener'

@app.route('/add_url', methods=['POST'])
def add_url():
    original_url = request.form['url']
    link = URL(original_url)
    db.session.add(link)
    db.session.commit()
    return f'Short URL is: {link.short_url}'

if __name__ == '__main__':
    app.run(debug=True)
