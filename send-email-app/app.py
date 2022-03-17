from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from flask import Flask, request, make_response, jsonify
import smtplib
import os
import json

from flask_cors import CORS

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app, resources={r"*": {"origins": "*"}})

my_email = os.environ.get('EMAIL')
password = os.environ.get('PASSWORD')


@app.route("/contact", methods=["POST"])
def contact():
    data = request.json

    msg = MIMEMultipart()
    msg['Subject'] = data['subject']
    msg['From'] = data['address']
    msg['To'] = os.environ.get("ADDRESS")
    msg.attach(MIMEText(data['message'], 'plain'))

    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(from_addr=data['address'],
                            to_addrs=os.environ.get("ADDRESS"),
                            msg=msg.as_string()
                            )

    response = make_response(
        jsonify(
            {"message": str("form send successfully")}
        )
    )
    response.headers["Content-Type"] = "application/json"
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


@app.route("/application", methods=["POST"])
def application():
    data = json.loads(request.form['json'])

    msg = MIMEMultipart()
    msg['Subject'] = data['subject']
    msg['From'] = data['address']
    msg['To'] = os.environ.get("ADDRESS")

    payload = MIMEBase('application', 'octate-stream', Name=request.files['file'].filename)
    payload.set_payload((request.files['file']).read())

    encoders.encode_base64(payload)

    payload.add_header('Content-Decomposition', 'attachment', filename=request.files['file'].filename)
    msg.attach(payload)
    msg.attach(MIMEText(data['message'], 'plain'))
    print("smtp")
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(from_addr=my_email,
                            to_addrs=os.environ.get("ADDRESS"),
                            msg=msg.as_string()
                            )
    response = make_response(
        jsonify(
            {"message": str("application send successfully")}
        )
    )

    return response


@app.route("/", methods=['POST', 'GET'])
def index():
    return {
        "status": "server is running"
    }


if __name__ == '__main__':
    app.run(debug=True)
