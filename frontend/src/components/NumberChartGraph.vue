<template>
	<div class="bg-white dark:bg-gray-800 shadow-sb-soft border border-gray-100 dark:border-gray-700 rounded-2xl p-5 space-y-2 transition-all duration-300 hover:shadow-sb-card-hover hover:-translate-y-1">
		<div class="text-sm font-medium text-ink-gray-5 uppercase tracking-wider">
			{{ __(title) }}
		</div>
		<div class="flex items-center gap-x-2">
			<slot name="prefix" />
			<div class="font-bold text-ink-gray-9 text-3xl">
				{{ value }}
			</div>
			<slot name="suffix" />
		</div>
	</div>
</template>
<script setup lang="ts">
const props = defineProps<{
	title: string
	value: number | string
}>()
</script>
