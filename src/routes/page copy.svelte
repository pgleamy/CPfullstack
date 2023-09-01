<script>
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

	<div transition:fade="{{ duration: 200, delay: 30 }}">
    <div class="inputContainer">
        {#each $inputs as input, index}
            <UserInput bind:value={$inputs[index]} on:input={() => handleInput($inputs[index], index)} />
        {/each}
    </div>
	</div>

</section>

<style>
    .chatWindow {
		position: sticky;
		left: 6px;
        width: 100%;
        height: 100vh;
        overflow-x: hidden; /* Hide overflow */
		overflow-y: auto;
        position: absolute;
		box-sizing: border-box;
    }

    .inputContainer {
        width: 100%;
        position: sticky;
		left: 6px;
        padding-top: 40px; /* Space for the header */
        overflow-x: hidden; /* Prevent horizontal scrolling */
        overflow-y: auto;   /* Allow vertical scrolling when needed */
        height: calc(100vh - 40px); /* Adjust based on header height */
		box-sizing: border-box;
    }
</style>



