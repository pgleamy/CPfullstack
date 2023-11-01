<script>
    import ConversationContainer from './conversationcontainer.svelte'; 
    import UserInput from './userinput.svelte';
    import { writable } from 'svelte/store';
    import { fade } from "svelte/transition";
    import ScrollSearch from './scrollsearch.svelte';
    import { activePage } from '$lib/headerchange.js';
    import { get } from '$lib/scrollStore.js';
    $activePage = 'chatPage';

    let CurrentPage; // Reference to the current page component
    let gender = "";
    gender = get('Gender');

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



<div class={`contentWrapper ${gender === 'Iris' ? 'Iris' : 'Argus'}`}  id='flex' >

    <section class="chatWindow">
        <div transition:fade="{{ duration: 100, delay: 30 }}">  
            <ConversationContainer />
        </div>
    </section>
    <div class="scrollSearchWrapper" transition:fade="{{ duration: 100, delay: 30 }}">
        <ScrollSearch />
    </div>

</div>



<style>

    .contentWrapper {
        position: relative;  /* Set position to relative for the pseudo-element */
        justify-content: flex-start;
        overflow: auto;
        height: 100vh;
        flex-grow: 1;
    }

    .contentWrapper.Iris::before {
        background-image: url('src/lib/images/FEMALE-hr.png');
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-size: 100% 100%;
        background-repeat: no-repeat;  
        background-position: center;  
        opacity: 10.0;  
        z-index: -1;  
        background-position: 70px -55px;
        animation: fadeOut 2.5s ease-in forwards !important;
    }

    .contentWrapper.Argus::before {
        background-image: url('src/lib/images/MALEhr.png');
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-size: 100% 100%;
        background-repeat: no-repeat;  
        background-position: center;  
        opacity: 10.0;  
        z-index: -1;  
        background-position: 70px -55px;
        animation: fadeOut 2.5s ease-in forwards !important;
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

    @keyframes fadeOut {
        0% {
            opacity: 10.0;  
        }     
        100% {
            opacity: 0.01; 
        }
    }

</style>

