from django.shortcuts import render
from django.template import Template, Context
from ViralPost.settings import TEMPLATE_DIR
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
from django.shortcuts import redirect
import urllib
from httplib2 import Http
import json
import requests
from BeautifulSoup import BeautifulSoup

address = []
name = []


# Create your views here.
def home(request):
    html = open(TEMPLATE_DIR+"/homepage.html").read()
    temp = Template(html)
    page = temp.render(Context({}))
    return HttpResponse(page)

def google_login(request):
    token_request_uri = "https://accounts.google.com/o/oauth2/auth"
    response_type = "code"
    client_id = '872948993591-gbvhk572pvknl7usc2feftj8cljfmnas.apps.googleusercontent.com'
    redirect_uri = 'http://localhost:8080/callback'
    scope = "https://www.google.com/m8/feeds/"
    url = "{token_request_uri}?response_type={response_type}&client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}".format(
        token_request_uri = token_request_uri,
        response_type = response_type,
        client_id = client_id,
        redirect_uri = redirect_uri,
        scope = scope)
    return HttpResponseRedirect(url)

def google_authenticate(request):
    print 'here'
    parser = Http()
    login_failed_url = '/'
    if 'error' in request.GET or 'code' not in request.GET:
        return HttpResponseRedirect('{loginfailed}'.format(loginfailed = login_failed_url))

    access_token_uri = 'https://accounts.google.com/o/oauth2/token'
    redirect_uri = 'http://localhost:8080/callback'
    params = urllib.urlencode({
        'code':request.GET['code'],
        'redirect_uri':redirect_uri,
        'client_id':'872948993591-gbvhk572pvknl7usc2feftj8cljfmnas.apps.googleusercontent.com',
        'client_secret':'au1LWhZY5nRZ6yeUzj-LGK-d',
        'grant_type':'authorization_code'
    })
    headers={'content-type':'application/x-www-form-urlencoded'}
    resp, content = parser.request(access_token_uri, method = 'POST', body = params, headers = headers)
    token_data = json.loads(content)
    resp, content = parser.request("https://www.googleapis.com/oauth2/v1/userinfo?access_token={accessToken}".format(accessToken=token_data['access_token']))
    google_profile = json.loads(content)
    return HttpResponseRedirect('http://localhost:8080/callback/')

def contact(request):
    params = {
    'client_id':'872948993591-gbvhk572pvknl7usc2feftj8cljfmnas.apps.googleusercontent.com',
    'client_secret':'au1LWhZY5nRZ6yeUzj-LGK-d',
    'code': request.GET['code'],
    'redirect_uri': 'http://localhost:8080/callback',
    'grant_type': 'authorization_code'
    }
    headers = {'accept': 'application/json'}
    url = 'https://www.googleapis.com/oauth2/v3/token'
    r = requests.post(url, params=params, headers=headers)
    data = r.json()
    access_token = data[u'access_token']
    contacts = requests.get('https://www.google.com/m8/feeds/contacts/default/full',headers = {'authorization': 'Bearer '+access_token,'accept': 'application/json'})
    soup = BeautifulSoup(contacts.content)
    item = soup.findAll('gd:email')
    names = soup.findAll('title')
    for type in names:
        if(type['type'] == "text"):
            if(type.getText()[:4] == "http"):
                name.append(" ")
            else:
                name.append( type.getText())
    for s in item:
        address.append(s['address'])
    return HttpResponseRedirect('/contacts')

def print_contact(request):
    data = []
    html = open(TEMPLATE_DIR+"/contacts.html").read()
    temp = Template(html)
    for i in range(len(address)):
        if (name[i+1]!=" " and name[i+1]!=""):
            print name[i+1],i
            data.append(name[i+1]+"         "+address[i])
    page = temp.render(Context({'data':data}))
    return HttpResponse(page)
