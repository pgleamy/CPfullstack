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

    let gender = "";
    gender = get('Gender');
    let face = "";
    let styleString = "";


    function updateFace() {
    if (gender === "Iris") {
        console.log("I'm Iris. Who's there?");
        return "url('src/lib/images/FEMALE.png')";
    } else {
        console.log("I'm Argus. Who's there?");
        return "url('src/lib/images/MALE.png')";
    }
}

    
    $: {
        console.log("Current gender: ", gender);
        face = updateFace();
        if (gender === "Iris") {
            console.log("I'm Iris. Who's there?");
            face = "url('src/lib/images/FEMALE.png')";
            console.log("face: ", face);
            styleString = `
        .contentWrapper::before {
            background-image: ${face};
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-size: 100% 100%; /* Cover the entire element */
            background-repeat: no-repeat;  /* Do not repeat the image */
            background-position: center;  /* Center the image */
            opacity: .01;  /* 0.002 Set opacity as needed */
            z-index: -1;  /* Place it behind the content */
            background-position: 50px -90px;
        }
        `;
        console.log("styleString: ", styleString);  // Log the style string
        } else if (gender !== "Iris") {
            console.log("I'm Argus. Who's there?");
            face = "url('src/lib/images/MALE.png')";
            console.log("face: ", face);
            styleString = `
        .contentWrapper::before {
            background-image: ${face};
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-size: 100% 100%; /* Cover the entire element */
            background-repeat: no-repeat;  /* Do not repeat the image */
            background-position: center;  /* Center the image */
            opacity: .006;  /* 0.002 Set opacity as needed */
            z-index: -1;  /* Place it behind the content */
            background-position: 90px -55px;
        }
        `;
        console.log("styleString: ", styleString);  // Log the style string
        }
    }

</script>



<!-- Inject the style tag into the DOM -->

{@html `<style>${styleString}</style>`}



<div class="contentWrapper" id='flex'>
    
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
    /*
    .contentWrapper {
        justify-content: flex-start;
        overflow: auto;
        height: 100vh;
        flex-grow: 1;
    }
    */

    .contentWrapper {
        position: relative;  /* Set position to relative for the pseudo-element */
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

