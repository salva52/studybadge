<template>
	<div>
		<header
			class="sticky top-0 z-10 flex items-center justify-between border-b bg-surface-white px-3 py-2.5 sm:px-5"
		>
			<Breadcrumbs class="h-7" :items="breadcrumbs" />
			<Button :loading="rankings.loading" @click="rankings.reload()">
				<template #prefix>
					<RefreshCw class="h-4 w-4 stroke-1.5 text-ink-gray-7" />
				</template>
				{{ __('Actualizar') }}
			</Button>
		</header>

		<div class="mx-auto flex w-full max-w-7xl flex-col gap-5 p-4 sm:p-6">
			<section
				class="overflow-hidden rounded-lg border border-outline-gray-2 bg-surface-white"
			>
				<div
					class="grid gap-5 border-b border-outline-gray-2 bg-surface-gray-1 p-5 lg:grid-cols-[1.2fr_0.8fr]"
				>
					<div class="flex flex-col justify-between gap-4">
						<div>
							<div
								class="mb-3 inline-flex w-fit items-center gap-2 rounded-full border border-outline-gray-2 bg-surface-white px-3 py-1 text-sm text-ink-gray-7"
							>
								<Coins class="h-4 w-4 stroke-1.5 text-yellow-600" />
								{{ __('Monedas StudyBadge') }}
							</div>
							<h1 class="text-3xl font-semibold text-ink-gray-9">
								{{ __('Rankings') }}
							</h1>
							<p class="mt-2 max-w-2xl text-base leading-6 text-ink-gray-7">
								{{
									__(
										'Gana monedas completando lecciones, cursos, certificados e insignias. Los primeros lugares pueden recibir premios.'
									)
								}}
							</p>
						</div>
						<div class="grid grid-cols-2 gap-3 sm:grid-cols-3">
							<div class="rounded-md bg-surface-white p-3">
								<div class="text-sm text-ink-gray-5">
									{{ __('Participantes') }}
								</div>
								<div class="mt-1 text-2xl font-semibold text-ink-gray-9">
									{{ formatNumber(rankings.data?.summary?.visible_members || 0) }}
								</div>
							</div>
							<div class="rounded-md bg-surface-white p-3">
								<div class="text-sm text-ink-gray-5">
									{{ __('Monedas totales') }}
								</div>
								<div class="mt-1 text-2xl font-semibold text-ink-gray-9">
									{{ formatNumber(rankings.data?.summary?.total_coins || 0) }}
								</div>
							</div>
							<div class="rounded-md bg-surface-white p-3">
								<div class="text-sm text-ink-gray-5">
									{{ __('Premios') }}
								</div>
								<div class="mt-1 text-2xl font-semibold text-ink-gray-9">
									Top {{ rankings.data?.summary?.top_prize_slots || 3 }}
								</div>
							</div>
						</div>
					</div>

					<div
						v-if="currentUser"
						class="rounded-lg border border-outline-gray-2 bg-surface-white p-4"
					>
						<div class="mb-4 flex items-start justify-between gap-3">
							<div class="flex items-center gap-3">
								<UserAvatar :user="currentUser" size="xl" />
								<div class="min-w-0">
									<div class="font-semibold text-ink-gray-9">
										{{ __('Tu ranking') }}
									</div>
									<div class="truncate text-sm text-ink-gray-6">
										{{ currentUser.full_name }}
									</div>
								</div>
							</div>
							<Badge v-if="currentUser.is_hidden" theme="gray">
								{{ __('Oculto') }}
							</Badge>
							<Badge v-else theme="green">
								#{{ currentUser.rank || '-' }}
							</Badge>
						</div>
						<div class="grid grid-cols-2 gap-3">
							<div class="rounded-md bg-yellow-50 p-3">
								<div class="flex items-center gap-2 text-sm text-yellow-700">
									<Coins class="h-4 w-4 stroke-1.5" />
									{{ __('Monedas') }}
								</div>
								<div class="mt-1 text-2xl font-semibold text-yellow-900">
									{{ formatNumber(currentUser.coins) }}
								</div>
							</div>
							<div class="rounded-md bg-blue-50 p-3">
								<div class="flex items-center gap-2 text-sm text-blue-700">
									<Sparkles class="h-4 w-4 stroke-1.5" />
									{{ __('Nivel') }}
								</div>
								<div class="mt-1 truncate text-lg font-semibold text-blue-900">
									{{ currentUser.level }}
								</div>
							</div>
						</div>
						<div
							v-if="currentUser.is_hidden"
							class="mt-4 flex items-start gap-2 rounded-md bg-surface-gray-2 p-3 text-sm leading-5 text-ink-gray-7"
						>
							<EyeOff class="mt-0.5 h-4 w-4 flex-shrink-0 stroke-1.5" />
							<span>
								{{
									__(
										'Tu perfil no aparece en la tabla. Puedes cambiarlo desde Editar Perfil.'
									)
								}}
							</span>
						</div>
					</div>
				</div>

				<div class="grid gap-4 p-5 md:grid-cols-3">
					<router-link
						v-for="entry in topThree"
						:key="entry.name"
						:to="profileRoute(entry)"
						class="rounded-lg border border-outline-gray-2 bg-surface-white p-4 transition hover:border-outline-gray-3"
					>
						<div class="mb-5 flex items-start justify-between gap-3">
							<div class="flex items-center gap-3">
								<div
									class="grid h-10 w-10 flex-shrink-0 place-items-center rounded-full"
									:class="podiumClass(entry.rank)"
								>
									<Medal class="h-5 w-5 stroke-1.5" />
								</div>
								<div class="min-w-0">
									<div class="truncate font-semibold text-ink-gray-9">
										{{ entry.full_name }}
									</div>
									<div class="truncate text-sm text-ink-gray-6">
										{{ entry.level }}
									</div>
								</div>
							</div>
							<div class="text-xl font-semibold text-ink-gray-9">
								#{{ entry.rank }}
							</div>
						</div>
						<div class="mb-3 flex items-end justify-between">
							<UserAvatar :user="entry" size="2xl" />
							<div class="text-end">
								<div class="text-sm text-ink-gray-5">
									{{ __('Monedas') }}
								</div>
								<div class="text-2xl font-semibold text-yellow-700">
									{{ formatNumber(entry.coins) }}
								</div>
							</div>
						</div>
						<div class="flex flex-wrap gap-2">
							<span
								v-for="highlight in entry.highlights"
								:key="highlight"
								class="rounded-full bg-surface-gray-2 px-2 py-1 text-xs text-ink-gray-7"
							>
								{{ highlight }}
							</span>
						</div>
					</router-link>
				</div>
			</section>

			<div class="grid gap-5 lg:grid-cols-[1fr_320px]">
				<section
					class="overflow-hidden rounded-lg border border-outline-gray-2 bg-surface-white"
				>
					<div
						class="flex items-center justify-between border-b border-outline-gray-2 p-4"
					>
						<div>
							<h2 class="text-lg font-semibold text-ink-gray-9">
								{{ __('Tabla de posiciones') }}
							</h2>
							<div class="text-sm text-ink-gray-6">
								{{ __('Ordenada por monedas acumuladas') }}
							</div>
						</div>
						<Trophy class="h-5 w-5 stroke-1.5 text-yellow-600" />
					</div>
					<div v-if="rankings.loading" class="p-8 text-center text-ink-gray-6">
						{{ __('Cargando rankings...') }}
					</div>
					<div
						v-else-if="!leaderboard.length"
						class="p-8 text-center text-ink-gray-6"
					>
						{{ __('Aun no hay actividad suficiente para mostrar rankings.') }}
					</div>
					<div v-else class="overflow-x-auto">
						<table class="w-full min-w-[720px]">
							<thead class="border-b border-outline-gray-2 bg-surface-gray-1">
								<tr class="text-left text-sm font-medium text-ink-gray-6">
									<th class="w-20 px-4 py-3">{{ __('Puesto') }}</th>
									<th class="px-4 py-3">{{ __('Perfil') }}</th>
									<th class="px-4 py-3">{{ __('Monedas') }}</th>
									<th class="px-4 py-3">{{ __('Ganadas por') }}</th>
								</tr>
							</thead>
							<tbody>
								<tr
									v-for="entry in leaderboard"
									:key="entry.name"
									class="border-b border-outline-gray-1 transition hover:bg-surface-gray-1"
									:class="entry.is_current_user ? 'bg-blue-50/60' : ''"
								>
									<td class="px-4 py-4">
										<div
											class="grid h-9 w-9 place-items-center rounded-full text-sm font-semibold"
											:class="podiumClass(entry.rank)"
										>
											{{ entry.rank }}
										</div>
									</td>
									<td class="px-4 py-4">
										<router-link
											:to="profileRoute(entry)"
											class="flex items-center gap-3"
										>
											<UserAvatar :user="entry" size="lg" />
											<div class="min-w-0">
												<div class="truncate font-medium text-ink-gray-9">
													{{ entry.full_name }}
												</div>
												<div class="truncate text-sm text-ink-gray-6">
													{{ entry.headline || entry.level }}
												</div>
											</div>
										</router-link>
									</td>
									<td class="px-4 py-4">
										<div class="flex items-center gap-2 font-semibold text-yellow-700">
											<Coins class="h-4 w-4 stroke-1.5" />
											{{ formatNumber(entry.coins) }}
										</div>
									</td>
									<td class="px-4 py-4">
										<div class="flex flex-wrap gap-2">
											<span
												v-for="highlight in entry.highlights"
												:key="highlight"
												class="rounded-full bg-surface-gray-2 px-2 py-1 text-xs text-ink-gray-7"
											>
												{{ highlight }}
											</span>
										</div>
									</td>
								</tr>
							</tbody>
						</table>
					</div>
				</section>

				<aside class="flex flex-col gap-5">
					<section class="rounded-lg border border-outline-gray-2 bg-surface-white p-4">
						<div class="mb-4 flex items-center gap-2">
							<Award class="h-5 w-5 stroke-1.5 text-pink-600" />
							<h2 class="font-semibold text-ink-gray-9">
								{{ __('Premios') }}
							</h2>
						</div>
						<div class="space-y-3">
							<div
								v-for="reward in rankings.data?.rewards || []"
								:key="reward.place"
								class="rounded-md bg-surface-gray-1 p-3"
							>
								<div class="font-medium text-ink-gray-9">
									#{{ reward.place }} {{ reward.title }}
								</div>
								<div class="mt-1 text-sm leading-5 text-ink-gray-6">
									{{ reward.description }}
								</div>
							</div>
						</div>
					</section>

					<section class="rounded-lg border border-outline-gray-2 bg-surface-white p-4">
						<div class="mb-4 flex items-center gap-2">
							<BookOpen class="h-5 w-5 stroke-1.5 text-green-600" />
							<h2 class="font-semibold text-ink-gray-9">
								{{ __('Como ganar monedas') }}
							</h2>
						</div>
						<div class="space-y-3">
							<div
								v-for="rule in rankings.data?.rules || []"
								:key="rule.label"
								class="flex items-center justify-between gap-3"
							>
								<span class="text-sm text-ink-gray-7">{{ rule.label }}</span>
								<span
									class="inline-flex items-center gap-1 rounded-full bg-yellow-50 px-2 py-1 text-sm font-medium text-yellow-800"
								>
									<Coins class="h-3.5 w-3.5 stroke-1.5" />
									{{ rule.coins }}
								</span>
							</div>
						</div>
					</section>
				</aside>
			</div>
		</div>
	</div>
