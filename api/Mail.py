from google.appengine.api import mail


class MailService():
    def __init__(self, subject, sender, recipient, body):
        self.subject = subject
        self.sender = sender
        self.recipient = recipient
        self.body = body

    def send_mail(self):
        try:
            mail.send_mail(sender=self.sender,
                           to=self.recipient,
                           subject=self.subject,
                           body=self.body)
            return True
        except Exception as e:
            print e
            return False
