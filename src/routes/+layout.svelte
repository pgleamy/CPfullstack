<!-- +layout.svelte -->

<script>

	// import {scrollStore, setInLocalStorage} from '$lib/scrollStore.js';	
	import Header from './Header.svelte';
	import './styles.css';


	import {scrollStore, setInLocalStorage} from '$lib/scrollStore.js';
	import { onMount } from 'svelte';
	// Assuming your build setup supports JSON imports:
	import directoryPaths from '$lib/directory_paths.json';


	onMount(() => {
		let path1, path2, path3;

		if (Array.isArray(directoryPaths) && directoryPaths.length === 3) {
			[path1, path2, path3] = directoryPaths;
			console.log("\n", directoryPaths.path1, "\n", directoryPaths.path2, "\n", directoryPaths.path3, "\n");
			setInLocalStorage('path1', directoryPaths.path1);
		} else {
			console.error("The JSON file does not contain exactly 3 directory paths.");
		}
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
