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
    let formattedTimestamp = formatTimestamp(timestamp);
    let roleClass;
    $: roleClass = llm_role;

    function resizeTextarea() {
        //const textArea = document.querySelector('#llm-response-textarea');
        textArea.style.height = 'auto'; // Reset height
        textArea.style.height = (textArea.scrollHeight) + 'px'; // Set height based on content
    }

    function formatTimestamp(isoTimestamp) {
        const date = new Date(isoTimestamp);
        
        const year = date.getFullYear();
        const month = date.toLocaleString('default', { month: 'short' });  // 'short' provides abbreviated month name
        const day = date.getDate();
        
        let hour = date.getHours();
        const minute = date.getMinutes();
        const second = date.getSeconds();

        const ampm = hour >= 12 ? 'pm' : 'am';

        // Convert hour from 24-hour to 12-hour format
        hour = hour % 12;
        hour = hour ? hour : 12; // the hour '0' should be '12'

        return `${month} ${day}, ${year}, ${hour}:${minute} ${ampm}`;
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
            <span>oOo {llm_name} oOo <span class={roleClass}>{llm_role}</span></span>
            <span id="timestamp"> - {formattedTimestamp} </span>
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
    padding-bottom: 2px;
    border: rgb(144, 119, 101) 0px solid;
    border-radius: 5px;
    background-color: transparent;
    font-size: 14px;
    line-height: 20px;
    color: #ffffff;
    resize: none;
    overflow: hidden;
    white-space: pre-wrap;
    word-wrap: break-word;
    min-height: 0px;
    margin-right: 50px;
    tab-size: 3;
    -webkit-font-smoothing: antialiased;
    }

    #message-input textarea::placeholder {
        color: #ffffff;
        -webkit-font-smoothing: antialiased;
    }

    #message-input textarea:focus {
        outline: none;
        box-shadow: 0 0 0 0.5px #492f0a;
        transition: box-shadow 0.25s ease-in-out;
        -webkit-font-smoothing: antialiased;
    }

    #title {
        display: flex;
        font-size: 0.85em;
        justify-content: left;
        align-items: baseline;
        color: rgb(254, 199, 169);
        padding-left: 3px;
        padding-bottom: 2px;
        -webkit-font-smoothing: antialiased;
    }

    #timestamp {
        font-size: 0.8em;
        color: rgb(161, 161, 161);
        padding-left: 2px;
        padding-bottom: 0px;
        -webkit-font-smoothing: antialiased;
    }

    .Write {
        color: rgb(77, 168, 224);
        font-size: 0.8em;
        text-transform: lowercase;
        -webkit-font-smoothing: antialiased;
    }

    .Code {
        color: rgb(236, 130, 77);
        font-size: 0.8em;
        text-transform: lowercase;
        -webkit-font-smoothing: antialiased;
    }

    .Talk {
        color: rgb(113, 208, 44);
        font-size: 0.8em;
        text-transform: lowercase;
        -webkit-font-smoothing: antialiased;
    }


</style> 