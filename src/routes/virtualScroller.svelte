<script>
/*
Bi-directional infinite virtual scrolling with elastic grip and scrubbing grip custom elements (plus up/down keys and scroll wheel of course)
    * The conversation-container holds messages. The messages are placed absolutely, relative to the mid-point of the container height. This container does not scroll.
    * The conversation-container has a height of 40000000px. This equals very roughly 2 million lines of text. This is the maximum chat session length.
    * onMount fetchConversationRestore places a block of messages at the starting point mid-way down the conversation-container. The block is based on where the user last left off in the conversation. It could be anywhere in the overall conversation.
    * The virtual-container sits on top of the conversation-container and is a 'window' into the conversation-container below it.
    * The virtual-container has a height of 100vh and overflow-y: auto. It is sized to fit the viewable UI window. It is the only container that scrolls.
    * The virtual-container must account while scrolling for the mid-point offset of the conversation-container message placement. So all scrollTop values must be adjusted by the variable halfWayPoint which is defined to equal the halfway point of the the conversation-container height
    * When messages are added to conversation-container there is no need to adjust them using halfWayPoint because halfWayPoint is hardcoded into conversation-container CSS. So a message placed at "top: 200px" will be placed at the halfway point of the conversation-container height + 200px automatically.
    * As the user scrolls, messages are loaded and pruned from the conversation-container as needed, and then the virtual container is scrolled to the appropriate position to see what is there.
    * Only a small number of messages remain loaded in the conversation-container at any time. Excess messages are pruned as the user scrolls away from them. This is very memory efficient and supports apparently instant scrolling of conversations of hundreds of thousands of messages. 
*/

const halfWayPoint = 10000000; // Halfway point of the conversation-container height

import UserInput from './userinput.svelte';

import UserInputSent from './userinputsent.svelte';
import LLMResponse from './llmresponse.svelte';
import {scrollStore, get, setInLocalStorage, updateScrollSettings} from '$lib/scrollStore.js';
import { onMount, onDestroy } from 'svelte';
import { invoke } from "@tauri-apps/api/tauri";
import { tick } from 'svelte';

// reactive state management for scrollsearch component
let conversation = []; // conversation history slice as requested from the backend
let conversationArray = []; // conversation history copied from conversation[]

let messages_path = get('messages_path');
let database_path = get('database_path');
let docs_drop_path = get('docs_drop_path');

let num_messages = 0; // total number of user, llm and bright_memory messages in the conversation
let num_user_llm_messages = 0; // total number of user and llm messages in the conversation
let conversationcontainer; // reference to the #conversation-container element   
let virtualcontainer; // reference to the #virtual-container element

// Infinite scroll observers
let topObserverElement;
let bottomObserverElement;

let userInputComponent; // Initialize the variable to bind the UserInput component

let hasReachedStart = false; // Initialize the flag for the start of the conversation
let hasReachedEnd = false; // Initialize the flag for the end of the conversation

let firstVisibleMessageNum;
$: firstVisibleMessageNum = $scrollStore.firstVisibleMessageNum; // Keep firstVisibleMessageNum in sync with the scrollStore
let lastVisibleMessageNum;
$: lastVisibleMessageNum = $scrollStore.lastVisibleMessageNum; // Keep lastVisibleMessageNum in sync with the scrollStore

$: firstConversationArrayMessageNum = conversation.length > 0 ? parseInt(conversation[0].message_num) : null; //First message number in the current conversation array
$: if (firstConversationArrayMessageNum !== null) localStorage.setItem('firstConversationArrayMessageNum', firstConversationArrayMessageNum.toString());
$: lastConversationArrayMessageNum = conversation.length > 0 ? parseInt(conversation[conversation.length - 1].message_num) : null // Last message number in the current conversation array
$: if (lastConversationArrayMessageNum !== null) localStorage.setItem('lastConversationArrayMessageNum', lastConversationArrayMessageNum.toString());

