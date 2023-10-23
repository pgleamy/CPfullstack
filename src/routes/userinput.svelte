<script>
    import { onMount } from 'svelte';
    import { setInLocalStorage } from '$lib/scrollStore.js';
    import { quill } from 'svelte-quill';
    import Quill from 'quill'; 
  
    let messageText = 'test';
    let username = 'Patrick';
    
    let quillInstance;
  
    let disabled = true;
    $: disabled = !messageText;

    let content = { html: "", text: "" };
    
    import { invoke } from '@tauri-apps/api/tauri';
    function sendMessage() {
      invoke('send_prompt', { messageText })
        .then(() => {
          console.log('Message sent successfully:', messageText);
        })
        .catch(error => {
          console.error('Failed to send message:', error);
        });
      messageText = '';
      setInLocalStorage('unsentPrompt', '');
    }
    
    onMount(() => {
    messageText = localStorage.getItem('unsentPrompt') || '';   
  
    quillInstance = new Quill('#editor', options);
    quillInstance.setText(messageText);

    quillInstance.on('text-change', async function() {
        // Wait for Quill to finish its internal update
        await new Promise(r => setTimeout(r, 0));
        
        messageText = quillInstance.getText().trim();
        setInLocalStorage('unsentPrompt', messageText);
    });
});


    
    // Quill editor options
    let options = {
      modules: {
        toolbar: false,
        clipboard: {},
        keyboard: {
          bindings: {}
        },
        history: {
          delay: 2000,
          maxStack: 100,
          userOnly: true
        }
      },
      theme: 'snow',
      placeholder: "",
        
    };
    
    function handleTextChange() {
        
        console.log('Text changed:', quillInstance.getText());
        messageText = quillInstance.getText().trim();
        // pause for 0.1 seconds
        setTimeout(() => {
            // get the text from the editor
            let text = quillInstance.getText();
            // set the text to the content variable
            content.text = text;
            // set the html to the content variable
            content.html = quillInstance.root.innerHTML;
            // log the content variable
            console.log(content);
        }, 100);
        setInLocalStorage('unsentPrompt', messageText);      
        console.log(messageText);
    }

    
</script>


    <main>
        <div id="editor-container">
            <div id="editor" use:quill={options} on:input={ handleTextChange } />
        </div>

        <div id="button-container">
            <button on:click={sendMessage} {disabled}></button> 
        </div>
    </main>
    <svelte:head>
	    <link href="//cdn.quilljs.com/1.3.6/quill.snow.css" rel="stylesheet">
    </svelte:head>

<style>

    #editor-container::-webkit-scrollbar,
    #editor-container {
    scrollbar-width: none;
    -ms-overflow-style: none;
    }

    #editor::-webkit-scrollbar,
    #editor {
    scrollbar-width: none;
    -ms-overflow-style: none;
    }


    /* The Quill editor when not focussed */
    #editor-container:focus-visible {
        width: calc(100vw - 67px);
        position: fixed;
        bottom: 4px;
        max-height: 180px;
        min-height: 20px;
        background: black;
        opacity: 0.7;
        color: rgba(255, 255, 255, 0.1);
        padding: 0px;
        padding-left: 0px;
        margin: 0px;
        border-radius: 20px;
        border: 2px solid #593d04;
        overflow-y: auto;
        overflow-x: hidden;
        overflow-wrap: break-word;
        font-smooth: always;
        -webkit-font-smoothing: antialiased;
        
    }   

    #editor {
        width: calc(100vw - 67px);
        position: static;
        bottom: 4px;
        max-height: 180px;
        min-height: 20px;
        background: black;
        opacity: 0.7;
        color: rgba(255, 255, 255, 0.1);
        padding: 0px;
        padding-left: 10px;
        font-size: 14px; 
        font-family: Arial, Helvetica, sans-serif;
        margin: 0px;
        border-radius: 17px;
        border: 2px solid #593d04;
        overflow-y: auto;
        overflow-wrap: break-word;
        overflow-x: auto;
        font-smooth: always;
        -webkit-font-smoothing: antialiased;
        scroll-behavior: smooth;
        scrollbar-width: thin;
        scrollbar-color: #1d24a1;
    }   

    /* The Quill editor when it's focused */
    #editor:focus-within {
        border:2px solid rgba(2, 92, 2, 1);
        box-shadow: none;
        outline: none;
        opacity: 0.95;
        background: black;
        color: rgba(255, 255, 255, 1);
        overflow-y: auto;
        overflow-x: hidden;
    }

    #button-container {
        margin-top: 0px;
        margin-bottom: 0px;
        display: flex;
        justify-content: right;
        align-items: right;
        position: fixed;
        bottom: 45px;
        right: 64px;
        background-color: transparent;
    }

    #button-container button {
        height: 39px;
        width: 24px;
        padding: 0px;
        border: 11px dotted #000000;
        border-radius: 40px;
        background-color: rgba(83, 202, 56, 0.542);
        display: flex;
        align-items: right;
        justify-content: right;
        color: #ffffff;
        cursor: pointer;
        transition: background-color 0.05s ease-in-out 0.05s;
        position: absolute;
    }

    #button-container button:disabled {
        background-color: transparent;
        cursor: not-allowed;
        pointer-events: none;
    }

    #button-container button:not(:disabled):hover {
        background-color: #00FF00;
    }

    #button-container button:not(:disabled):active {
        background-color: #4673b7;
        opacity: 1;
    }

    #button-container button:focus {
        outline: none;
        box-shadow: 0 0 0 2px #5ea7ff;
        background-color: rgba(46, 129, 41, 1);

    }

</style>
