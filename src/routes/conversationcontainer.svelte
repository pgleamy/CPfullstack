<script>

    import UserInput from './userinput.svelte';
    import virtualContainer from './virtualContainer.svelte';

    import UserInputSent from './userinputsent.svelte';
    import LLMResponse from './llmresponse.svelte';

    // reactive state management for scrollsearch component
    import {scrollStore, get, setInLocalStorage, updateScrollSettings} from '$lib/scrollStore.js';
    import { onMount, onDestroy } from 'svelte';
    import { invoke } from "@tauri-apps/api/tauri";
    import { tick } from 'svelte';

    let conversation = []; // conversation history slice as requested from the backend
    let num_messages = 0; // total number of user, llm and bright_memory messages in the conversation
    let num_user_llm_messages = 0; // total number of user and llm messages in the conversation
    let container; // reference to the conversation container element    

    const userInputFixedHeight = 300; // fixed height of the user input component. Used to push up the last message at end to be visible above the user input component area

     // Infinite scroll observers
    let topObserverElement;
    let bottomObserverElement;
    let userInputComponent; // Initialize the variable to bind the UserInput component
    let observer; // Initialize the observer variable for the infinite scroll logic

    // UP scroll positioning calculation variables for infinite scroll logic in UP direction
    let beforeScrollTop; // original scrollTop
    let afterScrollTop; // new scrollTop
    let scrollTopDifference; // difference between beforeScrollTop and afterScrollTop
    let beforeContainerHeight; // original height of entire conversation container before any changes
    let afterContainerHeight; // new height of entire conversation container after any changes
    let containerHeightDifference; // difference between beforeContainerHeight and afterContainerHeight
    let newScrollTop; // new scrollTop after accounting for the difference between before and after scrollTop and containerHeight

    let hasReachedStart = false; // Initialize the flag for the start of the conversation
    let hasReachedEnd = false; // Initialize the flag for the end of the conversation

    let lastScrollTop = 0;
    let isScrolling = false;
    $: if (targetMessage != totalMessages) { isScrolling = false } // Reactive statement to reset isScrolling when not at the bottom of the conversation

    
    $: targetMessage = $scrollStore.targetMessage; // Reactive assignment
    $: totalMessages = $scrollStore.totalMessages; // Reactive assignment

    // used by the mouse wheel event listener to determine the direction of the scroll and execution limiting
    let shouldFetchUp = false;
    let shouldFetchDown = false;

    // paddingBottom connects the top of user input to the bottom of last message for when the user scrolls to bottom
    let paddingBottom = '';  // Declare a variable to hold the padding-bottom value
    // Create a reactive statement to update paddingBottom whenever userInputHeight changes
    $: {
      if (isEndOfConversation) {
          paddingBottom = `padding-bottom: ${userInputFixedHeight}px;`;
          // scroll to bottom of conversation container so the send button is always visible
          scrollToBottom();
      } else {
          paddingBottom = '';
      }
    } // end of reactive statement to update paddingBottom
  
    // Set flags indicating the conversation array contains either of the first or last message in the conversation
    // Flags can then be use for various logic, e.g. to prevent the user from scrolling past the start or end of the conversation
    // or to prevent operations for seeking out of bounds of the conversation
    function updateEdgeFlags(fetchedMessages) {
      //console.log(`updateEdgeFlags ran`);  // Debug line
      hasReachedStart = fetchedMessages.some(msg => msg.block_id === "block_id_1"); 
      //console.log(fetchedMessages);  // Debug line
      //console.log(`hasReachedStart: ${hasReachedStart}`);  // Debug line
      hasReachedEnd = fetchedMessages.some(msg => msg.block_id === `block_id_${num_user_llm_messages}`);
      //console.log(`hasReachedEnd: ${hasReachedEnd}`);  // Debug line
    } // end of updateEdgeFlags function %% currently failing to update the flags correctly when user elastic scrolls in from prior message group

    function scrollToBottom() {
      if (isEndOfConversation && !isScrolling) {
        if (container) {
          container.scrollTop = container.scrollHeight;
        }
        tick().then(() => {
          if (userInputComponent) {
            container.scrollTop = container.scrollHeight;
            //console.log(`scrollToBottom ran`);
            //console.log(`scrollToBottom ran`);
          }
        });
      }
    } // end of scrollToBottom function


    // Start/End of conversation flags
    // AND to position the view of the messages correctly when the user input component is displayed or when at top of conversation showing from very start
    let isEndOfConversation = false;  // Initialize to false
    let isStartOfConversation = false; // Initialize to true
    $: {
        if (isEndOfConversation = (targetMessage === totalMessages)) {/* logic to check if the last fetched message is the last message in the entire conversation */
          //console.log(`isEndOfConversation: ${isEndOfConversation}`);
        } 
        if (isStartOfConversation = (targetMessage === 0)) {/* logic to check if the last fetched message is the first message in the entire conversation */
          //console.log(`isStartOfConversation: ${isStartOfConversation}`);
        }
      } // end of reactive statement to start/end of conversation 


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
      fetchConversationSlice(gripLocation, num_messages); // places the conversation back to the last known position
      //const endTime = Date.now();
      //const elapsed = endTime - startTime;

      // Infinite scroll logic

      const observerOptions = {
        root: container,
        rootMargin: '10px', // how early to start fetching the next part of the conversation
        threshold: 0
      };

      // Callback function to be executed when the top or bottom observer elements are intersecting
      // due to the user fine scrolling with the elastic grip element up or down respectively




