from app import fetch_yelp_data, process_yelp_data, search_google_places, extract_google_details, businesses, create_business_df

# Define search parameters for Yelp and Google
yelp_search_params = {
    'location': "34.052235,-118.243683",
    'term': "real estate",
    'radius': 20000,
    'limit': 50
}

google_search_params = {
    'location': "34.052235,-118.243683",
    'radius': 20000,
    'type': "real_estate_agency"
}

# Define the fields to return
return_fields = ['name', 'formatted_phone_number', 'formatted_address', 'rating']


# Fetch and process Yelp data
yelp_response = fetch_yelp_data(yelp_search_params)
if yelp_response.status_code == 200:
    process_yelp_data(yelp_response, return_fields)

# Search for Google places and extract details
google_place_ids = search_google_places(google_search_params)
extract_google_details(google_place_ids, return_fields)

#initialize df
business_df =create_business_df(businesses)

# Print the businesses list to verify the results
#for business in businesses:
    #print(vars(business))

print(business_df)
