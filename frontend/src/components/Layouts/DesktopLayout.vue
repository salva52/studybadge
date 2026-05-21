<template>
	<div class="flex h-screen w-screen">
		<div class="h-full">
			<AppSidebar />
		</div>
		<div class="flex-1 flex flex-col h-full overflow-auto bg-sb-bg">
			<slot />
		</div>
	</div>
</template>
<script setup>
import AppSidebar from '@/components/Sidebar/AppSidebar.vue'
</script>
