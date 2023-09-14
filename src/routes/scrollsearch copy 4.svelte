<script>
    //@ts-nocheck
    import { onMount, onDestroy } from "svelte";
    import {writable} from 'svelte/store';
    // reactive state management for scrollsearch component
    import {scrollStore} from '$lib/scrollStore.js'; 

    let isDragging = false;
    let circleY  = 0; // Y-coordinate of the circle
    let circleColor = "#008000"; // Default color
    const radius = 10; // Radius of the circle
    const svgWidth = 30; // Width of the SVG
    const containerWidth = 55; // Width of the container
    const bottomPadding = 96; // Padding at the bottom of the container
    let arrowPath;
    let arrowColor = "#FF0000";
    let updateArrowColorInterval; // Declare a variable to store the interval ID

    onDestroy(() => {
      clearInterval(updateArrowColorInterval); // Clear the interval
      window.removeEventListener('resize', setInitialPosition); // Remove window resize listener
    });

    // Set initial position based on container height
    function setInitialPosition() {
      const container = document.getElementById("custom-scrollbar");
      circleY = container.clientHeight - radius - bottomPadding;
    }

      // Update position when window is resized
    window.addEventListener('resize', setInitialPosition);

    // Call this function when the component mounts
    onMount(() => {
      setInitialPosition();
      window.addEventListener('resize', setInitialPosition);
      updateArrowColorInterval = setInterval(updateArrowColor, stepInterval); // Store the interval ID
    });
  
    function startDrag(e) {
  isDragging = true;
  circleColor = "#00FF00"; // Brighter when dragging
  document.body.style.userSelect = "none"; // Disable text selection
  document.body.style.cursor = "none"; // Hide the cursor
  window.addEventListener('mousemove', drag);
  window.addEventListener('mouseup', stopDrag);
}

function stopDrag(e) {
  isDragging = false;
  circleColor = "#008000"; // Reset color
  document.body.style.userSelect = "auto"; // Re-enable text selection
  document.body.style.cursor = "auto"; // Show the cursor
  window.removeEventListener('mousemove', drag);
  window.removeEventListener('mouseup', stopDrag);
}

function drag(e) {
  if (isDragging) {
    e.preventDefault(); 
    const container = document.getElementById("custom-scrollbar");
    const rect = container.getBoundingClientRect();
    const offsetY = e.clientY - rect.top; // Calculate the offset
    const lowerBound = radius;
    const upperBound = container.clientHeight - radius - bottomPadding;
    circleY = Math.min(Math.max(lowerBound, offsetY), upperBound);
  }
}

 // new message arrow indicator logic
  import { createEventDispatcher } from 'svelte'; // event dispatcher for bubbling of click on arrow event up to conversationcontainer.svelte
  const dispatch = createEventDispatcher();
  function handleArrowClick() {
    console.log("Arrow clicked");
    dispatch('scrollToLatest'); // dispatch event to parent conversationcontainer.svelte for scrolling to latest message
  }

 let isArrowVisible = true;
 let isArrowThrobbing = false;

  setInterval(() => {
    isArrowVisible = !isArrowVisible;
    arrowColor = isArrowVisible ? "#FF0000" : "#FFFFFF"; // Toggle between red and white
  }, 1000);

let startColor = [0, 255, 0]; // RGB for green
let endColor = [0, 128, 0]; // RGB for dark green
let steps = 100; // Number of steps for the transition
let stepInterval = 10; // Time in milliseconds for each step
let currentStep = 0;

function interpolateColor(start, end, step, maxSteps) {
  let r = start[0] + ((end[0] - start[0]) * step) / maxSteps;
  let g = start[1] + ((end[1] - start[1]) * step) / maxSteps;
  let b = start[2] + ((end[2] - start[2]) * step) / maxSteps;
  return `rgb(${Math.round(r)}, ${Math.round(g)}, ${Math.round(b)})`;
}

function updateArrowColor() {
  arrowPath = document.getElementById("arrow-path"); // Moved inside the function
  if (arrowPath) { // Check if element exists
    arrowPath.setAttribute("stroke", interpolateColor(startColor, endColor, currentStep, steps));
  }
  currentStep++;
  if (currentStep > steps) {
    [startColor, endColor] = [endColor, startColor];
    currentStep = 0;
  }
}

  // Function to start/stop throbbing
  function handleNewMessage(isOffScreen) {
    isArrowThrobbing = isOffScreen;
  }

  </script>

  
  <div class="flex-container">
    <div id="custom-scrollbar" on:mousemove={drag} on:mouseup={stopDrag} role="presentation" style="--container-width: {containerWidth}px;">
      <svg id="circle-svg" width="{svgWidth}" height="calc(100% + 20px)"> <!-- Adjusted height -->
        <!-- Existing Group element with events -->
        <g role="slider" aria-valuemin="0" aria-valuemax="1000" aria-valuenow="{circleY}" tabindex="0"
           on:mousedown={startDrag} on:mouseup={stopDrag}>
          <!-- Invisible reactive area -->
          <rect x="5" y="{circleY - 15}" width="30" height="30" fill="transparent" role="presentation"/>
          <!-- First line -->
          <rect x="10" y="{circleY - 8}" rx="3" ry="3" width="20" height="4" fill="{circleColor}" />
          <!-- Second line -->
          <rect x="10" y="{circleY}" rx="3" ry="3" width="20" height="4" fill="{circleColor}" />
          <!-- Third line -->
          <rect x="10" y="{circleY + 8}" rx="3" ry="3" width="20" height="4" fill="{circleColor}" />
        </g>
        <!-- New Group for arrow -->
        <g id="new-message-indicator" role="presentation" on:click={handleArrowClick}> /* This sends a dispatch to parent to scroll to bottom of conversation */
          <!-- Down arrow path -->
          <path bind:this={arrowPath} id="arrow-path" d="M 7 0 L 23 0 L 15 12 Z" stroke="green" stroke-width="2" fill="none" stroke-linejoin="round" transform="translate(5, {circleY + 18})" />
        </g>
      </svg>
    </div>
  </div>
  

  
  <style>
    .flex-container {
      display: flex;
      flex-direction: column;
      height: 100vh;
      padding-left: 0px;
      width: var(--container-width);
    }
  
    #custom-scrollbar {
      height: 100vh;
      position: relative;
      background: transparent;
      width: var(--container-width); /* Fixed width */
      padding-left: 0px;
    }
  
    #circle-svg {
      position: absolute;
      bottom: 0;
      height: 100vh;
      padding-left: 0px;
    }
    :focus{
      outline: none;
    }

  </style>
  
  
  