from django.conf.urls import url, include

from django.conf import settings
from AmbassadorPortal import views
from django.conf.urls.static import static

urlpatterns = [

    url(r'^sign-up-ambassador$', views.sign_up_ambassador, name="registration"),
    url(r'^sign-in$', views.sign_in, name="sign-in"),
    url(r'^locality-ambassadors$', views.locality_ambassadors, name="localityambassadors"),
    url(r'^search-person$', views.search_person, name="searchperson"),
    # url(r'^home$', views.home, name="home"),
    # url(r'^ambassadorhome$', views.amb_home, name="ambassadorhome"),
     url(r'^add-person$', views.add_person, name="addperson"),
     url(r'^get-localities$', views.get_localities, name="getlocalities"),
    # url(r'^searchparent$', views.get_parent, name="searchparent"),
    # url(r'^newsenter$', views.news_entry, name="newsenter"),
    # url(r'^profile$', views.ambassador_profile, name="profile"),
     url(r'^families$', views.get_families, name="families")
    # url(r'^showhierarchy$', views.show_hierarchy, name="showhierarchy"),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
