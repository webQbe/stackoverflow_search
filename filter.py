''' Filtering & Re-ranking results '''
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from settings import *


# Get text inside html
def get_page_content(row):
    soup = BeautifulSoup(row["html"])
    text = soup.get_text()
    return text


# Create Filter class
class Filter():
    # Pass list of results
    def __init__(self, results):
        # Pass in a dataframe of results
        self.filtered = results.copy()

        '''The results.copy() method creates a shallow copy of the results object.
            The self.filtered attribute stores this copied data.
            This ensures that self.filtered is an independent copy of results. Modifications to self.filtered won't affect the original results object passed to the constructor, and vice versa.
        '''

    # Setup Content Filter
    def content_filter(self):
        # Apply get_page_content() to each row of filtered df  
        page_content = self.filtered.apply(get_page_content, axis=1)

        # Split extracted text (x) into words & calculate word count
        word_count = page_content.apply(lambda x: len(x.split(" ")))

        # Normalize word count by 
        # dividing it by the median word count across all results.
        word_count /= word_count.median()

        # Assign RESULT_COUNT value to results where the normalized word count is less than or equal to 0.5
        # Pages with a low word count (below half the median) are penalized by increasing their rank (bad results have higher rank values)
        word_count[word_count <= .5] = RESULT_COUNT 

        # For all other results, sets the value to 0
        # Pages with a higher word count are not penalized
        word_count[word_count != RESULT_COUNT] = 0

        # Modify the existing rank column in the filtered DataFrame by adding the adjusted word count values.
        self.filtered["rank"] += word_count


    def filter(self):
        # Adjust rank column in the filtered DataFrame based on the word count
        self.content_filter()

        # Sort filtered DataFrame by the rank column in ascending order
        self.filtered = self.filtered.sort_values("rank", ascending=True)

        # Rounds the rank column to the nearest integer
        self.filtered["rank"] = self.filtered["rank"].round()

        return self.filtered