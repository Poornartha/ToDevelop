# Using : https://docs.python.org/3/library/smtplib.html,
# https://docs.python.org/3/library/email.compat32-message.html?highlight=attach#email.message.Message.attach

import smtplib

#Imports for the File Parsing ( Using email.MIME ):
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase

host = "smtp.gmail.com"
port = 587
username = "thomasmullerfc@gmail.com"
password = "poornartha"
recipients = "vidyasawantnmims@gmail.com"

# Adding and parsing an HTML File within the mail itself.
# Letting know of possible HTML file
the_msg = MIMEMultipart("alternative")
the_msg['Subject'] = "Testing"
the_msg['From'] = username
the_msg['To'] = "archits581@gmail.com"
plain_txt = "Ye Mail Aapko smtplib k dwara bheja gaya hai."
part_1 = MIMEText(plain_txt, 'plain')
the_msg.attach(part_1)

# Open the file you wish to send
filename = "puppies-cover.jpg"
attachment = open("puppies-cover.jpg", "rb")

#Define Type: Same for all
part_2 = MIMEBase('application', 'octet-stream')

# To change the payload into encoded form
part_2.set_payload(attachment.read())
encoders.encode_base64(part_2)
part_2.add_header('Content-Disposition', "attachment; filename= %s" % filename)
the_msg.attach(part_2)

#Send Mail:
email_conn = smtplib.SMTP(host, port)
email_conn.ehlo()
email_conn.starttls()
email_conn.login(username, password)
email_conn.sendmail(username, recipients, the_msg.as_string())
email_conn.quit()
