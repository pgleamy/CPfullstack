<script>
    //@ts-nocheck
    import { onMount, onDestroy } from 'svelte';

    export let user_name; // will hold the user name
    export let text = ''; // text from the message 
    let textArea; // will hold the textarea element  
    export let timestamp; // will hold the timestamp
    export let source; // will hold the source of the message
    export let llm_name; // will hold the llm name
    export let llm_role; // will hold the llm role
    export let status; // will hold the status of the message
    export let block_id; // will hold the block id

    function resizeTextarea() {
        //const textArea = document.querySelector('#llm-response-textarea');
        textArea.style.height = 'auto'; // Reset height
        textArea.style.height = (textArea.scrollHeight) + 'px'; // Set height based on content
    }

    onMount(() => {
        resizeTextarea();
        window.addEventListener('resize', resizeTextarea);
    });

    onDestroy(() => {
        window.removeEventListener('resize', resizeTextarea);
    });

    // Prevents the user from scrolling the entire conversation container 
    // when the llmresonpe textarea is focused, but capturing and killing 
    // those inputs.
    function handleLeftRightArrows(event) {
        if (event.key === "ArrowLeft" || event.key === "ArrowRight") {
            event.preventDefault();
        }
    }



</script>

<div id="wrapper">
    <div id="message-input" role="textbox" tabindex="0" on:keydown={handleLeftRightArrows}>
        <div id="title" contenteditable="false">
            <span>{llm_name} ({llm_role})</span>
            <span id="timestamp"> -{timestamp} </span>
        </div>
        <textarea bind:this={textArea} readonly on:input={resizeTextarea} name="OpenAIKey">{text}</textarea>  
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
        overflow-x: hidden;
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
    padding: 8px;
    padding-bottom: 0px;
    border: rgb(144, 119, 101) 0px solid;
    border-radius: 5px;
    background-color: transparent;
    font-size: 12.4px;
    line-height: 14.8px;
    color: #cccccc;
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
        box-shadow: 0 0 0 0.5px #492f0a;
        transition: box-shadow 0.25s ease-in-out;
    }

    #title {
        display: flex;
        font-size: 0.75em;
        justify-content: left;
        align-items: baseline;
        color: rgb(213, 93, 28);
        padding-left: 3px;
        padding-bottom: 2px;
    }

    #timestamp {
        font-size: 0.75em;
        color: rgb(93, 93, 93);
        padding-left: 2px;
        padding-bottom: 0px;
    }


</style> 