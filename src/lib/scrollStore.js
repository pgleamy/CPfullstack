// $lib/scrollStore.js
// @ts-nocheck

import { writable } from 'svelte/store';

// Function to set a setting in Local Storage
const setInLocalStorage = (key, value) => {
  localStorage.setItem(key, value);
};

// Function to get a setting from Local Storage
const get = (key) => {
  return localStorage.getItem(key) || null;
};

// Function to remove a setting from Local Storage
const remove = (key) => {
  localStorage.removeItem(key);
};

// Function to load all settings into an object
const load = () => {
  return {
    gripPosition: parseFloat(get('gripPosition')) || 0,
    downArrow: {
      isVisible: JSON.parse(get('downArrow_isVisible')) || false,
      isThrobbing: JSON.parse(get('downArrow_isThrobbing')) || false,
    },
    upArrow: {
      isVisible: JSON.parse(get('upArrow_isVisible')) || true,
      isThrobbing: JSON.parse(get('upArrow_isThrobbing')) || false,
    },
    searchModal: {
      isOpen: JSON.parse(get('searchModal_isOpen')) || false,
      query: get('searchModal_query') || "",
    },
    markingSystem: {
      hits: JSON.parse(get('markingSystem_hits')) || [],
      consolidatedHits: JSON.parse(get('markingSystem_consolidatedHits')) || [],
    },
    totalMessages: parseInt(get('totalMessages')) || 0,
  };
};

// Function to save all settings from an object
const save = (settings) => {
  for (const [key, value] of Object.entries(settings)) {
    if (typeof value === 'object') {
      for (const [subKey, subValue] of Object.entries(value)) {
        setInLocalStorage(`${key}_${subKey}`, JSON.stringify(subValue));
      }
    } else {
      setInLocalStorage(key, value);
    }
  }
};

// Initialize the settings store with either saved settings or default values
export const scrollStore = writable({
  ...load()
});

// Subscribe to the settings store to save changes to Local Storage
const unsubscribe = scrollStore.subscribe(currentSettings => {
  save(currentSettings);
});

// Function to update settings
export function updateScrollSettings(newSettings) {
  scrollStore.set(newSettings);
}

// Export the utility functions for external use
export {
  setInLocalStorage,
  get,
  remove,
  load,
  save
};