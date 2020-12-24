from django.shortcuts import redirect, render
from django.views import View
from .forms import RegisterForm
from django.contrib import messages
# Create your views here.

def home_view(request):
    return render(request, 'homeApp/base.html')



class Login(View):

    def get(self, request):
        form = RegisterForm()
        return render(request, 'homeApp/login.html', {'form':form})
    
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Welcome {username}')
            return redirect('login')
        
    
