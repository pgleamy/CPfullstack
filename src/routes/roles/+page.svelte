<script>
	import { selectedGender } from '$lib/store.js'; // Import shared state
	import { fade } from "svelte/transition";

	$: gender = $selectedGender;
  
	// Function to handle gender selection change
	function handleGenderChange(event) {
	  selectedGender.set(event.target.value);
	}
  </script>
  
  <svelte:head>
	  <title>Role Settings</title>
	  <meta name="description" content="Select LLMs, role and parameters" />
  </svelte:head>
  
  <div transition:fade="{{ duration: 200, delay: 30 }}">
  <div class="settings-page">
	  <h1 class="settings">Role Settings</h1>
  
	  <ul class="settings-list">
		
		  <li>
			  <div class="column1"><label for="gender">Gender:</label></div>
			  <div class="column2">
				  <select bind:value={gender} on:change={handleGenderChange} id="gender">
					  <option value="Jarvis">Male - Jarvis</option>
					  <option value="Iris">Female - Iris</option>
				  </select>
			  </div>
		  </li>

		  <li>
			  <div class="column1"><label for="role">Role:</label></div>
			  <div class="column2"><select id="role">
				<option>Code</option>
				<option>Write</option>
				<option>Talk</option>
			</select>
		</div>
		  </li>

		  <li>
			  <div class="column1"><label for="codingmodel">Model - Coding:</label></div>
			  <div class="column2">
				<select id="codingmodel">
					<option>OpenAI 3.5</option>
					<option>OpenAI 4.0</option>
				</select>
			</div>
		  </li>

		  <li>
			  <div class="column1"><label for="writingmodel">Model - Writing:</label></div>
			  <div class="column2">
					<select id=writingmodel>
						<option>OpenAI 3.5</option>
						<option>OpenAI 4.0</option>
						<option>Local LLM</option>
					</select>
				</div>
		  </li>

		  <li>
			<div class="column1"><label for="talkingModel">Model - Talking:</label></div>
			<div class="column2">
			  	<select id="talkingModel">
					<option>OpenAI 3.5</option>
					<option>OpenAI 4.0</option>
					<option>Local LLM</option>
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
  

