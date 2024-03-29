<script>
  //@ts-nocheck
  import { onMount, onDestroy } from "svelte";
  import { writable } from 'svelte/store';
  import { scrollStore, setInLocalStorage, get, load, reloadScrollStore } from '$lib/scrollStore.js';
  import { createEventDispatcher } from 'svelte';

  let isDragging = false;
  let gripY = 0; // Y-coordinate of the grip
  let gripColor = "#00C040"; // Default color for grip
  const radius = 10;
  const svgWidth = 30;
  const containerWidth = 55;
  const bottomPadding = 90;

  let arrowPath;
 
  let upArrowIsVisible = false;  
  let downArrowIsVisible = $scrollStore.downArrow.isVisible;  
  let gripPosition = $scrollStore.gripPosition;

  let downArrow = { isVisible: false };
  let upArrow = { isVisible: false };
  let searchModal = { isOpen: false, query: "" };
  let markingSystem = { hits: [], consolidatedHits: [] };
  let totalMessages = 0;

  onDestroy(() => {
    window.removeEventListener('resize', setInitialGripPosition);
    unsubscribe();  // Unsubscribe from the store
  });


  function resetElasticGripToNeutral() {
    // set dragspeed to 0
    setInLocalStorage('dragSpeedUpDown', 0);
    // set gripPosition to 0
    //setInLocalStorage('gripPosition', 0);
    // set targetMessage to 0
    //setInLocalStorage('targetMessage', 0);
  }




  function setInitialGripPosition() {
    const container = document.getElementById("custom-scrollbar");
    
    // Initial bottom position
    gripY = container.clientHeight - radius - bottomPadding;
    
    // Load saved gripPosition from local storage
    const savedGripPosition = get('gripPosition');
    
    if (savedGripPosition !== null) {
      // Calculate gripY based on saved gripPosition
      const lowerBound = radius + 19;
      const upperBound = container.clientHeight - radius - bottomPadding;
      const rangeOfMotion = upperBound - lowerBound;
      
      gripY = upperBound - savedGripPosition * rangeOfMotion;
    
      // Update down arrow visibility based on saved grip position
      setInLocalStorage('downArrow_isVisible', savedGripPosition > 0);
    } else {
      setInLocalStorage('downArrow_isVisible', false);
    }
  }

  onMount(() => {

    resetElasticGripToNeutral();

    setInitialGripPosition();

    let gripAtBottom = get('gripPosition');
    if (gripAtBottom > 0) {
      setInLocalStorage('downArrow_isVisible', true);
    }

    window.addEventListener('resize', setInitialGripPosition);
    
  });

  function startDrag(e) {
    if (isElasticDragging) return; // If elastic drag is active, exit
    isDragging = true;
    gripColor = "#00FF00";
    document.body.style.userSelect = "none";
    document.body.style.cursor = "none";
    window.addEventListener('mousemove', drag);
    window.addEventListener('mouseup', stopDrag);
  }

  function stopDrag(e) {
    isDragging = false;
    gripColor = "#00C040";
    document.body.style.userSelect = "auto";
    document.body.style.cursor = "auto";
    window.removeEventListener('mousemove', drag);
    window.removeEventListener('mouseup', stopDrag);
  }

  function drag(e) {
    //if (isElasticDragging) return; // If elastic drag is active, exit
    if (isDragging) {
      e.preventDefault();
      const container = document.getElementById("custom-scrollbar");
      const rect = container.getBoundingClientRect();
      const offsetY = e.clientY - rect.top - 21;
      const lowerBound = radius + 19;
      const upperBound = container.clientHeight - radius - bottomPadding;
      gripY = Math.min(Math.max(lowerBound, offsetY), upperBound);

      // Normalize grip position
      const rangeOfMotion = upperBound - lowerBound;
      const currentRelativePosition = gripY - lowerBound;
      gripPosition = 1 - (currentRelativePosition / rangeOfMotion); // 1 at the top, 0 at the bottom
      // Update local storage grip position
      setInLocalStorage('gripPosition', gripPosition);
      //reloadScrollStore(); // Reload the scrollStore

        // Update downArrowIsVisible
      const isVisible = gripPosition !== 0;
      downArrowIsVisible = isVisible;
      //console.log(`downArrowIsVisible = ${downArrowIsVisible}`);
      //reloadScrollStore(); // Reload the scrollStore
  
      if (isVisible === false) {
          setInLocalStorage('downArrow_isVisible', false);
          downArrowIsVisible = false;
          //reloadScrollStore(); // Reload the scrollStore
        } else {
          setInLocalStorage('downArrow_isVisible', true);
          downArrowIsVisible = true;
          //reloadScrollStore(); // Reload the scrollStore
        }
      }
}
  
