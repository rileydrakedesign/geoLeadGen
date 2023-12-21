from flask import Flask, request, jsonify
from app.app import fetch_yelp_data, process_yelp_data, search_google_places, extract_google_details, create_business_df, businesses
from possible_business_types import business_types


app = Flask(__name__)

@app.route('/search', methods=['POST'])
def search_businesses():
    data = request.json
    search_params_data = data.get('search_params', {}) 
    search_params = {
        'location': search_params_data.get('location'),
        'yelp_type': search_params_data.get('yelp_type'),
        'radius': search_params_data.get('radius'),
        'google_type': search_params_data.get('google_type')
    }

    return_fields = data.get('return_fields', [])

    google_types = []
    yelp_types = []


    descriptors = data.get('descriptors', [])

    for descriptor in descriptors:
        if descriptor in business_types:
            # Append corresponding Yelp and Google types to their respective lists
            yelp_types.append(business_types[descriptor]['yelp'])
            google_types.append(business_types[descriptor]['google'])




    yelp_data = fetch_yelp_data(search_params)
    yelp_processed = process_yelp_data(yelp_data, return_fields)
    google_place_ids = search_google_places(search_params)
    google_business_details = extract_google_details(google_place_ids, return_fields)

    business_df = (create_business_df(businesses))

    return business_df.to_json(orient='records')



if __name__ == '__main__':
    app.run(debug=True, host ='0.0.0.0', port=5001)  # Use debug=False for production
