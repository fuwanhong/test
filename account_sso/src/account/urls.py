from django.conf.urls import patterns, url, include


urlpatterns = patterns('account.views',

    url(r'^login/', 'login_page'),

    url(r'^openid_login/(?P<domain>\w+)$', 'openid_login', name="account_sso"),

    url(r'^popreturn/', 'popup_login_return'),

    url(r'^profile', 'show_profile'),

    url(r'^message/$', 'leave_msg', name="profile_msg"),

    url(r'^login_test/$', 'login_test'),

    url(r'^logout/', 'mylogout', name="mylogout"),


)