function handleDownArrowClick() {
  //console.log("Down arrow clicked");

  const container = document.getElementById("custom-scrollbar");
  const upperBound = container.clientHeight - radius - bottomPadding;
  const lowerBound = radius + 19;
  const range = upperBound - lowerBound;

  const duration = 400; // Duration in milliseconds
  const steps = 100; // Number of animation steps
  const stepDuration = duration / steps; // Duration of each step
  let currentStep = 0;

  const easeIn = (t) => t * t;
  
  const initialGripY = gripY;

  const animateGrip = () => {
    currentStep++;
    if (currentStep <= steps) {
      const t = currentStep / steps;
      const delta = upperBound - initialGripY;
      const targetGripY = initialGripY + delta * easeIn(t);

      const relativePosition = targetGripY - lowerBound;
      gripPosition = 1 - (relativePosition / range);

      gripPosition = Math.min(1, Math.max(0, gripPosition));

      setInLocalStorage('gripPosition', gripPosition);
      
      //console.log(`Frame ${currentStep}: gripPosition = ${gripPosition}`);

      gripY = targetGripY;

      setTimeout(animateGrip, stepDuration); // Use setTimeout to control speed
    } else {
      gripY = upperBound;
      gripPosition = 0;
      setInLocalStorage('gripPosition', gripPosition);

      downArrowIsVisible = false;
      setInLocalStorage('downArrow_isVisible', false);
      
    }
  };

  animateGrip(); // Initial call to start the animation
}

function handleUpArrowClick() {
  console.log("Up arrow clicked");
}

let prevState = null;
const unsubscribe = scrollStore.subscribe(currentState => {
  if (prevState) {
    for (const key in currentState) {
      if (!deepEqual(currentState[key], prevState[key])) {
        /* console.log(`Key ${key} changed`, {
          from: prevState[key],
          to: currentState[key]
        }); */
      }
    }
  }
  prevState = JSON.parse(JSON.stringify(currentState));  // Deep clone
});

// Deep equality check
function deepEqual(a, b) {
  if (a === b) return true;

  if (a && b && typeof a == 'object' && typeof b == 'object') {
    if (Array.isArray(a)) {
      if (a.length != b.length) return false;
      for (let i = 0; i < a.length; i++) {
        if (!deepEqual(a[i], b[i])) return false;
      }
      return true;
    }
    
    const keys = Object.keys(a);
    if (keys.length !== Object.keys(b).length) return false;

    for (let key of keys) {
      if (!b.hasOwnProperty(key)) return false;
      if (!deepEqual(a[key], b[key])) return false;
    }

    return true;
  }

  return false;
}


// Elastic grip control logic
let isDraggingElasticGrip = false;
const MAX_DRAG_DISTANCE = 170; // 2 inches in pixels (this may need adjustment based on your screen DPI)
const MIN_SPEED = 0; // The starting speed multiplier
const MAX_SPEED = 4.0; // Maximum speed multiplier, this can be adjusted to control the rate of scrolling
let dragDirection = null; // 'up' or 'down' or 'null'
let dragIntensity = 1;   // Ranges from 1 to 4
let dragSpeed = 0; // Calculated based on drag distance
let dragSpeedUpDown = 0;  // Calculated based on drag distance
let isElasticDragging = false; // True when the elastic grip is being dragged
let elasticGripColor = "#00C040"; // Default color for elastic grip
let topDotColor = "#006600"; // Default color for top dot
let middleDotColor = "#006600"; // Default color for middle dot
let bottomDotColor = "#006600"; // Default color for bottom dot
let startY = null; // This will store the initial Y position of the mouse
let deltaY = null; // This will store the delta Y position of the mouse
let initialDragY;  // Y-coordinate of where the drag started