</template>

<script setup>
import {
	Badge,
	Breadcrumbs,
	Button,
	createResource,
	usePageMeta,
} from 'frappe-ui'
import { computed } from 'vue'
import {
	Award,
	BookOpen,
	Coins,
	EyeOff,
	Medal,
	RefreshCw,
	Sparkles,
	Trophy,
} from 'lucide-vue-next'
import { sessionStore } from '@/stores/session'
import { formatNumber } from '@/utils'
import UserAvatar from '@/components/UserAvatar.vue'

const { brand } = sessionStore()

const rankings = createResource({
	url: 'lms.lms.api.get_rankings',
	params: {
		limit: 50,
	},
	auto: true,
})

const breadcrumbs = computed(() => [
	{
		label: __('Rankings'),
		route: { name: 'Rankings' },
	},
])

const leaderboard = computed(() => rankings.data?.leaderboard || [])
const currentUser = computed(() => rankings.data?.current_user)
const topThree = computed(() => leaderboard.value.slice(0, 3))

const profileRoute = (entry) => {
	return {
		name: 'Profile',
		params: {
			username: entry.username || entry.name,
		},
	}
}

const podiumClass = (rank) => {
	if (rank === 1) return 'bg-yellow-100 text-yellow-800'
	if (rank === 2) return 'bg-blue-100 text-blue-800'
	if (rank === 3) return 'bg-pink-100 text-pink-800'
	return 'bg-surface-gray-2 text-ink-gray-7'
}

usePageMeta(() => {
	return {
		title: __('Rankings'),
		icon: brand.favicon,
	}
})
</script>
