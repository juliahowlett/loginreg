#from __future__ import unicode_literals
from datetime import datetime
from django.db import models
import re
import bcrypt

EMAIL_MATCH = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

class UserManager(models.Manager):
	def validate_registration(self, post_data):
		print(post_data) 	
		errors = []
		user = None
		#check for empty fields
		for  key, value in post_data.items():
			if len(value) < 1:
				errors.append("All fields are required")
				break

		#min length for name /alias
		if len(post_data['name']) < 2 or len(post_data['alias']) < 2:
			errors.append("all fields must be at least 2 characters") 
			
		#email valid
		if not re.match(EMAIL_MATCH, post_data['email']):
			errors.append("email not valid")
			
		#email already in DB
		if self.filter(email=post_data['email']):
			errors.append("email already in use - must be new email")	
			print(errors)
		
		#min length for password
		if len(post_data['password']) < 8:
			errors.append("password must be at least 8 characters") 
			
		#passwords match 
		if post_data['password'] != post_data['confirm_pw']:
			errors.append("Passwords do not match")
		  
		# user must be 18 or older
		#if not datetime.strptime(post_data['dob'], "%Y-%m-%d"):
		#	errors.append("Please enter a valid date")
		years = (datetime.today() - datetime.strptime(post_data['dob'], "%Y-%m-%d")).days/365
		if years < 18:
			errors.append("Must be 18 or older to register")
			
		#if no errors, create a User
		if not errors:
			hashed_pw = bcrypt.hashpw(post_data['password'].encode(), bcrypt.gensalt())
				
			user = self.create(
				name = post_data['name'],
				alias = post_data['alias'],
				email = post_data['email'],
				password = hashed_pw,
				dob = post_data['dob']
				)
				
		return  errors, user		
	
	def validate_login(self, post_data):
		print(post_data) 	
		errors = []
		user = None
		#check all fields for input- check for empty fields
		for  key, value in post_data.items():
			if len(value) < 1:
				errors.append("All fields are required")
				print(errors)
				break
			
		#Check DB for Existing email / password	
		if not self.filter(email=post_data['email']):
			errors.append("Invalid email/password")
		else:
			user = self.get(email=post_data['email'])
			# if email is in DB then check passwords
			if not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()):
				errors.append("Invalid email/password")	
			
		return errors, user			
			
class Users(models.Model):
	name = models.CharField(max_length=255)
	alias = models.CharField(max_length=255)
	email = models.EmailField(unique=True)
	password = models.CharField(max_length=50)
	dob = models.DateField(auto_now=True)
	created_at = models.DateField(auto_now_add=True)
	updated_at = models.DateField(auto_now=True)
	
	objects = UserManager()
	
	def __repr__(self):
		return "<name: {}, alias: {}, email: {}>".format(self.name,self.alias,self.emailt)	

