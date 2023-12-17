from flask import Flask, request, jsonify



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

    return jsonify(search_params, return_fields)


if __name__ == '__main__':
    app.run(debug=True, host ='0.0.0.0', port=5001)  # Use debug=False for production
