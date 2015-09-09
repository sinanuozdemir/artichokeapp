from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin

urlpatterns = patterns('',
    
 url(r'^admin/', include(admin.site.urls)),
    url(r'lead_management/',  'legion.views.lead_management'),
    url(r'^lead_generation/login',  'legion.views.login_view'),
    url(r'^lead_generation?',  'legion.views.lead_generation'),
    url(r'supsec/',  'legion.views.supsecimport'),

    url(r'^$', 'dashboard.views.splash'),
    url(r'^legion/$', 'dashboard.views.splash'),
    
    # url(r'^legion/onboarding/almostthere', 'dashboard.views.onboarding2'),
    url(r'^getRandomAPICredentials', 'dashboard.views.getRandomAPICredentials'),
    url(r'^getRandomAPIProxies', 'dashboard.views.getRandomAPIProxies'),
    # url(r'^legion/onboarding/', 'dashboard.views.onboarding'),
    url(r'^legion/twitter/login/', 'dashboard.views.twitterLogin'),
    url(r'^twitter/success/', 'dashboard.views.twitterAuth'),
    url(r'^google/success/', 'dashboard.views.googleAuth'),
    url(r'^linkedin/success/', 'dashboard.views.linkedinAuth'),
    url(r'^mailchimp/success/', 'dashboard.views.mailchimpAuth'),
    
    url(r'^check/',  'dashboard.views.check'),

    url(r'^legion/dashboard/',  'dashboard.views.email_dashboard2'),

    url(r'^legion/inbound_info/(?P<page_num>\w+)?',  'dashboard.views.getInboundInfo'),

    url(r'^legion/logout/',  'dashboard.views.logout'),
    url(r'^legion/login/',  'dashboard.views.login'),
    url(r'^getEntityFromDB',  'dashboard.views.getEntityFromDB'),
    url(r'^putEntityInDB',  'dashboard.views.putEntityInDB'),
    
    url(r'^legion/forgot/',  'dashboard.views.forgot_password'),
	url(r'^legion/my_account/',  'dashboard.views.my_account'),
	url(r'^legion/signup/',  'dashboard.views.signup'),
	# url(r'^legion/choose-plan/',  'dashboard.views.chooseplan'),

    
    url(r'^legion/lead_stream/(?P<view_id>\d+)?', 'dashboard.views.lead_stream'),
    url(r'^legion/updated_lead_stream/?', 'dashboard.views.getUpdatedLeadStream'),

    url(r'^msg/i_seens_it/shh/(?P<message_id>\w+)?', 'dashboard.views.messageView'),
	# url(r'^legion/lead_stream/',  'dashboard.views.lead_stream'),
    
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



# urlpatterns += patterns('loginas.views',
#     url(r"^login/user/(?P<user_id>.+)/$", "user_login", name="loginas-user-login"),



handler404 = 'dashboard.views.error404'
