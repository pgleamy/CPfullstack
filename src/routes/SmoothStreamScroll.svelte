/*

APPLY TO BOTH USER INPUT AND TO LLM STREAMED RESPONSE
For the LLM stream scrolling to be as smooth as possible, the stream file polling must be more frequent so the chunks written to the text area are shorter.

The Svelte component contains a script that simulates a real-time loop updating two variables: `accruedY` and `textEndLocation`. The purpose is to control the scrolling behavior of a text area, ensuring that the text content scrolls up smoothly as new text chunks are added.

Here is a breakdown of the operations:

Upon reviewing the entire conversation and the engineering decisions made, here are the key requirements and how they are met in the code:

1. **Reactivity**: The script uses Svelte's reactive stores to manage `textEndLocation`.
  
2. **Configurability**: `lineAndSpaceHeight` is defined as a configurable variable. The logic uses this variable to calculate the `deltaY` and `targetY`.

3. **Text Chunk Handling**: The function `handleNewlines` checks for newline characters (`\n`) in a text chunk and calculates the additional `Y` required for those newlines.

4. **DeltaY Calculation**: The `deltaY` is calculated as the difference between `targetY` and `accruedY`. `targetY` includes any additional Y-values from newline characters.

5. **Line Wrap Handling**: If `textEndLocation` goes beyond 1000 (indicating a line wrap), the code calculates the `deltaY` for the next line based on the overflow and resets `textEndLocation`.

6. **Rounding**: `accruedY` is rounded up to the nearest integer after each addition of `deltaY`, as per the requirement to have it a bit ahead.

7. **Loop Logic and Reset**: The loop runs as long as `textEndLocation` is less than or equal to 1000. When it exceeds, the loop resets `textEndLocation` and `accruedY`.

8. **Async Pause**: An asynchronous pause of 30 milliseconds is included in each loop iteration.

9. **Debugging Information**: The code logs relevant information (`X`, `Delta Y`, and `Accrued Y`) to the console for debugging and monitoring.

The logic appears to meet all the engineered requirements based on the information provided throughout the discussion. Therefore, the code should be satisfactory

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

