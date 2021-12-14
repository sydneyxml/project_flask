from email.mime.text import MIMEText
import smtplib

def send_email(email, bmi, average_bmi, count):
  from_email = ""   # Please input your own email address
  from_password = ""    # Please input your password
  to_email = email
  
  subject = "BMI data"
  message = "Hey there, your BMI is <strong>%s</strong>. Average BMI of all is <strong>%s</strong> and that is calculated out <strong>%s</strong> of people." % (bmi, average_bmi, count)

  msg = MIMEText(message, 'html')
  msg['Subject'] = subject
  msg['To'] = to_email
  msg['From'] = from_email

  gmail = smtplib.SMTP('smtp.gmail.com', 587)
  gmail.ehlo()
  gmail.starttls()
  gmail.login(from_email, from_password)
  gmail.send_message(msg)

