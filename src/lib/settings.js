// $lib/settings.js
// @ts-nocheck

import { writable } from 'svelte/store';

// Function to set a setting in Local Storage
const setSetting = (key, value) => {
  localStorage.setItem(key, value);
};

// Function to get a setting from Local Storage
const getSetting = (key) => {
  return localStorage.getItem(key);
};

// Function to remove a setting from Local Storage
const removeSetting = (key) => {
  localStorage.removeItem(key);
};

// Function to load all settings into an object
const loadSettings = () => {
  return {
    Gender: getSetting('Gender') || "Iris", // Default value
    Role: getSetting('Role') || "Write", // Default value
    CodingModel: getSetting('CodingModel') || "GPT4.0", // Default value
    WritingModel: getSetting('WritingModel') || "GPT4.0", // Default value
    TalkingModel: getSetting('TalkingModel') || "GPT4.0", // Default value
  };
};

// Function to save all settings from an object
const saveSettings = (settings) => {
  for (const [key, value] of Object.entries(settings)) {
    setSetting(key, value);
  }
};

// Initialize the settings store with either saved settings or default values
export const settings = writable({
	...{
	  Gender: 'Argus',
	  Role: 'write',
	  CodingModel: 'GPT3.5',
	  WritingModel: 'GPT3.5',
	  TalkingModel: 'GPT3.5'
	},
	...loadSettings()
  });
  

// Subscribe to the settings store to save changes to Local Storage
const unsubscribe = settings.subscribe(currentSettings => {
  saveSettings(currentSettings);
});

// Function to update settings
export function updateSettings(newSettings) {
  settings.set(newSettings);
}

// Export the utility functions for external use
export {
  setSetting,
  getSetting,
  removeSetting,
  loadSettings,
  saveSettings
};

  
