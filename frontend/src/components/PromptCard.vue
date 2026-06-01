<template>
	<article class="prompt-card group flex flex-col justify-between min-h-[260px] bg-white rounded-2xl border border-gray-200 shadow-sm hover:shadow-lg hover:-translate-y-1 transition-all duration-300 overflow-hidden relative">
		<div class="p-5 flex-1 flex flex-col">
			<!-- Header -->
			<div class="flex items-start justify-between mb-4">
				<div class="flex items-center gap-2">
					<span class="text-[10px] font-bold px-2 py-0.5 rounded bg-blue-50 text-[#0b82e6] uppercase tracking-wider border border-blue-100/50">
						{{ prompt.category }}
					</span>
				</div>
				<!-- Badge -->
				<span v-if="prompt.badge" :class="[ 
					'text-[10px] font-black uppercase tracking-wider px-2 py-0.5 rounded-full border',
					prompt.badge === 'Plus' ? 'bg-amber-50 text-amber-600 border-amber-200' : 
					prompt.badge === 'Gratis' ? 'bg-emerald-50 text-emerald-600 border-emerald-200' :
					prompt.badge === 'Nuevo' ? 'bg-indigo-50 text-indigo-600 border-indigo-200' :
					'bg-gray-50 text-gray-600 border-gray-200'
				]">
					<Crown v-if="prompt.badge === 'Plus'" class="size-3 inline-block -mt-0.5 mr-0.5" />
					{{ prompt.badge }}
				</span>
			</div>

			<!-- Content -->
			<h3 class="text-base font-black text-gray-900 mb-2 leading-tight group-hover:text-[#0b82e6] transition-colors line-clamp-2" :title="prompt.title">
				<Crown v-if="prompt.isPremium" class="size-4 inline text-amber-500 mr-1 align-text-top" />
				{{ prompt.title }}
			</h3>
			<p class="text-sm text-gray-500 mb-4 line-clamp-3 leading-relaxed">{{ prompt.description }}</p>

			<!-- Variables -->
			<div class="mt-auto pt-4 border-t border-gray-100">
				<div class="flex items-center justify-between mb-3 text-xs text-gray-400 font-semibold">
					<span class="flex items-center gap-1 text-gray-500"><Clock class="size-3.5 text-gray-400" /> {{ prompt.timeSaved }}</span>
				</div>
				<div class="flex flex-wrap gap-1.5 mb-2" :class="{ 'select-none': prompt.isPremium && !isPlus }">
					<span 
						v-for="variable in prompt.variables" 
						:key="variable" 
						class="text-[10px] font-mono font-medium px-2 py-0.5 bg-gray-50 text-gray-600 rounded border border-gray-200 transition-all"
						:class="{ 'blur-[1.5px] opacity-50': prompt.isPremium && !isPlus }"
					>
						{{ '{' + '{' + variable + '}' + '}' }}
					</span>
				</div>
			</div>
		</div>

		<!-- Actions -->
		<div class="flex border-t border-gray-100 bg-gray-50/50 mt-auto">
			<button @click="$emit('view', prompt)" class="flex-1 py-3 text-sm font-bold text-gray-600 hover:text-gray-900 hover:bg-gray-100 transition-colors flex justify-center items-center gap-1.5">
				{{ __('Ver completo') }}
			</button>
			<div class="w-px bg-gray-200"></div>
			<button v-if="!prompt.isPremium || isPlus" @click="$emit('copy', prompt)" class="flex-1 py-3 text-sm font-bold text-[#0b82e6] hover:bg-blue-50 transition-colors flex justify-center items-center gap-1.5">
				<Copy class="size-4" /> {{ __('Copiar') }}
			</button>
			<router-link v-else :to="{ name: 'Plus' }" class="flex-1 py-3 text-sm font-bold text-amber-600 hover:bg-amber-50 transition-colors flex justify-center items-center gap-1.5">
				<Crown class="size-4" /> {{ __('Plus') }}
			</router-link>
		</div>
	</article>
</template>

<script setup>
import { Clock, Copy, Crown } from 'lucide-vue-next'
import { computed } from 'vue'
import { usersStore } from '@/stores/user'

defineProps({
	prompt: {
		type: Object,
		required: true
	}
})

defineEmits(['view', 'copy'])

const { userResource } = usersStore()
const isPlus = computed(() => !!userResource.data?.is_plus)
</script>

<style scoped>
:root[data-theme="dark"] .prompt-card {
	background-color: #1e293b;
	border-color: #334155;
}
:root[data-theme="dark"] .prompt-card h3 { color: #f8fafc; }
:root[data-theme="dark"] .prompt-card p { color: #94a3b8; }
:root[data-theme="dark"] .prompt-card .bg-blue-50 { background-color: rgba(30, 58, 138, 0.3); color: #93c5fd; }
:root[data-theme="dark"] .prompt-card .bg-gray-50 { background-color: #0f172a; border-color: #334155; }
:root[data-theme="dark"] .prompt-card .border-t { border-color: #334155; }
</style>
