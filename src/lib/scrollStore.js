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
    //upArrow: {
      //isVisible: get('upArrow_isVisible') !== null ? JSON.parse(get('upArrow_isVisible')) : false
    //},
    //searchModal: {
      //isOpen: get('searchModal_isOpen') !== null ? JSON.parse(get('searchModal_isOpen')) : false,
      //query: get('searchModal_query') || "",
    //},
    //markingSystem: {
      //hits: get('markingSystem_hits') !== null ? JSON.parse(get('markingSystem_hits')) : [],
      //consolidatedHits: get('markingSystem_consolidatedHits') !== null ? JSON.parse(get('markingSystem_consolidatedHits')) : [],
    //},
    totalMessages: parseInt(get('totalMessages')) || 0,

    targetMessage: parseInt(get('targetMessage')) || 0, // The target message of the fetchConversationSlice function

    dragSpeedUpDown: parseFloat(get('dragSpeedUpDown')) || 0, // Elastic grip scroll speed. Defaults to 0 to signify 0 drag velocity, otherwise is a positive number for up and a negative number for down

    //userInputComponentHeight: parseInt(get('userInputComponentHeight')) || 0, // Height of the user input component elements in pixels

    targetMessagesPixelHeight: parseInt(get('targetMessagesPixelHeight')) || 0, // Height of the conversation-container contents in pixels

    unsentPrompt: get('unsentPrompt') || "", // The unsent prompt contents
    unsentPromptQUILL: get('unsentPromptQUILL') || "", // The unsent prompt conten

    //fetchedMessageCount: parseInt(get('fetchedMessageCount')) || 0, // The number of individual messages fetched from the server in one item group
    messagesItemHeight: parseInt(get('messagesItemHeight')) || 0, // The height of the fetched item group of messages in pixels
    
    firstVisibleMessageNum: parseInt(get('firstVisibleMessageNum')) || 0,
    lastVisibleMessageNum: parseInt(get('lastVisibleMessageNum')) || 0,
    firstConversationArrayMessageNum: parseInt(get('firstConversationArrayMessageNum')) || 0,
    lastConversationArrayMessageNum: parseInt(get('lastConversationArrayMessageNum')) || 0,
    targetMessage: parseInt(get('targetMessage')) || 0,

    Role: get('Role') || "Write",

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

// Subscribe to the Svelte store (scrollStore) to save any changes to Local Storage on any changes to the store variables
const unsubscribe = scrollStore.subscribe(currentSettings => {
  // save all settings to Local Storage
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
  save,
};