function startElasticDrag(event) {
    //if (isDragging) return; // If normal drag is active, exit
    isElasticDragging = true;
    startY = event.clientY;  // Store the initial Y position of the mouse
    window.addEventListener('mousemove', elasticDrag); // Listen to mousemove on the window
    window.addEventListener('mouseup', stopElasticDrag);  // Listen to mouseup on the window
    event.stopPropagation();
}

function stopElasticDrag(event) {
    isElasticDragging = false;
    startY = null;  // Reset the initial Y position
    window.removeEventListener('mousemove', elasticDrag); // Remove the mousemove listener from the window
    window.removeEventListener('mouseup', stopElasticDrag);  // Remove the mouseup listener from the window
    //console.log("Stopped dragging");  // This will now only log when the grip is released
    
    // Reset the dot colors
    elasticGripColor = "#00C040";
    topDotColor = "#003300";
    middleDotColor = "#003300";
    bottomDotColor = "#003300";

    // Reset elastic grip dragSpeed to 0
    setInLocalStorage('dragSpeedUpDown', 0);
    dragSpeed = 0;

    event.stopPropagation();
}

function elasticDrag(e) {
    //if (isDragging) return; // If normal drag is active, exit
    e.stopPropagation();

    // Only proceed if the elastic grip is being dragged
    if (!isElasticDragging) return;

    if (startY === null) return; // Ensure startY is set

    const deltaY = e.clientY - startY; // Use the initial Y position for delta calculation

    // Determine the direction based on deltaY
    if (deltaY > 0) {
        dragDirection = 'down';
    } else if (deltaY < 0) {
        dragDirection = 'up';
    } // If deltaY is 0, dragDirection remains unchanged

    // Calculate speed based on drag distance
    const normalizedDistance = Math.min(Math.abs(deltaY), MAX_DRAG_DISTANCE) / MAX_DRAG_DISTANCE;
    dragSpeed = MIN_SPEED + (MAX_SPEED - MIN_SPEED) * normalizedDistance; 

    // Make dragSpeedUpDown negative if the direction is 'down', otherwise it stays as dragSpeed
    dragSpeedUpDown = (dragDirection === 'down') ? -dragSpeed : dragSpeed;
    // Update local storage with the calculated dragSpeedUpDown
    setInLocalStorage('dragSpeedUpDown', dragSpeedUpDown);

    // Calculate drag intensity
    dragIntensity = Math.ceil(dragSpeed);
    //console.log("Dragging", dragDirection);  // This will now only log when the grip is being dragged

    // Update visual feedback
    updateDotsBrightness();
}

function updateDotsBrightness() {
    const mellowRed = "#009900";
    const middleRed = "#FF0000";
    const brightRed = "#33FF00";
    
    if (dragDirection === 'up') {
        elasticGripColor = "#00FF00";  // Green color for the elastic grip
        
        bottomDotColor = "#003300";  // keep the bottom dot green
        middleDotColor = mellowRed;

        // Adjust top dot color based on dragIntensity
        if (dragIntensity === 1) {
            middleDotColor = mellowRed;
        } else if (dragIntensity === 2) {
            topDotColor = mellowRed;
        } else if (dragIntensity === 3) {
            middleDotColor = brightRed;
        } else if (dragIntensity === 4) {
            topDotColor = brightRed;
            middleDotColor = brightRed;
        }
        
    } else {  // This means it's 'up'
        elasticGripColor = "#00FF00";  // Green color for the elastic grip
        
        topDotColor = "#003300";  // keep the top dot green
        middleDotColor = mellowRed;

        // Adjust bottom dot color based on dragIntensity
        if (dragIntensity === 1) {
            middleDotColor = mellowRed;
        } else if (dragIntensity === 2) {
            bottomDotColor = mellowRed;
        } else if (dragIntensity === 3) {
            middleDotColor = brightRed;
        } else if (dragIntensity === 4) {
            bottomDotColor = brightRed;
            middleDotColor = brightRed;
        }
    }
}

</script>

