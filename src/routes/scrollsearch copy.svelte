<script>
    
    let isDragging = false;
    let circleY; // Y-coordinate of the circle
    let circleColor = "#008000"; // Default color
    const radius = 10; // Radius of the circle
    const svgWidth = 30; // Width of the SVG
    const containerWidth = 55; // Width of the container
    const bottomPadding = 96; // Padding at the bottom of the container
    
  
    // Set initial position based on container height
    function setInitialPosition() {
      const container = document.getElementById("custom-scrollbar");
      circleY = container.clientHeight - radius - bottomPadding;
    }

      // Update position when window is resized
    window.addEventListener('resize', setInitialPosition);

  
    // Call this function when the component mounts
    import { onMount } from "svelte";
    onMount(() => {
      setInitialPosition();
      window.addEventListener('resize', setInitialPosition);
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
  </script>
  
  
<div class="flex-container">
  <div id="custom-scrollbar" on:mousemove={drag} on:mouseup={stopDrag} role="presentation" style="--container-width: {containerWidth}px;">
    <svg id="circle-svg" width="{svgWidth}" height="100%">
      <!-- Group element with events -->
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
  
  
  