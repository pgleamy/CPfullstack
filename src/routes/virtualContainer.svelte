<script>
    import { onMount } from 'svelte';
    import { conversation } from './conversationcontainer.svelte';
    import { scrollStore, get, setInLocalStorage, totalMessages, targetMessage, targetMessagesPixelHeight, gripPosition, dragSpeedUpDown } from '$lib/scrollStore.js'; 
  
    const fixedOffset = 5000000;
    let itemCount = 0; // Number of items in the conversation[]
    let relativeOffsets = []; // Relative offsets of each item
    let itemHeights = []; // Height of each item in pixels
    let messageCounts = []; // Number of messages in each item (20 for slices, 10 for parts)
    let renderedStartOffset = 0; // Offset of the START of the first rendered item in the conversation[]
    let renderedEndOffset = 0; // Offset of the END of the last rendered item in the conversation[]
    let scrollingDirection = null;
    $: { 
        scrollingDirection = $dragSpeedUpDown < 0 ? 'UP' : 'DOWN';
        console.log('scrollingDirection', scrollingDirection);
    }


    // conversation[] subscription
    // Initialize and monitor the conversation array from conversationcontainer.svelte
    let currentConversation = [];
    let unsubscribe = conversation.subscribe(value => {
      currentConversation = value;
  
      // Logic to update itemCount, relativeOffsets, and messageCounts
      
      // Your existing code for determining new messages and updating arrays
      itemCount++;
      messageCounts.push(10); // Assuming it's a part
      const newRelativeOffset = /* logic to calculate new offset based on added messages */;
      relativeOffsets.push(newRelativeOffset);
  
      // Logic to trim messages based on itemCount and scrollingDirection
      if (itemCount > 3) {
        let messagesToTrim = 0;

        // If scrolling DOWN, trim the earliest messages
        if (scrollingDirection === "DOWN") {
          messagesToTrim = messageCounts.shift();
          conversation.update(oldMessages => oldMessages.slice(messagesToTrim));
          relativeOffsets.shift();
        }
        
        // If scrolling UP, trim the latest messages
        if (scrollingDirection === "UP") {
          messagesToTrim = messageCounts.pop();
          conversation.update(oldMessages => oldMessages.slice(0, -messagesToTrim));
          relativeOffsets.pop();
        }
        
        itemCount--;
      }

      renderedStartOffset = relativeOffsets[0];
      // Logic to determine the height of the last item in pixels
      const lastItemHeight = /* your logic here */;
      renderedEndOffset = relativeOffsets[itemCount - 1] + lastItemHeight;
      // Very detailed console log that creates a table showing the values of all of the current conversation[] items labelled and stacked vertically
      let tableData = [];
      for (let i = 0; i < itemCount; i++) {
        tableData.push({
        'Item': i + 1,
        'MsgCnt': messageCounts[i],
         'RelOff': relativeOffsets[i],
        'ItemHt': itemHeights[i]
        });
      }
      console.table(tableData);
      console.log(`Start Offset: ${renderedStartOffset}, End Offset: ${renderedEndOffset}`);
        
    }); // End of conversation[] subscribe
  

    onMount(() => {
      return () => {
        // Cleanup
        unsubscribe();
      };
    }); // End of onMount()

</script>

<!-- Virtual Container -->
<div id="virtual-container" style="height: 10000000px; position: relative;">
  <div id="conversation-container" style="position: relative; top: {fixedOffset}px;">
    <!-- The actual messages would be rendered here by ConversationContainer.svelte -->
  </div>
</div>

  
  