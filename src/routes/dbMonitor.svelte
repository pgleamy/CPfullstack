// pseudocode
<script>
    
    import { onMount } from 'svelte';
    import { dbEvents } from './store'; // Your Svelte store
  
    let windowHeight = 0;
    let headerHeight = 50; // Assuming header height is 50px
    let buffer = 10; // 10-pixel buffer
    let numMessages; // To be dynamically updated
  
    onMount(() => {
      // Initialize WebSocket or other real-time data listeners here
      windowHeight = window.innerHeight;
  
      const unsubscribe = dbEvents.subscribe(events => {
        numMessages = events.length;
      });
  
      return unsubscribe; // Cleanup
    });
  </script>
  
  <!-- SVG container -->
  <div id="monitor-container" style="height: {windowHeight - headerHeight - buffer}px;">
    {#each $dbEvents as event, index}
      <div class="spark" style="bottom: {(index / numMessages) * 100}%;" />
    {/each}
  </div>
  
  <style>
    #monitor-container {
      position: relative;
      width: 10px;
    }
  
    .spark {
      position: absolute;
      width: 10px;
      height: 10px;
      background-color: blue; /* initial color */
      opacity: 1; /* initial opacity */
      /* Add your initial size settings here */
  
      animation: fadeAway 2s ease-out forwards; /* 2s is just a placeholder, adjust as needed */
    }
  
    @keyframes fadeAway {
      0% {
        transform: translateY(0);
      }
      100% {
        transform: translateY(100px); /* move upwards by 100px */
        opacity: 0; /* fade away */
        width: 0; /* diminish size */
        height: 0; /* diminish size */
      }
    }
  </style>
  