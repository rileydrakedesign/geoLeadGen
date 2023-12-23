from flask import Flask, request, jsonify
from app.app import fetch_yelp_data, process_yelp_data, search_google_places, extract_google_details, create_business_df, businesses
from possible_business_types import business_types


app = Flask(__name__)

def map_business_types(user_selected_type):
    if user_selected_type in business_types:
        yelp_type = business_types[user_selected_type]['yelp']
        google_type = business_types[user_selected_type]['google']
    else:
        # Handle unknown types, maybe default or error
        yelp_type = None
        google_type = None
    return yelp_type, google_type

@app.route('/search', methods=['POST'])
def search_businesses():
    data = request.json


    user_selected_type = data.get('business_type', '')
    search_params = data.get('search_params', {}) 
    return_fields = data.get('return_fields', [])

    yelp_type, google_type = map_business_types(user_selected_type)

    if yelp_type and google_type:
        search_params['yelp_type'] = yelp_type
        search_params['google_type'] = google_type
    else:
        # Handle error or unknown type
        return jsonify({'error': 'Invalid business type'}), 400


    yelp_data = fetch_yelp_data(search_params)
    yelp_processed = process_yelp_data(yelp_data, return_fields)
    google_place_ids = search_google_places(search_params)
    google_business_details = extract_google_details(google_place_ids, return_fields)

    business_df = (create_business_df(businesses))

    return business_df.to_json(orient='records')



if __name__ == '__main__':
    app.run(debug=True, host ='0.0.0.0', port=5001)  # Use debug=False for production
