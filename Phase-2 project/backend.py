from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__, static_folder='C:\\Users\\neeharika\\Documents\\Phase-2 project')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\neeharika\\Documents\\Phase-2 project\\login.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email

def initialize_database():
    with app.app_context():
        db.create_all()
        if not User.query.all():
            example_credentials = [
                {'email': 'ntelap@gitam.in', 'password': 'Neeha2828'},
                {'email': 'shruthy@gitam.in', 'password': 'Shruthy0707'},
                {'email': 'nsam@gitam.in', 'password': 'sam0909'},
                {'email': 'shash@gitam.in', 'password': 'Shash0606'},
                {'email': 'kusubu@gitam.in', 'password': 'Kusu13224'}
            ]
            for cred in example_credentials:
                user = User(email=cred['email'], password=generate_password_hash(cred['password']))
                db.session.add(user)
            db.session.commit()

initialize_database()

@app.route('/')
def home():
    return render_template('Frontend.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

@app.route('/submit_login', methods=['POST'])
def submit_login():
    email = request.form.get('uname')
    password = request.form.get('psw')
    
    if not email or not password:
        return jsonify({'status': 'error', 'message': 'Email or password cannot be empty'})

    user = User.query.filter_by(email=email).first()
    
    if user:
        if check_password_hash(user.password, password):
            print("Login successful for user:", user.email)
            return jsonify({'status': 'success'})
        else:
            print("Incorrect password for user:", user.email)
            return jsonify({'status': 'error', 'message': 'Incorrect password'})
    else:
        print("User not found:", email)
        return jsonify({'status': 'error', 'message': 'User not found'})

if __name__ == '__main__':
    app.run(debug=True)
