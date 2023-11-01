<script>
	//@ts-nocheck
	
	import { page } from '$app/stores';
	import { settings } from '$lib/settings.js'; // Assuming 'settings' is a Svelte store
	import { onMount } from 'svelte';
	import { loadSettings, updateSettings } from '$lib/settings.js';
	// reactive state management for scrollsearch component
    import { scrollStore, setInLocalStorage, get } from '$lib/scrollStore.js'; 
	import { activePage } from '$lib/headerchange.js';

	let hideHeader = false;

	onMount(() => {
  		const initialSettings = loadSettings();
  		updateSettings(initialSettings);
		setTimeout(() => {
      		hideHeader = true;
    	}, 1000);

		const checkMousePosition = (e) => {
		if (e.clientY < 55) {
			hideHeader = false;
		} else {
			hideHeader = true;
		}
    };

    window.addEventListener('mousemove', checkMousePosition);

    return () => { // Cleanup
      window.removeEventListener('mousemove', checkMousePosition);
    };

	});
	
	$: logo = $settings.Gender === 'Argus' ? 'src/lib/images/Argus_logo_clear.png' : 'src/lib/images/Iris_logo_clear.png';
	$: name = $settings.Gender === 'Argus' ? 'Argus' : 'Iris';
	$: roleClass = $settings.Role === 'Write' ? 'write' : $settings.Role === 'Code' ? 'code' : 'talk';

</script>

<header class:hide={hideHeader} class={$activePage === 'chatPage' ? 'bg-black' : 'bg-transparent'}> <!-- Add the transition directive here -->
	
	<div class="corner">
		<div>
			<img src = {logo} alt="" /> <!-- dynamic logo src -->
		</div>
	</div>
	
	<nav>
		<ul>
			<li aria-current={$page.url.pathname === '/' ? 'page' : undefined}>
				<a href="/" draggable="false">{name}</a> <!-- Updated name -->
			</li>
			<li aria-current={$page.url.pathname === '/roles' ? 'page' : undefined}>
				<a href="/roles" draggable="false">(<span class={roleClass}>{$settings.Role}</span>)</a>
			</li>
		</ul>
	</nav>

</header>

<style>

	header {
		display: flex;
		justify-content: flex-start;
		padding-left: 33px;
		padding-top: 0px;
		z-index: 2;
		user-select: none;
		
	}

    .write {
        color: rgb(60, 131, 175);
    }

    .code {
        color: rgb(185, 65, 4);
    }

    .talk {
        color: rgb(83, 156, 30);
    }

	.corner {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 3.5em;
		height: 3.6em;
		padding-left: 0;
		padding-top: 0;		
	}

	.corner img {
		width: 4.3em;
		height: 5em;
		object-fit: fill;
        padding-right: 56px;
        padding-top: 26px;	
  		opacity: 0.9;
	}

	nav {
		display: flex;
		justify-content: center;
        padding-left: 0px;
		background: transparent;
		opacity: 1.0;
	}

	ul {
		position: relative;
		padding: 0;
		margin: 0;
		height: 4em;
		display: flex;
		justify-content: center;
		align-items: center;
		list-style: none;
		/*background: var(--background);*/
		background-size: contain;
		opacity: 1;
	}

	li {
		position: relative;
		height: 100%;
	}

	li[aria-current='page']::before {
		--size: 12px;
		content: '';
		width: 0;
		height: 0;
		position: absolute;
		top: 0;
		left: calc(50% - var(--size));
		border: var(--size) solid transparent;
		border-top: var(--size) solid var(--color-theme-1);
	}

	nav a {
		display: flex;
		height: 100%;
		align-items: center;
		padding: 0 0.15rem;
		color: #cbcbcb;
		font-weight: 900;
		font-size: 1rem;
		text-transform: none;
		letter-spacing: 0.0em;
		text-decoration: none;
	}

	a:hover {
		color: var(--color-theme-1);
	}

	header {
    transition: transform 0.35s ease;
  }

  .hide {
    transform: translateY(-125%);
  }

  .bg-black {
	background-color: rgba(0, 0, 0, 0.4);  
    backdrop-filter: blur(3px) brightness(95%);  /* blurs the content behind the header */
  }
  .bg-transparent {
    background-color: transparent;
	backdrop-filter: blur(3px) brightness(70%);  /* blurs the content behind the header */
  }

</style>
