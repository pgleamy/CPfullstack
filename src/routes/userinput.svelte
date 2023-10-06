<script>

    import { onMount, onDestroy, afterUpdate } from 'svelte';
    import { scrollStore, setInLocalStorage } from '$lib/scrollStore.js';
    import { createEventDispatcher } from 'svelte';

    const dispatch = createEventDispatcher();

    // Prompt handling before it is sent by the user
    function handleInput(event) {
        // tells conversationcontainer everytime a text event occurs
        dispatch('input', event.target.value);
        // save the unsent prompt to local storage character by character for persistence across scrolling/resize/page events
        setInLocalStorage('unsentPrompt', event.target.value);
        //console.log('Unsent prompt returned from local storage:', localStorage.getItem('unsentPrompt'));
        messageText = event.target.value;
        //console.log(messageText);
    }

    let messageText = '';
    let messageTextBackup = '';
    let username = 'Patrick';
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


    // Function to resize the textarea based on the content and report total height of all elements in the .sticky-input container in pixels
    function resizeTextarea(event) {

        // Directly use event.target instead of querying the DOM
        const textarea = event.target;

        // Dynamically set textarea height based on scrollHeight
        textarea.style.height = 'auto';
        textarea.style.height = `${textarea.scrollHeight}px`;

        const stickyInputContainer = document.querySelector('.sticky-input');
        if (!stickyInputContainer) return;

        // Calculate cumulative height
        let cumulativeHeight = Array.from(stickyInputContainer.children).reduce((acc, child) => {
            const computedStyle = window.getComputedStyle(child);
            return acc + child.offsetHeight + parseInt(computedStyle.marginTop) + parseInt(computedStyle.marginBottom);
        }, 0);

        // Update height and unsentPrompt in local storage
        setInLocalStorage('userInputHeight', cumulativeHeight);
        setInLocalStorage('unsentPrompt', textarea.value);

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
                          (diffMinutes % 60 > 0 ? diffMinutes % 60 + ' min ' : '');
        }, 60000);
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

    function handleTabKeyPress(event) {
        if (event.key === 'Tab') {
            event.preventDefault();  // Prevent focus switch
            const start = event.target.selectionStart;
            const end = event.target.selectionEnd;

            // Insert the tab character at the cursor position
            messageText = messageText.substring(0, start) + '\t' + messageText.substring(end);

            // Move the cursor to the right of the inserted tab character
            event.target.selectionStart = event.target.selectionEnd = start + 1;
        }
    }

    onMount(() => {

        requestAnimationFrame(() => {

            // Get the unsent prompt from local storage and set messageText
            const unsentPrompt = localStorage.getItem('unsentPrompt');
            if (unsentPrompt) {
                messageText = unsentPrompt;
            }

            const textarea = document.querySelector('#message-input textarea');
            textarea.value = messageText;  // Set the value directly on the textarea element

            console.log('onMount ran with userInputHeight:', $scrollStore.userInputHeight + 'px');
           
            resizeTextarea({ target: textarea });

            console.log('after resizeTextarea onMount ran with userInputHeight:', $scrollStore.userInputHeight + 'px');


        });
        dispatch('mounted', { resizeTextarea: () => resizeTextarea({ target: textarea }) });

    }); // end onMount

    // Start the prompt timer when the script loads
    startTimer();
    //console.log('User Input component LOADED');

</script>

<div id="wrapper" class="sticky-input">
<div id="message-input">
    <div id="title" contenteditable="false">
        <span>{username}</span>
        <span id="timestamp">
            -
            {endTime.toLocaleString('en-US', { month: 'long', day: 'numeric', hour: 'numeric', minute: 'numeric', hour12: true })} 
            | {elapsedTime}
        </span>
    </div>
    <textarea bind:value={messageText} placeholder="..." on:input={resizeTextarea} input type="text" on:input={handleInput} on:keydown={handleTabKeyPress} name="userinput"></textarea>
    <div id="button-container">
        <button on:click={sendMessage} {disabled}></button>
    </div>
</div>
</div>

<style>

    .sticky-input {
        position: sticky;
        bottom: 0;
        z-index: 999; 
        background: transparent;
    }

    #wrapper {
        width: 100%;
        display: contents;
        flex-direction: column;
        justify-content: flex-end;
        position: relative;
        Left: 0;
        right: 0;
        padding-top: 0px;
        padding-bottom: 0px;
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
        padding: 0px;
        background-color: transparent;
        border-radius: 0px;
        left: 0px;
        padding-bottom: 12px;
    }

    #message-input textarea {
    padding: 8px;
    padding-bottom: 2px;
    padding-top: 5px;
    margin-right: 50px;
    border: rgba(249, 245, 10, 0.298) 2px solid;
    box-shadow: 0 0 0 0.3px #323232;
    border-radius: 4px;
    background-color: #080808;
    font-size: 14px;
    line-height: 20px;
    color: #cccccc;
    resize: none;
    overflow: hidden;
    white-space: pre-wrap;
    word-wrap: break-word;
    min-height: 0px;
    tab-size: 3;
    }

    #message-input textarea::placeholder {
        color: #bbbbbb;
        font-size: 10px;
    }

    #message-input textarea:focus {
        outline: none;
        border: rgb(22, 64, 20) 2px solid;
        box-shadow: 0 0 0 0.3px #323232;
        transition: box-shadow 0.15s ease-in-out;
    }

    #button-container {
        width: calc(100% - 50px);
        margin-top: 5px;
        margin-bottom: 0px;
        display: flex;
        justify-content: center;
        align-items: cente
    }

    #message-input button {
        width: 95%;
        height: 14px;
        border: 0px solid;
        border-radius: 4px;
        background-color: rgb(22, 64, 20);
        display: flex;
        align-items: center;
        justify-content: center;
        color: #FFFFFF;
        cursor: pointer;
        transition: background-color 0.1s ease-in-out 0.1s;
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
        background-color: #1d437b;
        border: none;
    }

    #message-input button:not(:disabled):active {
        background-color: #4673b7;
        border: none;
    }

    #message-input button:focus {
        outline: none;
        box-shadow: 0 0 0 2px #5ea7ff;
        border: none;
    }

    #title {
        display: flex;
        font-size: 0.8em;
        justify-content: left;
        align-items: baseline;
        color: rgb(70, 145, 81);
        padding-left: 3px;
        padding-bottom: 0px;
    }

    #timestamp {
        font-size: 0.85em;
        color: rgb(151, 144, 144);
        padding-left: 2px;
        padding-bottom: 3px;
    }

    
</style> 