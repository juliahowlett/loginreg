from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import Users

def verify_session_user(request):
    try:
        request.session['id']
    except KeyError:
        return redirect('/')

def index(request): 
	context = {
	'all_users' : Users.objects.all(),
	}
	return render(request, 'loginreg/index.html', context)

def success(request, status): 
	print(status)
	context = {
	'the_user' : Users.objects.get(id=request.session['id']),
	'status' : status
	}
	return render(request, 'loginreg/success.html', context)	
	
def register(request):  #/loginreg/create_user
	print(request.POST)	
	status = None
	errors_or_user = Users.objects.validate_registration(request.POST)	
		
	if errors_or_user[0]:
		for fail in errors_or_user[0]:
			messages.error(request, fail)
		return redirect('/')
		
	status = "registered"	
	request.session['id'] = errors_or_user[1].id	

	return redirect('/success', status)	
	
def login(request): 	
	print(request.POST)	
	status = None
	errors_or_user = Users.objects.validate_login(request.POST)
	
	if errors_or_user[0]:
		for fail in errors_or_user[0]:
			messages.error(request, fail)
		return redirect('/')
		
	request.session['id'] = errors_or_user[1].id
	status = "logged in"	
	return redirect('/success', status)	
	
def logout(request):
	del request.session['id']
	return redirect('/index')
