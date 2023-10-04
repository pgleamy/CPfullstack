<!-- +layout.svelte -->

<script>
	import Header from './Header.svelte';
	import './styles.css';
</script>

<div class="app">
	<Header />

	<main>
		<slot />
		<div id="bottom-lock"></div>
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

	#bottom-lock {
		height: 2px;
		background-color: rgb(12, 73, 30);  /* You can make it transparent */
		position: fixed;
		bottom: 0;
		left: 0;
		right: 0;
		z-index: 0;  /* optional, if you want this to be above everything else */
  	}

</style>
