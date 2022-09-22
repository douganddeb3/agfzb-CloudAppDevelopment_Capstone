from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .models import CarDealer, CarMake, CarModel, DealerReview
# from .restapis import related methods
from .restapis import get_dealers_from_cf, get_request, get_dealers_by_state, get_dealer_reviews_from_cf, get_dealer_by_id
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
# def about(request):
# ...
def about(request):
    if request.method == "GET":
        return render(request,'djangoapp/about.html')

# Create a `contact` view to return a static contact page
#def contact(request):
def contact(request):
    if request.method == "GET":
        return render(request,'djangoapp/contact.html')
# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return redirect('djangoapp:index')
        else:
            # If not, return to login page again
            return render(request, 'djangoapp/user_login.html', context)
    else:
        return render(request, 'djangoapp/user_login.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to list view
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/register.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/register.html', context)


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/dnel_djangoserver-space/dealership-package/get-dealership"
        # https://6c1cc8db.us-south.apigw.appdomain.cloud/api/dealership"
        # Get dealers from the URL
        dealer_list = get_dealers_from_cf(url)
        # Concat all dealer's short name
        # dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        #return HttpResponse(dealer_names)
        context={}
        dealers_temp=[]
        for dealer in dealer_list:
            dealers_temp.append([{"city":dealer.city},
                     {"state":dealer.state},
                     {"full_name":dealer.full_name},
                     {"id": dealer.id}])
        context['dealers']=dealers_temp   
        
           
  
        return render(request, 'djangoapp/index.html', {'dealers':context['dealers']})


def get_dealerships_by_state(request, st):
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/dnel_djangoserver-space/dealership-package/get-dealership"
        # Get dealers from the URL
        dealerships = get_dealers_by_state(url,st)
        # Concat all dealer's short name
        context={}
        dealers_temp=[]
        for dealer in dealerships:
            print(dealer.city)
            dealers_temp.append([{"city":dealer.city},
                     {"state":dealer.state},
                     {"full_name":dealer.full_name},
                     {"id": dealer.id}])
        context['dealers']=dealers_temp  
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        #return HttpResponse(dealer_names)
        return render(request, 'djangoapp/index.html', {'dealers':context['dealers']})

def get_dealerships_by_state_abbr(request):
    if request.method == "POST":
        state=request.POST['state'].upper()
        st={}
        # A dict is being passed 
        st['st']=state
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/dnel_djangoserver-space/dealership-package/get-dealership"
        # Get dealers from the URL
        dealerships = get_dealers_by_state(url,st)
        # Concat all dealer's short name
        context={}
        dealers_temp=[]
        for dealer in dealerships:
            print(dealer.city)
            dealers_temp.append([{"city":dealer.city},
                     {"state":dealer.state},
                     {"full_name":dealer.full_name},
                     {"id": dealer.id}])
        context['dealers']=dealers_temp  
        print(f'dealers_temp: {dealers_temp}')
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        #return HttpResponse(dealer_names)
        return render(request, 'djangoapp/index.html', {'dealers':context['dealers']})


def get_dealerships_by_id(request, dealerId):
    if request.method == "GET":
        url = "https://6c1cc8db.us-south.apigw.appdomain.cloud/api/dealership"    
        dealer_details = get_dealer_by_id(url, dealerId)
        return HttpResponse(dealer_details)

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    # dealer_id = "1"
    print(type(dealer_id))
    if request.method == "GET":
        print("did we get here?")
        url = "https://6c1cc8db.us-south.apigw.appdomain.cloud/dealer/get_reviews"
        dealer_reviews = get_dealer_reviews_from_cf(url, dealer_id)
        return HttpResponse(dealer_reviews)
        
# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

