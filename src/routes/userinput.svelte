<script>
    import { onMount, onDestroy } from 'svelte';
    import { setInLocalStorage } from '$lib/scrollStore.js';
    import Quill from 'quill'; 
    import 'quill/dist/quill.snow.css';
 
    import hljs from 'highlight.js';
    import 'highlight.js/styles/an-old-hope.css';
   

let BlockEmbed = Quill.import('blots/block/embed');

class CodeBlockWithTitle extends BlockEmbed {
  static create(value) {
    let node = super.create(value);
    node.dataset.title = value.title;
    return node;
  }

  static value(domNode) {
    return { title: domNode.dataset.title };
  }
}

CodeBlockWithTitle.blotName = 'codeBlockWithTitle';
CodeBlockWithTitle.tagName = 'DIV';
CodeBlockWithTitle.className = 'ql-code-block-with-title';

Quill.register(CodeBlockWithTitle);

    // Quill editor options
    let options = {
      modules: {
        toolbar: false,
        clipboard: {},
        syntax: {
            highlight: text => hljs.highlightAuto(text).value,
        },
        keyboard: {
            bindings: {
                codeBlock: {
                    key: 'S',  // S
                    ctrlKey: true,  // This makes it a Ctrl+S shortcut
                    handler: function(range) {
                        const format = this.quill.getFormat(range);
                        this.quill.format('code-block', !format['code-block']);
                    }
                }
            }
        },
        history: {
          delay: 2000,
          maxStack: 100,
          userOnly: true
        },        
      },
      theme: 'snow',
    };
  
    let messageText = '';
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

        messageText = localStorage.getItem('unsentPrompt') || '';    
  
        quillInstance = new Quill('#editor', options);

       // Load saved Delta if any
        const savedDeltaString = localStorage.getItem('unsentPromptQUILL');
        if (savedDeltaString) {
            const savedDelta = JSON.parse(savedDeltaString);
            quillInstance.setContents(savedDelta);
        }

        quillInstance.on('text-change', function() {
           messageText = quillInstance.getText().trim();
           setInLocalStorage('unsentPrompt', messageText);

           const currentDelta = quillInstance.getContents();
           const deltaString = JSON.stringify(currentDelta);
           setInLocalStorage('unsentPromptQUILL', deltaString);
        }); 
    
    }); // End of onMount()
    
</script>

    <svelte:head>
	    <script href="highlight.js"></script>
    </svelte:head>

    <main>
        <div id="editor-container">            
            <div id="editor"></div>
        </div>

        <div id="button-container">
            <button on:click={sendMessage} {disabled}></button> 
        </div>
    </main>
    


<style>
    
    /* The Quill editor when focussed */
    #editor-container:focus-visible {
        width: calc(100vw - 67px);
        position: fixed;
        bottom: 4px;
        max-height: 400px; /* 180px */
        min-height: 20px;
        background: black;
        opacity: 0.8;
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
        height: 300px; 
        background: black;
        opacity: 0.18;
        color: rgba(255, 255, 255, 0.05);
        padding: 0px;
        padding-left: 0px;
        
        margin: 0px;
        border-radius: 17px;
        border: 2px solid #593d0474;
        overflow-y: auto;
        overflow-wrap: break-word;
        overflow-x: hidden;
        font-smooth: always;
        -webkit-font-smoothing: antialiased;
        scroll-behavior: smooth;
        scrollbar-width: thin;
        scrollbar-color: #1d24a1;
        transition: opacity 0.2s ease, color 0.2s ease;

        
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
    

</style>
