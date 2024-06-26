// $lib/scrollStore.js
// @ts-nocheck

import { writable } from 'svelte/store';

// Define custom event
const localStorageChangeEvent = new Event('localStorageChange');

let isEventBeingProcessed = false;

// Function to set a setting in Local Storage
const setInLocalStorage = (key, value) => {
  localStorage.setItem(key, value);
  if (!isEventBeingProcessed) {
    window.dispatchEvent(localStorageChangeEvent);
  }
};

// Listen for custom event and reload scrollStore when detected
window.addEventListener('localStorageChange', () => {
  if (!isEventBeingProcessed) {
    isEventBeingProcessed = true;
    reloadScrollStore();
    isEventBeingProcessed = false;
  }
});

// Function to get a setting from Local Storage
const get = (key) => {
  return localStorage.getItem(key);
};

// Function to remove a setting from Local Storage
const remove = (key) => {
  localStorage.removeItem(key);
};

// Function to load all settings from Local Storage into an object
const load = () => {

  return {
    gripPosition: parseFloat(get('gripPosition')) || 0,
    downArrow: {
      isVisible: get('downArrow_isVisible') !== null ? JSON.parse(get('downArrow_isVisible')) : false
    },
    upArrow: {
      isVisible: get('upArrow_isVisible') !== null ? JSON.parse(get('upArrow_isVisible')) : false
    },
    searchModal: {
      isOpen: get('searchModal_isOpen') !== null ? JSON.parse(get('searchModal_isOpen')) : false,
      query: get('searchModal_query') || "",
    },
    markingSystem: {
      hits: get('markingSystem_hits') !== null ? JSON.parse(get('markingSystem_hits')) : [],
      consolidatedHits: get('markingSystem_consolidatedHits') !== null ? JSON.parse(get('markingSystem_consolidatedHits')) : [],
    },
    totalMessages: parseInt(get('totalMessages')) || 0,

    targetMessage: parseInt(get('targetMessage')) || 0, // The target message of the fetchConversationSlice function

    dragSpeedUpDown: parseFloat(get('dragSpeedUpDown')) || 0, // Elastic grip scroll speed. Defaults to 0 to signify 0 drag velocity, otherwise is a positive number for up and a negative number for down

    userInputComponentHeight: parseInt(get('userInputComponentHeight')) || 0, // Height of the user input component elements in pixels

    targetMessagesPixelHeight: parseInt(get('targetMessagesPixelHeight')) || 0, // Height of the conversation-container contents in pixels

    unsentPrompt: get('unsentPrompt') || "", // The unsent prompt contents

    unsentPromptHeight: parseInt(get('unsentPromptHeight')) || 0, // Height of the unsent prompt component elements in pixels
 
    // variables for the persistent scroll restoration feature
    block_idDisplayedInMiddleOfDOM: get('block_idDisplayedInMiddleOfDom') || "", // The message currently displayed in the middle of the DOM
    startRestore: get('startRestore') || "", // The start block_id of the restore range
    endRestore: get('endRestore') || "", // The end block_id of the restore range
    targetMessagesPixelHeightRestore: parseInt(get('targetMessagesPixelHeightRestore')) || 0, // The target messages pixel height restoring into
    scrollTopRestore: parseInt(get('scrollTopRestore')) || 0, // Calculated ScrollTop value to restore to

  };
};

// Function to save all settings to Local Storage from an object
const save = (settings) => {
  for (const [key, value] of Object.entries(settings)) {
    if (typeof value === 'object') {
      for (const [subKey, subValue] of Object.entries(value)) {
        // Check if subValue is a string and handle it differently
        if (typeof subValue === 'string') {
          setInLocalStorage(`${key}_${subKey}`, subValue);  // Store string as-is
        } else {
          setInLocalStorage(`${key}_${subKey}`, JSON.stringify(subValue));  // Stringify non-string types
        }
      }
    } else {
      setInLocalStorage(key, value);
    }
  }
};

// Initialize the Svelte store (scrollStore) with settings from Local Storage or default values
export const scrollStore = writable({
  ...load()
});

// Subscribe to the Svelte store (scrollStore) to save any changes to Local Storage
const unsubscribe = scrollStore.subscribe(currentSettings => {
  save(currentSettings);
});

// Function to update settings
function updateScrollSettings(newSettings) {
  scrollStore.set(newSettings);
}

// Function to manually reload the Svelte store (scrollStore) from Local Storage
function reloadScrollStore() {
  scrollStore.set(load());
}

// Export the utility functions for external use
export {
  reloadScrollStore,
  updateScrollSettings,
  setInLocalStorage,
  get,
  remove,
  load,
  save
};