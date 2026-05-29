<template>
	<Dialog
		v-model="show"
		:options="{
			title: __('Racha de Estudio'),
		}"
	>
		<template #body-content>
			<div class="text-base">
				<div class="text-center bg-gradient-to-br from-amber-50 to-orange-50 p-6 rounded-xl border border-amber-100/50 relative overflow-hidden">
					<div class="absolute top-0 right-0 w-32 h-32 bg-amber-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-pulse"></div>
					<div class="absolute bottom-0 left-0 w-32 h-32 bg-orange-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20"></div>
					<div class="text-[48px] drop-shadow-md mb-2 relative z-10 animate-bounce">🔥</div>
					<div class="relative z-10">
						<div class="text-orange-700/80 font-medium mb-1 text-sm uppercase tracking-wide">
							{{
								streakInfo.data?.current_streak < 1
									? __('Puedes hacerlo mejor,')
									: streakInfo.data?.current_streak < 10
									? __('¡Sigue así,')
									: __('¡Eres increíble!,')
							}}
							{{ __(' tienes una racha de') }}
						</div>
						<div class="font-black text-4xl text-orange-600 drop-shadow-sm">
							{{ streakInfo.data?.current_streak }} <span class="text-2xl">{{ __('días') }}</span>
						</div>
					</div>
				</div>

				<div
					class="grid grid-cols-2 bg-slate-50 px-4 py-4 rounded-xl mt-6 border border-slate-100 shadow-inner"
				>
					<div class="space-y-1 border-e border-slate-200 me-4">
						<div class="text-slate-500 text-xs font-semibold uppercase tracking-wider">
							{{ __('Racha Actual') }}
						</div>
						<div class="font-bold text-2xl text-slate-800 flex items-baseline gap-1">
							{{ streakInfo.data?.current_streak }} <span class="text-sm font-medium text-slate-500">{{ __('días') }}</span>
						</div>
					</div>
					<div class="space-y-1 pl-2">
						<div class="text-slate-500 text-xs font-semibold uppercase tracking-wider">
							{{ __('Mejor Racha') }}
						</div>
						<div class="font-bold text-2xl text-slate-800 flex items-baseline gap-1">
							{{ streakInfo.data?.longest_streak }} <span class="text-sm font-medium text-slate-500">{{ __('días') }}</span>
						</div>
					</div>
				</div>

				<div
					class="flex gap-3 bg-indigo-50/50 text-indigo-700/80 border border-indigo-100/50 p-4 rounded-xl text-sm leading-relaxed mt-5"
				>
					<div class="text-indigo-400 mt-0.5">
						<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>
					</div>
					<div>
						{{
							__(
								'Tu racha cuenta el número de días seguidos que has estado aprendiendo (lecciones, quiz o prácticas). No te preocupes, los fines de semana no rompen tu racha.'
							)
						}}
					</div>
				</div>
			</div>
		</template>
	</Dialog>
</template>
<script setup lang="ts">
import { Dialog } from 'frappe-ui'

const show = defineModel<boolean>({
	default: false,
})

const props = defineProps<{
	streakInfo: {
		data: {
			current_streak: number
			longest_streak: number
		}
	}
}>()
</script>