// used by the mouse wheel event listener to determine the direction of the scroll and execution limiting
let shouldFetchUp = false;
let shouldFetchDown = false;

// Set flags indicating the conversation array contains the first and/or last message in the entire conversation.
// Flags can then be use for various logic, e.g. to prevent the user from scrolling past the start or end of the conversation
// or to prevent operations for seeking out of bounds of the conversation, or to add padding to the very last message 
function updateEdgeFlags() {
    if (conversation.length === 0) {
        hasReachedStart = false;
        hasReachedEnd = false;
        return;
    }
    firstConversationArrayMessageNum = parseInt(conversation[0].message_num);
    localStorage.setItem('firstConversationArrayMessageNum', firstConversationArrayMessageNum);
    hasReachedStart = (firstConversationArrayMessageNum === 1); // will be true if the first message in the conversation array is the first message in the entire conversation
    let lastConversationArrayMessageNum = parseInt(conversation[conversation.length - 1].message_num);
    localStorage.setItem('lastConversationArrayMessageNum', lastConversationArrayMessageNum);   
    hasReachedEnd = (lastConversationArrayMessageNum === totalMessages); // will be true if the last message in the conversation array is the last message in the entire conversation 
}

// Scrolls virtual-container to the specified message number in the conversation
// The message must be in the conversation array and await tick(); must be called before calling this function
function scrollToMessage(firstVisibleMessageNum) {    
    const targetMessageElement = conversationcontainer.querySelector(`[messagenum="${firstVisibleMessageNum}"]`);
    if (targetMessageElement) {
        let messageTop = parseFloat(targetMessageElement.style.top);
        virtualcontainer.scrollTop = halfWayPoint + messageTop; // adding halfWaying is necessary to account for the conversation-container mid-point offset
    } else {
        console.error(`No message element found with message_num: ${targetMessageNum}`);
    }
}

// Scrubbing grip control logic
// gripLocation is a number between 0 and 1 that represents the position of the grip relative to the whole conversation
// This calls throttled and debounced versions of fetchConversationSlice to fetch the conversation slice based on gripLocation
//$: gripLocation = $scrollStore.gripPosition; // sets gripLocation to the current gripPosition in scrollStore
let totalMessages;
$: totalMessages = $scrollStore.totalMessages; // Keep totalMessages in sycn with the scrollStore
let gripLocation; // Initialize gripLocation to the current gripPosition in scrollStore
$: gripLocation = $scrollStore.gripPosition; // sets gripLocation to the current gripPosition in scrollStore
let userMovingGrip = false; // Flag to track user grip movement
$: userMovingGrip = $scrollStore.userMovingGrip; // Keep userMovingGrip in sync with the scrollStore

$: if (userMovingGrip === true && typeof totalMessages !== 'undefined' && totalMessages > 0) {
    handleGripMovement();
}
function handleGripMovement() {
    console.log('User is Moving the Scrubbing Grip');  // Debug line
    throttledFetch(gripLocation, totalMessages);
    debouncedFetch(gripLocation, totalMessages);
}

// Infinite scroll animation speed control logic used by the elastic grip element
let lastRenderTime = Date.now();
const animateScroll = () => {
    const currentTime = Date.now();
    const deltaTime = (currentTime - lastRenderTime);  // Time since last frame in seconds
    lastRenderTime = currentTime;
    // the numeric value controls the relative speed of fine scrolling
    const dragSpeedUpDown = parseFloat(localStorage.getItem('dragSpeedUpDown')) * 0.6 || 0; // 0.6 is the normal speed multiplier
    if (virtualcontainer) { virtualcontainer.scrollTop += dragSpeedUpDown * deltaTime; requestAnimationFrame(animateScroll); }
}; // end of elastic grip animateScroll function. 

