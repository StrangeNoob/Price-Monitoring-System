from django.shortcuts import render,redirect
from .forms import UrlForm
from .models import URLCollection
import requests
from bs4 import BeautifulSoup
import smtplib
import time

def sign(request):
    if request.method == 'POST':
        form = UrlForm(request.POST)

        if form.is_valid():
            Url=request.POST['Url']
            Email=request.POST['Email']
            Price=request.POST['Price']
            Price= float(Price)
            print(Price)
            new_Url = URLCollection(URL=request.POST['Url'],email=request.POST['Email'],price=request.POST['Price'])
            new_Url.save()
            print("Object Created")
            check_price()
            return redirect('mail')
    else: 
        form = UrlForm()
    context = {'form':form}    
    return render(request, 'sign.html',context)
def check_price() :
    URLobject = URLCollection.objects.order_by('-date_added')
    for url in URLobject:
        headers = {"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}
        pages = requests.get(url.URL, headers=headers)
        soup = BeautifulSoup(pages.content,'html.parser')
        if(url.URL.__contains__('amazon.com')):
                title = soup.find(id='productTitle').get_text()
                price = soup.find(id='priceblock_ourprice').get_text()
                price = price.replace(',','')
                price = price[2:]
                print(title.strip())
                print(price.strip())
                convertedprice = float(price)
                if(convertedprice < url.price):
                    send_mail(url.URl,title,url.price)
                    url.sendMail = True
        else:
                soup = BeautifulSoup(pages.content, 'html.parser')
                price=''
                title=''
                for foo in soup.find_all('div', attrs={'class': '_1vC4OE _3qQ9m1'}):
                    price=foo.text
                price = price.replace(',','')
                price = price[1:]                           
                print(price.strip())
                convertedprice = float(price)
                if(convertedprice < url.price):
                    send_mail(url.URl,title,url.price)
                    print("Hey Email Has been Sent")
                    url.sendMail = True
                else:
                    print('Item Price is too high')
        

              

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
    
def mail(request):
      return render(request,'mail.html')
#while (True):
#   check_price()
#   
#     
#
#   time.sleep(3600)

