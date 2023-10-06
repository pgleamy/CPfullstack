<script>
    import UserInput from './userinput.svelte.failed';
    import UserInputSent from './userinputsent.svelte';
    import LLMResponse from './llmresponse.svelte';
    // reactive state management for scrollsearch component
    import {scrollStore, get} from '$lib/scrollStore.js';
    import { onMount, onDestroy } from 'svelte';
    import { invoke } from "@tauri-apps/api/tauri";

    let conversation = []; // conversation history slice as requested from the backend
    let num_messages = 0; // total number of messages in the conversation

    let container; // reference to the conversation container element    

    // Infinite scroll variables
    let topObserverElement;
    let bottomObserverElement;


    // Scrubbing grip control logic
    // gripLocation is a number between 0 and 1 that represents the position of the grip relative to the whole conversation
    $: gripLocation = $scrollStore.gripPosition; // sets gripLocation to the current gripPosition in scrollStore
    $: {
    throttledFetch(gripLocation, num_messages);
    debouncedFetch(gripLocation, num_messages);
    } // controls the fetching of the conversation slice based on gripLocation for smooth interaction

    onMount(async () => {
      // get the conversation history slice from the backend
      num_messages = await invoke('get_num_messages');
      console.log("Current number of messages: " + num_messages);
      console.log("Current gripLocation: " + gripLocation);
     
      // start a simple debugging timer
      const startTime = Date.now();
      fetchConversationSlice(gripLocation, num_messages);
      const endTime = Date.now();
      const elapsed = endTime - startTime;
      console.log(`Elapsed time: ${elapsed} milliseconds`);

      // Infinite scroll logic
      const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
      };
      const observerCallback = (entries, observer) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const direction = parseFloat(localStorage.getItem('dragSpeedUpDown')) || 0;
            if (entry.target === topObserverElement && direction > 0) {
              // Load more messages at the top
              // TODO: Call fetchConversationSlice and update state
            } else if (entry.target === bottomObserverElement && direction < 0) {
              // Load more messages at the bottom
              // TODO: Call fetchConversationSlice and update state
            }
          }
        });
      };
      const observer = new IntersectionObserver(observerCallback, observerOptions);
      observer.observe(topObserverElement);
      observer.observe(bottomObserverElement);


    }); // end of onMount


async function fetchConversationSlice(gripLocation, num_messages) {
  const buffer = 10;
  const totalMessagesToFetch = 20;
  
  // Step 1: Calculate the target message based on gripLocation
  // Invert the gripLocation to align with the array indexing
  const targetMessage = Math.round((1 - gripLocation) * num_messages);
  console.log(`Calculated targetMessage: ${targetMessage}`);  // Debug line

  // Initialize start and end
  let start = targetMessage - buffer;
  let end = targetMessage + buffer;

  // Step 2 and 3: Adjust start and end according to the logic
  if (start < 0) {
    // Shift 'end' if 'start' is less than 0
    end += Math.abs(start);
    start = 0;
  }
  
  if (end > num_messages) {
    // Shift 'start' if 'end' is more than total messages
    start -= (end - num_messages);
    end = num_messages;
  }
  
  // Ensure start is not negative after the above adjustment
  if (start < 0) start = 0;

  // Debug line
  console.log(`Adjusted start and end: ${start}, ${end}`);

  // Step 4: If total messages < 20, fetch all
  if (num_messages < totalMessagesToFetch) {
    start = 0;
    end = num_messages;
  }
  
  // Step 5: Fetch the conversation slice
  try {
    const fetchedData = await invoke('fetch_conversation_history', { params: {start, end} });
    console.log("Fetched conversation slice:", fetchedData);  // Debug line
    
    if (fetchedData && Array.isArray(fetchedData.message)) {
      conversation = fetchedData.message;
    } else {
      console.warn("Fetched data is not in the expected format:", fetchedData);
      conversation = [];
    }

    return conversation;
  } catch (error) {
    console.error(`Failed to fetch conversation slice: ${error}`);
    conversation = [];
    return null;
  }
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
const debouncedFetch = debounce(fetchAndDisplayConversationSlice, 90);

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
const throttledFetch = throttle(fetchAndDisplayConversationSlice, 90);


async function fetchAndDisplayConversationSlice(gripLocation, num_messages) {
    //const container = document.getElementById('conversation-container');

    // Fade out
    if (container) {  // Check to ensure the container is not null
      container.style.opacity = '0';
    }

    // Fade out
    //container.style.opacity = '0';

    await fetchConversationSlice(gripLocation, num_messages);

    // After a slight delay to ensure content is replaced, fade in
    setTimeout(() => {
      if (container) { // Check to ensure the container is not null
        container.style.opacity = '1';
      }
    }, 25);
}


</script>



  <div id="clip-container">
    <div id="conversation-container" bind:this={container}> 
      
      <div bind:this={topObserverElement} id="top-observer"></div>

      {#each conversation as entry}
        {#if entry.source === 'user'}
          <UserInputSent {...entry} />
        {:else if entry.source === 'llm'}
          <LLMResponse {...entry} />
        {/if}
      {/each}

      <div bind:this={bottomObserverElement} id="bottom-observer"></div>

      <UserInput />
    </div>
  </div>

   
  <style>
    #conversation-container {
      transition: all 0.5s ease-in-out;
      display: flex;
      flex-direction: column;
      align-items: flex-start;
      width: 100%;
      position: relative;
      bottom: 0;
      left: 5px !important;
      padding-bottom: 0px;
      padding-right: 0px;
      user-select: none;
      opacity: 1;
      transition: opacity 500ms ease-in-out;

      overflow-y: hidden; /* hides default vertical scrolling bar */
      overflow-x: hidden; /* hides default horizontal scrolling bar */
    }

    #clip-container {
    position: fixed;
    top: 79px;
    bottom: 5px;
    left: 0;
    right: 0;
    clip-path: inset(0);
    overflow: hidden;
  }


  #top-observer, #bottom-observer {
    width: 100%;
    height: 1px;
  }
 
  </style>
  