// Executed when UP or DOWN arrow keys are pressed.
async function handleArrowKeyScroll(event) {
  // Determine the direction based on the key pressed
  let direction = null;
  if (event.key === "ArrowUp") {
    direction = "UP";
  } else if (event.key === "ArrowDown") {
    direction = "DOWN";
  }

  // If neither UP nor DOWN arrow keys were pressed, exit the function
  if (!direction) return;

  if (direction === "DOWN" && shouldFetchDown && !hasReachedEnd) {
    if (hasReachedEnd) {
      return;  // Skip the fetch operation
    }
    await fetchConversationPart("DOWN");
    shouldFetchDown = false; // Reset the flag after fetching
  } else if (direction === "UP" && shouldFetchUp && !hasReachedStart) {
    if (hasReachedStart) {
      return;  // Skip the fetch operation
    }
    await fetchConversationPart("UP");
    shouldFetchUp = false; // Reset the flag after fetching
  }
}

async function handleWheelScroll(event) {
  const direction = event.deltaY > 0 ? "DOWN" : "UP";

  if (direction === "UP" && shouldFetchUp && !hasReachedStart) {
    await fetchConversationPart(direction);
    shouldFetchUp = false; // Reset the flag after fetching
  } else if (direction === "DOWN" && shouldFetchDown && !hasReachedEnd) {
    await fetchConversationPart(direction);
    shouldFetchDown = false; // Reset the flag after fetching
  }
}

// Fetches a slice of the conversation history from the backend for the scrubbing grip element
async function fetchConversationSlice(gripLocation, totalMessages) {

    console.log(`fetchConversationSlice ran`);  // Debug line

    const MessagesToFetch = 20; // Maximum number of messages to fetch

    if (gripLocation < 0 || gripLocation > 1 || isNaN(totalMessages)) {
      throw new Error('Invalid Input');
    }

    let targetMessage = Math.round(totalMessages * (1 - gripLocation));
    // Store targetMessage in local storage
    setInLocalStorage('targetMessage', targetMessage);
    //localStorage.setItem('targetMessage', targetMessage);

    let start = Math.max(targetMessage - buffer, 0); // buffer is 10
    let end = Math.min(targetMessage + buffer, totalMessages);

    if (totalMessages < MessagesToFetch) {
      start = 0;
      end = totalMessages;
    } else {
      if (targetMessage < buffer) {
        start = 0;
        end = Math.min(MessagesToFetch, totalMessages);
      }
      if (totalMessages - targetMessage < buffer) {
        end = totalMessages;
        start = Math.max(totalMessages - MessagesToFetch, 0);
      }
    }

    try {
        const fetchedData = await invoke('fetch_conversation_history', { params: { start, end } });

        // Check if the fetched data is in the expected format and update the conversation
        if (fetchedData && Array.isArray(fetchedData.message)) {
            conversation = fetchedData.message; // Update the conversation array
            localStorage.setItem('conversationArray', JSON.stringify(conversation)); // Store in local storage
            updateEdgeFlags(); // Update edge flags as necessary
            // Any additional logic for UI updates, scrolling adjustments, etc.
        } else {
            console.warn("Fetched data is not in the expected format:", fetchedData);
            conversation = []; // Reset the conversation array if data format is not as expected
        }

        return conversation; // Return the updated conversation
    } catch (error) {
        console.error('Failed to fetch conversation slice:', error);
        conversation = []; // Reset the conversation array in case of error
        return null;
    }

  }

// script level store of each message in the conversation array and each message's pixel height.
let messageHeights = {};
// Ideal number of messages on each side of the target message, subject to adjustment, is not sole source of truth but only a starting point
const buffer =  10; 

