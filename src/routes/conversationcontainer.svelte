<script>
    import UserInput from './userinput.svelte';
    import UserInputSent from './userinputsent.svelte';
    import LLMResponse from './llmresponse.svelte';
    
    // This is a placeholder for the conversation data.
    // In the real application, this will be fetched from the SQL database.
    let conversation = [
        { 
            type: 'user', 
            userName: 'Patrick Leamy', 
            messageText: 'Hello, Jarvis!', 
            timestampStart: 'Sep 1, 2023, 12:00 PM',
            timestampEnd: 'Sep 1, 2023, 12:00:30 PM',
            llmName: 'Jarvis',
            role: 'Talker'
        },
        { 
            type: 'llm', 
            llmName: 'Jarvis', 
            messageText: 'Hello, Patrick! How can I assist you today?', 
            responseTime: 'Sep 1, 2023, 12:01 PM',
            role: 'Talker'
        },
        { 
            type: 'user', 
            userName: 'Patrick Leamy', 
            messageText: 'Hello, Jarvis!', 
            timestampStart: 'Sep 1, 2023, 12:00 PM',
            timestampEnd: 'Sep 1, 2023, 12:00:30 PM',
            llmName: 'Jarvis',
            role: 'Talker'
        },
        { 
            type: 'llm', 
            llmName: 'Jarvis', 
            messageText: 'Hello, Patrick! How can I assist you today?', 
            responseTime: 'Sep 1, 2023, 12:01 PM',
            role: 'Talker'
        },
        { 
            type: 'user', 
            userName: 'Patrick Leamy', 
            messageText: 'Hello, Jarvis!', 
            timestampStart: 'Sep 1, 2023, 12:00 PM',
            timestampEnd: 'Sep 1, 2023, 12:00:30 PM',
            llmName: 'Jarvis',
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
      transition: all 0.4s ease-in-out;
      display: flex;
      flex-direction: column;
      align-items: flex-start;
      width: 100%;
      position: relative;
      bottom: 0;
      left: 6px !important;
      padding-bottom: 10px;
      padding-right: 0px;
      overflow: hidden;
    }

    #clip-container {
    position: fixed;
    top: 79px;
    bottom: 10px;
    left: 0;
    right: 0;
    clip-path: inset(0);
    overflow: hidden;
  }
 
  </style>
  