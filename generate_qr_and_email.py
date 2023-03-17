import qrcode
import smtplib
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import sqlite3

sender_email = 'your_email@gmail.com'
sender_password = 'your_password'

message_subject = 'Your QR code'
message_body = 'Here is your QR code:'

tickets = {}

data = pd.read_excel('file.xlsx')

for index, row in data.iterrows():
    tickets[row['id']] = row['email']

for id in tickets:
    # Create the QR code image
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data('http://127.0.0.1:5000/check_ticket?id={}'.format(id))
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    
    # Create the email message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = tickets[id]
    message['Subject'] = message_subject
    
    # Add the message body
    message.attach(MIMEText(message_body))
    
    # Add the QR code image as an attachment
    qr_code = MIMEImage(img_byte_arr)
    qr_code.add_header('ID', '<{}>'.format(id))
    message.attach(qr_code)
    
    # Connect to the SMTP server and send the email
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, tickets[id], message.as_string())

    conn = sqlite3.connect('tickets.db')

    conn.execute('''INSERT INTO tickets
                    VALUES ({}, 'unused');'''.format(id))
    
    conn.commit()
    conn.close()