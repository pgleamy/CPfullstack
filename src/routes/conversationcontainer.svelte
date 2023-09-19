<script>
    import UserInput from './userinput.svelte';
    import UserInputSent from './userinputsent.svelte';
    import LLMResponse from './llmresponse.svelte';
    // reactive state management for scrollsearch component
    import {scrollStore} from '$lib/scrollStore.js';
    import { onMount, onDestroy } from 'svelte';
    import { invoke } from "@tauri-apps/api/tauri";

    let conversation = [];

    onMount(async () => {
      const { message } = await invoke("fetch_conversation_history", {
      params: { start: 0, end: 2 }
      });
      conversation = message;
    });

  </script>


<div id="clip-container">
  <div id="conversation-container"> 
    {#each conversation as entry}
      {#if entry.source === 'user'}
        <UserInputSent {...entry} />
      {:else if entry.source === 'llm'}
        <LLMResponse {...entry} />
      {/if}
    {/each}
    <UserInput />
  </div>
</div>

   
  <style>
    #conversation-container {
      transition: all 0.5s ease-in-out;
      display: flex;
      flex-direction: column;
      align-items: flex-start;
      width: 100%;
      position: relative;
      bottom: 0;
      left: 5px !important;
      padding-bottom: 0px;
      padding-right: 0px;
      overflow: hidden;
      user-select: none;
    }

    #clip-container {
    position: fixed;
    top: 79px;
    bottom: 5px;
    left: 0;
    right: 0;
    clip-path: inset(0);
    overflow: hidden;
  }
 
  </style>
  