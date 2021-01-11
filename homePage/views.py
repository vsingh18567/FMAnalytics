from django.shortcuts import redirect, render
from django.views import View
from .forms import RegisterForm
from django.contrib import messages


# Create your views here.
class Home(View):

	def get(self, request):
		return render(request, 'homePage/home.html')


class Register(View):
	def get(self, request):
		form = RegisterForm()
		return render(request, 'homePage/register.html', {'form': form})

	def post(self, request):
		form = RegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'Welcome {username}! Please login below')
			return redirect('login')
		else:
			return render(request, 'homePage/register.html', {'form': form})


