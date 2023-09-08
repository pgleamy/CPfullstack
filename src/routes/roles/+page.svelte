<script>
	//@ts-nocheck

	import { onMount } from 'svelte';
	import { setSetting, getSetting, loadSettings } from '$lib/settings.js';
	import { fade } from "svelte/transition";
	import { settings } from '$lib/settings.js';

	let set = {}; // Initialize local state

	// Subscribe to Svelte store and update local state
	settings.subscribe(value => {
  		set = value;
	});

	onMount(() => {
  		const loadedSettings = loadSettings();
  		settings.set({
    Gender: 'Argus',
    Role: 'write',
    CodingModel: 'GPT3.5',
    WritingModel: 'GPT3.5',
    TalkingModel: 'GPT3.5',
	openAiKey: '',
    ...loadedSettings
  });
});
  
function handleSettingChange(event, settingKey) {
  set[settingKey] = event.target.value;
  setSetting(settingKey, set[settingKey]);
  settings.update(s => ({ ...s, [settingKey]: set[settingKey] }));
}

	function handleGenderChange(event) {
	  set.Gender = event.target.value;
	  setSetting('Gender', set.Gender);
	}
  
	function handleRoleChange(event) {
	  set.Role = event.target.value;
	  setSetting('Role', set.Role);
	}
  
	function handleCodingModelChange(event) {
	  set.CodingModel = event.target.value;
	  setSetting('CodingModel', set.CodingModel);
	}
  
	function handleWritingModelChange(event) {
	  set.WritingModel = event.target.value;
	  setSetting('WritingModel', set.WritingModel);
	}
  
	function handleTalkingModelChange(event) {
	  set.TalkingModel = event.target.value;
	  setSetting('TalkingModel', set.TalkingModel);
	}

	function handleOpenAiKeyChange(event) {
  		set.openAiKey = event.target.value;
  		// Call a Rust function to securely store the key using Keyring
  		secureStoreKey(set.openAiKey);
	}



	$: backgroundImage = set.Gender === 'Argus' ? '../src/lib/images/ArgusSprint.jpg' : '../src/lib/images/IrisSprint.jpg';

  </script>
  
  <svelte:head>
	  <title>Settings</title>
	  <meta name="description" content="Select LLMs, role and parameters" />
  </svelte:head>
  
  <span class="halo-text">

  <div transition:fade="{{ duration: 200, delay: 30 }}">

  <div class="background-wrapper"> 
	<div class="background" style="background-image: url({backgroundImage});"></div>
  <div class="settings-page">
	  <h1 class="settings">Settings</h1>
  
	  <ul class="settings-list">
		
		  <li>
			  <div class="column1"><label for="gender">Gender ♂️♀️</label></div>
			  <div class="column2">
				<select bind:value={set.Gender} on:change={(e) => handleSettingChange(e, 'Gender')} id="gender">
					<option value="Argus">Argus</option>
					<option value="Iris">Iris</option>
				</select>
			  </div>
		  </li>

		  <li>
			  <div class="column1"><label for="role">Role 🛠️ </label></div>
			  <div class="column2">
				<select bind:value={set.Role} on:change={(e) => handleSettingChange(e, 'Role')} id="role">
					<option>Code</option>
					<option>Write</option>
					<option>Talk</option>
				</select>
		</div>
		  </li>

		  <li>
			  <div class="column1"><label for="codingmodel">Coding 💻</label></div>
			  <div class="column2">
				<select bind:value={set.CodingModel} on:change={(e) => handleSettingChange(e, 'CodingModel')} id="codingmodel">
					<option>GPT3.5</option>
					<option>GPT4.0</option>
				</select>
			</div>
		  </li>

		  <li>
			  <div class="column1"><label for="writingmodel">Writing 🪶</label></div>
			  <div class="column2">
				<select bind:value={set.WritingModel} on:change={(e) => handleSettingChange(e, 'WritingModel')} id="writingmodel">
					<option>GPT3.5</option>
					<option>GPT4.0</option>
				</select>
				</div>
		  </li>

		  <li>
			<div class="column1"><label for="talkingmodel">Talking 😏</label></div>
			<div class="column2">
				<select bind:value={set.TalkingModel} on:change={(e) => handleSettingChange(e, 'TalkingModel')} id="talkingmodel">
					<option>GPT3.5</option>
					<option>GPT4.0</option>
				</select>
			</div>
		  </li>

		  <li>
			<div class="column1"><label for="openAiKey">OpenAi 🔑</label></div>
			<div class="column2">
			  <input type="password" placeholder="COPY then PASTE your key here" id="openAiKey" on:input={handleOpenAiKeyChange} />
			</div>
		  </li>

	  </ul>
  </div>
  </div>
  </div>

  </span>
  
  <style>
	  .settings-page {
		  position: absolute;
		  left: 0;
		  width: 100%;
		  padding: 10px;
		  padding-top: 60px;
		  font-family: system-ui, Arial, sans-serif;
	  }
  
	  .settings-list li {
		  display: grid; /* Use CSS Grid */
		  grid-template-columns: 80px 150px; /* Define two columns with the specified widths */
		  align-items: center; /* Vertical alignment */
		  margin-bottom: 8px;
		  padding-left: 4px;
	  }
  
	  .settings {
		  font-size: 1.4em;
		  font-weight: bold;
		  text-align: left;
		  padding-bottom: 0px;
		  padding-top: 0px;
		  padding-left: 0px;
	  }
  
	  h1 {
		  color: hsl(13, 100%, 85%);
	  }
  
	  .settings-list {
		  list-style: none;
		  padding-left: 0;
		  text-align: left;
		  font-size: 0.9em;
	  }
  
	  label {
		  font-weight: default;
		  text-align: left;
		  color: #ffffff;
	  }
  
	  select {
		  width: 45%;
		  padding: 3px;
		  border-radius: 5px;
		  border: 1px solid #fe6a20;
		  background-color: #682525;
		  text-align: left;
		  font-size: 0.8em;
		  color: #ffffff;
		  outline: none;
	  }

	  .background-wrapper {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 1; /* Place it below other elements */
    opacity: 1;
    background-size: cover; /* Cover the entire div */
    background-position: center; /* Center the image */
	transition: background-image 0.8s ease-in-out;
  }

  .background {
  position: fixed;  /* Fixed or absolute based on your need */
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;  /* Ensures the background stays behind the content */
  opacity: 0.73;  /* Set your desired opacity level */
  background-size: cover;
  background-position: top;
}

  .halo-text {
  text-shadow: 
    0.8px 0 0 #9e0000, 
    -0.8px 0 0 #9e0000, 
    0 0.8px 0 #9e0000, 
    0 -0.8px 0 #9e0000,
    0.8px 0.8px #9e0000,
    -0.8px -0.8px 0 #9e0000,
    0.8px -0.8px 0 #9e0000,
    -0.8px 0.8px 0 #9e0000;
}

input[type="password"] {
  width: 100%;
  padding: 4px;
  border-radius: 5px;
  border: 1px solid #fe6a20;
  background-color: #682525;
  color: #ffffff;
  outline: none;
  font-size: 0.5em;
  margin-left: 0px;
}

input[type="password"]::placeholder {
  color: white;
}

  </style>
  

