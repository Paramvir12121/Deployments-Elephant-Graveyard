from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from python_dotenv import read_dotenv

# Load environment variables from .env file


import os
import rollbar
import rollbar.contrib.flask
from flask import got_request_exception

app = Flask(__name__)
CORS(app)

# Configuration for SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///feedback.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
    

# Define the Feedback model
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    comment = db.Column(db.String(200), nullable=False)

# Route to submit feedback
@app.route('/feedback', methods=['POST'])
def submit_feedback():
    data = request.get_json()
    name = data.get('name')
    comment = data.get('comment')

    if not name or not comment:
        return jsonify({'error': 'Name and comment are required'}), 400

    new_feedback = Feedback(name=name, comment=comment)
    db.session.add(new_feedback)
    db.session.commit()

    return jsonify({'message': 'Feedback submitted successfully'}), 201

# Route to get all feedback
@app.route('/feedback', methods=['GET'])
def get_feedback():
    feedbacks = Feedback.query.all()
    feedback_list = [{'id': fb.id, 'name': fb.name, 'comment': fb.comment} for fb in feedbacks]
    return jsonify(feedback_list)

if __name__ == '__main__':
    # Ensure tables are created at startup
    with app.app_context():
        db.create_all()
        print("Tables created successfully!")
        """init rollbar module"""
        rollbar.init(
            # access token
            '',
            # environment name - any string, like 'production' or 'development'
            'flasktest',
            # server root directory, makes tracebacks prettier
        root=os.path.dirname(os.path.realpath(__file__)),
        # flask already sets up logging
        allow_logging_basic_config=False)

    # send exceptions from `app` to rollbar, using flask's signal system.
    got_request_exception.connect(rollbar.contrib.flask.report_exception, app)
    app.run(debug=True)
