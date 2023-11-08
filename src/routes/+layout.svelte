<!-- +layout.svelte -->

<script>
	import Header from './Header.svelte';
	import './styles.css';

	
	import { onMount } from 'svelte';
	import { readable } from 'svelte/store';

	let directory_paths = readable([], set => {
		fetch('src-tauri/directory_paths.json')
			.then(response => response.json())
			.then(data => {
				if (!Array.isArray(data)) {
					throw new Error("The JSON structure is expected to be an array of strings.");
				}
				if (data.length !== 3) {
					throw new Error("The JSON file does not contain exactly 3 directory paths.");
				}
				set(data);
			})
			.catch(error => console.error(error));
	});


</script>

<div class="app">
	<Header />
	<main>
		<slot />
	</main>
</div>

<style>
	.app {
		display: flex;
		flex-direction: column;
		min-height: 100vh;
	}

	main {
		display: flex;
		flex-direction: column;
	}

</style>
