<template>
	<Popover placement="right-start" trigger="hover" class="flex w-full">
		<template #target="{ togglePopover }">
			<button
				class="flex w-full items-center justify-between rounded-lg px-3 py-2 text-sm font-medium text-slate-700 dark:text-slate-300 hover:bg-indigo-50 dark:hover:bg-indigo-500/10 hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors group"
			>
				<div class="flex items-center gap-3">
					<Wrench class="w-4 h-4 text-slate-400 dark:text-slate-500 group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-colors" />
					<span class="whitespace-nowrap">
						{{ __('Configuración') }}
					</span>
				</div>
				<ChevronRight class="h-4 w-4 text-slate-400 dark:text-slate-500 group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-colors" />
			</button>
		</template>
		<template #body>
			<div
				class="grid grid-cols-3 justify-between mx-3 p-2 rounded-lg bg-surface-modal shadow-2xl ring-1 ring-black ring-opacity-5"
			>
				<div key="name" class="py-1 px-2 hover:bg-surface-gray-2 rounded">
					<router-link
						:to="{
							name: 'DataImportList',
							query: {
								step: 'list',
							},
						}"
					>
						<div class="flex flex-col items-center space-y-1">
							<ArrowDownToLine
								class="size-9 text-ink-gray-7 p-2 bg-surface-gray-2 rounded-md"
							/>
							<div class="text-sm text-ink-gray-7">
								{{ __('Importar') }}
							</div>
						</div>
					</router-link>
				</div>
			</div>
		</template>
	</Popover>
</template>
<script setup lang="ts">
import { Popover } from 'frappe-ui'
import { ArrowDownToLine, Wrench, ChevronRight } from 'lucide-vue-next'
</script>
