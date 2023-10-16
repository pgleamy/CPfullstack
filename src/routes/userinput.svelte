<script>

    import { onMount, onDestroy } from 'svelte';
    import { scrollStore, setInLocalStorage } from '$lib/scrollStore.js';
    import { createEventDispatcher } from 'svelte';

    let messageText = '';
    let username = 'Patrick';
    let startTime = new Date();
    let endTime = new Date();
    /**
     * @type {number | undefined}
     */
    let interval;
    let elapsedTime = '';

    // Event dispatcher used by the resizeTextarea function below to communicate changes 
    // in this component to the parent component so the parent can then make adjustment to sibling components
    // based on the data returned by this component after it has been resized
    const dispatch = createEventDispatcher();

    // Prompt handling before it is sent by the user to update local storage and the messageText variable
    function handleInput(event) {
        
        // save the unsent prompt to local storage character by character for persistence across scrolling/resize/page events
        setInLocalStorage('unsentPrompt', event.target.value);
        //console.log('Unsent prompt returned from local storage:', localStorage.getItem('unsentPrompt'));
        
        // save the same data to the messageText variable for use in the sendMessage function
        messageText = event.target.value;
        //console.log(messageText);

    }   // end handleInput

    // Reactive statement to control the disabled state of the send button
    // If there is no message text, the button is disabled
    let disabled = true;
    $: disabled = !messageText;

   
    function handleTabKeyPress(event) {
        if (event.key === 'Tab') {
            event.preventDefault();  // Prevent focus switch
            const textarea = event.target;
            const start = textarea.selectionStart;
            const end = textarea.selectionEnd;

            // Insert the tab character at the cursor position
            textarea.value = textarea.value.substring(0, start) + '\t' + textarea.value.substring(end);

            // Move the cursor to the right of the inserted tab character
            textarea.selectionStart = textarea.selectionEnd = start + 1;

            // Update messageText to keep it in sync with textarea's value
            messageText = textarea.value;
        }
    }


    // Function to resize the textarea based on the content and to report total height of all elements in the .sticky-input container in pixels
    function resizeTextarea(event) {

        // 1. Resize the textarea based on its content
        event.target.style.height = '0px';  // Reset height
        const newHeight = event.target.scrollHeight + 'px';
        event.target.style.height = newHeight; 

        // 2. Calculate the cumulative height of all elements within the component
        const componentContainer = document.querySelector('.sticky-input');
        if (!componentContainer) {
            console.error("Could not find the .sticky-input container");
            return;
        }

        let cumulativeHeight = 0;
        Array.from(componentContainer.children).forEach(child => {
            const computedStyle = window.getComputedStyle(child);
            cumulativeHeight += child.offsetHeight +
                parseInt(computedStyle.marginTop) +
                parseInt(computedStyle.marginBottom);
        });
        
        // Tell parent container about all relevent changes to this component
        // such as: the new height of the textarea, the new cumulative height of all elements in the component
        setInLocalStorage('userInputComponentHeight', cumulativeHeight + 7); // pixel height of the whole component. 7px is a buffer so the messages above it are spaced up a bit
        setInLocalStorage('unsentPromptHeight', newHeight); // pixel height of only the textarea
        dispatch('resize', { newHeight: newHeight, cumulativeHeight: cumulativeHeight + 7 });

    } // end resizeTextarea


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
    } // end startTimer
    
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
        setInLocalStorage('unsentPrompt', '');
        // Stop the timer
        clearInterval(interval);
        
        setInLocalStorage('unsentPromptHeight', 27);
        setInLocalStorage('userInputComponentHeight', 81); 

        const textarea = document.querySelector('.sticky-input textarea');
        //console.log('message-input textarea:', textarea);
        if (textarea) {
            textarea.style.height = (localStorage.getItem('unsentPromptHeight') || '0') + 'px';
            //console.log('message-input textarea height:', textarea.style.height);

        }

    } // end sendMessage



    onMount(() => {

        messageText = localStorage.getItem('unsentPrompt') || '';
        // set the textarea height to the height of the unsent prompt
        const textarea = document.querySelector('.sticky-input textarea');
        //console.log('message-input textarea:', textarea);
        if (textarea) {
            textarea.style.height = (localStorage.getItem('unsentPromptHeight') || '0') + 'px';
            //console.log('message-input textarea height:', textarea.style.height);

        }

    }); // end onMount


    onDestroy(() => {

        // Stop the timer
        clearInterval(interval);

    }); // end onDestroy

    // Start the prompt timer when the script loads
    startTimer()

</script>


<div id="message-input" class="sticky-input">
    <div id="title" contenteditable="false">
        <span>{username}</span>
        <span id="timestamp">
            -
            {endTime.toLocaleString('en-US', { month: 'short', day: 'numeric', hour: 'numeric', minute: 'numeric', hour12: true })} 
            | {elapsedTime}
        </span>
    </div>
    <textarea bind:value={messageText} placeholder="..." rows="1" on:input={resizeTextarea} on:input={handleInput} on:keydown={handleTabKeyPress} name="userinput"></textarea>
    <div id="button-container">
        <button on:click={sendMessage} {disabled}></button>
    </div>
</div>



<style>

    .sticky-input {
        position: sticky;
        bottom: 0;
        z-index: 999; 
        background: transparent;
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
        color: #ffffff;
        resize: none;
        overflow: hidden;
        white-space: pre-wrap;
        word-wrap: break-word;
        min-height: 0px;
        tab-size: 3;
        -webkit-font-smoothing: antialiased;
    }

    #message-input textarea::placeholder {
        color: #fcfcfc;
        font-size: 10px;
        -webkit-font-smoothing: antialiased;
    }

    #message-input textarea:focus {
        outline: none;
        border: rgb(22, 64, 20) 2px solid;
        box-shadow: 0 0 0 0.3px #323232;
        transition: box-shadow 0.15s ease-in-out;
        -webkit-font-smoothing: antialiased;
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
        height: 18px;
        border: 0px solid;
        border-radius: 4px;
        background-color: rgb(46, 129, 41);
        display: flex;
        align-items: center;
        justify-content: center;
        color: #FFFFFF;
        cursor: pointer;
        transition: background-color 0.05s ease-in-out 0.05s;
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
        background-color: #00FF00;
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
        color: rgb(111, 217, 127);
        padding-left: 3px;
        padding-bottom: 0px;
        -webkit-font-smoothing: antialiased;
    }

    #timestamp {
        font-size: 0.8em;
        color: rgb(194, 194, 194);
        padding-left: 2px;
        padding-bottom: 3px;
        -webkit-font-smoothing: antialiased;
    }

    
</style> 