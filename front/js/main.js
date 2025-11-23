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
    const form = document.getElementById("searchBar");

    if (form) {
        // Defensive: ensure form won't do a native submit
        form.setAttribute("action", "javascript:void(0);");
        form.addEventListener("submit", async (e) => {
            e.preventDefault();
            e.stopImmediatePropagation();   // block other submit handlers
            // Call existing handler
            await submitTheSearch(e);
        }, {capture: true});             // capture early

        // Prevent default submit if Enter pressed in the input (extra safety)
        const input = document.getElementById("search");
        if (input) {
            input.addEventListener("keydown", (ev) => {
            if (ev.key === "Enter") {
                ev.preventDefault();
                ev.stopImmediatePropagation();
                // optionally run search:
                submitTheSearch(new Event('submit'));
            }
            }, {capture:true});
        }
    }

    // Ensure the button is non-submitting
    const button = document.getElementById("searchButton");
    if (button) {
        button.type = "button";
        button.addEventListener("click", submitTheSearch);
    }
}

// Procedural Workflow Function
const submitTheSearch = async (event) => {

    event.preventDefault(); /* Stop page reload */

    clearSearchResults();

    if (event && event.preventDefault) {
        event.preventDefault();
        event.stopPropagation();
        event.stopImmediatePropagation && event.stopImmediatePropagation();
    }

    console.log("submitTheSearch starting", new Date().toISOString());

    // disable submit button to avoid double submits + indicate busy
    const submitBtn = event.submitter || document.querySelector('#searchBar button[type="submit"]');
    if (submitBtn) submitBtn.disabled = true;

    try {
        // WAIT for the async processing to finish before continuing
        await processTheSearch();
        console.log("submit handler attached")
        
    } catch (err) {
        console.error("Search failed:", err);
        // Optionally show user-friendly error UI here
    } finally {
        // re-enable submit button
        if (submitBtn) submitBtn.disabled = false;
        // Focus search input after results processed
        setSearchFocus();
    }

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
    if(Array.isArray(resultArray) && resultArray.length){
        // Build search results
        buildSearchResults(resultArray);

    } 

    // Set stats line (always called, regardless of results)
    // be defensive: if resultArray is undefined, treat length as 0
    setStatsLine(Array.isArray(resultArray) ? resultArray.length : 0);

}

