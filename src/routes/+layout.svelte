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
		let messages_path, database_path, docs_drop_path;

		if (Array.isArray(directoryPaths) && directoryPaths.length === 3) {
			[messages_path, database_path, docs_drop_path] = directoryPaths;
			//console.log("\n", messages_path, "\n", database_path, "\n", docs_drop_path, "\n");
			setInLocalStorage('messages_path', messages_path);
			setInLocalStorage('database_path', database_path);
			setInLocalStorage('docs_drop_path', docs_drop_path);
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
