from settings import *
from flask import Flask, request, jsonify
import requests
from requests.exceptions import RequestException
import pandas as pd
from storage import DBStorage
from urllib.parse import quote_plus
from datetime import datetime

''' Define search_api() to connect API endpoint & 
    return search results 
    Each page contains 10 results '''
''' Define search_api() to connect API endpoint & 
    return search results 
    Each page contains 10 results '''
def search_api(query, pages=int(RESULT_COUNT/10)):

    results = []

    for i in range(0, pages):
        ''' start defines 1st record on each page'''
        start = i * 10 + 1

        ''' Format search url 
            'quote_plus()' replaces invalid characters with valid url characters
            'start' defines which page we need results from
        '''
        url = SEARCH_URL.format(
            key = SEARCH_KEY,
            cx = SEARCH_ID,
            query = quote_plus(query),
            start = start
        )

        ''' Check formatted url '''
        print(url)

        ''' Make a request to google custom search api '''
        response = requests.get(url)

        ''' Decode json response '''
        ''' Make a request to google custom search api '''
        response = requests.get(url)

        ''' Decode json response '''
        data = response.json()

        ''' Get items from data & append to results (list of dic) '''
        results += data["items"]
        ''' Get items from data & append to results (list of dic) '''
        results += data["items"]

    ''' Create DataFrame with results '''
    res_df = pd.DataFrame.from_dict(results)
    ''' Create DataFrame with results '''
    res_df = pd.DataFrame.from_dict(results)

    ''' Add a New Column (rank) '''
    res_df["rank"] = list(range(1, res_df.shape[0] + 1))
    ''' Creates a sequence from 1 to the number of rows.      
        Example for 2 rows: [1, 2].
        Assigns this list to a new column rank.
    '''

    ''' Reorder Columns '''
    res_df = res_df[["link", "rank", "snippet", "title"]]
    ''' Reorders the columns to match the specified order
        If there are additional columns in res_df, they are excluded from the new DataFrame.
    '''
    
    ''' Add a New Column (rank) '''
    res_df["rank"] = list(range(1, res_df.shape[0] + 1))
    ''' Creates a sequence from 1 to the number of rows.      
        Example for 2 rows: [1, 2].
        Assigns this list to a new column rank.
    '''

    ''' Reorder Columns '''
    res_df = res_df[["link", "rank", "snippet", "title"]]
    ''' Reorders the columns to match the specified order
        If there are additional columns in res_df, they are excluded from the new DataFrame.
    '''
    
    return res_df


''' Define scrape_page() that takes in a list of links & 
    returns full html of pages '''
''' Define scrape_page() that takes in a list of links & 
    returns full html of pages '''
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
    columns = ["query", "rank", "link", "title", "snippet", "html", "created"] 

    ''' Init storage class ''' 
    storage = DBStorage()  

    ''' Site to search '''
    query = query + " site:stackoverflow.com"

    ''' Site to search '''
    query = query + " site:stackoverflow.com"

    ''' Check if query has been run already '''
    stored_results = storage.query_results(query)
    ''' Skip if no results found '''
    if stored_results.shape[0] > 0:
        """ Return results from database """  
        ''' Convert sqlite timestamps to pandas datetime objects '''
        stored_results["created"] = pd.to_datetime(stored_results["created"])
        return stored_results[columns]

    print("[search] received:", query)
    df_before = storage.query_results(query)
    print("[search] rows in DB before fetch:", len(df_before))
    ''' Find results with search_api(query) '''
    results = search_api(query)

    ''' Scrape html from pages and store in dataframe '''
    results["html"] = scrape_page(results["link"])

    ''' Remove results with empty html '''

    ''' Remove results with empty html '''
    results = results[results["html"].str.len() > 0].copy()

    """ Assign columns """
    results["query"] = query

    ''' Convert to sqlite time format '''
    results["created"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    ''' Remove extra columns & put columns in right order '''
    results = results[columns]

    ''' Iterate over results df & use insert_row() to insert each row into db '''
    results.apply(lambda x: storage.insert_row(x), axis=1)

    df_after = storage.query_results(query)
    print("[search] rows in DB after inserts:", len(df_after))
    return jsonify({"results": df_after.to_dict(orient="records")})

    return results