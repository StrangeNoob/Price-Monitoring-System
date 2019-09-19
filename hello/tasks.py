from .models import URLCollection
import requests
from bs4 import BeautifulSoup
import smtplib
from celery import shared_task
import time


@shared_task
def every():
    URLobject = URLCollection.objects.order_by('date_added')
    for url in URLobject:
        print(url.id)
        print(url.email)
        print(url.URL)
        print(url.price)
        url.sendMail=check_price(url.id,url.URL,url.email,url.price)
        url.save()
        print(url.sendMail)
    remove_from()
    return None
    
    
def remove_from():
    URLCollection.objects.filter(sendMail=True).delete()    

def check_price(Id,URL,email,Price) :
        headers = {"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}
        pages = requests.get(URL, headers=headers)
        soup = BeautifulSoup(pages.content,'html.parser')
        print(Id)
        print(URL)
        print(email)
        Price=float(Price)
        if(URL.__contains__('amazon')):
                title = soup.find(id='productTitle').get_text()
                price = soup.find(id='priceblock_ourprice').get_text()
                price = price.replace(',','')
                price = price[2:]
                print(title.strip())
                print(price.strip())
                convertedprice = float(price)
                if(convertedprice < Price):
                    send_mail(URL,title,email)
                    return True
                else:
                    return False    
       
        elif(URL.__contains__('flipkart')):
                soup = BeautifulSoup(pages.content, 'html.parser')
                price=''
                title=''
                for foo in soup.find_all('div', attrs={'class': '_1vC4OE _3qQ9m1'}):
                    price=foo.text
                price = price.replace(',','')
                price = price[1:]                           
                print(price.strip())
                convertedprice = float(price)
                if(convertedprice < Price):
                    send_mail(URL,title,email)
                    print("Hey Email Has been Sent")
                    return True
                else:
                    return False   
        else:
                title = soup.find(id='productName').get_text()
                price = soup.find(id='price').get_text()
                price = price.replace(',','')
                price = price[1:]
                print(title.strip())
                print(price.strip())
                convertedprice = float(price)
                if(convertedprice < Price):
                    send_mail(URL,title,email)
                    return True
                else:
                    return False    

def send_mail(URL,Title,Email):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('sipun2599@gmail.com','swzpexjtsptldsel')
    subject = 'Price went down for '+ Title +''
    if(URL.__contains__('amazon.com')):
        body = ' check the amazon link '+ URL
    else:
        body = ' check the flipkart link '+ URL       
    msg = f"Subject: {subject} \n\n {body}"
    print(Email)
    server.sendmail(
        'sipun2599@gmail.com',
        Email,
        msg
    )
    server.quit()            

#every()   
