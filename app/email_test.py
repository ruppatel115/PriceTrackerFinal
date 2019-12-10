import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def main():
    import smtplib

    gmail_user = 'price.tracker2019@gmail.com'
    gmail_password = 'ptpassword'

    sent_from = gmail_user
    to = ['deucewatson@aol.com']
    subject = 'Price Dropped'
    body = 'Prices have dropped!'

    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, ", ".join(to), subject, body)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()

        print('Email sent!')
    except:
        print('Something went wrong...')


if __name__ == '__main__':
    main()
