<script>
    import ConversationContainer from './conversationcontainer.svelte'; 
    import UserInput from './userinput.svelte';
    import { writable } from 'svelte/store';
    import { fade } from "svelte/transition";
    import ScrollSearch from './scrollsearch.svelte';
    import { activePage } from '$lib/headerchange.js';
    import { get } from '$lib/scrollStore.js';
    $activePage = 'chatPage';

    let CurrentPage; // Reference to the current page component




    import { onMount } from 'svelte';
    
    onMount(() => {

        /*
  const element = document.querySelector('.contentWrapper');
    // Log the element to the console
    console.log(element);
  
  if (element) {
    console.log(element);
    element.addEventListener('animationstart', function(event) {
      if (event.animationName === 'fadeOut') {
        console.log('FadeOut animation started');
      }
    });
    
    element.addEventListener('animationend', function(event) {
      if (event.animationName === 'fadeOut') {
        console.log('FadeOut animation ended');
      }
    });
  } else {
    console.log('Element not found');
  }
  */
  
  restartAnimation();
});




  let animate = true;
  function restartAnimation() {
    console.log('Restarting animation');
    animate = true;
    // Force reflow to reset the animation
    document.querySelector('.contentWrapper').offsetWidth;
    animate = true;
  }




    // Function to switch to a new page with fade transition
    function switchPage(pageComponent) {
        CurrentPage = pageComponent; // Update to the new page component
    }

    const initialInputs = JSON.parse(localStorage.getItem('inputs') || '[""]');
    const inputs = writable(initialInputs);

    inputs.subscribe(value => {
        localStorage.setItem('inputs', JSON.stringify(value));
    });

    function handleInput(value, index) {
        if (index === $inputs.length - 1 && value) {
            inputs.update(items => [...items, '']);
        }
        $inputs[index] = value;
    }

    // Places the lmm character's face dimly in the background, reactive to gender
    let gender = "";
    gender = get('Gender');
    let face = "";
    let styleString = "";
    let fadeOut = 4000;
    function updateFace() {
        if (gender === "Iris") {
            console.log("I'm Iris. Who's there?");
            return "url('src/lib/images/FEMALE.png')";
        } else {
            console.log("I'm Argus. Who's there?");
            return "url('src/lib/images/MALE.png')";
        }
    }
    $: {
        console.log("Current gender: ", gender);
        face = updateFace();
        if (gender === "Iris") {
            //console.log("I'm Iris. Who's there?");
            face = "url('src/lib/images/FEMALE.png')";
            //console.log("face: ", face);
            styleString = `
        .contentWrapper::before {
            background-image: url('src/lib/images/FEMALE.png');
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-size: 100% 100%; /* Cover the entire element */
            background-repeat: no-repeat;  /* Do not repeat the image */
            background-position: center;  /* Center the image */
            opacity: 1;   /* Initial opacity */
            z-index: -1;  /* Place it behind the content */
            background-position: 50px -90px;
            animation: fadeOut ${fadeOut / 1000}s cubic-bezier(1, -0.47, 0.73, 1.24) forwards !important;
        }
        `;
        console.log("styleString: ", styleString);  // Log the style string
        } else if (gender === "Argus") {
            //console.log("I'm Argus. Who's there?");
            face = "url('src/lib/images/MALE.png')";
            //console.log("face: ", face);
            styleString = `
        .contentWrapper::before {
            background-image: url('src/lib/images/MALE.png');
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-size: 100% 100%; /* Cover the entire element */
            background-repeat: no-repeat;  /* Do not repeat the image */
            background-position: center;  /* Center the image */
            opacity: 1;   /* Initial opacity */
            z-index: -1;  /* Place it behind the content */
            background-position: 90px -55px;
            animation: fadeOut ${fadeOut / 1000}s cubic-bezier(1, -0.47, 0.73, 1.24) forwards !important;
        }
        `;
        //console.log("styleString: ", styleString);  // Log the style string
        }
    }

</script>



<!-- Injects the correct character's face style tag into the DOM -->
{@html `<style>${styleString}</style>`}
 <!-- For testing purposes only   <button on:click={restartAnimation} >Restart Animation</button>     -->
<div class={`contentWrapper ${gender === 'Iris' ? 'Iris' : 'Argus'}`}  id='flex' >

    <section class="chatWindow">
        <div transition:fade="{{ duration: 100, delay: 30 }}">  
            <ConversationContainer />
        </div>
    </section>
    <div class="scrollSearchWrapper" transition:fade="{{ duration: 100, delay: 30 }}">
        <ScrollSearch />
    </div>

</div>

<style>


    .contentWrapper {
        position: relative;  /* Set position to relative for the pseudo-element */
        justify-content: flex-start;
        overflow: auto;
        height: 100vh;
        flex-grow: 1;
    }


    
    .contentWrapper.Iris::before {
            background-image: url('src/lib/images/FEMALE.png');
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-size: 100% 100%;
            background-repeat: no-repeat;  
            background-position: center;  
            opacity: 1;  
            z-index: -1;  
            background-position: 90px -55px;
            animation: fadeOut 2s cubic-bezier(1, 1, 0.73, 1.24) forwards !important;
        }

        .contentWrapper.Argus::before {
            background-image: url('src/lib/images/MALE.png');
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-size: 100% 100%;
            background-repeat: no-repeat;  
            background-position: center;  
            opacity: 1;  
            z-index: -1;  
            background-position: 90px -55px;
            animation: fadeOut 2s cubic-bezier(1, 1, 0.73, 1.24) forwards !important;
        }
        


    
    .chatWindow {
        flex-grow: 1;
    }
    .scrollSearchWrapper {
        flex-shrink: 0;
        margin-left: 10px;
        display: inline-flex;
        width: auto;
    }
    #flex{
        display: flex;
    }


    @keyframes fadeOut {
        0% {
            opacity: 1;  
        }     
        100% {
            opacity: 0.01; 
        }
    }


    /*
    button {
        z-index: 
        position: relative; 
    }
    */

</style>

