<script>
    import { onMount } from 'svelte';

    export let userName; // This will be populated from the user's profile
    export let messageText; // This will be populated from the array   
    export let timestampStart; // will hold the start timestamp
    export let timestampEnd; // will hold the end timestamp
    export let llmName; 
    export let role; 
  
    function resizeTextarea(event) {
      event.target.style.height = 'auto'; // Reset height
      event.target.style.height = event.target.scrollHeight + 'px'; // Set height based on content
    }
  
    onMount(() => {
      resizeTextarea({ target: document.querySelector('#message-input textarea') });
    });
  </script>
  
  <div id="wrapper">
    <div id="message-input">
      <div id="title" contenteditable="false">
        <span>{userName}</span>
        <span id="timestamp"> ({timestampStart} - {timestampEnd}) </span>
      </div>
      <textarea readonly>{messageText}</textarea>  <!-- Make it read-only -->
    </div>
  </div>
  
 
<style>

    #wrapper {
        width: 100%;
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
        position: relative;
        Left: 0;
        right: 0;
        padding-top: 5px; 
    }

    #message-input {
        width: 98%;
        display: flex;
        flex-direction: column;
        padding: 2px;
        background-color: transparent;
        border-radius: 0px;
        left: 0px;
    }

    #message-input textarea {
    padding: 6px;
    padding-bottom: 0px;
    border: rgb(82, 112, 143) 2px solid;
    border-radius: 5px;
    background-color: #1b1b1b;
    font-size: 12px;
    line-height: 13px;
    color: #e3e3e3;
    resize: none;
    overflow: hidden;
    white-space: pre-wrap;
    word-wrap: break-word;
    min-height: 24px;
    margin-right: 50px;
    }

    #message-input textarea::placeholder {
        color: #767676;
    }

    #message-input textarea:focus {
        outline: none;
        box-shadow: 0 0 0 0.5px #a7c3ff;
        transition: box-shadow 0.25s ease-in-out;
    }

    #title {
        display: flex;
        font-size: 0.5em;
        justify-content: space-between;
        align-items: baseline;
        color: rgb(49, 150, 186);
        padding-left: 3px;
        padding-bottom: 2px;
    }

    #timestamp {
        font-size: 0.6em;
        color: darkgoldenrod;
        padding-right: 60px;
    }
</style> 
  