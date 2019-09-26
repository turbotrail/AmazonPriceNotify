import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

URL='https://www.amazon.in/Samsung-Galaxy-Storage-Additional-Exchange/dp/B07KXBMYCW/ref=br_msw_pdt-5?_encoding=UTF8&smid=A14CZOWI0VEHLG&pf_rd_m=A1VBAL9TL5WCBF&pf_rd_s=&pf_rd_r=TKFDG3T4Q8SHW0X6X5D8&pf_rd_t=36701&pf_rd_p=cc9b62a5-2189-486a-89b4-4eda80243fbe&pf_rd_i=desktop'

def pric():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches",["ignore-certificate-errors"])
    options.add_argument('--disable-gpu')
    options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(URL)
    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')

    title = soup.find(id='productTitle')
    #print(soup)
    print(title.get_text().strip())


    price=soup.find(id='priceblock_dealprice')
    print(float(price.get_text().strip().replace('₹ ','').replace(',','')))

    amz_price=float(price.get_text().strip().replace('₹ ','').replace(',',''))

    driver.close()

    if (amz_price < 19000.00):
        send_mail()

def send_mail():
    server=smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login('someone@some.com','AccessKey generated')
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Price Drop from Python"
    msg['From'] = 'someone@some.com'
    msg['To'] = 'someone@some.com'

    text = "You Have been notified of the following product price drop"
    html = """\
    <html> <body><a href='https://www.amazon.in/Samsung-Galaxy-Storage-Additional-Exchange/dp/B07KXBMYCW/ref=br_msw_pdt-5?_encoding=UTF8&smid=A14CZOWI0VEHLG&pf_rd_m=A1VBAL9TL5WCBF&pf_rd_s=&pf_rd_r=TKFDG3T4Q8SHW0X6X5D8&pf_rd_t=36701&pf_rd_p=cc9b62a5-2189-486a-89b4-4eda80243fbe&pf_rd_i=desktop'>Link</a>'</body></html>
    """
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    msg.attach(part1)
    msg.attach(part2)

    server.sendmail('jp.s.gog@gmail.com','jeyaprakashsenguttuvan@gmail.com',msg.as_string())
    print('email sent')
    server.quit()

pric()