// Fetches a slice of the conversation history from the backend for the scrubbing grip element
// THIS WORKS WITH THE CONVERSATION_HISTORY array from the backend which is indexed from 0. The
// topMessageNum is already adjusted -1 to match the array indexing BEFORE being passed to this function.
async function fetchConversationRestore() {
    firstVisibleMessageNum = parseInt(localStorage.getItem('firstVisibleMessageNum')) || 0;
    totalMessages = parseInt(localStorage.getItem('totalMessages')) || 0;

    if (totalMessages === 0 || isNaN(firstVisibleMessageNum)) {
        return;
    }

    // Adjust start and end to handle being near the start or end of the conversation
    let start = Math.max(firstVisibleMessageNum - (buffer + 1), 0);
    let end = Math.min(firstVisibleMessageNum + (buffer - 1), totalMessages);

    // If near the end, adjust the start index to maintain the buffer range
    if (end === totalMessages) {
        start = Math.max(totalMessages - buffer * 2, 0);
    }

    // If the conversation is smaller than the buffer range, fetch the entire conversation
    if (totalMessages <= buffer * 2) {
        start = 0;
        end = totalMessages;
    }

    console.log(`fetchConversationRestore() start: ${start}, end: ${end}`);  // Debug line

    try {
        const fetchedData = await invoke('fetch_conversation_history', { params: { start, end } });
        if (fetchedData && Array.isArray(fetchedData.message)) {
            conversation = fetchedData.message;
            await tick(); 
            await updateMessageHeights(conversation);           
            await placeMessagesPrecisely(conversation);          
            await scrollToMessage(firstVisibleMessageNum);  // Scroll to the target message
            // save to local storage conversationArray
            localStorage.setItem('conversationArray', JSON.stringify(conversation));            
            await updateEdgeFlags();  // Update UI flags
                   
        } else {
            console.warn("Fetched data is not in the expected format:", fetchedData);
            conversation = [];
        }
    } catch (error) {
        console.error('Failed to fetch conversation slice:', error);
        conversation = [];
    }
} // end of fetchConversationRestore function

// Universal helper functions for infinite scroll message measurement and precise placement
async function updateMessageHeights(messages) {
    messages.forEach(message => {
        const height = calculateHeightOfMessage(message);
        messageHeights[message.message_num] = height;
        console.log(`Message ${message.message_num} has height ${height}`);  // Debug line
    });
    console.log(`messageHeights: ${JSON.stringify(messageHeights)}`);  // Debug line
}
function calculateHeightOfMessage(message) {
    const messageElement = document.querySelector(`[messagenum='${message.message_num}']`);
    return messageElement ? messageElement.offsetHeight : 0; // Return 0 if the message is not found
}

// Places messages precisely in the conversation container based on their pixel height
// There is no need to adjust for the conversation-container mid-point offset because it is hardcoded into the conversation-container CSS
async function placeMessagesPrecisely(messages) { 
    let cumulativeHeight = 0; // starting point
    messages.forEach(message => {
        const messageElement = document.querySelector(`[messagenum='${message.message_num}']`);
        if (messageElement) {
            messageElement.style.position = 'absolute';
            messageElement.style.top = `${cumulativeHeight}px`;
            //console.log(`Message ${message.message_num} placed at ${cumulativeHeight}px`);  // Debug line
            cumulativeHeight += messageHeights[message.message_num];
        }
    });
    await tick();
    // Position topObserverElement just after the first message
    if (topObserverElement) {
        topObserverElement.style.position = 'absolute';
        topObserverElement.style.top = `${messageHeights[messages[0].message_num]}px`;
        console.log(`topObserverElement placed at ${messageHeights[messages[0].message_num]}px`);
    }
    // Position bottomObserverElement just after the last message
    if (bottomObserverElement) {
        bottomObserverElement.style.position = 'absolute';
        bottomObserverElement.style.top = `${cumulativeHeight}px`;
        console.log(`bottomObserverElement placed at ${cumulativeHeight}px`);  // Debug line
    }

    const observer = new IntersectionObserver(observerCallback, observerOptions);

    if (topObserverElement) {
        observer.observe(topObserverElement);
    }

    if (bottomObserverElement) {
        observer.observe(bottomObserverElement);
    }
}

