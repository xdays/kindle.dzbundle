# Dropzone Action Info
# Name: Kindle
# Description: Send book to Kindle
# Handles: Files
# Creator: xdays
# URL: https://xdays.me
# Events: Clicked, Dragged
# KeyModifiers: Command, Option, Control, Shift
# OptionsNIB: ExtendedLogin
# SkipConfig: No
# RunsSandboxed: Yes
# Version: 1.0
# MinDropzoneVersion: 3.5

import time
import smtplib
import os
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send(subject, sender, passwd, recipients, text='', html='', files=[]):
    # get server name from username
    mail_server = 'smtp.' + sender.split('@')[1]
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ';'.join(recipients)

    # Create the body of the message (a plain-text and an HTML version).
    text = text.encode('utf8')
    html = html.encode('utf8')

    # Record the MIME types of both parts - text/plain and text/html.
    text_part = MIMEText(text, 'plain')
    html_part = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(text_part)
    msg.attach(html_part)
    for file in files:
        with open(file, "rb") as f:
            file_part = MIMEApplication(f.read(), Name=os.path.basename(file))
        # After the file is closed
        file_part[
            'Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(
                file)
        msg.attach(file_part)

    try:
        s = smtplib.SMTP()
        s.connect(mail_server)
        s.login(sender, passwd)
        s.sendmail(sender, recipients, msg.as_string())
        s.close()
        return (True, None)
    except Exception as e:
        return (False, str(e))


def dragged():
    try:
        username = os.environ['username']
        password = os.environ['password']
        recipients = os.environ['remote_path'].split(',')
    except Exception as e:
        print(e)
        dz.error('Error', 'Please configure this action')
    rt = send("Here is my book", username, password, recipients, files=items)
    if rt[0] == True:
        dz.finish("All book are sent to Kindle successfully")
    else:
        dz.error('Error', rt[1])
    dz.url(False)