const observerCallback = async (entries, observer) => {
  for (const entry of entries) {
    if (entry.isIntersecting) {
      if (entry.target.id === 'top-observer') {
        shouldFetchUp = true;
      } else if (entry.target.id === 'bottom-observer') {
        shouldFetchDown = true;
      }
      
      const dragSpeedUpDown = parseFloat(localStorage.getItem('dragSpeedUpDown')) || 0;
      const direction = Math.sign(dragSpeedUpDown);  // 1 for down, -1 for up

      if (direction > 0 && shouldFetchDown) {
        if (hasReachedEnd) {
          return;  // Skip the fetch operation
        }
        await fetchConversationPart("DOWN");
        shouldFetchDown = false; // Reset the flag
      } else if (direction < 0 && shouldFetchUp) {
        if (hasReachedStart) {
          return;  // Skip the fetch operation
        }
        await fetchConversationPart("UP");
        shouldFetchUp = false; // Reset the flag
      }
    }
  }
};






      /* // SECOND VERSION
      const observerCallback = async (entries, observer) => {
      for (const entry of entries) {
        if (entry.isIntersecting) {
          const dragSpeedUpDown = parseFloat(localStorage.getItem('dragSpeedUpDown')) || 0;
          const direction = lastWheelDirection ? lastWheelDirection : Math.sign(dragSpeedUpDown);  // Use wheel direction if available

          lastWheelDirection = null;  // Reset the wheel direction

          if (direction === "DOWN" || direction > 0) {
            if (hasReachedEnd) {
              return;  // Skip the fetch operation
            }
            await fetchConversationPart("DOWN");
          } else if (direction === "UP" || direction < 0) {
            if (hasReachedStart) {
              return;  // Skip the fetch operation
            }
            await fetchConversationPart("UP");
          }
        }
      }
    };
    */
 

      /* // OLDER VERSION
      const observerCallback = async (entries, observer) => {
        for (const entry of entries) {
          if (entry.isIntersecting) {
            const dragSpeedUpDown = parseFloat(localStorage.getItem('dragSpeedUpDown')) || 0;
            const direction = Math.sign(dragSpeedUpDown);  // 1 for down, -1 for up

            if (direction > 0) {
              if (hasReachedEnd) {
                //console.log("At END of Conversation");  // Debug line
                return;  // Skip the fetch operation
              }
              await fetchConversationPart("DOWN");
            } else if (direction < 0) {
              if (hasReachedStart) {
                //console.log("At START of Conversation");  // Debug line
                return;  // Skip the fetch operation
              }
              await fetchConversationPart("UP");
            }
          }
        }
      }; // end of observerCallback function
      */


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


      // Event listener to control scrollBottom function when at end of entire conversation
      contain.addEventListener("scroll", function() {
      let st = contain.scrollTop;
      let atBottom = targetMessage === totalMessages; // Check if at the bottom
      
      if (st != lastScrollTop && (targetMessage === totalMessages)) { // Add the atBottom condition
        isScrolling = true;
        //console.log(`Scrolling at the bottom`);
        } else if (targetMessage !== totalMessages) {
          isScrolling = false;
          //console.log(`Not scrolling at the bottom`);
          return;
        }
        lastScrollTop = st <= 0 ? 0 : st;
        //console.log(`last bit ran`);
      }, false);






      // Add the mouse wheel event listener
      container.addEventListener('wheel', handleWheelScroll);






  }); // end of onMount


  onDestroy(() => {
    //container.removeEventListener('scroll', handleScroll);
    //container.removeEventListener('wheel', handleWheelScroll);
  });




  
