from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import path

def log_in(request):
	if request.method == 'POST':
		data = request.POST
		username = data['username'].replace('"', '').replace("'", '').replace(';', '')
		password = data['password'].replace('"', '').replace("'", '').replace(';', '')

		errors = []

		# Ensure username is provided
		if username == '':
			errors.append('Enter your username')
		# Verify username length
		elif len(username) < 4 or len(username) > 16:
			errors.append('Your username should be between 4 and 16 characters')
		# Verify uniqueness
		else:
			unique = False
			try:
				User.objects.get(username=username)
			except User.DoesNotExist:
				unique = True
			if unique:
				errors.append('Username not found')

		# Ensure password is provided
		if password == '':
			errors.append('Enter your password')
		# Verify password length
		elif len(password) < 8 or len(password) > 24:
			errors.append('Your password should be between 8 and 24 characters')

		# Alert user of errors
		if len(errors) != 0:
			return render(request, 'user/login.html', context={'errors': errors})
	
		# No errors, create user
		user = User.objects.get(username=username)
		if check_password(password, user.password):
			login(request, user)
			return redirect('main:index')
		else:
			return render(request, 'user/login.html', context={'errors': ['Your password is incorrect']})
	
	return render(request, 'user/login.html', context={})

def log_out(request):
	logout(request)
	return redirect('main:index')

def sign_up(request):
	if request.method == 'POST':
		data = request.POST
		username = data['username'].replace('"', '').replace("'", '').replace(';', '')
		password1 = data['password1'].replace('"', '').replace("'", '').replace(';', '')
		password2 = data['password2'].replace('"', '').replace("'", '').replace(';', '')

		errors = []

		# Ensure username is provided
		if username == '':
			errors.append('Must provide a username')
		# Verify username length
		elif len(username) < 4 or len(username) > 16:
			errors.append('Username must be between 4 and 16 characters')
		# Verify uniqueness
		else:
			unique = False
			try:
				User.objects.get(username=username)
			except User.DoesNotExist:
				print('No users found')
				unique = True
			if not unique:
				errors.append('Username already taken')

		# Ensure password is provided
		if password1 == '':
			errors.append('Must provide a password')
		# Verify password length
		elif len(password1) < 8 or len(password1) > 24:
			errors.append('Password must be between 8 and 24 characters')
		# Confirm password
		elif password1 != password2:
			errors.append('Password mismatch: both passwords must be the same')

		# Alert user of errors
		if len(errors) != 0:
			return render(request, 'user/signup.html', context={'errors': errors})
	
		# No errors, create user
		user = User(username=username, password=password1)
		user.save()
		login(request, user)
		return redirect('main:index')
	
	return render(request, 'user/signup.html', context={})
