from django.conf.urls import patterns, url
from TREC import views
from registration.backends.simple.views import RegistrationView

# Create a new class that redirects the user to the index page, if successful at logging
class MyRegistrationView(RegistrationView):
    def get_success_url(self,request, user):
        return '/rango/'


urlpatterns = patterns('',
    url(r'^$', views.homepage, name='homepage'),
    #url(r'^admin/', include(admin.site.urls)),
    #url(r'^TREC/', include('TREC.urls')),
        #Add in this url pattern to override the default pattern in accounts.
    url(r'^accounts/register/$', MyRegistrationView.as_view(), name='registration_register'),
    #url(r'^accounts/', include('registration.backends.simple.urls')),
)
