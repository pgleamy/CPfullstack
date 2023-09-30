<script>
    import ConversationContainer from './conversationcontainer.svelte'; 
    import UserInput from './userinput.svelte';
    import { writable } from 'svelte/store';
    import { fade } from "svelte/transition";
    import ScrollSearch from './scrollsearch.svelte';
    import { activePage } from '$lib/headerchange.js';
    $activePage = 'chatPage';

    let CurrentPage; // Reference to the current page component

    // Function to switch to a new page with fade transition
    function switchPage(pageComponent) {
        CurrentPage = pageComponent; // Update to the new page component
    }

    const initialInputs = JSON.parse(localStorage.getItem('inputs') || '[""]');
    const inputs = writable(initialInputs);

    inputs.subscribe(value => {
        localStorage.setItem('inputs', JSON.stringify(value));
    });

    function handleInput(value, index) {
        if (index === $inputs.length - 1 && value) {
            inputs.update(items => [...items, '']);
        }
        $inputs[index] = value;
    }

</script>

<div class="contentWrapper" id='flex'>
    <section class="chatWindow">
        <div transition:fade="{{ duration: 500, delay: 60 }}">
            <ConversationContainer />
        </div>
    </section>
    <div class="scrollSearchWrapper" transition:fade="{{ duration: 100, delay: 10 }}">
        <ScrollSearch />
    </div>

</div>

<style>
    .contentWrapper {
        justify-content: flex-start;
        overflow: auto;
        height: 100vh;
        flex-grow: 1;
    }
    .chatWindow {
        flex-grow: 1;

    }
    .scrollSearchWrapper {
        flex-shrink: 0;
        margin-left: 10px;
        display: inline-flex;
        width: auto;
    }
    #flex{
        display: flex;
    }

</style>

