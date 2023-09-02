<script>
    import ConversationContainer from './conversationcontainer.svelte'; 
    import UserInput from './userinput.svelte';
    import { writable } from 'svelte/store';
	import { fade } from "svelte/transition";

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

<section class="chatWindow">
    <div transition:fade="{{ duration: 100, delay: 100 }}">
        <ConversationContainer /> <!-- Add the conversation container here -->
    </div>
</section>

<style>
    .chatWindow {
		height: 100vh;
        overflow-x: hidden; /* Hide overflow */
		overflow-y: auto;
        box-sizing: border-box; 
    }
</style>
