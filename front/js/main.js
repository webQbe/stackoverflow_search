// Import Functions
import { setSearchFocus, showClearTextButton, clearPushListener, clearSearchText } from "./searchBar.js";
import { getSearchTerm, retrieveSearchResults } from "./dataFunctions.js";
import { buildSearchResults, clearStatsLine, setStatsLine, clearSearchResults } from "./searchResults.js";

// Listen for changes in the document's readiness state
document.addEventListener("readystatechange", event => {

    // Check if the document has reached the complete state
    if (event.target.readyState === "complete"){

        /* readyState is a property of the document that represents its loading status.

           It can have the following values:
                loading: The document is still loading.
                interactive: The document has been loaded and parsed, 
                             but sub-resources (e.g., images, stylesheets) 
                             may still be loading.
                complete: The document and all its sub-resources have finished loading.

        */
        initApp();

    }

    /* The difference is that DOMContentLoaded fires earlier, as soon as the HTML is parsed,
       while readystatechange with complete waits for the entire page to load. */
});


const initApp = () => {

    // Focus search input
    setSearchFocus();

    /* Adding 3 Event Listeners to clear input text */

    // Search input
    const search = document.getElementById("search");
    search.addEventListener("input", showClearTextButton);

    // Clear button 
    const clear = document.getElementById("clear");

    // On click
    clear.addEventListener("click", clearSearchText);
    // On focus & Space OR Enter keydown 
    clear.addEventListener("keydown", clearPushListener);






    // Select form
    const from = document.getElementById("searchBar");

    // Listen for from submit
    from.addEventListener("submit",  submitTheSearch);

}

// Procedural Workflow Function
const submitTheSearch = (event) => {

    event.preventDefault(); /* Stop page reload */

    // Clear previous results
    clearSearchResults();

    // Process search
    processTheSearch();

    // Focus search input
    setSearchFocus();

}


const processTheSearch = async() => {

    //  Call clear stats line()
    clearStatsLine();

    // Get search term
    const searchTerm = getSearchTerm(); 

    if (searchTerm === "") return; // Stop if search term is empty

    // Get results array
    const resultArray = await retrieveSearchResults(searchTerm);
    // Skip if resultArray is empty
    if(resultArray.length){

        // Build search results
        buildSearchResults(resultArray);

    } 

    // Set stats line (always called, regardless of results)
    setStatsLine(resultArray.length);

}

