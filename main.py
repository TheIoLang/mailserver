from flask import Flask, request, redirect
from dill_tils.email import Email
from dill_tils.flask import is_human
import os

app = Flask(__name__)

@app.route('/send', methods=['POST'])
def send():
    name = request.form['name']
    email_address = request.form['email']
    topic = request.form['subject']
    message = request.form['message']
    captcha_response = request.form['g-recaptcha-response']

    subject = f'{topic} - IO Contact Form - {name}'

    email = f"""
Hi IO admins,
There has been a new entry in the contact form.


Name: {name}
Email: {email_address}
Topic: {topic}

Message: {message}

"""

    recipient_one = os.environ['RECIPIENT_ONE']
    recipient_two = os.environ['RECIPIENT_TWO']
    sender = os.environ['SENDER']
    password = os.environ['PASSWORD']

    if is_human(captcha_response, os.environ['RECAPTCHA_SECRET_KEY']):
    
        e1 = Email(recipient_one, sender, password)
        e2 = Email(recipient_two, sender, password)

        e1.send_email(subject, email)
        e2.send_email(subject, email)

    
        return redirect('https://theiolang.github.io/contact/sent')

    else:
        return redirect('https://theiolang.github.io/contact')

@app.route('/')
@app.route('/<a>')
def index(a: str = ''):
    return redirect('https://github.com/TheIoLang/mailserver')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
