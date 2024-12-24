from flask import Flask, request, jsonify
from googleSearch import scrape_google
from bingScrapper import scrape_bing
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("API_KEY")

def require_api_key(func):
    def wrapper(*args, **kwargs):
        api_key = request.headers.get('x-api-key')
        if api_key and api_key == API_KEY:
            return func(*args, **kwargs)
        else:
            return jsonify({"error": "Unauthorized"}), 401
    wrapper.__name__ = func.__name__
    return wrapper

@app.route('/api/google_search', methods=['POST'])
@require_api_key
def api_google_search():
    data = request.get_json()
    query = data.get('query') if data else None
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400

    results = scrape_google(query)
    return jsonify(results)

@app.route('/api/bing_search', methods=['POST'])
@require_api_key
def api_bing_search():
    data = request.get_json()
    query = data.get('query') if data else None
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400

    results = scrape_bing(query)
    return jsonify(results)

if __name__ == '__main__':
    port = 5000  # Default port
    app.run(debug=True, port=port)
