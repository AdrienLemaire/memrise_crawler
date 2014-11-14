#!/usr/bin/env python
# -*- coding: utf-8 -*-

from email import Encoders
from email.Header import Header
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

from local_settings import *  # NOQA

FILE_JOINED = False
MAIL_TITLE = '[Memrise] Daily diff'


def sendMail(message, encoding='utf-8'):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = Header(MAIL_TITLE.encode(encoding), encoding)
    msg['From'] = SENDER
    msg['To'] = SENDER
    text = message
    msg.attach(MIMEText(text.encode(encoding), 'html', encoding))
    # Attach file if specified
    if FILE_JOINED:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(FILE_JOINED, 'rb').read())
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' %
            FILE_JOINED.split("/")[-1])
        msg.attach(part)
    s = smtplib.SMTP(HOST, PORT)
    s.starttls()
    s.login(SENDER, SENDER_PASSWORD)
    try:
        s.sendmail(SENDER, SENDER, msg.as_string())
    except:
        s.quit()
        return  '%s Failed to send mail' % (SENDER)

    s.quit()
    return '%s / mail sent !' % (SENDER)

if __name__ == '__main__':
    # Real email testing, for you to check your message formatting
    sendMail('Test', SENDER)
