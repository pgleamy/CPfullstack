/* pseudo code for locationSaveRestore.js 

function saveLocation():
    # Get the current state and scroll position of the user's view
    currentBlockIdDisplayedInMiddleOfDOM = calculateBlockIdDisplayedInMiddleOfDOM()
    currentScrollTop = getScrollTop()

    # Calculate startRestore and endRestore
    startRestore = calculateStartRestore(currentBlockIdDisplayedInMiddleOfDOM)
    endRestore = calculateEndRestore(currentBlockIdDisplayedInMiddleOfDOM)

    # Calculate targetMessagesPixelHeightRestore
    targetMessagesPixelHeightRestore = calculateTargetMessagesPixelHeightRestore(startRestore, endRestore)

    # Store these values in persistent storage
    storeInLocalStorage("block_idDisplayedInMiddleOfDOM", currentBlockIdDisplayedInMiddleOfDOM)
    storeInLocalStorage("startRestore", startRestore)
    storeInLocalStorage("endRestore", endRestore)
    storeInLocalStorage("targetMessagesPixelHeightRestore", targetMessagesPixelHeightRestore)
    storeInLocalStorage("scrollTop", currentScrollTop)

# Function to calculate the block_id displayed in the middle of the DOM
function calculateBlockIdDisplayedInMiddleOfDOM():
    # Logic to determine the block_id currently displayed in the middle of the visible area
    # ...

# Function to calculate startRestore based on the current block_id
function calculateStartRestore(currentBlockIdDisplayedInMiddleOfDOM):
    # Logic to calculate startRestore considering edge cases
    # ...

# Function to calculate endRestore based on the current block_id
function calculateEndRestore(currentBlockIdDisplayedInMiddleOfDOM):
    # Logic to calculate endRestore considering edge cases
    # ...

# Function to calculate targetMessagesPixelHeightRestore
function calculateTargetMessagesPixelHeightRestore(startRestore, endRestore):
    # Fetch messages from startRestore to endRestore and calculate their total pixel height
    # ...

# Function to get the current scroll position
function getScrollTop():
    # Retrieve the current scroll position
    # ...

# Function to store data in local storage
function storeInLocalStorage(key, value):
    # Store the key-value pair in local storage
    # ...

# Main program flow
saveLocation()


function restoreLocation():
    # Retrieve values from local storage
    storedBlockIdDisplayedInMiddleOfDOM = retrieveFromLocalStorage("block_idDisplayedInMiddleOfDOM")
    storedStartRestore = retrieveFromLocalStorage("startRestore")
    storedEndRestore = retrieveFromLocalStorage("endRestore")
    storedTargetMessagesPixelHeightRestore = retrieveFromLocalStorage("targetMessagesPixelHeightRestore")
    storedScrollTop = retrieveFromLocalStorage("scrollTop")

    # Restore the user's view based on the stored values
    scrollToBlockId(storedBlockIdDisplayedInMiddleOfDOM)
    restoreScrollPosition(storedScrollTop)

# Function to retrieve data from local storage
function retrieveFromLocalStorage(key):
    # Retrieve the value associated with the given key from local storage
    # ...

# Function to scroll to a specific block_id
function scrollToBlockId(blockId):
    # Logic to scroll to the specified block_id
    # ...

# Function to restore the scroll position
function restoreScrollPosition(scrollTop):
    # Set the scroll position to the stored value
    # ...

# Main program flow
restoreLocation()

*/



