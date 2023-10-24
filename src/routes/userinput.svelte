<script>
    import { onMount, onDestroy } from 'svelte';
    import { setInLocalStorage } from '$lib/scrollStore.js';
    import Quill from 'quill'; 

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
        
    };
  
    let messageText = 'test';
    let username = 'Human(s)';
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

      quillInstance.setText(messageText);
    }
    
    onMount(() => {
        // Initialize messageText from local storage
        messageText = localStorage.getItem('unsentPrompt') || '';   

        // Initialize Quill instance
        quillInstance = new Quill('#editor', options);

        // Set the Quill editor text from local storage
        quillInstance.setText(messageText);

        // Listen for text changes in Quill editor
        quillInstance.on('text-change', async function() {
            // Wait for Quill to finish its internal update
            await new Promise(r => setTimeout(r, 0));

            // Update messageText and local storage
            messageText = quillInstance.getText().trim();
            setInLocalStorage('unsentPrompt', messageText);
        });

    });
    
</script>


    <main>
        <div id="editor-container">            
            <div id="editor" spellcheck="false"></div>
        </div>

        <div id="button-container">
            <button on:click={sendMessage} {disabled}></button> 
        </div>
    </main>
    <svelte:head>
	    <link href="//cdn.quilljs.com/1.3.6/quill.snow.css" rel="stylesheet">
    </svelte:head>

<style>

    

    
    /* The Quill editor when not focussed */
    #editor-container:focus-visible {
        width: calc(100vw - 67px);
        position: fixed;
        bottom: 4px;
        max-height: 300px; /* 180px */
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
        height: 190px; 
        background: black;
        opacity: 0.18;
        color: rgba(255, 255, 255, 0.18);
        padding: 0px;
        padding-left: 0px;
        font-size: 14.5px;
        margin: 0px;
        border-radius: 17px;
        border: 2px solid #593d04;
        overflow-y: auto;
        overflow-wrap: break-word;
        overflow-x: hidden;
        font-smooth: always;
        -webkit-font-smoothing: antialiased;
        scroll-behavior: smooth;
        scrollbar-width: thin;
        scrollbar-color: #1d24a1;
        transition: opacity 0.2s ease, color 0.2s ease;

        font-family: var(--font-body); /* Futura from styles.css */
        
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
        transition: opacity 0.2s ease, color 0.2s ease;
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
        border: 11px dotted rgb(0, 3, 23);
        border-radius: 40px;
        background-color: rgba(82, 227, 50, 0.542);
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
        border: 11px dotted rgba(10, 21, 98, 0);
    }

    #button-container button:not(:disabled):hover {
        background-color: #04e004;
        transition: background-color 0.05s ease-in-out 0.05s;
    }

    #button-container button:not(:disabled):active {
        background-color: #4673b7;
        opacity: 1;
        transition: background-color 0.05s ease-in-out 0.05s;
    }

    #button-container button:focus {
        outline: none;
        box-shadow: 0 0 0 2px #5ea7ff;
        background-color: rgba(46, 129, 41, 1);
        transition: background-color 0.2s ease-in-out 0.2s;

    }



    /* Style the scrollbar container */
    #editor::-webkit-scrollbar {
        width: 12px;
    }




</style>
