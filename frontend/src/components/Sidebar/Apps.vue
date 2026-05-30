<template>
	<Popover placement="right-start" trigger="hover" class="flex w-full">
		<template #target="{ togglePopover }">
			<button
				class="flex w-full items-center justify-between rounded-lg px-3 py-2 text-sm font-medium text-slate-700 dark:text-slate-300 hover:bg-indigo-50 dark:hover:bg-indigo-500/10 hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors group"
			>
				<div class="flex items-center gap-3">
					<LayoutGrid class="w-4 h-4 text-slate-400 dark:text-slate-500 group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-colors" />
					<span class="whitespace-nowrap">
						{{ __('Aplicaciones') }}
					</span>
				</div>
				<ChevronRight class="h-4 w-4 text-slate-400 dark:text-slate-500 group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-colors" />
			</button>
		</template>
		<template #body>
			<div
				class="grid grid-cols-3 justify-between mx-3 p-2 rounded-lg bg-surface-modal shadow-2xl ring-1 ring-black ring-opacity-5"
			>
				<div v-for="app in apps.data" key="name">
					<a
						:href="app.route"
						class="flex flex-col gap-1.5 rounded justify-center items-center py-2 px-3 hover:bg-surface-gray-2"
					>
						<img class="size-8" :src="app.logo" />
						<div class="text-sm text-ink-gray-7" @click="app.onClick">
							{{ app.title }}
						</div>
					</a>
				</div>
			</div>
		</template>
	</Popover>
</template>
<script setup>
import { Popover, createResource } from 'frappe-ui'
import { LayoutGrid, ChevronRight } from 'lucide-vue-next'

const apps = createResource({
	url: 'frappe.apps.get_apps',
	cache: 'apps',
	auto: true,
	transform: (data) => {
		let _apps = [
			{
				name: 'frappe',
				logo: '/assets/lms/images/desk.png',
				title: __('Escritorio'),
				route: '/desk/learning',
			},
		]
		data.map((app) => {
			if (app.name === 'lms') return
			_apps.push({
				name: app.name,
				logo: app.logo,
				title: __(app.title),
				route: app.route,
			})
		})
		return _apps
	},
})
</script>
