from django.shortcuts import render,redirect
from .forms import UrlForm
import requests
from bs4 import BeautifulSoup
import smtplib

def sign(request):
    if request.method == 'POST':
        form = UrlForm(request.POST)

        if form.is_valid():
            Url=request.POST['Url']
            Email=request.POST['Email']
            Price=request.POST['Price']
            Price= float(Price)
            print(Price)
            check_price(Url,Email,Price)
    else: 
        form = UrlForm()
    context = {'form':form}    
    return render(request, 'sign.html',context)
def check_price(URL,Email,Price) :

        headers = {"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}
        pages = requests.get(URL, headers=headers)
        soup = BeautifulSoup(pages.content,'html.parser')
        if(URL.__contains__('amazon.com')):
                title = soup.find(id='productTitle').get_text()
                price = soup.find(id='priceblock_ourprice').get_text()
                price = price.replace(',','')
                price = price[2:]
                print(title.strip())
                print(price.strip())
                convertedprice = float(price)
                if(convertedprice < Price):
                    send_mail(URL,title,Email)
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
                if(convertedprice < Price):
                    send_mail(URL,title,Email)
        return redirect('sign')

              

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
    print("Hey Email Has been Sent")
    server.quit()            
