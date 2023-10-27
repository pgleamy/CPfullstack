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
        messagesItemHeight, 
        fetchedMessageCount  
    } from '$lib/scrollStore.js'; 
  
    const fixedOffset = 5000000;
    const massiveContainerHeight = '10000000px';
    const itemLimit = 3; // Number of items to keep in the conversation[] array
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
  
      updateConversationState();

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


    function updateConversationState() {
        // Step 1: Perform trimming if necessary
        if (itemCount > itemLimit) {
            trimArrays(scrollingDirection);
        }

        // Step 2: Update itemCount
        itemCount++;

        // Step 3: Update fetchedMessageCount and messageCounts
        const fetchedMessageCount = get('fetchedMessageCount') || 0;
        messageCounts.push(fetchedMessageCount);

        // Step 4: Update itemHeights and lastItemHeight
        let lastItemHeight = 0;
        if (scrollingDirection === 'DOWN') {
            const storedHeight = get('messageHeight') || 0;
            itemHeights.push(storedHeight);
            lastItemHeight = storedHeight;
        } else if (scrollingDirection === 'UP') {
            const storedHeight = get('messageHeight') || 0;
            itemHeights.unshift(storedHeight);
            lastItemHeight = storedHeight;
        } 

        // Step 5: Update newRelativeOffset and relativeOffsets
        let newRelativeOffset;
        if (scrollingDirection === 'DOWN') {
            newRelativeOffset = itemHeights.slice(0, -1).reduce((acc, val) => acc + val, 0);
        } else if (scrollingDirection === 'UP') {
            newRelativeOffset = renderedStartOffset - lastItemHeight;
        }
        relativeOffsets.push(newRelativeOffset);

        // Step 6: Update renderedStartOffset and renderedEndOffset
        renderedStartOffset = relativeOffsets[0];
        renderedEndOffset = relativeOffsets[itemCount - 1] + lastItemHeight;
    } // End of updateConversationState()


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
    } // End of trimArrays()



    onMount(() => {
      return () => {
        // Cleanup
        unsubscribe();
      };
    }); // End of onMount()

</script>



<!-- Virtual Container -->
<div id="virtual-container" style="height: { massiveContainerHeight }; position: relative;">
  <div id="conversation-container" style="position: relative; top: {fixedOffset}px;">
    <!-- The actual messages would be rendered here by ConversationContainer.svelte -->
  </div>
</div>

  
  