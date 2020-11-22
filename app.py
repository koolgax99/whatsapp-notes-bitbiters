from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from datetime import datetime
from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://rsmzlhyxcgokna:7888f898f4ca6cf9ded4ced4749198d58622f1049250d7e012e35966c6836a47@ec2-54-156-85-145.compute-1.amazonaws.com:5432/derh9045bmvb8c'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


def isWordPresent(sentence, word):
    s = sentence.split(" ")
    for i in s:
        if (i == word):
            return True
    return False


db = SQLAlchemy(app)


class Note(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text())
    number = db.Column(db.String)

    def __init__(self, message, number):
        self.message = message
        self.number = number


@app.route("/")
def hello():
    return render_template("/index.html")


@app.route("/sms", methods=['POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    msg = request.form.get('Body')
    phone = request.form.get('From')

    # Create reply
    resp = MessagingResponse()
    resp.message("Did you just say:{} ".format(msg))

    print(msg)
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    word = "#note"

    if (isWordPresent(msg, word)):
        msg = msg.replace("#note", '')
        message = msg
        number = phone
        data = Note(message, number)
        db.session.add(data)
        db.session.commit()
        resp.message("Okay, I noted down your point.")
    else:
        print("No notes\n")

    return str(resp)


@app.route("/note", methods=['POST'])
def notes():
    number = request.form['number']
    phone = "whatsapp:+91" + str(number)
    notes = Note.query.filter_by(number=phone).all()
    print(notes)


    if notes is None:
        msg = "No notes found"
    else:
        for i in range(len(notes)):
            print(notes[i].message)
            msg = notes[i].message

    return render_template("/note.html",  notes = notes)


if __name__ == "__main__":
    app.run(debug=True)
