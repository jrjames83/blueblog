from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse
from django.views.generic import CreateView
# Create your views here.


"""    
http://jessenoller.com/blog/2011/12/19/
quick-example-of-extending-usercreationform-in-django

"""
#This is a django generic view
class UserRegistrationView(CreateView):
	form_class = UserCreationForm #part of auth contrib app
	template_name = 'user_registration.html'


	def get_success_url(self):
		return reverse('home')


