<script lang="ts">
  import { browser } from '$app/environment';
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';

  // Flag to prevent automatic redirects
  let hasHandledNavigation = false;

  onMount(() => {
    if (browser) {
      hasHandledNavigation = true;
      
      // Clear any possibly stored redirect targets
      if (sessionStorage.getItem('redirect_target')) {
        sessionStorage.removeItem('redirect_target');
      }
    }
  });
</script>

<slot></slot> 