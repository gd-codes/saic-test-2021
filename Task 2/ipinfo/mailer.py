
import smtplib
import os
import json
import argparse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.utils import formatdate


def send(receivers, body, content):

    message = MIMEMultipart()
    message['From'] = os.environ['IPLOG_SENDER_ADDR']
    message['To'] = ', '.join(receivers)
    message['Date'] = formatdate(localtime=True)
    message.attach(MIMEText(body, 'plain'))

    attachment = MIMEBase('text', 'json')
    with open(content, 'r') as logfile :
        c = logfile.read()
        attachment.set_payload(c)
        try :
            j = json.loads(c)
            ja, jt = j['address'], j['timestamp']
        except :
            ja, jt = '?', '?'
    message['Subject'] = f"IP scan of {ja} - {jt}"
    attachment.add_header('Content-Disposition', 
        f'attachment; filename={os.path.basename(content)}')
    message.attach(attachment)

    server = smtplib.SMTP(r'smtp.gmail.com:587')
    try :
        server.starttls()
        server.login(os.environ['IPLOG_SENDER_ADDR'], os.environ['IPLOG_SENDER_AUTH'])
        server.sendmail(os.environ['IPLOG_SENDER_ADDR'], receivers, message.as_string())
    finally :
        server.quit()


if __name__ == '__main__':

    pass