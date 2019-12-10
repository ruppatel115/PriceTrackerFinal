import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# def main():
#     import smtplib
#
#     gmail_user = 'price.tracker2019@gmail.com'
#     gmail_password = 'ptpassword'
#
#     sent_from = gmail_user
#     to = ['ruppatel11599@gmail.com']
#     subject = 'Price Dropped'
#     body = 'Prices have dropped!'
#
#     email_text = """\
#     From: %s
#     To: %s
#     Subject: %s
#
#     %s
#     """ % (sent_from, ", ".join(to), subject, body)
#
#     try:
#         server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
#         server.ehlo()
#         server.login(gmail_user, gmail_password)
#         server.sendmail(sent_from, to, email_text)
#         server.close()
#
#         print('Email sent!')
#     except:
#         print('Something went wrong...')

def send_mail():
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()

        server.login('price.tracker2019@gmail.com', 'ptpassword')

        subject = 'Price dropped down!'

        msg = "Subject: {subject}\n\n{body}"

        server.sendmail(
            'price.tracker2019@gmail.com',
            'ruppatel11599@gmail.com',
            msg
        )
        print('EMAIL HAS BEEN SENT')

        server.quit()

if __name__ == '__main__':
    send_mail()
