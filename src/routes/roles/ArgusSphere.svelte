<script>
    import { onMount } from 'svelte';
  
    let canvas;
    let ctx;
    let rotation = { x: 0, y: 0 };
    const size = 120;
    const colors = ['#ce9', '#aaa', '#353', '#29a'];
    const sphere = [];
    const keysPressed = {};
  
    function createSphere() {
      for (let i = 0; i <= Math.PI * 2; i += 0.2) {
        const line = [];
        for (let j = 0; j <= Math.PI; j += 0.1) {
          line.push({
            x: size * Math.sin(i) * Math.sin(j),
            y: size * Math.cos(i),
            z: size * Math.sin(i) * Math.cos(j)
          });
        }
        sphere.push(line);
      }
    }
  
    function drawSphere() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.imageSmoothingEnabled = true;  // Enable antialiasing
      ctx.imageSmoothingQuality = 'high';  // Optional: Set the quality to 'high' for better antialiasing
      ctx.setTransform(1, 0, 0, 1, 0, 0);
      ctx.translate(canvas.width / 2, canvas.height / 2);

      ctx.lineWidth = 4;
  
      for (let i = 0; i < sphere.length; i++) {
        
        ctx.strokeStyle = colors[i % colors.length];
        ctx.beginPath();
        for (let j = 0; j < sphere[i].length; j++) {
          let x = sphere[i][j].x;
          let y = sphere[i][j].y * Math.cos(rotation.y) - sphere[i][j].z * Math.sin(rotation.y);
          let z = sphere[i][j].y * Math.sin(rotation.y) + sphere[i][j].z * Math.cos(rotation.y);
  
          x = x * Math.cos(rotation.x) - z * Math.sin(rotation.x);
          z = z * Math.cos(rotation.x) + x * Math.sin(rotation.x);
  
          if (j === 0) {
            ctx.moveTo(x, y);
          } else {
            ctx.lineTo(x, y);
          }
        }     
        ctx.closePath();
        ctx.stroke();
      }
      ctx.setTransform(1, 0, 0, 1, 0, 0);

    }
  
    let lastRenderTime = 0;
const renderInterval = 100; // Time in milliseconds, e.g., 100ms

function update(timestamp) {
  if (!lastRenderTime || timestamp - lastRenderTime >= renderInterval) {
    if (keysPressed['ArrowUp']) rotation.y -= 0.08;
    if (keysPressed['ArrowDown']) rotation.y += 0.08;
    if (keysPressed['ArrowLeft']) rotation.x -= 0.08;
    if (keysPressed['ArrowRight']) rotation.x += 0.08;
    drawSphere();
    lastRenderTime = timestamp;
  }
  window.requestAnimationFrame(update);
}
  
    function handleKeyDown(e) {
      keysPressed[e.key] = true;
    }
  
    function handleKeyUp(e) {
      keysPressed[e.key] = false;
    }
  
function handleResize() {
    const devicePixelRatio = window.devicePixelRatio || 1;
    const internalScale = devicePixelRatio * 2; // Increased scale for higher resolution
    const displayScale = 2; // Adjust this value to reduce the sphere's visual scale

    canvas.width = window.innerWidth / 2 * internalScale;
    canvas.height = window.innerHeight / 2 * internalScale;

    // Keep the displayed size of the canvas the same
    canvas.style.width = `${window.innerWidth / 2}px`;
    canvas.style.height = `${window.innerHeight / 2}px`;

    // Reset any existing transformations
    ctx.setTransform(1, 0, 0, 1, 0, 0);

    // Scale down the context to reduce the visual size of the sphere
    ctx.scale(displayScale, displayScale);

    // Translate the context so that the sphere is centered
    ctx.translate((canvas.width / 2) / displayScale, (canvas.height / 2) / displayScale);
}


  
    onMount(() => {
      canvas = document.getElementById('sphereCanvas');
      ctx = canvas.getContext('2d');
      handleResize(); // Set initial canvas size
      createSphere();
      window.requestAnimationFrame(update); // Start the animation loop
  
      window.addEventListener('keydown', handleKeyDown);
      window.addEventListener('keyup', handleKeyUp);
      window.addEventListener('resize', handleResize);
  
      return () => {
        // Cleanup event listeners when the component is destroyed
        window.removeEventListener('keydown', handleKeyDown);
        window.removeEventListener('keyup', handleKeyUp);
        window.removeEventListener('resize', handleResize);
      };
    });
  </script>
  
  <style>
    canvas {
      position: fixed;
      bottom: -0px; /* 10% of the viewport height minus 65 pixels */
      right: -50px; /* 10% of the viewport width minus 65 pixels */
      z-index: 0;
      background-color: transparent;
      justify-content: center;
    }
  </style>
  
  <canvas id="sphereCanvas"></canvas>
  