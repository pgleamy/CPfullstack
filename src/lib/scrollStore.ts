import { writable } from 'svelte/store';

// Define the interface for the store
interface Scroll {
  scrollPosition: number; // [0 - 1]
  setPosition: (position: number) => void;
}

// Function to create the store
function createScrollStore(): Scroll {
  // Create a writable store with an initial value of 0
  const { subscribe, set } = writable(0);

  // Function to set the scroll position
  function setPosition(value: number) {
    // Ensure the position is within the range [0, 1]
    const constrainedPosition = Math.max(0, Math.min(value, 1));
    set(constrainedPosition);
  }

  return {
    subscribe, // Expose the subscribe method for reactivity
    setPosition, // Expose the method to set the scroll position
  };
}

// Create the store instance
const scroll = createScrollStore();

// Export the store
export { scroll };