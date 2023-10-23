<script>

    import { onMount, onDestroy } from 'svelte';
    import { scrollStore, setInLocalStorage } from '$lib/scrollStore.js';
    import { createEventDispatcher } from 'svelte';

    let messageText = '';
    let username = 'Patrick';
    
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
        const newHeight = (event.target.scrollHeight - 20) + 'px';
        event.target.style.height = newHeight; 

        // 2. Calculate the cumulative height of all elements within the component
        const componentContainer = document.querySelector('#message-input');
        //console.log('componentContainer:', componentContainer);
        if (!componentContainer) {
            console.error("Could not find the #message-input container");
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
        setInLocalStorage('userInputComponentHeight', cumulativeHeight ); // pixel height of the whole component. 7px is a buffer so the messages above it are spaced up a bit
        setInLocalStorage('unsentPromptHeight', newHeight); // pixel height of only the textarea
        dispatch('resize', { newHeight: newHeight, cumulativeHeight: cumulativeHeight });




       // Additional logic to keep cursor in view
       const unsentPromptHeight = parseInt(localStorage.getItem('unsentPromptHeight'));

    // Additional logic to keep cursor in view
    const textarea = event.target;  // You already have this
    const cursorPosition = textarea.selectionEnd;
    const textBeforeCursor = textarea.value.substring(0, cursorPosition);
    const textAreaLineHeight = 20;  // Assuming line-height is 20px
    const lines = textBeforeCursor.split('\n');
    let cursorLine = 0;

    for (let line of lines) {
        cursorLine += Math.ceil((line.length * 8) / (textarea.clientWidth));  // Assuming average character width is 8px
    }

    const cursorPixelPosition = cursorLine * textAreaLineHeight;

    // Scroll the textarea if necessary
    const maxViewablePixel = textarea.scrollTop + textarea.clientHeight;
    if (cursorPixelPosition > maxViewablePixel) {
        textarea.scrollTop = cursorPixelPosition - textarea.clientHeight;
    } else if (cursorPixelPosition < textarea.scrollTop) {
        textarea.scrollTop = cursorPixelPosition;
    }

    console.log(unsentPromptHeight, textarea.clientHeight);
    // If the unsentPromptHeight exceeds the max height, then we need to adjust the scroll
    if (unsentPromptHeight > textarea.clientHeight) {
        textarea.scrollTop = unsentPromptHeight - textarea.clientHeight;
    }



    } // end resizeTextarea

    
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

</script>

<div id="message-input">
    <textarea bind:value={messageText} placeholder="..." rows="2" on:input={resizeTextarea} on:input={handleInput} on:keydown={handleTabKeyPress} name="userinput"></textarea>
    
    <div id="button-container">
        <button on:click={sendMessage} {disabled}></button>
    </div>
</div>


<style>
 
    #message-input {
        width: 100%;
        display: flex;
        flex-direction: column;
        position: relative;
        padding: 0px;
        padding-bottom: 0px;
        background-color: transparent;
        border-radius: 0px;
        margin-right: 0px;
        padding-right: 0px;
        margin-right: 0px;
        overflow: hidden;

    }

    #message-input textarea {
        padding: 7px;
        padding-bottom: 7px;
        padding-top: 7px;
        padding-right:40px;
        margin-right: 0px;
        border: rgba(249, 245, 10, 0.298) 2px solid;
        box-shadow: 0 0 0 0.3px #323232;
        border-radius: 4px;
        background-color: #080808;
        font-size: 14px;
        line-height: 20px;
        color: #ffffff;       
        white-space: pre-wrap;
        word-wrap: break-word;
        min-height: 40px;
        tab-size: 3;
        -webkit-font-smoothing: antialiased;
        resize: none;
        overflow: auto;
        scroll-behavior: smooth;
        max-height: 165px; 
    }

    #message-input textarea::placeholder {
        color: #fcfcfc;
        font-size: 14px;
        -webkit-font-smoothing: antialiased;
    }

    #message-input textarea:focus {
        outline: none;
        border: rgb(22, 64, 20) 2px solid;
        box-shadow: 0 0 0 0.3px #323232;
        transition: box-shadow 025s ease-in-out;
        -webkit-font-smoothing: antialiased;
    }

    #button-container {
        
        margin-top: 0px;
        margin-bottom: 0px;
        display: flex;
        justify-content: right;
        align-items: right;
        position: fixed;
        bottom:47px;
        right: 70px;
        background-color: transparent;
    }

    #message-input button {
        width: 100%;
        height: 25px;
        width: 25px;
        padding-right: 0px;
        padding-left: 0px;
        padding-bottom: 0px;
        padding-top: 0px;
        border: 0px solid;
        border-radius: 4px;
        background-color: rgb(46, 129, 41);
        display: flex;
        align-items: right;
        justify-content: right;
        color: #FFFFFF;
        cursor: pointer;
        transition: background-color 0.05s ease-in-out 0.05s;
        position: absolute;
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


    #message-input textarea::-webkit-scrollbar {
        width: 9px;  /* Width of the scrollbar */
        background: transparent;  /* Background color of the scrollbar */
    }

    #message-input textarea::-webkit-scrollbar-thumb {
        background-color: #232323;  /* Color of the draggable scrolling element */
        border-radius: 4px;  /* Roundness of the draggable scrolling element */
    }

    #message-input textarea::-webkit-scrollbar-thumb:hover {
        background-color: #00FF00;  /* Color when cursor is over the draggable scrolling element */
    }

    #message-input textarea::-webkit-scrollbar-track {
        background-color: transparent;  /* Color of the track that the scrollbar moves along */
        border-radius: 0px;  /* Roundness of the track */
    }


    
</style> 