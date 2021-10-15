
import smtplib
import os
import json
import argparse
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.utils import formatdate

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def send(receivers, body, content_paths):

    message = MIMEMultipart()
    message['From'] = os.environ['IPLOG_SENDER_ADDR']
    message['To'] = ', '.join(receivers)
    message['Date'] = formatdate(localtime=True)
    sub = "IP scan of "
    message.attach(MIMEText(body, 'plain'))

    # Create message attachments and nice subject line
    if isinstance(content_paths, str):
        content_paths = [content_paths]
    for content in content_paths:
        attachment = MIMEBase('text', 'json')
        with open(content.strip(), 'r') as logfile :
            c = logfile.read()
            attachment.set_payload(c)
            try :
                j = json.loads(c)
                ja, jt = j['address'], j['timestamp']
                dt = datetime.datetime.fromisoformat(jt).strftime('%x %X')
            except :
                ja, dt = '?', '?'
        sub += f"{ja} - {dt}; "
        attachment.add_header('Content-Disposition', 
            f'attachment; filename={os.path.basename(content)}')
        message.attach(attachment)

    message['Subject'] = sub

    # Connect to Gmail & send
    server = smtplib.SMTP(r'smtp.gmail.com:587')
    try :
        server.starttls()
        server.login(os.environ['IPLOG_SENDER_ADDR'], os.environ['IPLOG_SENDER_AUTH'])
        server.sendmail(os.environ['IPLOG_SENDER_ADDR'], receivers, message.as_string())
    finally :
        server.quit()


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--to', type=str, nargs='*', help="Recipient addresses", default=[])
    parser.add_argument('-n', type=int, help="Number of last records to send", default=1)
    parser.add_argument('--body', type=str, help="Email body content", default="")
    args = parser.parse_args()

    if not os.path.isfile('.RECENT') :
        raise FileNotFoundError("Could not find the module's log file location")
    with open('.RECENT', 'r') as f :
        files = f.readlines()[::-1][:args.n]
    if args.to :
        send(args.to, args.body, files)
        print("Sent !...")
        