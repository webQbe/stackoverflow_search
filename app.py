from flask import Flask, request, jsonify
from search import search # Import Search() we created
import html # To render html
from storage import DBStorage 

# Run Flask server with  'flask --debug run --port 5001'

# Init Flask app
app = Flask(__name__)


head = """
    <style>
        /* Style the search results */
        .site {
            font-size: .8rem;
            color: green;
        }

        .score {
            font-size: 0.9rem;
            color: gray;
            margin-bottom: 30px;
        }

        .rel-button {
            cursor: pointer;
            color: blue;
        }
    </style>
    <script>

        // Define relevant() function, which sends a POST request to the /relevant endpoint with the search query and link as a JSON payload.

        const relevant = function(query, link){
            fetch("/relevant", {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    "query" : query,
                    "link" : link,
                })
            });
        }
    </script>
"""


# Search Form
search_template = head + """
    <form action="/" method="post">
        <input type="text" name="query">
        <input type="submit" value="Search">
    </form>
"""

# Generate HTML for each search result
result_template =  """
    <!-- onclick attribute calls the relevant() function with 
         the corresponding query and link. -->
    <p class="site">{rank}: {link} 
        <span class="rel-button" 
                onclick='relevant("{query}", "{link}");'>Relevant
        </span>
    </p>
    <a href="{link}">{title}</a>
    <p class="score">{score} Votes</p>
"""

def show_search_form():
    return search_template


def run_search(query):
    results = search(query)

    rendered = search_template

    # Iterate across rows in results
    for index, row in results.iterrows():
        # Append to rendered
        rendered += result_template.format(**row) 
        ''' Pass current row of data to the template, 
             so placeholder text in html will be replaced.
        '''
    # Return search results page
    return rendered


# Create a new route (127.0.0.1:5001)
# for GET & POST requests 
@app.route("/", methods=["GET", "POST"]) # URL on web server 
def search_form():
    # Search for something if it's a POST request
    if request.method == "POST":
        # Get query from request data 
        query = request.form["query"] 
        return run_search(query)
    else:
        return show_search_form()
    
    
# Endpoint for /relevant
@app.route("/relevant", methods=["POST"])
def mark_relevant():
    # Extract query and link from the JSON payload
    data = request.get_json()
    query = data["query"]
    link = data["link"]
    # Init a new instance of the DBStorage class
    storage = DBStorage() 
    # Set relevance score of the query and link to 10
    storage.update_relevance(query, link, 10)
    # Responds with a JSON object indicating success
    return jsonify(success=True)

