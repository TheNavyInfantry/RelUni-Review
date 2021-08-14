from reluni_review import mail, url_for
from flask_mail import Message
from reluni_review.config import Config


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender=Config.config['mail_sender'], #Change this with real one
                  recipients=[user.email_address])
    text = "To reset your password, visit the following link: " + url_for('users.reset_token', token=token, _external=True) \
           + "If you did not make this request then simply ignore this email and no changes will be made."

    msg.body = text

    mail.send(msg)
