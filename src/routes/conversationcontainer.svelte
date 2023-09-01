<script>
    import UserInput from './userinput.svelte';
    import UserInputSent from './userinputsent.svelte';
    import LLMResponse from './llmresponse.svelte';
    
    // This is a placeholder for the conversation data.
    // In the real application, this will be fetched from the SQL database.
    let conversation = [
        { 
            type: 'user', 
            username: 'Patrick Leamy', 
            text: 'Hello, Jarvis!', 
            timestampStart: 'Sep 1, 2023, 12:00 PM',
            timestampEnd: 'Sep 1, 2023, 12:00:30 PM',
            llmName: 'Jarvis',
            role: 'Talker'
        },
        { 
            type: 'llm', 
            llmName: 'Jarvis', 
            text: 'Hello, Patrick! How can I assist you today?', 
            timestamp: 'Sep 1, 2023, 12:01 PM',
            role: 'Talker'
        }
    ];

  </script>
  
  <div id="conversation-container">
    {#each conversation as entry}
        {#if entry.type === 'user'}
            <UserInputSent {entry} />
        {:else if entry.type === 'llm'}
            <LLMResponse {entry} />
        {/if}
    {/each}
    <UserInput />
</div>
   
  <style>
    #conversation-container {
      /* Your styling here */
      display: flex;
      flex-direction: column;
      align-items: flex-end;
      width: 100%;
      position: fixed;
      bottom: 0;
      left: 30;
      padding-top: 100px;
      padding-bottom: 20px;
      mask-image: linear-gradient(to bottom, transparent, black 10%, black 90%, transparent);
    }
  </style>
  