/*

APPLY TO BOTH USER INPUT AND TO LLM STREAMED RESPONSE
For the LLM stream scrolling to be as smooth as possible, the stream file polling must be more frequent so the chunks written to the text area are shorter.

The Svelte component contains a script that simulates a real-time loop updating two variables: `accruedY` and `textEndLocation`. The purpose is to control the scrolling behavior of a text area, ensuring that the text content scrolls up smoothly as new lines are added.

Here is a breakdown of the operations:

### Variables:

1. `lineAndSpaceHeight`: A configurable variable representing the total height of a text line and the space beneath it, initialized to 21 pixels.
  
2. `textEndLocation`: A Svelte writable store, initialized to 0. It represents the x-coordinate where the text ends in a 2D space, simulating the horizontal position of the text cursor.

3. `accruedY`: A local variable initialized to 0, representing the y-coordinate that needs to be scrolled to, to make room for the new text line.

### Functions:

1. `runLoop()`: An asynchronous function responsible for executing the loop logic.

2. Within `runLoop()`, a `while` loop runs as long as `textEndLocation` is less than or equal to 1000.
  
    - `targetY` is calculated based on `textEndLocation` and `lineAndSpaceHeight`. It represents the desired y-coordinate to scroll to.
  
    - `deltaY` represents the difference between `targetY` and the current `accruedY`. It's added to `accruedY`, which is then rounded up to the nearest integer.
  
    - Logs the current state of `textEndLocation`, `deltaY`, and `accruedY` to the console for debugging or monitoring.
  
    - Randomly increments `textEndLocation` by a value between 5 and 15, simulating the text growing horizontally.
  
    - If `textEndLocation` exceeds 1000, `accruedY` is set to `lineAndSpaceHeight`, and the loop breaks.

    - Pauses for 30 milliseconds before the next iteration.

### Execution Flow:

1. The script starts by initializing the variables and Svelte store.
  
2. It then calls `runLoop()`, initiating the asynchronous loop that simulates the scrolling behavior.

### Other Considerations:

- The asynchronous delay of 30 milliseconds is used to throttle the loop, allowing for smoother real-time updates.
  
- If `textEndLocation` exceeds 1000, the `accruedY` is set to `lineAndSpaceHeight`, ensuring that the scroll reaches the target position.

This component could be used as a part of a larger application where the text area's content dynamically grows, and smooth scrolling is desired.

*/
<script>
  import { writable } from 'svelte/store';

  let lineAndSpaceHeight = 21;
  let textEndLocation = writable(0);

  // Function to handle newline characters in a text chunk
  function handleNewlines(textChunk) {
    let additionalY = 0;
    if (textChunk.endsWith('\n')) {
      additionalY += lineAndSpaceHeight;
      const extraNewlines = textChunk.match(/\n/g).length - 1;
      additionalY += lineAndSpaceHeight * extraNewlines;
    }
    return additionalY;
  }

  async function runLoop() {
    let accruedY = 0;
    let $textEndLocation = 0;
    let textChunk = ""; // Replace with actual text chunk in your implementation

    while ($textEndLocation <= 1000) {
      const additionalY = handleNewlines(textChunk);
      const targetY = ((lineAndSpaceHeight / 1000) * $textEndLocation) + additionalY;
      let deltaY = targetY - accruedY;

      if ($textEndLocation > 1000) {
        const overflow = $textEndLocation - 1000;
        $textEndLocation = overflow; // Reset to the overflow amount
        deltaY = overflow * (lineAndSpaceHeight / 1000); // Set deltaY for the next line based on the overflow
      }

      accruedY += deltaY;
      accruedY = Math.ceil(accruedY); // Round Y up to the nearest integer

      console.log(`X: ${$textEndLocation}, Delta Y: ${deltaY.toFixed(2)}, Accrued Y: ${accruedY}`);

      $textEndLocation += Math.floor(Math.random() * 11) + 5; // Increment X by a random number between 5 and 15

      if ($textEndLocation > 1000) {
        accruedY = lineAndSpaceHeight; // Set Y to the target value
        console.log(`X: ${$textEndLocation}, Delta Y: 0, Accrued Y: ${lineAndSpaceHeight}`);
      }

      await new Promise(resolve => setTimeout(resolve, 30)); // 30 milliseconds pause
    }

    // Reset X and Y for the next loop
    $textEndLocation = 0;
    accruedY = 0;
  }

  runLoop();
</script>

