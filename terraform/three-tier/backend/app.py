from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_cors import CORS
from dotenv import load_dotenv
import os
import rollbar
import rollbar.contrib.flask
from flask import got_request_exception
import logging
# Load environment variables from the .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s')

app.logger.info("Flask app started!")

rollbar.init(
            access_token=os.getenv('ROLLBAR_ACCESS_TOKEN'),  # Load Rollbar access token from .env
            environment=os.getenv('FLASK_ENV', 'development'),  # Default to development if not specified
            root=os.path.dirname(os.path.realpath(__file__)),
            allow_logging_basic_config=False
        )

# Configuration for SQLite database (from .env)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///feedback.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)




# Define the Feedback model
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    comment = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()
    print("Database tables created.")

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

@app.route('/cause-error')
def cause_error():
    # Intentionally raise an error to trigger Rollbar
    raise Exception("This is a test exception to trigger Rollbar!")

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
        print("Database tables created successfully.")
        # Send exceptions from `app` to Rollbar, using Flask's signal system
        got_request_exception.connect(rollbar.contrib.flask.report_exception, app)

    app.run(debug=True)
