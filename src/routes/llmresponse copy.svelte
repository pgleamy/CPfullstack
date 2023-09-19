<script>
    //@ts-nocheck
    import { onMount } from 'svelte';

    export let user_name; // will hold the user name
    export let text; // text from the message   
    export let timestamp; // will hold the timestamp
    export let source; // will hold the source of the message
    export let llm_name; // will hold the llm name
    export let llm_role; // will hold the llm role
    export let status; // will hold the status of the message
    export let block_id; // will hold the block id

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
            <span>{llm_name} ({llm_role})</span>
            <span id="timestamp"> -{timestamp} </span>
        </div>
        <textarea readonly>{text}</textarea>  <!-- Make it read-only -->
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