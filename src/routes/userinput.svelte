<script>
    import { onMount } from 'svelte';
    import { setInLocalStorage } from '$lib/scrollStore.js';
    import { quill } from 'svelte-quill';
  
    let messageText = 'test';
    let username = 'Patrick';
  
    let disabled = true;
    $: disabled = !messageText;
    
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
    });
    
    // Quill editor options
    const options = {
      modules: {
        toolbar: [],
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
    
    function handleQuillTextChange() {
      setInLocalStorage('unsentPrompt', messageText);
    }
    
</script>
    
    <input use:quill={options} bind:value={messageText} on:text-change={handleQuillTextChange}/>
 
    <div id="button-container">
        <button on:click={sendMessage} {disabled}></button> 
    </div>

<style>

    input {
        width: calc(100vw - 75px);
        position: fixed;
        bottom: 4px;
        max-height: 170px;
        min-height: 50px;
        scrollbar-width: thin;
        scrollbar-color: #1d24a1;
        background:black;
        opacity: 0.7;
        color: rgba(255, 255, 255, 0.1);
        padding: 5px;
        border-radius: 20px;
        border: 2px solid #593d04;
        box-shadow: none;
        overflow-y: auto;
        overflow-wrap: break-word;
        overflow-x: hidden;
        font-smooth: always;
        -webkit-font-smoothing: antialiased;
        scroll-behavior: smooth;
    }   

    /* The Quill editor when it's focused */
    input:focus {
        border:2px solid rgba(2, 92, 2, 1);
        box-shadow: none;
        outline: none;
        opacity: 0.95;
        background: black;
        color: rgba(255, 255, 255, 1);
        overflow-y: auto;
        overflow-wrap: break-word;
        overflow-x: hidden;
    }

    #button-container {
        margin-top: 0px;
        margin-bottom: 0px;
        display: flex;
        justify-content: right;
        align-items: right;
        position: fixed;
        bottom: 47px;
        right: 70px;
        background-color: transparent;
    }

    #button-container button {
        height: 25px;
        width: 25px;
        padding: 0px;
        border: 0px solid;
        border-radius: 4px;
        background-color: rgba(46, 129, 41, 0.4);
        display: flex;
        align-items: right;
        justify-content: right;
        color: #FFFFFF;
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
