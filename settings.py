SEARCH_KEY = "MY_SEARCH_API_KEY"
SEARCH_ID = "MY_SEARCH_ID"
COUNTRY = "lk"

''' Create URL to Call Get Search Results 
    by Pass-in API Key, ID, Query, Result Page, & Country'''
SEARCH_URL = "https://www.googleapis.com/customsearch/v1?key={key}&cx={cx}&q={query}&start={start}&gl=" + COUNTRY

''' Define Result Count Per Search '''
RESULT_COUNT = 20