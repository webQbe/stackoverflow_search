from flask import Flask, request, jsonify
from flask_cors import CORS
from search import search # Import Search() we created
import html # To render html
from filter import Filter # Import filter class
from storage import DBStorage 
import traceback
import pandas as pd
import json


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

            print("[debug] results type:", type(results))
            # optionally print small summary
            try:
                print("[debug] results sample:", getattr(results, "json", lambda: None)() or str(results)[:200])
            except Exception:
                pass

            # Normalize various possible return types into a DataFrame
            results_df = None
            data = None

            # 1) Flask Response (has get_json)
            if hasattr(results, "get_json"):
                # Flask Response: prefer get_json
                try:
                    data = results.get_json(silent=True)  # returns dict/list or None
                except Exception:
                    # fallback to raw data
                    try:
                        data = json.loads(results.get_data(as_text=True))
                    except Exception:
                        data = None

            # 2) requests.Response or similar (has json method)
            elif hasattr(results, "json"):
                json_attr = results.json
                if callable(json_attr):
                    try:
                        data = json_attr()
                    except Exception:
                        # sometimes .json is actually an attr (dict) — handle below
                        data = json_attr
                else:
                    # .json already a dict/list
                    data = json_attr

            # 3) Plain python dict or list
            elif isinstance(results, dict) or isinstance(results, list):
                data = results

            # 4) DataFrame already returned by search()
            elif isinstance(results, pd.DataFrame):
                results_df = results.copy()

            # Convert `data` (if any) into items list and then DataFrame
            if results_df is None:
                items = []
                if isinstance(data, dict):
                    items = data.get("items") or data.get("results") or []
                elif isinstance(data, list):
                    items = data
                # defensive fallback
                if items is None:
                    items = []

                # ensure items is list of dicts
                try:
                    results_df = pd.DataFrame.from_dict(items)
                except Exception:
                    # fallback to empty dataframe
                    results_df = pd.DataFrame()

            # Ensure required columns exist so Filter won't crash
            if "rank" not in results_df.columns:
                results_df["rank"] = range(1, len(results_df) + 1)
            if "html" not in results_df.columns:
                results_df["html"] = ""
                                        

            fi = Filter(results_df) # Initialize filter
            results = fi.filter()  # Re-rank results

            # Convert filtered results to a list of dictionaries
            results_dict = results.to_dict(orient="records")
            return jsonify({"results": results_dict}), 200

        except Exception as exc:
                print("Exception in /search handler:")
                traceback.print_exc()   # <-- prints full traceback to console
                return jsonify({"error": "internal server error", "detail": str(exc)}), 500 
