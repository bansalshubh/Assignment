from django.shortcuts import render,HttpResponse,redirect
from requests_oauthlib import OAuth2Session
from salesintegrate.oauth import OAuth
from .models import SalesUser
import urllib.request
from django.contrib.auth import get_user_model,login
import requests

client_id = '3MVG9pRzvMkjMb6nqNOaTvQyL3GfRolyQIB2rCE7F7BxrGTwyEQteLqwqu540BDxxs8MSNwh3W9XPWSLfCha4'
secret = 'Your Secret Key'
redirect_uri = "http://localhost:8000/oauth/callback"
scope = "full refresh_token"

def index(request):
    return render(request,'index.html')

def oauth(request,domain="login"):
    url = f"https://{domain}.salesforce.com/services/oauth2/authorize"
    url_args = {
        "client_id": client_id,
        
        "redirect_uri": redirect_uri,
        "response_type": "code",
        # "scope": scope,
        # "state": domain,
    }
    args = urllib.parse.urlencode(url_args)
    url = f"{url}?{args}"
    response = redirect(url)
    state = request.GET.get("state")
    print(response)
    return response

def oauth_callback(request):
    code = request.GET.get("code")
    state = request.GET.get("state")
    print(state)
    print("hello")
    url = "https://login.salesforce.com/services/oauth2/token"
    if not code:
        return redirect("/")
    data = {
        "client_id": client_id,
        "client_secret": secret,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
        "code": code,
    }
    response = requests.post(url, data)
    print(response)
    oauths = OAuth(response.json())
    print(oauths)
    user = get_or_createUser(oauths)
    print(user)
    login(request, user)
    return HttpResponse("Hello")


def get_or_createUser(oauth: OAuth):
    """
    Accepts an OAuth object and retrieves a User, creating one if it doesn't exist
    """
    # print("getorcrreate")
    salesforce_id = oauth.id
    email = oauth.email
    fname = oauth.first_name
    lname = oauth.last_name
    username = oauth.username
    SalesUser = get_user_model()
    user = SalesUser.objects.filter(username=salesforce_id).first()

    if not user:
        user = SalesUser.objects.create_user(salesforce_id, fname,lname,email=email,username=username)

    return user
