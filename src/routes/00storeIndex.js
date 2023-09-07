// storeIndex.js
// Centralized export for ALL stores

import chatStore from './chatStore.svelte';
import gripButtonStore from './gripButtonStore.svelte';
import arrowButtonStore from './arrowButtonStore.svelte';
import selectedGender from '$lib/settings.js';
// ... any other stores

export {
  chatStore,
  gripButtonStore,
  arrowButtonStore,
  // ... any other stores
};
