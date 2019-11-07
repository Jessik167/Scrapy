# -*- encoding: utf-8 -*-
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_mail(text_message):
    port = 587  # For starttls
    smtp_server = "outlook.office365.com"
    sender_email = "jguerrero@apdif.com.mx"
    receiver_email = "jguerrero@apdif.com.mx"
    password = '3M0r@le$11560'
    
    message = MIMEMultipart("alternative")
    message["Subject"] = "Inicio lectura de Archivo"
    message["From"] = sender_email
    message["To"] = receiver_email
    
    # Create the plain-text and HTML version of your message
    text = """\
    Hi,
    How are you?
    Real Python has many great tutorials:
    www.realpython.com"""
    html = """\
    <html>
      <body>
        <p>Hi,<br>
           How are you?<br>
           <a href="http://www.realpython.com">"""+text_message+"""</a> 
           has many great tutorials.
        </p>
      </body>
    </html>
    """
    
    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    
    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)
    
    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(sender_email, password)
            server.sendmail(
            sender_email, receiver_email, message.as_string()
        )
            
def error_mail(subject, text_message):
    port = 587  # For starttls
    smtp_server = "outlook.office365.com"
    sender_email = "jguerrero@apdif.com.mx"
    receiver_email = "jguerrero@apdif.com.mx"
    password = '3M0r@le$11560'
    
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email
    
    # Create the plain-text and HTML version of your message
    text = """\
    Hi,
    How are you?
    Real Python has many great tutorials:
    www.realpython.com"""
    html = """\
    <html>
      <body>
        <p>Hi,<br>
           How are you?<br>
           """+text_message+""" 
           has many great tutorials.
        </p>
      </body>
    </html>
    """
    
    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    
    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)
    
    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(sender_email, password)
            server.sendmail(
            sender_email, receiver_email, message.as_string()
        )