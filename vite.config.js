import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [sveltekit()],

	server: {
		watch: {
			// Replace this pattern with the appropriate pattern to match the directories or files you want to ignore
			ignored: [ 
				'C:/Users/Leamy/Desktop/ChatPerfect/src-tauri/users/**',
				'C:/Users/Leamy/Desktop/ChatPerfect/src/backend/**',
			],
		},
	},

	optimizeDeps: {
        exclude: ['C:/Users/Leamy/Desktop/ChatPerfect/src-tauri/users/', 'C:/Users/Leamy/Desktop/ChatPerfect/src/backend/']
      }

});

