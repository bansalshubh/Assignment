from django.contrib import admin
from django.urls import path
from salesintegrate.views import oauth,index,oauth_callback

urlpatterns = [
    path("",index,name="home"),
    path("oauth/", oauth, {"domain": "login"}, name="oauth"),
    path("oauth/sandbox", oauth, {"domain": "test"}, name="oauth-sandbox"),
    path("oauth/callback",oauth_callback,name="oauth_callback")
]