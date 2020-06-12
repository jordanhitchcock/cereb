import random
from datetime import datetime

from django.shortcuts import render, redirect
from django import forms
from django.http import HttpResponse

from .models import Visitors


class EmailForm(forms.Form):
    email = forms.EmailField(label='', widget=forms.TextInput(attrs={'placeholder': 'Enter your email to learn more...'}))


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField(label='Your Email')
    content = forms.CharField(widget=forms.Textarea, label='Tell us about your favorite smart home device!', required=True)


def home(request):

    # Create session key if none:
    if not request.session.session_key:
        request.session.create()
    session_id = request.session.session_key

    # See if there is already a template for this session
    try:
        template_name = request.session['template_name']
    except KeyError:
        template_name = randomized_template_name()
        request.session['template_name'] = template_name

        # new session, so save to Visitors db
        visitor = Visitors(session_id=session_id, template_name=template_name, visit_dt=datetime.now(),
                           ip=request.META['REMOTE_ADDR'])
        visitor.save()

    # has already submitted email or contacted for session or not
    has_submitted_email = request.session.get('has_submitted_email', False)
    has_contacted = request.session.get('has_contacted', False)

    if request.method == 'POST':
        # sign up
        if request.POST['action'] == 'Sign up!':
            form = EmailForm(request.POST, label_suffix='')
            if form.is_valid():
                request.session['has_submitted_email'] = True

                # update model
                try:
                    visitor = Visitors.objects.get(session_id=request.session.session_key)

                except:
                    visitor = Visitors(session_id=session_id, template_name=template_name, visit_dt=datetime.now(),
                           ip=request.META['REMOTE_ADDR'])

                visitor.signup_email = form.cleaned_data['email']
                visitor.save()

                return redirect('home')

        # contact us
        if request.POST['action'] == 'Contact Us':
            form = ContactForm(request.POST, label_suffix='')
            if form.is_valid():
                request.session['has_contacted'] = True

                # update model
                try:
                    visitor = Visitors.objects.get(session_id=request.session.session_key)
                except:
                    visitor = Visitors(session_id=session_id, template_name=template_name, visit_dt=datetime.now(),
                           ip=request.META['REMOTE_ADDR'])

                visitor.contact_name = form.cleaned_data['name']
                visitor.contact_email = form.cleaned_data['email']
                visitor.contact_content = form.cleaned_data['content']
                visitor.save()

                return redirect('home')

    else:
        form = EmailForm()

    return render(request, template_name, {'email_form': form,
                                           'contact_form': ContactForm(),
                                           'has_submitted_email': has_submitted_email,
                                           'has_contacted': has_contacted})


def randomized_template_name():
    return random.choice(['www/indexA.html', 'www/indexB.html'])








