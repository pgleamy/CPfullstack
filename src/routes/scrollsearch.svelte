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

    setInitialGripPosition();

    let gripAtBottom = get('gripPosition');
    if (gripAtBottom > 0) {
      setInLocalStorage('downArrow_isVisible', true);
    }

    window.addEventListener('resize', setInitialGripPosition);
    
  });

  function startDrag(e) {
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
    
    if (isDragging) {
      e.preventDefault();
      const container = document.getElementById("custom-scrollbar");
      const rect = container.getBoundingClientRect();
      const offsetY = e.clientY - rect.top;
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

  const duration = 1000; // Duration in milliseconds
  const steps = 50; // Number of animation steps
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
      //reloadScrollStore(); // Reload the scrollStore
      //console.log(`Frame ${currentStep}: gripPosition = ${gripPosition}`);

      gripY = targetGripY;

      setTimeout(animateGrip, stepDuration); // Use setTimeout to control speed
    } else {
      gripY = upperBound;
      gripPosition = 0;
      setInLocalStorage('gripPosition', gripPosition);

      downArrowIsVisible = false;
      setInLocalStorage('downArrow_isVisible', false);
      //reloadScrollStore(); // Reload the scrollStore
    }
  };

  animateGrip(); // Initial call to start the animation
}

function handleUpArrowClick() {
  console.log("Up arrow clicked");
}

  let cursorStyle = "grab"; // Default cursor style



let prevState = null;
const unsubscribe = scrollStore.subscribe(currentState => {
  if (prevState) {
    for (const key in currentState) {
      if (!deepEqual(currentState[key], prevState[key])) {
        console.log(`Key ${key} changed`, {
          from: prevState[key],
          to: currentState[key]
        });
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

function debounce(func, wait) {
  let timeout;
  return function() {
    const context = this, args = arguments;
    clearTimeout(timeout);
    timeout = setTimeout(() => {
      func.apply(context, args);
    }, wait);
  };
}


</script>

<div class="flex-container">
  <div id="custom-scrollbar" on:mousemove={drag} on:mouseup={stopDrag} role="presentation" style="--container-width: {containerWidth}px;">
    <svg id="grip-svg" width="{svgWidth}" height="calc(100% + 20px)">
        <!-- Elastic Grip elements -->
        <g role="slider" aria-valuemin="0" aria-valuemax="1" aria-valuenow="0" tabindex="0">
          <!-- Invisible clickable area for the elastic grip -->
          <rect x="14" y="{gripY - 26}" width="12" height="30" fill="transparent" role="presentation"/>
          <!-- Elastic Grip visual element (capsule shape) -->
          <rect x="12" y="{gripY - 27}" width="16" height="30" rx="10" ry="5" stroke="{gripColor}" stroke-width="3" fill="none" />
          <!-- First dot -->
          <circle cx="20" cy="{gripY - 4}" r="1.5" fill="{gripColor}" />
          <!-- Second dot (middle) -->
          <circle cx="20" cy="{gripY - 11}" r="1.5" fill="{gripColor}" />
          <!-- Third dot -->
          <circle cx="20" cy="{gripY - 18}" r="1.5" fill="{gripColor}" />
      </g>
      <!-- Grip element with drag functionality and ARIA attributes -->
      <g role="slider" aria-valuemin="0" aria-valuemax="1" aria-valuenow="{gripY}" tabindex="0"
         on:mousedown={startDrag} on:mouseup={stopDrag}>
        <!-- Invisible clickable area for the grip -->
        <rect x="11" y="{gripY + 11}" width="30" height="21" fill="transparent" role="presentation"/>
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
        <rect x="12" y="{gripY + 36}" width="16" height="10" fill="transparent" role="presentation"/>
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
    width: var(--container-width);
    background: transparent;
  }

  #custom-scrollbar {
    height: 100vh;
    position: relative;
    background: transparent;
    width: var(--container-width);
    padding-left: 0px;
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

</style>

  
  
  