// Fetches a part of the conversation history from the backend for the infinite scrolling elastic grip element
// Unlike the scrubbing grip, this function does NOT need throttling or debouncing
let userHasScrolled = false; // Flag to track user scroll

async function fetchConversationPart(direction) {

    if (!userHasScrolled) {
        return; // Exit if no user scroll has occurred
    }


    let start, end;
    let newMessageHeights = {};
    let messagesToAdd = 10;
    totalMessages = parseInt(localStorage.getItem('totalMessages')) || 0;

    if (direction === "UP" && !hasReachedStart) {
      const firstMessageNum = parseInt(conversation[0].message_num);
      start = Math.max(firstMessageNum - messagesToAdd, 0);
      end = parseInt(conversation[0].message_num) - 1;
      console.log(`UP start: ${start}, end: ${end}`);  // Debug line
    } else if (direction === "DOWN") {
        start = parseInt(conversation[conversation.length - 1].message_num);
        end = Math.min(start + messagesToAdd - 1, totalMessages);
        console.log(`DOWN start: ${start}, end: ${end}`);  // Debug line
    }

    try {
        const fetchedData = await invoke('fetch_conversation_history', { params: { start, end } });

        if (fetchedData && Array.isArray(fetchedData.message)) {
            // Calculate height before adding new messages
            let oldHeight = calculateTotalHeightOfConversation();

            // Add new messages and update message heights
            if (direction === "UP") {
                conversation = fetchedData.message.concat(conversation);
                localStorage.setItem('conversationArray', JSON.stringify(conversation));
            } else {
                conversation = conversation.concat(fetchedData.message);
                localStorage.setItem('conversationArray', JSON.stringify(conversation));
            }
            await tick();
            fetchedData.message.forEach(message => {
                newMessageHeights[message.message_num] = calculateHeightOfMessage(message);
            });
            Object.assign(messageHeights, newMessageHeights);

            // Prune messages and adjust scroll position
            let prunedHeight = pruneMessages(direction, fetchedData.message.length);

            // Adjust scroll position
            if (direction === "UP") {
                let newHeight = calculateTotalHeightOfConversation();
                conversationcontainer.scrollTop += newHeight - oldHeight - prunedHeight;
            }

            // Update edge flags and local storage
            updateEdgeFlags();
            localStorage.setItem('conversationArray', JSON.stringify(conversation));
        } else {
            console.warn("Fetched data is not in the expected format:", fetchedData);
        }
    } catch (error) {
        console.error(`Failed to fetch conversation part: ${error}`);
    }
}

function pruneMessages(direction, numAdded) {
    let prunedHeight = 0;
    if (conversation.length > 20) {
        let messagesToPrune = numAdded;
        while (messagesToPrune > 0) {
            let messageNum;
            if (direction === "UP") {
                messageNum = conversation.pop().message_num;
            } else {
                messageNum = conversation.shift().message_num;
            }
            prunedHeight += messageHeights[messageNum];
            delete messageHeights[messageNum];
            messagesToPrune--;
        }
    }
    return prunedHeight;
}

function adjustScrollPosition(oldHeight, newHeight) {
    conversationcontainer.scrollTop += (newHeight - oldHeight);
}

function calculateTotalHeightOfConversation() {
    return conversation.reduce((total, message) => {
        return total + (messageHeights[message.message_num] || 0);
    }, 0);
}

// debounce function to prevent excessive calls to fetchConversationSlice
function debounce(func, wait) {
  let timeout;
  return function(...args) {
    const context = this;
    clearTimeout(timeout);
    timeout = setTimeout(() => {
      func.apply(context, args);
    }, wait);
  };
}
const debouncedFetch = debounce(fetchConversationSlice, 90);

