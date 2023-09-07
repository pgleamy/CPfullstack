<script>
	//@ts-nocheck

	import { setSetting, getSetting, loadSettings } from '$lib/settings.js';
	import { fade } from "svelte/transition";
	import { settings } from '$lib/settings.js';
  
	let set = loadSettings();
  
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
  </script>
  
  <svelte:head>
	  <title>Settings</title>
	  <meta name="description" content="Select LLMs, role and parameters" />
  </svelte:head>
  
  <div transition:fade="{{ duration: 200, delay: 30 }}">
  <div class="settings-page">
	  <h1 class="settings">Settings</h1>
  
	  <ul class="settings-list">
		
		  <li>
			  <div class="column1"><label for="gender">Gender:</label></div>
			  <div class="column2">
				<select bind:value={settings.Gender} on:change={(e) => handleSettingChange(e, 'Gender')} id="gender">
					<option value="Argus">Argus</option>
					<option value="Iris">Iris</option>
				</select>
			  </div>
		  </li>

		  <li>
			  <div class="column1"><label for="role">Role:</label></div>
			  <div class="column2">
				<select bind:value={settings.Role} on:change={(e) => handleSettingChange(e, 'Role')} id="role">
					<option>Code</option>
					<option>Write</option>
					<option>Talk</option>
				</select>
		</div>
		  </li>

		  <li>
			  <div class="column1"><label for="codingmodel">Model - Coding:</label></div>
			  <div class="column2">
				<select bind:value={settings.CodingModel} on:change={(e) => handleSettingChange(e, 'CodingModel')} id="codingmodel">
					<option>GPT3.5</option>
					<option>GPT4.0</option>
				</select>
			</div>
		  </li>

		  <li>
			  <div class="column1"><label for="writingmodel">Model - Writing:</label></div>
			  <div class="column2">
				<select bind:value={settings.WritingModel} on:change={(e) => handleSettingChange(e, 'WritingModel')} id="writingmodel">
					<option>GPT3.5</option>
					<option>GPT4.0</option>
				</select>
				</div>
		  </li>

		  <li>
			<div class="column1"><label for="talkingmodel">Model - Talking:</label></div>
			<div class="column2">
				<select bind:value={settings.TalkingModel} on:change={(e) => handleSettingChange(e, 'TalkingModel')} id="talkingmodel">
					<option>GPT3.5</option>
					<option>GPT4.0</option>
				</select>
			</div>
		  </li>

	  </ul>
  </div>
  </div>
  
  <style>
	  .settings-page {
		  position: absolute;
		  left: 0;
		  width: 100%;
		  padding: 20px;
		  padding-top: 0px;
		  font-family: system-ui, Arial, sans-serif;
	  }
  
	  .settings-list li {
		  display: grid; /* Use CSS Grid */
		  grid-template-columns: 200px 120px; /* Define two columns with the specified widths */
		  align-items: center; /* Vertical alignment */
		  margin-bottom: 20px;
		  padding-left: 10px;
	  }
  
	  .settings {
		  font-size: 1.3em;
		  font-weight: bold;
		  text-align: left;
		  padding-bottom: 10px;
		  padding-top: 0px;
	  }
  
	  h1 {
		  color: #2066fe;
	  }
  
	  .settings-list {
		  list-style: none;
		  padding-left: 0;
		  text-align: left;
	  }
  
	  label {
		  font-weight: bold;
		  text-align: left;
	  }
  
	  select {
		  width: 120%;
		  padding: 4px;
		  border-radius: 5px;
		  border: 3px solid #2066fe;
		  text-align: left;
	  }
  </style>
  