function handleWheelScroll(event) {
  const direction = event.deltaY > 0 ? "DOWN" : "UP";

  if (direction === "UP" && shouldFetchUp && !hasReachedStart) {
    fetchConversationPart(direction);
    shouldFetchUp = false; // Reset the flag after fetching
  } else if (direction === "DOWN" && shouldFetchDown && !hasReachedEnd) {
    fetchConversationPart(direction);
    shouldFetchDown = false; // Reset the flag after fetching
  }
}



  /* // OLDER VERSION
  let lastWheelDirection = null;  // "UP" or "DOWN"
  function handleWheelScroll(event) {
  const direction = event.deltaY > 0 ? "DOWN" : "UP";

  if ((direction === "UP" && !hasReachedStart) || (direction === "DOWN" && !hasReachedEnd)) {
    fetchConversationPart(direction);
  }
}
*/




  
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

    // scrolls to the middle of the fetched message slice
  
    if (gripLocation > 0 && gripLocation < 1) {
      await tick();  // Wait for Svelte to update the DOM
      const sliceHeight = await getContainerHeight();
      container.scrollTop = (sliceHeight/2);
    }
    

    if (fetchedData && Array.isArray(fetchedData.message)) {
      conversation = fetchedData.message;


      // save to local storage conversationArray
      localStorage.setItem('conversationArray', JSON.stringify(conversation));

      updateEdgeFlags(fetchedData.message); // Update the edge flags
      //console.log(`Updated conversation slice: ${conversation}`);  // Debug line
      //console.log*(conversation);  // Debug line
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
let lastFetchedDownMessages = null; // Initialize the variable to store the last fetched messages in the DOWN direction
let lastFetchedUpMessages = null; // Initialize the variable to store the last fetched messages 
async function fetchConversationPart(direction) {

  //console.log("fetchConversationPart()");  // Debug line
  const totalMessagesToFetch = 10; // Number of messages to fetch
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
  
  if(end >= num_user_llm_messages) {
    end = num_user_llm_messages;
    start = end - totalMessagesToFetch;
  }

  //console.log(`end: ${end}`);  // Debug line

  // Validate start and end ranges against num_user_llm_messages
  if (start >= 0 && end <= num_user_llm_messages) {

    try {
      const fetchedData = await invoke('fetch_conversation_history', { params: {start, end} });

      // save to local storage conversationArray
      localStorage.setItem('conversationArray', JSON.stringify(fetchedData.message));

      if (fetchedData && Array.isArray(fetchedData.message)) {

        updateEdgeFlags(fetchedData.message); // Update the edge flags

        if (direction === "UP") {

          beforeScrollTop = container.scrollTop; // Measure the scroll position before modifying the array
          beforeContainerHeight = container.scrollHeight; // Measure the container height before modifying the array

          //console.log(`beforeScrollTop: ${beforeScrollTop}`);  // Debug line
          //console.log(`beforeContainerHeight: ${beforeContainerHeight}`);  // Debug line

          // CONDITIONALLY add new messages to the start of the conversation array
          if (!hasReachedStart) {
            conversation = [...fetchedData.message, ...conversation];

            // save to local storage conversationArray
            localStorage.setItem('conversationArray', JSON.stringify(conversation));

            //console.log(`Duplicate Start. Did not prepend.`);  // Debug line
          } 

          //console.log("Current conversation:", conversation);  // Debug line
             
          await tick(); // Wait for the DOM to update


          // Use requestAnimationFrame to wait until the next repaint
          requestAnimationFrame(async () => {
            
            afterScrollTop = container.scrollTop; // Measure the scroll position after modifying the array
            afterContainerHeight = container.scrollHeight; // Measure the container height after modifying the array

            //console.log(`afterScrollTop: ${afterScrollTop}`);  // Debug line
            //console.log(`afterContainerHeight: ${afterContainerHeight}`);  // Debug line

            // Calculate the difference and adjust the scroll position
            scrollTopDifference = afterScrollTop - beforeScrollTop;
            containerHeightDifference = afterContainerHeight - beforeContainerHeight;
            //console.log(`scrollTopDifference: ${scrollTopDifference}`);  // Debug line
            //console.log(`ContainerHeightDifference: ${containerHeightDifference}`);  // Debug line

            //container.scrollTop = afterScrollTop - scrollDifference;
            newScrollTop = beforeScrollTop + scrollTopDifference + containerHeightDifference;
            //console.log(`newScrollTop: ${newScrollTop}`);  // Debug line
            container.scrollTop = newScrollTop;
            //console.log(`container.scrollTop: ${container.scrollTop}`);  // Debug line
          });

        } else if (direction === "DOWN") {
          //conversation = [...conversation, ...fetchedData.message]; // Update for reactivity

          // If the messages are not the same, append them to the conversation array
          
            if (!hasReachedEnd) {
              conversation = [...conversation, ...fetchedData.message]; // Update for reactivity
              //console.log(`Duplicate End. Did not append.`);  // Debug line

              // save to local storage conversationArray
              localStorage.setItem('conversationArray', JSON.stringify(conversation));

            }

            // Update the last fetched messages
            lastFetchedDownMessages = fetchedData.message;
          
        }


      } else {
        console.warn("Fetched data is not in the expected format:", fetchedData);
      }
    } catch (error) {
      console.error(`Failed to fetch conversation part: ${error}`);
    }

  } else {
    console.warn("Start and end values are out of range.");
  }

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


// Track the message displayed in the very middle of user's viewable area
function findMiddleVisibleMessage() {
  if (!container) {
    return null;
  }
  
  const messages = container.querySelectorAll('.message-class');
  const middle = container.scrollTop + container.clientHeight / 2;

  let closestMessageIndex = null;
  let closestDistance = Infinity;

  for (let i = 0; i < messages.length; i++) {
    const rect = messages[i].getBoundingClientRect();
    const containerRect = container.getBoundingClientRect();
    const messageMiddle = rect.top - containerRect.top + container.scrollTop + rect.height / 2;
    
    const distanceToMiddle = Math.abs(middle - messageMiddle);

    if (distanceToMiddle < closestDistance) {
      closestDistance = distanceToMiddle;
      closestMessageIndex = i + 1; // add one to line up properly at start/end of conversation
    }
  }
  return closestMessageIndex; // Returns the index of the message closest to the middle
}
$: {
  if (container) {
    const middleVisibleMessageIndex = findMiddleVisibleMessage();
    if (middleVisibleMessageIndex !== null) {
      //setInLocalStorage('middleVisibleMessageIndex', middleVisibleMessageIndex);
      
      // Access the block_id of the middle visible message
      const middleVisibleMessage = conversation[middleVisibleMessageIndex];
      const middleVisibleBlockId = middleVisibleMessage ? middleVisibleMessage.block_id : null;
      
      // Do something with middleVisibleBlockId, for example, save it to local storage
      if (middleVisibleBlockId !== null) {
          // Extract the numeric part from the block_id
          const blockIdNumber = middleVisibleBlockId.split('_').pop();
          const totalMessages = num_user_llm_messages;

          // const gripPosition = 1 - (blockIdNumber / totalMessages) ;
          // Store only the numeric part in local storage
          setInLocalStorage('middleVisibleBlockId', blockIdNumber);
      }
    }
  }
}

</script>


<div id="clip-container" bind:this={container} class="parent-container">
  <div id="conversation-container">

    <div bind:this={topObserverElement} id="top-observer" ></div>

    {#each conversation as entry, index}
      <div class="{index === conversation.length - 1 ? 'last-message-class' : 'message-class'}" 
      style="{index === conversation.length - 1 ? paddingBottom : ''} width: 100%;" 
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
    <div bind:this={bottomObserverElement} id="bottom-observer" ></div>
  </div> <!-- End of conversation-container -->
</div> <!-- End of clip-container -->

<div class="user-input-container">
  <UserInput bind:this={userInputComponent} />
</div>


  <style>

    #conversation-container {
      transition: all 0.3s ease-in-out;
      display: flex;
      flex-direction: column;
      align-items: flex-start;
      width: 100%;
      position: relative;
      bottom: 0px;
      left: 7px;
      padding-bottom: 5px;
      padding-right: 0px;
      user-select: none;
      opacity: 0.9;
      transition: opacity 300ms ease-in-out;

      overflow-y: hidden; /* hides default vertical scrolling bar */
      overflow-x: hidden; /* hides default horizontal scrolling bar */

      overflow: hidden; /* hides default scrolling bars */

      scroll-behavior: smooth;

    }

    #clip-container {
    position: fixed;
    top: 0px;
    bottom: 10px;
    left: 0px;
    right: 0px;
    overflow: hidden;
    scrollbar-width: none; /* hides scrollbar in Firefox */
    min-height: 96%;
    width: 100%;
    height: 100%;
    overflow-y: auto; /* Makes it scrollable */
    background-color: transparent;

    
   
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

    margin-bottom: 15px; 
  }

   /* This attaches to the last conversation message only, pushing it up above user input component dynamically */
  .last-message-class {
    padding-bottom: ''; /* will be dynamic, when set to dynamic height of user input component */
 
  }


.user-input-container {
  position: fixed;
  bottom: 1.5px;
  left: 7px;
  right: 53px;
  max-height: 100vh; /* Maximum of 20% of the view height = 40vh */
  overflow-y: auto;  /* Hide overflow */
  padding-right:3px;
  overflow: auto; /* hides default scrolling bars */
  overflow-x: hidden; /* hides default horizontal scrolling bar */
}
 
  </style>
  