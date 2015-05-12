from django.shortcuts import render
from django.template import Context, loader
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import os
from django.conf.urls.static import static
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from models import User
from django.contrib.auth.models import User
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from app.static import directory_index
from app.static import serve
from django import forms
import logging
import re
import sys
from axes.decorators import watch_login
from axes.utils import reset

logger = logging.getLogger('app')

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

MEDIA_ROOT = "/var/log/remote/"

def index(request):
    context_dict = {'boldmessage': "I am bold font from the context"}

    # Return a rendered response to send to the client.
    return render(request, 'app/index.html', context_dict)

@watch_login
def user_login(request):

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
                # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
                # because the request.POST.get('<variable>') returns None, if the value does not exist,
                # while the request.POST['<variable>'] will raise key error exception
        username = request.POST.get('username')
        password = request.POST.get('password')

        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # get last login date
        if user is not None:
            last_login = user.last_login

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                
        
        #reset(username=username)

                logger.debug("SUCCESS LOGIN FROM " + request.META['REMOTE_ADDR'] + " FOR " + username + ", Authentication success")
                return render(request, 'base.html',{'last_login': last_login})
            else:
                # An inactive account was used - no logging in!
                logger.debug("FAILED LOGIN FROM " + request.META['REMOTE_ADDR'] + " FOR " + username + ", This account is non active")
                return HttpResponse("Your account is disabled.")
        else:
            logger.debug("FAILED LOGIN FROM " + request.META['REMOTE_ADDR'] + " FOR " + username + ", Authentication failure")
            #return HttpResponseRedirect("")
            return render(request, 'app/login.html', {'invalid': True})

            # Bad login details were provided. So we can't log the user in.
            #print "Invalid login details: {0}, {1}".format(username, password)
            #return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        logger.debug("ACCESS FROM " + request.META['REMOTE_ADDR'])
        return render(request, 'app/login.html', {'invalid': True })



    
def get_absolute_pathname(pathname='', safe=True):
    if not pathname:
        return os.path.join(MEDIA_ROOT, 'index')
    if safe and '..' in pathname.split(os.path.sep):
        return get_absolute_pathname(pathname='')
    return os.path.join(MEDIA_ROOT, pathname)       



@login_required
def retrieve_path(request, path, document_root):
   try:
       if request.user.is_authenticated():
         user_n = request.user.username
         abs_pathname = get_absolute_pathname(user_n)
         url = document_root
         current_url = "%s/%s/" %(url,user_n)
         req_user = re.search('/var/log/remote/(.+?)/', abs_pathname)
         response = serve(request, path, abs_pathname, directory_index( path, document_root))
         if str(abs_pathname + "/" + path).endswith('/'):
            logger.debug("RETRIEVE DIRECTORY INDEX from " + request.META['REMOTE_ADDR'] + " for " + user_n + ", " + abs_pathname + "/" + path)
         else:
            logger.debug("DOWNLOAD FILE REQUEST from " + request.META['REMOTE_ADDR'] + " for " + user_n + ", " + abs_pathname + "/" + path)
         
         return response
       else:
          return HttpResponse("Permission Denied, Try Again")  
 
   except ObjectDoesNotExist:
        return HttpResponse("Sorry you don't have permission to access this file")



@login_required
def protected_serve(request, path, show_indexes, document_root):
    try:
        if request.user.is_authenticated():
         pathname = request.user.get_username()
         abs_pathname = get_absolute_pathname(pathname)
         url = document_root
         if url == path:
           new_url = url.replace("/appata/", "")
         return serve(request, path, show_indexes, document_root)
    except ObjectDoesNotExist:
        return HttpResponse("Sorry you don't have permission to access this file")
 
 



# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logger.debug(request.user.username + " logout")
    logout(request)
    # Take the user back to the homepage.
    return HttpResponseRedirect('/app/')




@login_required
def change_password(request):
    try:
        if request.POST:
            form = Change_password_form(request.POST)
            user = request.user.username
            old_password = request.POST['old_password']
            new_password1 = request.POST['new_password1']
            new_password2 = request.POST['new_password2']
            if not User.objects.get(username=user).check_password(old_password):
                msg = 'Old password is not valid.'
                return render(request, '../templates/internal_error.html', {'msg':msg})
            if form.is_valid():
                if new_password1 == new_password2 and old_password != new_password1:
                    u = User.objects.get(username=user)
                    u.set_password(new_password1)
                    u.save()
                    logger.debug("CHANGE PASSWORD DONE FROM "+request.META['REMOTE_ADDR'] + " FOR " + user)
                    return render(request, '../templates/password_change_done.html')            
                else:
                    form = Change_password_form()
                    return render(request, '../templates/password_change_form.html', {'form':form})
            else:
                return render(request, '../templates/password_change_form.html', {'form':form})

### View Change Password Page ###
        else:
            form = Change_password_form()
            return render(request, '../templates/password_change_form.html', {'form':form})
#################################

    except:
        logger.error("ERRORS OCCURS " + " FROM " + request.META['REMOTE_ADDR'] + ", " + str(sys.exc_info()[1]))
        return render(request, '../templates/password_change_form.html', {'form':form})

class Change_password_form(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Old Password'}), required=True)
    new_password1= forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'New Password'}), required=True, min_length=8)
    new_password2= forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm New Password'}), required=True, min_length=8)
    action = forms.CharField(label="action", required=True)

    def clean(self):
        cleaned_data = super(Change_password_form, self).clean()
        old_password = self.cleaned_data.get('old_password')
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')
        action = self.cleaned_data.get('action')
        
        # password policy
        reg_pattern = r'(?=.{8,})(?=.*[0-9]+.*)(?=.*[a-z]+.*)(?=.*[A-Z]+.*)'

        if old_password == new_password1:
            raise forms.ValidationError("New password should be changed.")
        if not re.match(reg_pattern, new_password1):
            raise forms.ValidationError("Please check the password policy.")
        if new_password1 != new_password2:
            raise forms.ValidationError("New password is wrong.")   
        return self.cleaned_data


##################################################


@login_required
def update_config(request):
    try:
        if request.POST:
            user = request.user.username
            u = User.objects.get(username=user)
            if u.is_superuser == True:
                #logger.debug("EDITING RSYSLOG CONFIG")
                os.system('python /home/www/project/app/lib/EditRsyslog.py')
                return render(request, '../templates/admin/config_update_done.html')
            else:
                #logger.error("ERROR OCCURS FROM " + request.META['REMOTE_ADDR'] + sys.exc_info()[1])
                return render(request, '../templates/internal_error.html')
        else:
            #logger.debug("RECEIVED GET METHOD FROM " + request.META['REMOTE_ADDR'])
            return render(request, '../templates/internal_error.html')
    except:
        #logger.debug("ERROR OCCURS " + " FROM " + request.META['REMOTE_ADDR'] + ", " + sys.exc_info()[1])
            return render(request, '../templates/internal_error.html')

class Update_config_form(forms.Form):
    action = forms.CharField(label="action", required=True)
    def clean(self):
                cleaned_data = super(Update_config_form, self).clean()
                action = self.cleaned_data.get('action')

################################

