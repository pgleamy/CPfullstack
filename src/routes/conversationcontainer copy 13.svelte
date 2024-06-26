<script>
    import UserInput from './userinput.svelte';

    import UserInputSent from './userinputsent.svelte';
    import LLMResponse from './llmresponse.svelte';
    // reactive state management for scrollsearch component
    import {scrollStore, get, setInLocalStorage} from '$lib/scrollStore.js';
    import { onMount, onDestroy } from 'svelte';
    import { invoke } from "@tauri-apps/api/tauri";
    import { tick } from 'svelte';


    let conversation = []; // conversation history slice as requested from the backend
    let num_messages = 0; // total number of user, llm and bright_memory messages in the conversation
    let num_user_llm_messages = 0; // total number of user and llm messages in the conversation
    let container; // reference to the conversation container element    

     // Infinite scroll observers
    let topObserverElement;
    let bottomObserverElement;
    let userInputComponent; // Initialize the variable to bind the UserInput component
    let observer; // Initialize the observer variable for the infinite scroll logic








    // Reactive state management for fine scrolling scroll adjustments in fetchConversationPart function
    let initialBeforeScrollTop = null; 
    let initialGripLocation = gripLocation;  // Initialize with the current gripLocation value
    // Reactive statement to monitor gripLocation
    $: {
      // Logic to reset initialBeforeScrollTop when gripLocation changes
      if (initialBeforeScrollTop !== null && gripLocation !== initialGripLocation) {
        initialBeforeScrollTop = null;
      }
      initialGripLocation = gripLocation;  // Update initialGripPosition to the new value
    }
    



    
    $: targetMessage = $scrollStore.targetMessage; // Reactive assignment
    $: totalMessages = $scrollStore.totalMessages; // Reactive assignment

    // Connects the top of user input to the bottom of last message as user types
    let paddingBottom = '';  // Declare a variable to hold the padding-bottom value
    // Create a reactive statement to update paddingBottom whenever userInputHeight changes
    $: {
      if (isEndOfConversation) {
          paddingBottom = `padding-bottom: ${$scrollStore.userInputComponentHeight}px;`;
          // scroll to bottom of conversation container so the send button is always visible
          scrollToBottom();
      } else {
          paddingBottom = '';
      }
    } // end of reactive statement to update paddingBottom


    function scrollToBottom() {
      if (container) {
          container.scrollTop = container.scrollHeight;
        }
        tick().then(() => {
          if (userInputComponent) {
            container.scrollTop = container.scrollHeight;
          }
        });
        //console.log("Scrolling to bottom");
    } // end of scrollToBottom function



    // Start/End of conversation logic to display the user input component only after the last message in the entire conversation history
    // AND to position the view of the messages correctly when the user input component is displayed or when at top of conversation showing from very start
    let isEndOfConversation = false;  // Initialize to false
    let isStartOfConversation = false; // Initialize to true
    $: {
        if (isEndOfConversation = (targetMessage === totalMessages)) {;/* logic to check if the last fetched message is the last message in the entire conversation */
          //console.log(`isEndOfConversation: ${isEndOfConversation}`);
        } 
        if (isStartOfConversation = (targetMessage === 0)) {;/* logic to check if the last fetched message is the first message in the entire conversation */
          //console.log(`isStartOfConversation: ${isStartOfConversation}`);
        }
      } // end of reactive statement to start/end of conversation 
    let endScrollTrigger = false;
    let startScrollTrigger = false;
    $: {
      if (isEndOfConversation && !endScrollTrigger) {
        if (container) {
          container.scrollTop = container.scrollHeight;
        }
        tick().then(() => {
          if (userInputComponent) {
            container.scrollTop = container.scrollHeight;
          }
        });
        endScrollTrigger = true;  // Prevent further downward scrolling until flag is reset
        startScrollTrigger = false; // Reset the other flag
      } else if (isStartOfConversation && !startScrollTrigger) {
        if (container) {
          container.scrollTop = 0;
        }
        startScrollTrigger = true; // Prevent further upward scrolling until flag is reset
        endScrollTrigger = false; // Reset the other flag
      } else if (!isEndOfConversation && !isStartOfConversation) {
        // Reset both flags if neither condition is metlogic
        endScrollTrigger = false;
        startScrollTrigger = false;
      }
    } // end of reactive statement to position the view of the messages correctly when the user input component is displayed or when at top of conversation showing from very start


    // Scrubbing grip control logic
    // gripLocation is a number between 0 and 1 that represents the position of the grip relative to the whole conversation
    $: gripLocation = $scrollStore.gripPosition; // sets gripLocation to the current gripPosition in scrollStore
    // controls the fetching of the conversation slice based on gripLocation for smooth interaction
    $: {
      if (num_messages > 0) {
        throttledFetch(gripLocation, num_messages);
        debouncedFetch(gripLocation, num_messages);
      }
    } // end of reactive statement to fetch conversation slice based on local variable gripLocation (throttled and debounced)

    // Infinite scroll animation speed control logic used by the elastic grip element
    let lastRenderTime = Date.now();
    const animateScroll = () => {
      const currentTime = Date.now();
      const deltaTime = (currentTime - lastRenderTime);  // Time since last frame in seconds
      lastRenderTime = currentTime;
      // the numeric value controls the relative speed of fine scrolling
      const dragSpeedUpDown = parseFloat(localStorage.getItem('dragSpeedUpDown')) * 0.6 || 0; 
      if (container) { container.scrollTop += dragSpeedUpDown * deltaTime; requestAnimationFrame(animateScroll); }
    }; // end of elastic grip animateScroll function. 


  onMount(async () => {

      // get the conversation history slice from the backend
      num_messages = await invoke('get_num_messages');
      setInLocalStorage('totalMessages', num_messages);

    //console.log("Current number of all user, llm and bright_memory messages: " + num_messages);

      num_user_llm_messages = await invoke('get_total_llm_user_messages');
      //console.log("Current number of all user, llm and bright_memory messages: " + num_messages);
      //console.log("Current number of user and llm messages: " + num_user_llm_messages);
      //console.log("Current gripLocation: " + gripLocation);

      // start a simple debugging timer
      //const startTime = Date.now();
      fetchConversationSlice(gripLocation, num_messages); 
      //const endTime = Date.now();
      //const elapsed = endTime - startTime;

      // Infinite scroll logic

      const observerOptions = {
        root: container,
        rootMargin: '50px', // how early to start fetching the next part of the conversation
        threshold: 0
      };

      // Callback function to be executed when the top or bottom observer elements are intersecting
      // due to the user fine scrolling with the elastic grip element up or down respectively
      const observerCallback = async (entries, observer) => {

        for (const entry of entries) {
          if (entry.isIntersecting) {
            const dragSpeedUpDown = parseFloat(localStorage.getItem('dragSpeedUpDown')) || 0;
            const direction = Math.sign(dragSpeedUpDown);  // 1 for down, -1 for up

            console.log(`direction: ${direction}`);  // Debug line

            if (direction > 0) {
              console.log('Triggered later messages...');
              await fetchConversationPart("DOWN");
            } else if (direction < 0) {
              console.log('Triggered earlier messages...');
              await fetchConversationPart("UP");
            }
          }
        }
      }; // end of observerCallback function

      //const observer = new IntersectionObserver(observerCallback, observerOptions);
      observer = new IntersectionObserver(observerCallback, observerOptions); // initialized globally above
      observer.observe(topObserverElement);
      observer.observe(bottomObserverElement);

      //container.addEventListener('scroll', handleScroll); scroll wheel listener disabled for now while testing elastic grip
      requestAnimationFrame(animateScroll);

      
      // Constantly monitors the conversation container for changes
      // and obtains the exact pixel height of all the components in the conversation container
      // each time the contents of the container change. 
      // Accounts for all changes, including window resizing, user input, etc.
      const contain = document.getElementById('clip-container');
      async function measureHeight() {        
        const currentHeight = contain.scrollHeight;       
        await setInLocalStorage('targetMessagesPixelHeight', currentHeight);
        return;
      }
      const observ = new MutationObserver(async () => {
        await measureHeight();
      });
      observ.observe(contain, { childList: true, subtree: true, attributes: true, characterData: true });

  }); // end of onMount

  onDestroy(() => {
    container.removeEventListener('scroll', handleScroll);
  });

  // Non-reactive function to return the container pixel height
  async function getContainerHeight() {
      const contain = document.getElementById('clip-container');
      const currentHeight = contain.scrollHeight;
      return currentHeight;
  }

