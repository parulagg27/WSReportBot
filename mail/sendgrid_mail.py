#echo "export SENDGRID_API_KEY='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'" > sendgrid.env

import sendgrid
import os
from sendgrid.helpers.mail import *
import traceback


def send_mail(mail_subject, mail_body, to_email):
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("parulagg27@gmail.com")
    # to_email = Email("mehulkumarnirala@gmail.com")
    content = Content("text/html", mail_body)
    to_email = Email(to_email)
    # content = Content("text/plain", "and easy to do anywhere, even with Python")
    mail = Mail(from_email, mail_subject, to_email, content)
    try:
        response = sg.client.mail.send.post(request_body=mail.get())
        # sg.cl/ient.mail.send.post(request_body=mail.get())
        print(response.status_code)
        print(response.body)
        print(response.headers)
        return True
    except urllib.HTTPError:
        msg = "Got following error while sending mail :{}".format(traceback.format_exc())
        print(msg)
        return False

if __name__ == '__main__':
    subject = "Sending with SendGrid is Fun"
    body = "and easy to do anywhere, even with Python"
    to ="mehulkumarnirala@gmail.com"
    send_mail(subject,body,to)

