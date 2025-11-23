export const clearSearchResults = () => {

    // Select #searchResults container
    const parentElement = document.getElementById("searchResults");

    // Select last element
    let lastChild = parentElement.lastElementChild;

    while(lastChild){
        
        parentElement.removeChild(lastChild);

        // Re-assign next lastChild when 
        // previous lastChild is removed
        lastChild = parentElement.lastElementChild;

        /* This loop will continue until all #searchResults elements are deleted */

    }
};


// Pass resultArray to Build Search Results
export const buildSearchResults = (resultArray) => {

    resultArray.forEach(result => {

        /* Define variables for current result */

        // Create a result item
        const resultItem = createResultItem(result);

        // Create a div element for current result
        const resultContents = document.createElement("div");

        // Add a class to resultContents div
        resultContents.classList.add("resultContents");

        // Skip if result has no image
        if(result.img){
            const resultImage = createResultImage(result);

            // Append resultImage to resultContents div
            resultContents.append(resultImage);
        }

        const resultText = createResultText(result);

        // Append resultText to resultContents div 
        resultContents.append(resultText);

        // Append resultContents div to resultItem
        resultItem.append(resultContents);

        // Select searchResults div
        const searchResults = document.getElementById("searchResults");

        // Append resultItem to searchResults div
        searchResults.append(resultItem);

    });

};

// Define Helper Functions

const createResultItem = (result) => {

    // Create resultItem div
    const resultItem = document.createElement("div");
    // Add class
    resultItem.classList.add("resultItem");

    // Create resultTitle div
    const resultTitle = document.createElement("div");
    resultTitle.classList.add("resultTitle");

    // Create a tag
    const link = document.createElement("a");

    // Add link
    link.href = result.link;

    // Set result title as link text
    link.textContent = result.rank + ") " + result.title;

    // Open link in a new tab
    link.target = "_blank";

    // Append a tag to resultTitle div
    resultTitle.append(link);

    // Append resultTitle div to resultItem div
    resultItem.append(resultTitle);

    return resultItem;

};

const createResultImage = (result) => {

    const resultImage = document.createElement("div");
    resultImage.classList.add("resultImage");

    // Create img tag
    const img = document.createElement("img");
    img.src = result.img; // Set image url from result as image source
    img.alt = result.title; // Set result title as image alt text

    // Append img to div
    resultImage.append(img);

    return resultImage;

};

const createResultText = (result) => {

    const resultText = document.createElement("div");
    resultText.classList.add("resultText");

    // Create a <p> element
    const resultDescription = document.createElement("p");
    resultDescription.classList.add("resultDescription");

    // Set text from result as resultDescription text
    resultDescription.textContent = result.snippet;

    // <p> element to resultText <div>
    resultText.append(resultDescription);

    return resultText;
     
};

export const clearStatsLine = () => {

    // Clear stats Element Text
    document.getElementById("stats").textContent = "";

};

export const setStatsLine = (numberOfResults) => {

    // Select stats div element
    const statLine = document.getElementById('stats'); 

    if(numberOfResults){
        // resultArray.length > 0

        statLine.textContent = `Displaying ${numberOfResults} results.`;

    } else {

        statLine.textContent = `Sorry! No results.`;

    }

};