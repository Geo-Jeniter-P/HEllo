from flask import Flask, request, jsonify, render_template, url_for
from flask_mail import Mail, Message
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL')

mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_email', methods=['POST'])
def send_email():
    if request.method == 'POST':
        try:
            name = request.form['name']
            email = request.form['email']
            subject = request.form['subject']
            message_body = request.form['message']

            msg = Message(
                subject=f"New Portfolio Contact: {subject} from {name}",
                sender=app.config['MAIL_DEFAULT_SENDER'],
                recipients=[RECIPIENT_EMAIL]
            )
            msg.body = f"""
You have a new message from your portfolio website:

Name: {name}
Email: {email}
Subject: {subject}

Message:
{message_body}
"""
            mail.send(msg)

            return jsonify({'success': True, 'message': 'Message sent successfully! Thank you.'}), 200

        except Exception as e:
            print(f"Error sending email: {e}")
            return jsonify({'success': False, 'message': f'Failed to send message. Please try again later. Error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)