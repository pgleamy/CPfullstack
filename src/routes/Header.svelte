<script>
	import { page } from '$app/stores';
	import { selectedGender } from '$lib/store.js'; // Import the shared state
	
	// Reactive values for logo and name based on selected gender
	$: logo = $selectedGender === 'Jarvis' ? 'src/lib/images/Jarvis_logo.jpg' : 'src/lib/images/Iris_logo.jpg';
	$: name = $selectedGender === 'Jarvis' ? 'JARVIS' : 'IRIS';

	let role = "write"; // default role is Write. Also Code, Talk
	// Reactive statement to determine the class based on role
	$: roleClass = role === 'write' ? 'write' : role === 'code' ? 'code' : 'talk';

</script>

<header > <!-- Add the transition directive here -->
	
	<div class="corner">
		<a href="https://github.com/pgleamy">
			<img src= {logo} alt="" /> <!-- Updated logo src -->
		</a>
	</div>
	
	<nav>
		<ul>
			<li aria-current={$page.url.pathname === '/' ? 'page' : undefined}>
				<a href="/">{name}</a> <!-- Updated name -->
			</li>
			<li aria-current={$page.url.pathname === '/roles' ? 'page' : undefined}>
				<a href="/roles">(<span class={roleClass}>{role}</span>)</a>
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
	}

    .write {
        color: rgb(83, 189, 255);
    }

    .code {
        color: rgb(255, 85, 0);
    }

    .talk {
        color: rgb(108, 203, 40);
    }

	.corner {
		width: 3em;
		height: 3em;
		padding-left: 0;
		padding-top: 0;
	}

	.corner a {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 100%;
		height: 100%;
		overflow: visible;
	}

	.corner img {
		width: 5em;
		height: 5em;
		object-fit: fill;
        padding-right: 54px;
        padding-top: 30px;	
	}

	nav {
		display: flex;
		justify-content: center;
        padding-left: 0px;
		--background: rgb(0, 0, 0);
	}

	ul {
		position: relative;
		padding: 0;
		margin: 0;
		height: 6em;
		display: flex;
		justify-content: center;
		align-items: center;
		list-style: none;
		background: var(--background);
		background-size: contain;
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
		color: var(--color-text);
		font-weight: 900;
		font-size: 1rem;
		text-transform: none;
		letter-spacing: 0.0em;
		text-decoration: none;
	}

	a:hover {
		color: var(--color-theme-1);
	}

</style>
