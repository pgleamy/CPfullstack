<script>
    import UserInput from './userinput.svelte';
    import UserInputSent from './userinputsent.svelte';
    import LLMResponse from './llmresponse.svelte';
    // reactive state management for scrollsearch component
    import {scrollStore} from '$lib/scrollStore.js'; 
    
    // This is a placeholder for the conversation data.
    // In the real application, this will be fetched from the SQL database.
    let conversation = [
        { 
            type: 'user', 
            userName: 'Patrick Leamy', 
            messageText: 'Hello, Argus!', 
            timestampStart: 'Sep 1, 2023, 12:00 PM',
            timestampEnd: 'Sep 1, 2023, 12:00:30 PM',
            llmName: 'Argus',
            role: 'Talker'
        },
        { 
            type: 'llm', 
            llmName: 'Argus', 
            messageText: 'Hello, Patrick! How can I assist you today?', 
            responseTime: 'Sep 1, 2023, 12:01 PM',
            role: 'Talker'
        },
        { 
            type: 'user', 
            userName: 'Patrick Leamy', 
            messageText: 'Hello, Iris!', 
            timestampStart: 'Sep 1, 2023, 12:00 PM',
            timestampEnd: 'Sep 1, 2023, 12:00:30 PM',
            llmName: 'Iris',
            role: 'Talker'
        },
        { 
            type: 'llm', 
            llmName: 'Iris', 
            messageText: 'Hello, Patrick! How can I assist you today?', 
            responseTime: 'Sep 1, 2023, 12:01 PM',
            role: 'Talker'
        },
        { 
            type: 'user', 
            userName: 'Patrick Leamy', 
            messageText: 'Hello again, Argus!', 
            timestampStart: 'Sep 1, 2023, 12:00 PM',
            timestampEnd: 'Sep 1, 2023, 12:00:30 PM',
            llmName: 'Argus',
            role: 'Talker'
        },
    ];
     
  
  // Function to scroll to the bottom
  function scrollToBottom() {
    console.log('Scrolling to bottom');
    const conversationContainer = document.getElementById('conversation-container');
    conversationContainer.scrollTop = conversationContainer.scrollHeight;
  }

  </script>

<div id="clip-container">
  <div id="conversation-container" on:scrollToLatest={scrollToBottom}> 
    {#each conversation as entry}
      {#if entry.type === 'user'}
        <UserInputSent {...entry} />
      {:else if entry.type === 'llm'}
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
  