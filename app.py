from flask import Flask, request, jsonify
from flask_cors import CORS
from search import search # Import Search() we created
import html # To render html
from filter import Filter # Import filter class
from storage import DBStorage 


# Init Flask app
app = Flask(__name__)

# Enable CORS
CORS(app)

# Search endpoint
@app.route("/search", methods=["POST"])
def search_endpoint():
    try:
        # Extract search query from the JSON payload
        data = request.get_json()
        query = data.get("query", "")
        
        if not query:
            return jsonify({"error": "Query is required"}), 400

        # Perform search and filtering
        results = search(query)
        fi = Filter(results)  # Initialize filter
        results = fi.filter()  # Re-rank results

        # Convert filtered results to a list of dictionaries
        results_dict = results.to_dict(orient="records")
        return jsonify({"results": results_dict}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    

