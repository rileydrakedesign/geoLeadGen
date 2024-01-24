# Import necessary libraries
import numpy as np
import pandas as pd
import googlemaps
import requests
import json
from openpyxl import load_workbook
from dotenv import load_dotenv
import os
import pprint

# ---- API KEYS ----
load_dotenv()

GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
YELP_API_KEY = os.environ.get('YELP_API_KEY')


# Define the base URL endpoints for Yelp API
YELP_BUSINESS_SEARCH_ENDPOINT = "https://api.yelp.com/v3/businesses/search"
# Define the headers for Yelp API requests (used for authentication)
HEADERS = {'Authorization': 'bearer %s' % YELP_API_KEY}

# Initialize the Google Maps client
gmaps = googlemaps.Client(key=GOOGLE_API_KEY)


# Define a Business class to represent each business entity
class Business:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


#list businesses to convert to dataframe later
businesses = []


        


# Function to fetch data from the Yelp API
def fetch_yelp_data(search_params):
    '''search_params will be defined in separate flask python file
    with an api that recieves the frontend data and stores it in var that 
    will be passed into func when ran'''

    # Implement Yelp API fetching logic
    yelp_search = requests.get(url= YELP_BUSINESS_SEARCH_ENDPOINT, params= search_params, headers= HEADERS)

    return yelp_search

    


# Function to process and structure Yelp API data
def process_yelp_data(yelp_data, return_fields):
    # Convert Yelp data into a structured format 
    yelp_data = yelp_data.json()
    #dynamic list of dictionaries for user return fields 
    business_data = [
    {**{field: business.get(field) for field in return_fields}, **{'platform': 'Yelp'}}
    for business in yelp_data['businesses']
    ]


    #create business objects and store in businesses list
    for data in business_data:
        business = Business(**data)
        businesses.append(business)
    
    return businesses


# Function to search for places using Google Maps API
def search_google_places(search_params):
    # Implement logic to search for places on Google Maps for place ids
    nearbySearch = gmaps.places_nearby(location=search_params['location'],
                                        radius=search_params.get('radius'),
                                        type=search_params.get('type'))
    #iterate through results to get place ids for details search
    placeIds = [place['place_id'] for place in nearbySearch['results'] if place.get('business_status') == "OPERATIONAL"]

    return placeIds
    
    


# Function to extract detailed information for each place from Google Maps API
def extract_google_details(place_ids, return_fields):
    # Retrieve details for each place
    for place_id in place_ids:
        place_details = gmaps.place(place_id=place_id, fields=return_fields)

        if 'result' in place_details:
            business_data = {field: place_details['result'].get(field) for field in return_fields}
            business_data['platform'] = "Google"

            business = Business(**business_data)
            businesses.append(business)
        
    return businesses

def create_business_df(businesses_list):
    #check if list is empty and initialize df 
    if businesses_list:
        #turn each object into dictionary 
        business_dicts = [vars(business) for business in businesses_list]
        #store list of dicts in df
        return pd.DataFrame(business_dicts)
    else:
        print("business list is empty")
        return None    

