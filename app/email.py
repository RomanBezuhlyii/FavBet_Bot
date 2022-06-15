from flask_mail import Message
from app import mail, app
from flask import render_template

def send_mail(subject, sender, recipients, text_body, html_body):
    msg = Message(subject=subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)

def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_mail('[MyWebsite] Восстановление пароля',
              sender=app.config['ADMINS'][0],
              recipients=[user.email],
              text_body='',
              html_body=render_template('password_reset_msg_tmp.html', user=user, token=token))