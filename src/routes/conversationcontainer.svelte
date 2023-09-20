<script>
    import UserInput from './userinput.svelte';
    import UserInputSent from './userinputsent.svelte';
    import LLMResponse from './llmresponse.svelte';
    // reactive state management for scrollsearch component
    import {scrollStore} from '$lib/scrollStore.js';
    import { onMount, onDestroy } from 'svelte';
    import { invoke } from "@tauri-apps/api/tauri";

    let conversation = []; // conversation history slice as requested from the backend
    let num_messages = 0; // total number of messages in the conversation
    let gripLocation = 0; // 0 = bottom, 1 = top
    $: gripLocation = $scrollStore.gripPosition; // sets gripLocation to the current gripPosition in scrollStore

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
      //const { message } = await invoke("fetch_conversation_history", {
      //params: { start: 0, end: 2 }
      //});
      //conversation = message;

    });



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






  </script>


<div id="clip-container">
  <div id="conversation-container"> 
    {#each conversation as entry}
      {#if entry.source === 'user'}
        <UserInputSent {...entry} />
      {:else if entry.source === 'llm'}
        <LLMResponse {...entry} />
      {/if}
    {/each}
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
      overflow: hidden;
      user-select: none;
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
 
  </style>
  