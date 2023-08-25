<script>
    import { onMount } from 'svelte';
    let showButton = true;
    let cubes = Array.from({ length: 10 }, (_, i) => i); // Number of cubes
  
    function handleClick() {
      showButton = false;
      setTimeout(() => {
        const cubesElement = document.querySelector('.cubes');
        cubesElement.style.opacity = 0;
      }, 500);
    }
  
    onMount(() => {
      if (!showButton) {
        const cubesElement = document.querySelector('.cubes');
        cubesElement.style.animation = 'jiggle 0.5s infinite, fade 1s forwards';
      }
    });
  </script>
  
  <style>
    .button {
      background-color: brightblue;
    }
  
    .cube {
      border: 1px solid brightblue; /* Thin lines */
      width: 10px; /* Small size */
      height: 10px;
    }
  
    @keyframes jiggle {
      0%, 100% { transform: translate(0); }
      50% { transform: translate(3px, 3px); } /* Random jiggle effect */
    }
  
    @keyframes fade {
      to { opacity: 0; }
    }
  
    .cubes {
      opacity: 1;
      animation: jiggle 0.5s infinite;
    }
  </style>
  
  {#if showButton}
    <button class="button" on:click={handleClick}>Click Me</button>
  {:else}
    <div class="cubes">
      {#each cubes as cube}
        <div class="cube"></div>
      {/each}
    </div>
  {/if}
  