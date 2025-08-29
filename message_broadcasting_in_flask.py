import os
import smtplib
from email.mime.text import MIMEText

from dotenv import load_dotenv
from flask import Flask, jsonify, request

load_dotenv()

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return "Welcome to the Message Broadcasting Service!"


@app.route('/message_broadcasting_in_flask', methods=['POST'])
def message_broadcasting_in_flask():
    try:
        data = request.json
        subject = data.get('subject')
        html_content = data.get('html')
        recipients = data.get('recipients')

        sender_email = os.getenv('sender_email')
        sender_password = os.getenv('sender_password')

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            for recipient in recipients:
                msg = MIMEText(html_content, 'html')
                msg['Subject'] = subject
                msg['From'] = sender_email
                msg['To'] = recipient
                server.sendmail(sender_email, recipient, msg.as_string())
        return jsonify({"status": "success", "message": "Emails sent successfully"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True)