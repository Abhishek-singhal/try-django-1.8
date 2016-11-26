from django.conf import settings
from django.core.mail import send_mail 
from django.shortcuts import render
import socks

from .forms import ContactForm, SignUpForm

#socks.wrapmodule(send_mail)


def home(request):
	title = 'Welcome'
	form = SignUpForm(request.POST or None)
	context = {
		"title":  title,
		"form":form,
	}
	if form.is_valid():
		#form.save()
		instance = form.save(commit=False)
		if not instance.full_name:
			instance.full_name = "Anknown"
		instance.save()
		context = {
			"title": "Thank You"
		}

	return render(request,"home.html", context)
def contact(request):
	form = ContactForm(request.POST or None)
	context = {"form":form,}
	if form.is_valid():
		from_email = form.cleaned_data.get("email")
		from_message = form.cleaned_data.get("message")
		from_full_name = form.cleaned_data.get("full_name")
		subject = 'Site contact form'
		from_email = settings.EMAIL_HOST_USER
		to_email = [from_email]
		contact_message = "%s: %s via %s"%(
			from_full_name,
			from_message,
			from_email)
		send_mail(subject,
		 	contact_message,
		 	 from_email,
		 	 to_email,
		 	 fail_silently=False)
	#	for key,value in form.cleaned_data.iteritem:
	#		print(key,value)
	return render(request,"forms.html",context)