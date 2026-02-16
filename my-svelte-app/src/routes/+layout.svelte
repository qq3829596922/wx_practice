<script>import "../app.css";
import favicon from '$lib/assets/favicon.svg';
import { Toaster} from 'svelte-sonner';                                                              
let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href="{favicon}" />
</svelte:head>
<Toaster 
position="top-center"                                                                               
richColors                                                                                          
duration={3000}
/> 

{@render children()}

                                                                                            
<div>
	hello
	dasd
</div>