<script>
    let messageText = '';
    let username = 'Patrick Leamy';
    let startTime = new Date();
    let endTime = new Date();
    /**
     * @type {number | undefined}
     */
    let interval;
    let elapsedTime = '';

    // Reactive statement to control the disabled state
    let disabled = true;
    $: disabled = !messageText;

    function resizeTextarea(event) {
        event.target.style.height = 'auto'; // Reset height
        event.target.style.height = event.target.scrollHeight + 'px'; // Set height based on content
    }

    function startTimer() {
        startTime = new Date();
        interval = setInterval(() => {
            endTime = new Date();
            let diff = endTime - startTime;
            let diffSeconds = Math.floor(diff / 1000);
            let diffMinutes = Math.floor(diffSeconds / 60);
            let diffHours = Math.floor(diffMinutes / 60);
            let diffDays = Math.floor(diffHours / 24);
            elapsedTime = (diffDays > 0 ? diffDays + ' day(s) ' : '') + 
                          (diffHours % 24 > 0 ? diffHours % 24 + ' hrs ' : '') + 
                          (diffMinutes % 60 > 0 ? diffMinutes % 60 + ' min ' : '') + 
                          (diffSeconds % 60 > 0 ? diffSeconds % 60 + ' sec' : '');
        }, 1000);
    }
    
import { invoke } from '@tauri-apps/api/tauri';

function sendMessage() {
  // Call the Rust backend command with the message text
  invoke('send_prompt', { messageText })
    .then(() => {
      console.log('Message sent successfully:', messageText);
    })
    .catch(error => {
      console.error('Failed to send message:', error);
    });

  // Clear the message text
  messageText = '';

  // Stop the timer
  clearInterval(interval);
}



    import { onMount } from 'svelte';

    onMount(() => {
    resizeTextarea({ target: document.querySelector('#message-input textarea') });
    });

    // Start the timer when the script loads
    startTimer();
</script>

<div id="wrapper">
<div id="message-input">
    <div id="title" contenteditable="false">
        <span>{username}</span>
        <span id="timestamp">
            {startTime.toLocaleString('en-US', { month: 'short', day: 'numeric', year: 'numeric', hour: 'numeric', minute: 'numeric', second: 'numeric', hour12: true })} to 
            {endTime.toLocaleString('en-US', { month: 'short', day: 'numeric', year: 'numeric', hour: 'numeric', minute: 'numeric', second: 'numeric', hour12: true })} 
            ({elapsedTime})
        </span>
    </div>
    <textarea bind:value={messageText} placeholder="..." rows="1" on:input={resizeTextarea}></textarea>
    <div id="button-container">
        <button on:click={sendMessage} {disabled}></button>
    </div>
</div>
</div>

<style>

    #wrapper {
        width: 95%;
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
        position: relative;
        Left: 0;
        right: 0;
        padding-right: 50px;
        padding-top: 5px;
    }

    #message-input {
        width: 98%;
        display: flex;
        flex-direction: column;
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
    padding: 5px;
    padding-bottom: 1px;
    border: rgb(196, 181, 19) 1.5px solid;
    box-shadow: 0 0 0 0.6px #ffffff;
    border-radius: 5px;
    background-color: #1b1b1b;
    font-size: 12px;
    line-height: 15px;
    color: #e3e3e3;
    resize: none;
    overflow: hidden;
    white-space: pre-wrap;
    word-wrap: break-word;
    min-height: 24px;
    }

    #message-input textarea::placeholder {
        color: #767676;
    }

    #message-input textarea:focus {
        outline: none;
        border: rgb(141, 158, 255) 1.5px solid;
        box-shadow: 0 0 0 0.4px #ffffff;
        transition: box-shadow 0.15s ease-in-out;
    }

    #button-container {
        width: 100%;
        margin-top: 4px;
        margin-bottom: 0px;
        display: flex;
        justify-content: center;
    }

    #message-input button {
        width: 97%;
        height: 14px;
        border: 0px solid;
        border-radius: 4px;
        background-color: #3b79ff;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #FFFFFF;
        cursor: pointer;
        transition: background-color 0.1s ease-in-out 0.1s, color 0.1s ease-in-out 0.1s;
    }

    #message-input button:disabled {
        background-color: transparent;
        cursor: not-allowed;
        pointer-events: none;
    }

    #message-input button:disabled:hover {
        background-color: transparent;
        border: none;
    }

    #message-input button:not(:disabled):hover {
        background-color: #3888ff;
        border: none;
    }

    #message-input button:not(:disabled):active {
        background-color: #64a2ff;
        border: none;
    }

    #message-input button:focus {
        outline: none;
        box-shadow: 0 0 0 2px #5ea7ff;
        border: none;
    }

    #title {
        display: flex;
        font-size: 0.7em;
        justify-content: space-between;
        align-items: baseline;
        color: rgb(158, 241, 170);
        padding-left: 12px;
        padding-bottom: 2px;
    }

    #timestamp {
        font-size: 0.6em;
        color: darkgoldenrod;
        padding-right: 10px;
    }
</style> 