<script>
    import { onMount } from 'svelte';
    import { conversation } from './conversationcontainer.svelte';
    import { 
        scrollStore, 
        get, 
        setInLocalStorage, 
        totalMessages, 
        targetMessage, 
        targetMessagesPixelHeight, 
        gripPosition, 
        dragSpeedUpDown, 
        messageHeight, // add to local storage
        fetchedMessageCount  // add to local storage
    } from '$lib/scrollStore.js'; 
  
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
      const fetchedMessageCount = get('fetchedMessageCount') || 0; // Retrieve the number of fetched messages from local storage
      messageCounts.push(fetchedMessageCount); // number of messages fetches as reported in local storage
      const newRelativeOffset = 0/* logic to calculate new offset based on added messages */;
      relativeOffsets.push(newRelativeOffset);
  
      // Logic to trim messages based on itemCount and scrollingDirection
      if (itemCount > 3) {
        trimArrays(scrollingDirection);
      }

      // Calculate renderedStartOffset and renderedEndOffset then output to console log
      // a report of the current state of the conversation[] array as a table
      renderedStartOffset = relativeOffsets[0];
      let storedHeight = updateLastItemHeight(); 
      let lastItemHeight = storedHeight ? storedHeight : 0;
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



    // Obtains the pixel height of the last item in the conversation[] array
    function updateLastItemHeight() {
        let lastItemHeight = 0;
        try {
            const storedHeight = get('messageHeight'); 
            lastItemHeight = storedHeight ? storedHeight : 0;
        } catch (error) {
            console.log('Failed to retrieve messageHeight from local storage: ', error);
        }

        // Based on the scrolling direction, either append or prepend to itemHeights[]
        if (scrollingDirection === 'DOWN') {
            itemHeights.push(lastItemHeight);
        } else if (scrollingDirection === 'UP') {
            itemHeights.unshift(lastItemHeight);
        }
    }



    function trimArrays(direction) {
        let messagesToTrim = 0;
        
        if (direction === 'DOWN') {
            messagesToTrim = messageCounts.shift();
            conversation.update(oldMessages => oldMessages.slice(messagesToTrim));
            relativeOffsets.shift();
            itemHeights.shift();
        }
        
        if (direction === 'UP') {
            messagesToTrim = messageCounts.pop();
            conversation.update(oldMessages => oldMessages.slice(0, -messagesToTrim));
            relativeOffsets.pop();
            itemHeights.pop();
        }
        
        itemCount--;
    }



  

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

  
  