<script>
  //@ts-nocheck
  import { onMount, onDestroy } from "svelte";
  import { writable } from 'svelte/store';
  import { scrollStore, setInLocalStorage, get, load } from '$lib/scrollStore.js';
  import { createEventDispatcher } from 'svelte';

  let isDragging = false;
  let gripY = 0; // Y-coordinate of the grip
  let gripColor = "#00C040"; // Default color for grip
  const radius = 10;
  const svgWidth = 30;
  const containerWidth = 55;
  const bottomPadding = 96;

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
  });

function setInitialGripPosition() {
  const container = document.getElementById("custom-scrollbar");
  
  // Initial bottom position
  gripY = container.clientHeight - radius - bottomPadding;
  
  // Load saved gripPosition from local storage
  const savedGripPosition = get('gripPosition');  // Assuming 'get' fetches from local storage
  
  if (savedGripPosition !== null) {
    // Calculate gripY based on saved gripPosition
    const lowerBound = radius + 19;
    const upperBound = container.clientHeight - radius - bottomPadding;
    const rangeOfMotion = upperBound - lowerBound;
    
    gripY = upperBound - savedGripPosition * rangeOfMotion;
  
    // Update down arrow visibility based on saved grip position
    const isVisible = savedGripPosition !== 0;
    setInLocalStorage('downArrow_isVisible', isVisible);
    downArrowIsVisible = isVisible; // Directly set the state variable
  } else {
    // Default value when there's no saved grip position
    setInLocalStorage('downArrow_isVisible', false);
    downArrowIsVisible = false;
  }
}

  onMount(() => {

    setInitialGripPosition();
    // Explicitly set the value in local storage and the reactive variable
    setInLocalStorage('downArrow_isVisible', false);
    downArrowIsVisible = false;
    // If gripPosition > 0 then show the down arrow
    let gripAtBottom = get('gripPosition');
    if (gripAtBottom > 0) {
      setInLocalStorage('downArrow_isVisible', true);
      downArrowIsVisible = true;
    }

    window.addEventListener('resize', setInitialGripPosition);
 
    const unsubscribe = scrollStore.subscribe(value => {

      gripPosition = value.gripPosition;

      downArrow = {
        isVisible: value.downArrow.isVisible,
      };
      
      upArrow = {
        isVisible: value.upArrow.isVisible,
      };

      searchModal = {
        isOpen: value.searchModal.isOpen,
        query: value.searchModal.query
      };

      markingSystem = {
        hits: value.markingSystem.hits,
        consolidatedHits: value.markingSystem.consolidatedHits
      };

    totalMessages = value.totalMessages;
    });

    // Cleanup function
    return () => {

      window.removeEventListener('resize', setInitialGripPosition);
      unsubscribe();  // Unsubscribe from the store
    };

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

        // Update downArrowIsVisible
      const isVisible = gripPosition !== 0;
      downArrowIsVisible = isVisible;
      console.log(`downArrowIsVisible = ${downArrowIsVisible}`);
  
      if (isVisible === false) {
          setInLocalStorage('downArrow_isVisible', false);
          downArrowIsVisible = false;
        } else {
          setInLocalStorage('downArrow_isVisible', true);
          downArrowIsVisible = true;
        }
      }

}
  
function handleDownArrowClick() {
  console.log("Down arrow clicked");

  const container = document.getElementById("custom-scrollbar");
  const upperBound = container.clientHeight - radius - bottomPadding;
  const lowerBound = radius + 19;
  const range = upperBound - lowerBound;

  const duration = 1000; // Duration in milliseconds
  const steps = 60; // Number of animation steps
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

  let cursorStyle = "grab"; // Default cursor style
</script>

<div class="flex-container">
  <div id="custom-scrollbar" on:mousemove={drag} on:mouseup={stopDrag} role="presentation" style="--container-width: {containerWidth}px;">
    <svg id="grip-svg" width="{svgWidth}" height="calc(100% + 20px)">
      <!-- Grip element with drag functionality and ARIA attributes -->
      <g role="slider" aria-valuemin="0" aria-valuemax="1" aria-valuenow="{gripY}" tabindex="0"
         on:mousedown={startDrag} on:mouseup={stopDrag}>
        <!-- Invisible clickable area for the grip -->
        <rect x="10" y="{gripY - 8}" width="30" height="21" fill="transparent" role="presentation"/>
        <!-- Grip visual elements -->
        <rect x="10" y="{gripY - 8}" rx="3" ry="3" width="20" height="4"         fill="{gripColor}" />
        <rect x="10" y="{gripY}" rx="3" ry="3" width="20" height="4" fill="{gripColor}" />
        <rect x="10" y="{gripY + 8}" rx="3" ry="3" width="20" height="4" fill="{gripColor}" />
      </g>
      <!-- Up arrow indicator for new messages -->
      <g id="up-arrow-indicator" role="presentation" on:click={handleUpArrowClick} visibility={upArrowIsVisible ? 'visible' : 'hidden'}>
        <!-- Invisible clickable area for the up arrow -->
        <rect x="11" y="{gripY - 28}" width="18" height="14" fill="transparent" role="presentation"/>
        <!-- Up arrow visual element -->
        <path id="up-arrow-path" d="M 7 12 L 23 12 L 15 0 Z" stroke="orange" stroke-width="2" fill="none" stroke-linejoin="round" transform="translate(5, {gripY - 28})" />
      </g>
      <!-- Down arrow indicator for new messages -->
      <g id="down-arrow-indicator" role="presentation" on:click={handleDownArrowClick} visibility={downArrowIsVisible ? 'visible' : 'hidden' } class="fade-in {downArrowIsVisible ? 'visible' : ''}">
        <!-- Invisible clickable area for the down arrow -->
        <rect x="11" y="{gripY + 20}" width="18" height="13" fill="transparent" role="presentation"/>
        <!-- Down arrow visual element -->
        <path bind:this={arrowPath} id="down-arrow-path" d="M 7 0 L 23 0 L 15 12 Z" stroke="#00C040" stroke-width="2" fill="none" stroke-linejoin="round" transform="translate(5, {gripY + 20})" />
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

  
  
  