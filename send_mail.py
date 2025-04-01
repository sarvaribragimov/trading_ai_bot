import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time

# SMTP settings
smtp_server = 'smtp.gmail.com'  # Replace with the SMTP server of your email provider
smtp_port = 587  # Use the appropriate port (e.g., 587 for TLS, 465 for SSL)
smtp_username = 'deeorbeckbus@gmail.com'
smtp_password = 'awwqaqfcvpuxdxnu'

# Email content
sender_email = 'deeorbeckbus@gmail.com'
receiver_email = 'deeorback@gmail.com'
subject = 'AAPL, AAPL aksiyasi sotildi'
message = """What is Lorem Ipsum?
Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."""

# Create a MIME message
msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Subject'] = subject

# Attach the email message
msg.attach(MIMEText(message, 'plain'))

# Connect to the SMTP server
while True:

    try:
        smtp = smtplib.SMTP(smtp_server, smtp_port)
        smtp.starttls()  # Use TLS encryption (comment out if using SSL)
        smtp.login(smtp_username, smtp_password)

        # Send the email
        smtp.sendmail(sender_email, receiver_email, msg.as_string())

        print('Email sent successfully!')
    except Exception as e:
        print(f'Error: {str(e)}')
    finally:
        smtp.quit()  # Close the SMTP connection

    time.sleep(1)
