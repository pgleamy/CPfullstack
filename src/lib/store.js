import { writable } from 'svelte/store';
import Cookies from 'js-cookie';

function createCookieStore(key, startValue) {
	const storedValue = Cookies.get(key);
	const initialValue = storedValue ? storedValue : startValue;

	const store = writable(initialValue);

	store.subscribe(value => {
		Cookies.set(key, value, { expires: 365 });
	});

	return store;
}

export const selectedGender = createCookieStore('selectedGender', 'Jarvis');