// throttle function to prevent excessive calls to fetchConversationSlice

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    }
}
const throttledFetch = throttle(fetchConversationSlice, 90);


const throttledFindFirstVisibleMessage = throttle(findFirstVisibleMessage, 100); // call this !!!!!
function findFirstVisibleMessage() {
    if (!conversationcontainer || !virtualcontainer) {
        return;
    }

    const messages = conversationcontainer.querySelectorAll('.message-class');
    let closestTop = Infinity; // Initialize with a large number
    let firstVisibleMessageNum = null;

    for (const message of messages) {
        const rect = message.getBoundingClientRect();

        // Calculate the absolute distance from the top of the viewport
        // finds the message with it top closest to the top of the viewport then exits
        const distanceFromTop = Math.abs(rect.top);

        // Update closestTop and firstVisibleMessageNum if this message is closer to the top
        if (distanceFromTop < closestTop) {
            closestTop = distanceFromTop;
            firstVisibleMessageNum = message.getAttribute('messagenum');
        }
    }

    // Update the firstVisibleMessageNum if a message was found
    if (firstVisibleMessageNum !== null) {
        //console.log(`First visible message number: ${firstVisibleMessageNum}`);
        setInLocalStorage('firstVisibleMessageNum', firstVisibleMessageNum);
        
    } else {
        console.log("No visible messages found");
    }
}


// function to find the top and bottom visible messages in DOM
const throttledFindBottomVisibleMessage = throttle(findBottomVisibleMessage, 100); // call this !!!!!
function findBottomVisibleMessage() {
  if (!conversationcontainer || !virtualcontainer) {
    return;
  }

  const messages = conversationcontainer.querySelectorAll('.message-class');
  let tempLastVisibleMessageNum = null;

  for (const message of messages) {
    const rect = message.getBoundingClientRect();
    const containerRect = virtualcontainer.getBoundingClientRect();

    // Check if the message is within the viewport of virtualcontainer
    const isWithinViewport = (rect.bottom > containerRect.top) && (rect.top < containerRect.bottom);

    if (isWithinViewport) {
      const messageNum = message.getAttribute('messagenum'); // Or just 'messagenum' if it's not a data attribute

      // Update last visible message number for each message in the viewport
      // continues until the last message in the viewport is found then exits
      tempLastVisibleMessageNum = messageNum;
    }

  }
  // Update the reactive variables if the values have changed
  if (tempLastVisibleMessageNum !== null) {
    lastVisibleMessageNum = tempLastVisibleMessageNum;
    //console.log(`lastVisibleMessageNum: ${lastVisibleMessageNum}`);  // Debug line
    setInLocalStorage('lastVisibleMessageNum', lastVisibleMessageNum);
  }
}

const observerOptions = {
    root: virtualcontainer,
    rootMargin: '0px', // how early to start fetching the next part of the conversation
    threshold: 1 // how much of the observer element needs to be visible before the callback is executed
};
// Callback function to be executed when the top or bottom observer elements intersect
// due to the user fine scrolling with the elastic grip element up or down respectively
const observerCallback = async (entries, observer) => {
    for (const entry of entries) {
        if (entry.isIntersecting) {
            if (entry.target.id === 'top-observer' && !hasReachedStart) {
                await fetchConversationPart("UP");
                console.log(`top-observer is intersecting`);  // Debug line
            } else if (entry.target.id === 'bottom-observer' && !hasReachedEnd) {
                await fetchConversationPart("DOWN");
                console.log(`bottom-observer is intersecting`);  // Debug line
            }
        }
    }
};


