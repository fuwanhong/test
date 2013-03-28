import re
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseNotFound
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import mail_admins, send_mail
from settings_devel import EMAIL_HOST_USER
# from django.contrib.sessions.models import Session
# from django.contrib.auth.backends import ModelBackend


@login_required
def login_test(request):
    return render_to_response("home.html",
            context_instance=RequestContext(request))


def mylogout(request):
    logout(request)
    return HttpResponse('Loged out successfuly.')


def login_page(request):
    request.session["next"] = request.GET.get('next')

    return render_to_response("account_sso.html",
            context_instance=RequestContext(request))


def openid_login(request, domain):
    if domain == 'company':
        url = 'https://www.google.com/accounts/o8/ud?hd=smalltreemedia.com&openid.ns=http://specs.openid.net/auth/2.0&openid.ns.pape=http://specs.openid.net/extensions/pape/1.0&openid.claimed_id=http://specs.openid.net/auth/2.0/identifier_select&openid.identity=http://specs.openid.net/auth/2.0/identifier_select&openid.return_to=http://localhost:8000/accounts/profile&openid.realm=http://localhost:8000/accounts/&openid.assoc_handle=ABSmpf6DNMw&openid.mode=checkid_setup&openid.ui.ns=http://specs.openid.net/extensions/ui/1.0&openid.ui.mode=popup&openid.ui.icon=true&openid.ns.ax=http://openid.net/srv/ax/1.0&openid.ax.mode=fetch_request&openid.ax.type.email=http://axschema.org/contact/email&openid.ax.type.firstname=http://axschema.org/namePerson/first&openid.ax.type.lastname=http://axschema.org/namePerson/last&openid.ax.required=email,firstname,lastname'
    else:
        url = 'https://www.google.com/accounts/o8/ud?openid.ns=http://specs.openid.net/auth/2.0&openid.ns.pape=http://specs.openid.net/extensions/pape/1.0&openid.claimed_id=http://specs.openid.net/auth/2.0/identifier_select&openid.identity=http://specs.openid.net/auth/2.0/identifier_select&openid.return_to=http://localhost:8000/accounts/profile&openid.realm=http://localhost:8000/accounts/&openid.assoc_handle=ABSmpf6DNMw&openid.mode=checkid_setup&openid.ui.ns=http://specs.openid.net/extensions/ui/1.0&openid.ui.mode=popup&openid.ui.icon=true&openid.ns.ax=http://openid.net/srv/ax/1.0&openid.ax.mode=fetch_request&openid.ax.type.email=http://axschema.org/contact/email&openid.ax.type.firstname=http://axschema.org/namePerson/first&openid.ax.type.lastname=http://axschema.org/namePerson/last&openid.ax.required=email,firstname,lastname'

    return HttpResponseRedirect(url)


def popup_login_return(request):

    return render_to_response("popup_return.html",
            context_instance=RequestContext(request))


def show_profile(request):
    if request.GET.get('openid.mode') == 'cancel':
        return HttpResponse('Some Error Happened!')

    elif request.GET.get('openid.ext1.value.email') and request.GET.get('openid.ext1.mode')=='fetch_response':
        firstname = request.GET.get('openid.ext1.value.firstname')
        lastname = request.GET.get('openid.ext1.value.lastname')
        email = request.GET.get('openid.ext1.value.email')
        next = request.session['next']

        username = re.split('@', email)[0]
        username = re.sub('\.', '', username)
        username = username.partition('+')[0]
        request.session["username"] = username
        print "items(): ", request.session.items()

        if User.objects.filter(username=username).exists():
            if User.objects.filter(username=username, email=email).exists():
                pass
            else:
                User.objects.filter(username=username).update(email=email)

            user = User.objects.get(username=username)
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            if user.is_active:
                login(request, user)
                results = {
                        "jump_url": next,
                        "username": username,
                }

                return render_to_response("welcome.html", results,
                        context_instance=RequestContext(request))
            else:
                results = {
                        "username": username,
                        "msg": "Your account is NOT active, please contact System Admin for support "
                }

                return render_to_response("welcome.html", results,
                        context_instance=RequestContext(request))
        else:
            UserObj = User.objects.create(first_name=firstname, last_name=lastname, email=email, is_active=False, username=username, password='')

            return HttpResponseRedirect(reverse("profile_msg"))

    else:
        return HttpResponseNotFound()


@csrf_exempt
def leave_msg(request):
    if request.method == 'GET':
        var = {
            'msg': 'You have logged in with Openid.'
            }

        return render_to_response("leave_msg.html", var,
                context_instance=RequestContext(request))

    else:
        username = request.session['username']
        user = User.objects.get(username=username)
        content = request.POST['content']
        msg = '<p>System Email. Please approve this guy and assgin proper Permissions for new user: %s.</p>' % username
        content = '<p>Leave a message with you: %s</p>' % content
        active_link = '<p>Permission Assgin Link Address: <a href="http://127.0.0.1:8000/admin/auth/user/%s">Assgin Permission</a></p>' % user.id
        mail_admins('A New guy is Coming', 'why message here not be sent', html_message = msg+content+active_link)

        # return HttpResponseRedirect(next)
        return HttpResponse('email & comment success')

