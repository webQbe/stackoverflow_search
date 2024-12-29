from settings import *
import requests
from requests.exceptions import RequestException
import pandas as pd
from storage import DBStorage
from urllib.parse import quote_plus
from datetime import datetime

''' Define search_api() to connect to Stack Exchange API and return search results '''
def search_api(query, pages=int(RESULT_COUNT/10)):

    results = []

    for page in range(1, pages + 1):  # Pages start from 1 for Stack Exchange API
        ''' Format search url '''
        params = {
            "order": "desc",
            "sort": "relevance",
            "q": quote_plus(query), # format query string
            "site": SITE,
            "page": page,
            "pagesize": 10,
            "key": STACKEXCHANGE_API_KEY
        }

        # Make a request to Stack Exchange API
        response = requests.get(STACKEXCHANGE_SEARCH_URL, params=params)
        response.raise_for_status()  # Raise exception for HTTP errors
        data = response.json()

        # Get items from data & append to results
        if "items" in data:
            results += data["items"]

    
    if results:
        # Create DataFrame with results
        res_df = pd.DataFrame(results)

        # Select relevant columns
        res_df = res_df[["title", "link", "score"]]

        # Add rank column
        # Assign rank to each row, starting at 1 and incrementing by 1 for each result
        res_df["rank"] = list(range(1, res_df.shape[0] + 1))

        # Columns are reordered so that rank appears first
        res_df = res_df[["rank", "title", "link", "score"]]

    else:
        # If results is empty or None, 
        # an empty DataFrame is created with predefined columns
        res_df = pd.DataFrame(columns=["rank", "title", "link", "score"])

    return res_df


''' Define scrape_page() that takes in a list of links & returns full html of pages '''
def scrape_page(links):

    html = []

    ''' Iterate through links list '''
    for link in links:

        try:
            ''' Download page html '''
            data = requests.get(link, timeout=5)

            ''' Append text from data to html list '''
            html.append(data.text)

        except RequestException:
            ''' When html can't be downloaded properly,
              assume html is empty '''
            html.append("")

    ''' Return updated list'''
    return html


''' Define search() to take query & 
    check if we already searched for something & stored it to db.
    If we did, it will return results from db, 
    if we didn't it will query API, get new results, format, save to db and then return.
'''
def search(query):
    ''' Pass columns into storage '''
    columns = ["query", "rank", "link", "title", "snippet", "html", "created"] 

    ''' Init storage class ''' 
    storage = DBStorage()  

    ''' Check if query has been run already '''
    stored_results = storage.query_results(query)
    ''' Skip if no results found '''
    if stored_results.shape[0] > 0:
        """ Return results from database """  
        ''' Convert sqlite timestamps to pandas datetime objects '''
        stored_results["created"] = pd.to_datetime(stored_results["created"])
        return stored_results[columns]

    ''' Find results with search_api(query) '''
    results = search_api(query)

    ''' Scrape html from pages and store in dataframe '''
    results["html"] = scrape_page(results["link"])
    # Filter rows with with empty html column
    results = results[results["html"].str.len() > 0].copy()
    ''' [results["html"].str.len() > 0] 
        Creates a boolean mask where True indicates rows with non-empty html content.
        With .copy(), a new independent DataFrame is created, ensuring no link to the original.
    '''

    """ Assign columns """
    results["query"] = query

    ''' Convert to sqlite time format '''
    results["created"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    ''' Remove extra columns & put columns in right order '''
    results = results[columns]

    ''' Iterate over results df & use insert_row() to insert each row into db '''
    results.apply(lambda x: storage.insert_row(x), axis=1)

    return results