// Export function
export const setSearchFocus = () => {

    // Select search input & focus
    document.getElementById("search").focus();
}

// Make Clear Text Button X Visible
export const showClearTextButton = () => {

    // Select text input
    const search = document.getElementById("search");

    // Select clear X button
    const clear = document.getElementById("clear");

    
    if(search.value.length){

        // Remove .none class from clear button
        clear.classList.remove("none");

        // Add .flex class
        clear.classList.add("flex");

    } else {

        clear.classList.add("none");
        clear.classList.remove("flex");
        
    }



};

export const clearSearchText = (event) => {

    event.preventDefault(); 
    
    // Clear search input
    document.getElementById("search").value = "";

    // Hide clear X button
    const clear = document.getElementById("clear");
    clear.classList.add("none");
    clear.classList.remove("flex");

    // Focus search input
    setSearchFocus();

};

export const clearPushListener = (event) => {

    // Check if Enter OR Space key is pressed
    if(event.key === "Enter" || event.key === " "){

        event.preventDefault(); // Prevent typing space or enter

        // Call click() on clear X button
        document.getElementById("clear").click();

    }

};