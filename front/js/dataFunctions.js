
export const getSearchTerm = () => {

    // Select search input value & trim
    const rawSearchTerm = document.getElementById("search").value.trim();

    // Look for 2 or more repeated spaces within search phrase
    const regex = /[ ]{2,}/gi;

    // Replace repeated spaces with single space
    const searchTerm = rawSearchTerm.replaceAll(regex, " ");

    // Returned refined search term
    return searchTerm;

}

// Export results array
export const retrieveSearchResults = async (searchTerm) => {

    if (!searchTerm) return [];

    // Pass search string to get search results
    const searchResults = await requestData(searchTerm);

    // Defensive: ensure array
    if (!searchResults || !Array.isArray(searchResults)) return [];

    // Convert raw results into the objects the UI expects (rank, title, snippet, link)
    const resultArray = processResults(searchResults);

    return resultArray; 

}

const getSearchString = (searchTerm) => {

    // Set max character length of response
    const maxChars = getMaxChars();

    const baseUrl = "http://127.0.0.1:5001/search"; // Flask server URL
    const searchString = `${baseUrl}?query=${encodeURIComponent(searchTerm)}`;
    return searchString

}

const getMaxChars = () => {

    // Get viewport width value
    const width = window.innerWidth || document.body.clientWidth;

    let maxChars;
    // Decide max characeters based on screen width
    if (width < 414) maxChars = 65;
    if (width >= 414 && width < 1400) maxChars = 100;
    if (width >= 1400 ) maxChars = 130;
    return maxChars;
}

const requestData = async (searchTerm) => {
    const baseUrl = "http://127.0.0.1:5001/search"; // Flask server URL

    try {
        console.log("requestData: about to POST", searchTerm, new Date().toISOString());
        const response = await fetch(baseUrl, {
            method: "POST", // Use POST method
            headers: {
                "Content-Type": "application/json", // Set headers
            },
            body: JSON.stringify({ query: searchTerm }), // Send search term as JSON
        });
        console.log("requestData: fetch returned", response.status, new Date().toISOString());



        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json(); // Parse JSON
        const searchResults = data.results;  // Access the "results" array

        // If results isn't an array
        if (!Array.isArray(searchResults)) {
            console.error("Expected an array but got:", searchResults);
            return [];
        }

        // Return raw results (let caller process into UI shape)
        return searchResults;
    } 
    catch (error) {
        console.error("Error fetching search results:", error);
        return [];
    }
};


const processResults = (searchResults) => {

    const resultArray = searchResults.map(result => ({
        rank: result.rank,
        title: result.title,
        snippet: result.snippet,
        link: result.link
    }));

    console.log("Processed search results:", resultArray);

    // After looping through results
    return resultArray;
} 