onMount( async () => {

    firstVisibleMessageNum = parseInt(localStorage.getItem('firstVisibleMessageNum')); // get the firstVisibleMessageNum from local storage and set the local variable
    lastVisibleMessageNum = parseInt(localStorage.getItem('lastVisibleMessageNum')); // get the lastVisibleMessageNum from local storage and set the local variable

    totalMessages = await invoke('get_num_messages', {databasePath: database_path}); // total number of messages in the entire conversation
    localStorage.setItem('totalMessages', totalMessages); // get the totalMessages from local storage and set the local variable
    //console.log(`onMount totalMessages: ${totalMessages}`);  // Debug line

    // This variable will only be needed if I implement bright memories
    //num_user_llm_messages = await invoke('get_total_llm_user_messages', {databasePath: database_path});

    //console.log(`onMount firstVisibleMessageNum: ${firstVisibleMessageNum}`);  // Debug line
    await fetchConversationRestore(firstVisibleMessageNum); // restore the conversation location to the last known position

    requestAnimationFrame(animateScroll);

    // Add the mouse wheel event listener
    conversationcontainer.addEventListener('wheel', handleWheelScroll), () => {
        userHasScrolled = true;
    }

    // Add the keydown event listener for the UP and DOWN arrow keys
    conversationcontainer.addEventListener('keydown', handleArrowKeyScroll), () => {
        userHasScrolled = true;
    }

    
    virtualcontainer.addEventListener('scroll', throttledFindFirstVisibleMessage);
    virtualcontainer.addEventListener('scroll', throttledFindBottomVisibleMessage);

}); // end of onMount()


</script>



<div id="virtual-container" bind:this={virtualcontainer}>
    <div id="conversation-container" bind:this={conversationcontainer}>

        <div bind:this={topObserverElement} id="top-observer" style="background-color: red;"></div>

        {#each conversation as entry, index}
            <div class="message-class" messagenum={entry.message_num}>
                {#if entry.source === 'user' || entry.source === 'llm'}
                    {#if entry.source === 'user'}
                        <UserInputSent {...entry} />
                    {:else if entry.source === 'llm'}
                        <LLMResponse {...entry} />
                    {/if}
                {/if}
            </div>
        {/each}

        <div bind:this={bottomObserverElement} id="bottom-observer" style="background-color: red;"></div>
      
    </div>
</div>

<div class="user-input-container">
    <UserInput bind:this={userInputComponent} />
</div>
  


<style>
   
    #virtual-container {
        position: fixed;
        bottom: 0px;
        left: 0px;
        right: 0px;
        overflow: hidden;
        overflow-y: auto;
        scrollbar-width: none; /* hides scrollbar in Firefox */
        -ms-overflow-style: none; /* Internet Explorer 11 */
        scrollbar-width: none; /* Microsoft Edge */
        width: 100%;
        height: 100vh; /* takes up the whole viewport */
        background-color: transparent;
    }

    ::-webkit-scrollbar {
            display: none; /* Hide scrollbar in Chrome */
    }

    #conversation-container {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        width: 100%;
        position: absolute; 
        height:  20000000px;
        top:     10000000px;
        padding-right: 0px;
        user-select: none;
        opacity: 0.99;
        overflow-y: hidden; /* hides default scrolling bars */
        scroll-behavior: smooth;
        position: absolute;
        scrollbar-width: none; /* hides scrollbar in Firefox */
        scrollbar-width: none; /* hides scrollbar in Firefox */
        -ms-overflow-style: none; /* Internet Explorer 11 */
        scrollbar-width: none; /* Microsoft Edge */
    }

    .message-class {
        margin-bottom: 0px; /* or any other suitable value */
        position: relative;
        width: 100%;
        bottom: 0px;
        left: 0px;
        right: 0px;
        padding: 5px;
    }

    #top-observer, #bottom-observer {
        width: 100%;
        height: 2px;
    }

    .user-input-container {
        position: fixed;
        bottom: 1.5px;
        left: 7px;
        right: 53px;
        max-height: 100vh; 
        overflow-y: auto;  /* Hide overflow */
        padding-right:3px;
        overflow: auto; /* hides default scrolling bars */
        overflow-x: hidden; /* hides default horizontal scrolling bar */
    }

</style>