// Fetches a slice of the conversation history from the backend for the scrubbing grip element
async function fetchConversationSlice(gripLocation, num_messages) {
  const buffer = 10;
  const totalMessagesToFetch = 20;
  
  // Step 1: Calculate the target message based on gripLocation
  // Invert the gripLocation to align with the array indexing
  const targetMessage = Math.round((1 - gripLocation) * num_messages);
  //console.log(`Calculated targetMessage: ${targetMessage}`);  // Debug line
  setInLocalStorage('targetMessage', targetMessage);

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
  //console.log(`Adjusted start and end: ${start}, ${end}`);

  // Step 4: If total messages < 20, fetch all
  if (num_messages < totalMessagesToFetch) {
    start = 0;
    end = num_messages;
  }
  
  // Step 5: Fetch the conversation slice & handle top and bottom properly
  try {

    //console.log(`Initial gripLocation: ${gripLocation}, Initial num_messages: ${num_messages}`);

    const fetchedData = await invoke('fetch_conversation_history', { params: {start, end} });
    //console.log("Fetched conversation slice:", fetchedData);  // Debug line

    // Additional logic to handle initial scroll position if grip at top or bottom
    if (gripLocation === 0 && container) {
      container.scrollTop = container.scrollHeight;
    } else if (gripLocation === 1 && container) {
      container.scrollTop = 0;
    }

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
} // end of fetchConversationSlice function


// Fetches a part of the conversation history from the backend for the infinite scrolling elastic grip element
// Unlike the scrubbing grip, this function does NOT need throttling or debouncing
async function fetchConversationPart(direction) {

  let beforeScrollTop = null; // Initialize to null

  // renable the observer
  //observer.observe(bottomObserverElement);

  console.log("Running fetchConversationPart");  // Debug line
  
  const totalMessagesToFetch = 5; // Number of messages to fetch

  let start, end;

  if (direction === "UP") {
    const firstBlockIdNum = parseInt(conversation[0].block_id.split("_").pop(), 10);

    console.log('Fetching earlier messages...');
    console.log(`firstBlockIdNum: ${firstBlockIdNum}`);  // Debug line

    start = Math.max((firstBlockIdNum - 1) - totalMessagesToFetch, 0);
    end = firstBlockIdNum - 1;

  } else if (direction === "DOWN") {
    const lastBlockIdNum = parseInt(conversation[conversation.length - 1].block_id.split("_").pop(), 10);

    console.log('Fetching later messages...');
    console.log(`lastBlockIdNum: ${lastBlockIdNum}`);  // Debug line

    start = lastBlockIdNum;
    end = Math.min(lastBlockIdNum + totalMessagesToFetch, num_user_llm_messages);
  }

  // Validate start and end ranges against num_user_llm_messages
  if (start >= 0 && end <= num_user_llm_messages) {
    try {
      const fetchedData = await invoke('fetch_conversation_history', { params: {start, end} });
  
      if (fetchedData && Array.isArray(fetchedData.message)) {
        if (direction === "UP") {
      
          beforeScrollTop = await getContainerHeight();
          console.log(`beforeScrollTop: ${beforeScrollTop}`);  // Debug line

          // Add new messages to the start of the conversation array
          conversation = [...fetchedData.message, ...conversation];

          await tick(); // Wait for the DOM to update

          // Measure the scroll position after modifying the array
          const afterScrollTop = await getContainerHeight();
          console.log(`afterScrollTop: ${afterScrollTop}`);  // Debug line

          //observer.unobserve(bottomObserverElement); // disable the bottom observer

          // Calculate the difference and adjust the scroll position
          const scrollDifference = afterScrollTop - beforeScrollTop;
          console.log(`scrollDifference: ${scrollDifference}`);  // Debug line
          
          container.scrollTop = afterScrollTop - scrollDifference;
          console.log(`container.scrollTop: ${container.scrollTop}`);  // Debug line
          
        } else if (direction === "DOWN") {
          conversation = [...conversation, ...fetchedData.message]; // Update for reactivity
        }
      } else {
        console.warn("Fetched data is not in the expected format:", fetchedData);
      }
    } catch (error) {
      console.error(`Failed to fetch conversation part: ${error}`);
    }

    console.log("Current conversation:", conversation);  // Debug line

  } else {
    console.warn("Start and end values are out of range.");
  }

  // renable the observer
  //observer.observe(bottomObserverElement);

} // end of fetchConversationPart function



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


// Manipulation of gripLocation(local)/gripPosition(scrollStore) based on mouse scroll wheel events
function handleScroll() {
    

}

</script>


<div id="clip-container" bind:this={container} class="parent-container">
  <div id="conversation-container"  > 

    <div bind:this={topObserverElement} id="top-observer"></div>

    {#each conversation as entry, index}
    <div class="{index === conversation.length - 1 && isEndOfConversation ? 'last-message-class' : ''}" 
    style="{index === conversation.length - 1 && isEndOfConversation ? paddingBottom : ''} width: 100%; " 
    >
        {#if entry.source === 'user' || entry.source === 'llm'}
          {#if entry.source === 'user'}
            <UserInputSent {...entry} />
          {:else if entry.source === 'llm'}
            <LLMResponse {...entry} />
          {/if}
        {/if}
      </div>
    {/each}

    <div bind:this={bottomObserverElement} id="bottom-observer"></div>

    {#if isEndOfConversation}
      <div class="user-input">
        <UserInput bind:this={userInputComponent} on:input={scrollToBottom} />
      </div>
    {/if}
  </div>
</div>

   
  <style>

    #conversation-container {
      transition: all 0.3s ease-in-out;
      display: flex;
      flex-direction: column;
      align-items: flex-start;
      width: 100%;
      position: relative;
      bottom: 0;
      left: 7px;
      padding-bottom: 0px;
      padding-right: 0px;
      user-select: none;
      opacity: 0.9;
      transition: opacity 300ms ease-in-out;

      overflow-y: hidden; /* hides default vertical scrolling bar */
      overflow-x: hidden; /* hides default horizontal scrolling bar */

    }

    #clip-container {
    position: fixed;
    top: 0px;
    bottom: 0px;
    left: 0;
    right: 0;
    clip-path: inset(0);
    overflow: auto;
    scrollbar-width: none; /* hides scrollbar in Firefox */
    min-height: 100vh;
    width: 100%;
    overflow-y: auto; /* Makes it scrollable */


  }

  #clip-container::-webkit-scrollbar {
    display: none; /* For Chrome, Safari */
  }


  #top-observer, #bottom-observer {
    width: 100%;
    height: 1px;
  }

  .parent-container {
    position: relative;
    overflow-y: auto; /* Makes it scrollable */
    height: 100vh; /* Or some height that fits your layout */
    width: 100%;

  }

  .user-input {
    position: absolute;
    bottom: 0px;
    width: 100%;
  }

   /* This attaches to the last conversation message only, pushing it up above user input component dynamically */
  .last-message-class {
    padding-bottom: ''; /* will be dynamic, when set to dynamic height of user input component */
  }

 
  </style>
  