<div class="flex-container">
  <div id="custom-scrollbar" on:mousemove={drag} on:mouseup={stopDrag} role="presentation" style="--container-width: {containerWidth}px;">
    <svg id="grip-svg" width="{svgWidth + 24}" height="calc(100% + 20px)">
        <!-- Elastic Grip elements -->
        <g id="elastic-grip" role="slider" aria-valuemin="0" aria-valuemax="1" aria-valuenow="0" tabindex="0" 
            on:mousedown={startElasticDrag} on:mouseup={stopElasticDrag} on:mousemove={elasticDrag}> 
          <!-- Invisible clickable area for the elastic grip -->
          <rect x="10" y="{gripY - 28}" width="40" height="33" fill="transparent" role="presentation" />
          <!-- Elastic Grip visual element (capsule shape) -->
          <rect x="12" y="{gripY - 27}" width="16" height="30" rx="10" ry="5" stroke="{elasticGripColor}" stroke-width="3" fill="none" />
          <!-- First dot -->
          <circle cx="20" cy="{gripY - 4}" r="2.2" fill="{bottomDotColor}" />
          <!-- Second dot (middle) -->
          <circle cx="20" cy="{gripY - 11}" r="2.7" fill="{middleDotColor}" />
          <!-- Third dot -->
          <circle cx="20" cy="{gripY - 18}" r="2.3" fill="{topDotColor}" />
      </g>
      <!-- Grip element with drag functionality and ARIA attributes -->
      <g role="slider" aria-valuemin="0" aria-valuemax="1" aria-valuenow="{gripY}" tabindex="0"
         on:mousedown={startDrag} on:mouseup={stopDrag}>
        <!-- Invisible clickable area for the grip -->
        <rect x="10" y="{gripY + 11}" width="40" height="21" fill="transparent" role="presentation"/>
        <!-- Grip visual elements -->
        <rect x="10" y="{gripY + 11}" rx="3" ry="3" width="20" height="4" fill="{gripColor}" />
        <rect x="10" y="{gripY + 19}" rx="3" ry="3" width="20" height="4" fill="{gripColor}" />
        <rect x="10" y="{gripY + 27}" rx="3" ry="3" width="20" height="4" fill="{gripColor}" />
      </g>
      <!-- Up arrow indicator for new messages -->
      <g id="up-arrow-indicator" role="presentation" on:click={handleUpArrowClick} visibility={upArrowIsVisible ? 'visible' : 'hidden'}>
        <!-- Invisible clickable area for the up arrow -->
        <rect x="11" y="{gripY - 9}" width="18" height="14" fill="transparent" role="presentation"/>
        <!-- Up arrow visual element -->
        <path id="up-arrow-path" d="M 7 12 L 23 12 L 15 0 Z" stroke="orange" stroke-width="2" fill="none" stroke-linejoin="round" transform="translate(5, {gripY - 13})" />
      </g>
      <!-- Down arrow indicator for new messages -->
      <g id="down-arrow-indicator" role="presentation" on:click={handleDownArrowClick} visibility={downArrowIsVisible ? 'visible' : 'hidden' } class="fade-in {downArrowIsVisible ? 'visible' : ''}">
        <!-- Invisible clickable area for the down arrow -->
        <rect x="10" y="{gripY + 38}" width="40" height="18" fill="transparent" role="presentation"/>
        <!-- Down arrow visual element -->
        <path bind:this={arrowPath} id="down-arrow-path" d="M 7 0 L 23 0 L 15 12 Z" stroke="#00C040" stroke-width="2" fill="none" stroke-linejoin="round" transform="translate(5, {gripY + 38})" />
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
    padding-right: 4px;
    width: var(--container-width);
    background: transparent;
  }

  #custom-scrollbar {
    height: 100vh;
    position: relative;
    background: transparent;
    width: var(--container-width);
    padding-left: 0px;
    padding-right: 0px;
  }

  #grip-svg {
    position: absolute;
    bottom: 0;
    height: 100vh;
    padding-left: 2px;
  }
  :focus { /* Hides focus ring on grip */
    outline: none;
  }

  #down-arrow-indicator {
  cursor: pointer;
}

#grip-svg {
  cursor: pointer;
}

.fade-in {
  transition: opacity 1s ease-in-out;
  opacity: 0;
}

.fade-in.visible {
  opacity: 1;
}


#custom-scrollbar, #grip-svg {
  cursor: default;
}

/* Add pointer cursor for the clickable areas */
#grip-svg rect, #up-arrow-indicator rect, #down-arrow-indicator rect {
  cursor: pointer;
}


</style>

  
  
  