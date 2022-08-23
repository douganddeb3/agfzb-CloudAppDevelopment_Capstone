import requests
import json
# import related models here
from .models import CarDealer, CarModel, CarMake, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    
    if 'st' in kwargs:    
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs['st'])
        # elif kwargs['dealerId']:
        #     response = requests.get(url, headers={'Content-Type': 'application/json'},
        #                                 params=kwargs['dealerId']) 
    elif 'dealerId' in kwargs:
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                            params=kwargs['dealerId'])
    elif 'dealer_id' in kwargs:
        print(kwargs.get('dealer_id').replace("dealer_id","dealerId",2))
        dealerId=kwargs.get('dealer_id').replace("dealer_id","dealerId")
        print(f'dealerId is {dealerId}')
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                            params= dealerId)
    else: 
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                            params='')          
    json_data = json.loads(response.text)
    return json_data

def get_dealers_from_cf(url):
    results = [] 
    # Call get_request with a URL parameter
    json_result = get_request(url)
    print('JSON RESULT CF')
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["body"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],state=dealer_doc["state"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

def get_dealer_by_id(url, dealerId):
    results = [] 
    # Call get_request with a URL parameter
    json_result = get_request(url, dealerId=dealerId)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["body"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],state=dealer_doc["state"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results



def get_dealers_by_state(url, st):
    results = [] 
    # Call get_request with a URL parameter
    json_result = get_request(url,st=st)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["body"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],state=dealer_doc["state"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, dealer_id):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
    results=[]
    dealerId = {"dealer_id":dealer_id}
    print(f'DEALERID= {dealerId}')
    json_result = get_request(url, dealer_id=dealer_id)

    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["body"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = DealerReview(dealership=dealer_doc["dealership"], name=dealer_doc["name"], purchase=dealer_doc["purchase"],
                                   review=dealer_doc["review"], purchase_date=dealer_doc["purchase_date"], car_make=dealer_doc["car_make"],
                                   car_model=dealer_doc["car_model"],car_year=dealer_doc["car_year"],
                                   id=dealer_doc["id"])
            print(f'dealer_obj is {dealer_obj}')
            dealer_obj.sentiment = analyze_review_sentiments(dealer_obj.review)
            results.append(dealer_obj)

    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(dealerReview):

    print(f'dealelReview is {dealerReview}')
    url = "https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/54a42847-84c8-479c-be82-0f99e213d067"
    api_key = "0d994aayHKIY2j2fUUcxvqGslY4UTwWjxoX9x_Ae0OuD"
    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2021-08-01',authenticator=authenticator)
    natural_language_understanding.set_service_url(url)
    response = natural_language_understanding.analyze( text=dealerReview+" hello hello hello",features=Features(sentiment=SentimentOptions(targets=[text+"hello hello hello"]))).get_result()
    label=json.dumps(response, indent=2)
    label = response['sentiment']['document']['label']
    print(f('label is {label}'))
