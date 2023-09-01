<script>
    import { onMount } from 'svelte';
    let messageText = ''; // This will be populated from the LLM response
    const llmName = 'Jarvis'; // Hardcoded for now
    let responseTime;

    function resizeTextarea(event) {
        event.target.style.height = 'auto'; // Reset height
        event.target.style.height = event.target.scrollHeight + 'px'; // Set height based on content
    }

    onMount(() => {
        resizeTextarea({ target: document.querySelector('#message-input textarea') });
        responseTime = new Date().toLocaleString('en-US', { month: 'short', day: 'numeric', year: 'numeric', hour: 'numeric', minute: 'numeric', hour12: true });
    });
</script>

<div id="wrapper">
    <div id="message-input">
        <div id="title" contenteditable="false">
            <span>{llmName}</span>
            <span id="timestamp"> ({responseTime}) </span>
        </div>
        <textarea readonly>{messageText}</textarea>  <!-- Make it read-only -->
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
    padding: 10px;
    padding-bottom: 1px;
    border: rgb(115, 115, 115) 1px solid;
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
    }

    #message-input textarea::placeholder {
        color: #767676;
    }

    #message-input textarea:focus {
        outline: none;
        box-shadow: 0 0 0 1px #6E9BFF;
        transition: box-shadow 0.15s ease-in-out;
    }

    #title {
        display: flex;
        font-size: 0.6em;
        justify-content: space-between;
        align-items: baseline;
        color: lightblue;
        padding-left: 10px;
        padding-bottom: 2px;
    }

    #timestamp {
        font-size: 0.6em;
        color: darkgoldenrod;
        padding-right: 10px;
    }
</style> 