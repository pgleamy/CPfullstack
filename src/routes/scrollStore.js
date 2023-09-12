//@ts-nocheck

import { writable } from 'svelte/store';

function persistentStore(key, value) {
  const storedValue = localStorage.getItem(key);
  const initial = storedValue ? JSON.parse(storedValue) : value;
  const store = writable(initial);

  store.subscribe(($value) => {
    localStorage.setItem(key, JSON.stringify($value));
  });

  return store;
}

export const scrollStore = persistentStore('scrollStore', {
  gripButton: {
    position: 0, // Relative position, starts at the bottom at position 0
    color: '#008000', // Default color of dark green
    isDragging: false, // True when the grip button is being dragged
  },
  downArrow: {
    isVisible: true,  // This is always visible except when the grip button is at the bottom at position 0
    color: '#008000', // Default color of dark green
    isThrobbing: false, // only throbs if unviewed search results below grip button in "Search" mode, and if new off screen unseen llm message below grip button in "Conversation" mode
  },
  upArrow: {
    isVisible: false, // Only visible in "Search" mode
    color: '#b30000', // only visible in "Search" mode as red up arrow
    isThrobbing: false, // only throbs if unviewed search results above grip button
  },
  searchModal: {
    isOpen: false,
    query: '', // Store the search query
  },
  markingSystem: {
    hits: [], // Array of hit positions
    consolidatedHits: [], // Array of consolidated hit positions and counts
  },
  totalMessages: 0, // Total number of messages in SQLite database
});
