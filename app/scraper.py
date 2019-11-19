import requests
from bs4 import BeautifulSoup
import smtplib

Url = "https://www.amazon.com/Apple-AirPods-Charging-Latest-Mo" \
      "del/dp/B07PXGQC1Q/ref=sr_1_1_sspa?keywords=ai" \
      "rpods&qid=1569519451&sr=8-1-spons&psc=1&" \
      "spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUExOEZHS1lGTlZQN0Z" \
      "HJmVuY3J5cHRlZElkPUEwODgzNDExMUExUlAxUkk4UTI4SSZlbmNy" \
      "eXB0ZWRBZElkPUExMDA0ODcwREJCVUpMV1FWMk9MJndpZGdldE5hbWU9c" \
      "3BfYXRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1" \
      "ZQ==https://www.amazon.com/Apple-AirPods-Charging-Latest-Mode" \
      "l/dp/B07PXGQC1Q/ref=sr_1_1_sspa?keywords=airpods&qid=1569519" \
      "451&sr=8-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUExOEZHS1" \
      "lGTlZQN0ZHJmVuY3J5cHRlZElkPUEwODgzNDExMUExUlAxUkk4UTI4SSZlbmNy" \
      "eXB0ZWRBZElkPUExMDA0ODcwREJCVUpMV1FWMk9MJndpZGdldE5hbWU9c3BfY" \
      "XRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ=="

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15"}



def check_price():

    page = requests.get(Url, headers=headers)

    soup = BeautifulSoup(page.content, "html.parser")

    title = soup.find(id = "productTitle").get_text()
    price = soup.find(id = "priceblock_ourprice").get_text()

    converted_price =  float(price[1:5])

    if(converted_price < 160):
        send_mail()
        print(converted_price)
        print(title.strip())



def send_mail():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('ruppatel11599@gmail.com', 'birthday11599')

    subject = 'Price dropped down!'
    body = Url;
    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(
        'ruppatel11599@gmail.com',
         'grendal27@gmail.com',
        msg
    )
    print('EMAIL HAS BEEN SENT')


    server.quit()



check_price()

