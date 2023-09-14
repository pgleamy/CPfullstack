<script>
  //@ts-nocheck
  import { onMount, onDestroy } from "svelte";
  import { writable } from 'svelte/store';
  import { scrollStore } from '$lib/scrollStore.js';
  import { setInLocalStorage, get, load } from '$lib/scrollStore.js';
  import { createEventDispatcher } from 'svelte';

  let isDragging = false;
  let gripY = 0; // Y-coordinate of the grip
  let gripColor = "#008000"; // Default color for grip
  const radius = 10;
  const svgWidth = 30;
  const containerWidth = 55;
  const bottomPadding = 96;

  let arrowPath;
  let arrowColor = "#FF0000";
  let updateDownArrowColorInterval;

  let upArrowIsVisible = false;  // Renamed from isUpArrowVisible
  let downArrowIsVisible = false;  // Renamed from isDownArrowVisible
  let gripPosition;
  let downArrow = { isVisible: false, isThrobbing: false };
  let upArrow = { isVisible: false, isThrobbing: false };
  let searchModal = { isOpen: false, query: "" };
  let markingSystem = { hits: [], consolidatedHits: [] };
  let totalMessages = 0;

  onDestroy(() => {
    clearInterval(updateDownArrowColorInterval);
    window.removeEventListener('resize', setInitialGripPosition);
  });

  function setInitialGripPosition() {
    const container = document.getElementById("custom-scrollbar");
    gripY = container.clientHeight - radius - bottomPadding;
  }

  window.addEventListener('resize', setInitialGripPosition);

  onMount(() => {

    setInitialGripPosition();
    window.addEventListener('resize', setInitialGripPosition);
    updateDownArrowColorInterval = setInterval(updateArrowColor, stepInterval);

    const unsubscribe = scrollStore.subscribe(value => {
      gripPosition = value.gripPosition;
      
      downArrow = {
        isVisible: value.downArrow.isVisible,
        isThrobbing: value.downArrow.isThrobbing
      };
      
      upArrow = {
        isVisible: value.upArrow.isVisible,
        isThrobbing: value.upArrow.isThrobbing
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
    clearInterval(updateDownArrowColorInterval);
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
    gripColor = "#008000";
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
      // Update downArrowIsVisible
      downArrowIsVisible = gripY !== upperBound;  // Renamed from isDownArrowVisible
    }
  }

  function handleDownArrowClick() {
    console.log("Down arrow clicked");
  }

  let isArrowVisible = true;
  let isArrowThrobbing = false;

  setInterval(() => {
    isArrowVisible = !isArrowVisible;
    arrowColor = isArrowVisible ? "#FF0000" : "#FFFFFF";
  }, 1000);

  let startColor = [0, 255, 0];
  let endColor = [0, 128, 0];
  let steps = 100;
  let stepInterval = 10;
  let currentStep = 0;

  function interpolateColor(start, end, step, maxSteps) {
    let r = start[0] + ((end[0] - start[0]) * step) / maxSteps;
    let g = start[1] + ((end[1] - start[1]) * step) / maxSteps;
    let b = start[2] + ((end[2] - start[2]) * step) / maxSteps;
    return `rgb(${Math.round(r)}, ${Math.round(g)}, ${Math.round(b)})`;
  }

  function updateArrowColor() {
    arrowPath = document.getElementById("down-arrow-path");
    if (arrowPath) {
      arrowPath.setAttribute("stroke", interpolateColor(startColor, endColor, currentStep, steps));
    }
    currentStep++;
    if (currentStep > steps) {
      [startColor, endColor] = [endColor, startColor];
      currentStep = 0;
    }
  }

  function handleNewMessage(isOffScreen) {
    isArrowThrobbing = isOffScreen;
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
      <g id="down-arrow-indicator" role="presentation" on:click={handleDownArrowClick} visibility={downArrowIsVisible ? 'visible' : 'hidden'}>
        <!-- Invisible clickable area for the down arrow -->
        <rect x="11" y="{gripY + 20}" width="18" height="13" fill="transparent" role="presentation"/>
        <!-- Down arrow visual element -->
        <path bind:this={arrowPath} id="down-arrow-path" d="M 7 0 L 23 0 L 15 12 Z" stroke="green" stroke-width="2" fill="none" stroke-linejoin="round" transform="translate(5, {gripY + 20})" />
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
    padding-left: 0px;

  }
  :focus {
    outline: none;
  }

  #down-arrow-indicator {
  cursor: pointer;
}

#grip-svg {
  cursor: pointer;
}

</style>

  
  
  