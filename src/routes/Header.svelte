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

	

	const storedRole = get('Role');  // Fetch the role from local storage or default to 'Write'
  	let selectedRole = get('Role'); // Fetch the role from the scrollStore or default to storedRole



	// Subscribe to store changes and update roleClass and llm_role
	$: llm_role = selectedRole;
	$: roleClass = llm_role;




	
	$: {
    	localStorage.setItem('Role', selectedRole);
		
  	}





	function updateSelectColor(event) {
		const selectElement = event.target;
		const selectedValue = selectElement.value;

		switch (selectedValue) {
			case 'Code':
			selectElement.style.color = 'rgb(185, 65, 4)';
			break;
			case 'Write':
			selectElement.style.color = 'rgb(60, 131, 175)';
			break;
			case 'Talk':
			selectElement.style.color = 'rgb(83, 156, 30)';
			break;
			default:
			selectElement.style.color = 'initial'; // reset to default
		}
	}





	
	onMount(() => {


		

  		const initialSettings = loadSettings();
  		updateSettings(initialSettings);
		setTimeout(() => {
      		hideHeader = true;
    	}, 1000);

		const checkMousePosition = (e) => {
		if (e.clientY < 55) {
			hideHeader = false;
		} 	else {
				hideHeader = true;
			}
    	};

    	window.addEventListener('mousemove', checkMousePosition);

		return () => { // Cleanup
		window.removeEventListener('mousemove', checkMousePosition);
		};




		// Get window dimensions
		const windowHeight = window.innerHeight;
		const windowWidth = window.innerWidth;

		// Calculate the position
		const topPos = windowHeight - 40 + "px";
		const rightPos = windowWidth - 40 + "px";

		// Update the position of the dropdown
		const dropdown = document.getElementById('roleDropdown');
		dropdown.style.top = topPos;
		dropdown.style.right = rightPos;




		const selectElement = document.getElementById('roleDropdown');
  		updateSelectColor({ target: selectElement })

	}); // end onMount
	
	$: logo = $settings.Gender === 'Argus' ? 'src/lib/images/Argus_logo_clear.png' : 'src/lib/images/Iris_logo_clear.png';
	$: name = $settings.Gender === 'Argus' ? 'Argus' : 'Iris';
	$: roleClass = $settings.Role === 'Write' ? 'write' : $settings.Role === 'Code' ? 'code' : 'talk';




	let showOptions = false;
  

  function selectRole(role) {
    selectedRole = role;
    showOptions = false;
  }





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
				<a href="/roles" draggable="false"><span class={roleClass}><span class="plus" align="center">+</span><span class="minus" align="center">-</span></span></a> <!-- {$settings.Role} -->
			</li>
		</ul>
	</nav>



	<div id="wrapper">
		<div id="message-input" role="textbox" tabindex="0">
		  <div id="title" style="position: relative;">
			<span class={selectedRole}></span>
			<select id="roleDropdown" bind:value={selectedRole} on:change={updateSelectColor}>
				<option value="Code">Code</option>
				<option value="Write">Write</option>
				<option value="Talk">Talk</option>
			</select>
		  </div>
		</div>
	  </div>



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
		--size: 5px;
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



		font-size: 1.3em;  /* Update this */
  		font-weight: bold; /* Update this */

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
    backdrop-filter: blur(4px) brightness(95%);  /* blurs the content behind the header */
  }
  .bg-transparent {
    background-color: transparent;
	backdrop-filter: blur(3px) brightness(70%);  /* blurs the content behind the header */
  }





  .custom-select {
    position: relative;
  }


  #roleDropdown {
    position: absolute;
	font-weight: 400;
    top: 26px;
    left: 6px;
	color: rgb(161, 104, 52);
	background: transparent;
	border: none;
	font-size: 1rem;
	text-align: center;
	box-shadow: none;
	line-height: 1.8;
	padding: 0px;
	font-size: .8em;  /* Update this */
  	font-weight: bold; /* Update this */
	  font-family: var(--font-mono)
  }

  #roleDropdown option {
	background-color: black; /* Background color of the list of options */
	color: rgb(211, 206, 200); /* Text color of the list of options */
	border: none; /* Removes the default border around the dropdown list */
	box-shadow: none;
	border: none;
	line-height: 1.8;
	padding: 5px;

    position: absolute;
    right: 30px;
    top: 31px;
	
  }

  #roleDropdown:focus {
	border: none;
  outline: none; /* Removes the outline when the element receives focus */
}

#roleDropdown {
  border: none; /* Removes the border */
  outline: none; /* Removes the outline when the element receives focus */
  /* other styles */
}



.plus {
  color: rgb(134, 180, 255);
  font-size: 1em;
  font-weight: bold; /* Update this */
  justify-content: right;
  padding-left: 7px;
}

.minus {
  color: #77fc77;
  font-size: 1.06em; /* bigger than plus so centered vertically */
  font-weight: bold; /* Update this */
  justify-content: right;
  padding-left: 0px;
}



</style>
