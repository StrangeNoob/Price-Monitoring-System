from django.shortcuts import render,redirect
from .forms import UrlForm
from .models import URLCollection



def mail(request):
    return render(request,'mail.html')
    
def sign(request):
    if request.method == 'POST':
        form = UrlForm(request.POST)
        if form.is_valid():
            Url=request.POST['Url']
            Email=request.POST['Email']
            Price=request.POST['Price']
            Price=float(Price)
            new_Url = URLCollection(URL=request.POST['Url'],email=request.POST['Email'],price=request.POST['Price'])
            new_Url.save()
            print("Object Created")          
            return redirect('mail')
    else: 
        form = UrlForm()
    context = {'form':form}    
    return render(request, 'sign.html',context)
       
    

