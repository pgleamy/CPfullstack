// headerchange.js
// stores the current page for the header background color
import { writable } from 'svelte/store';

export const activePage = writable('chatpage');
