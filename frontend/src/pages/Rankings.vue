<template>
	<div class="rankings-page">
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

		<div class="mx-auto flex w-full max-w-7xl flex-col gap-6 p-4 sm:p-6">
			<!-- ═══════════ HERO SECTION ═══════════ -->
			<section class="rankings-hero">
				<div class="hero-decoration">
					<div class="hero-orb hero-orb--1"></div>
					<div class="hero-orb hero-orb--2"></div>
					<div class="hero-orb hero-orb--3"></div>
				</div>

				<div class="hero-content">
					<div class="hero-text">
						<div class="hero-badge">
							<Coins class="h-4 w-4 stroke-1.5" />
							<span>{{ __('Monedas StudyBadge') }}</span>
						</div>
						<h1 class="hero-title">{{ __('Rankings') }}</h1>
						<p class="hero-subtitle">
							{{
								__(
									'Gana monedas completando lecciones, cursos, certificados e insignias. Los primeros lugares pueden recibir premios.'
								)
							}}
						</p>
					</div>

					<div class="hero-stats">
						<div class="stat-card">
							<div class="stat-icon stat-icon--users">
								<Users class="h-5 w-5 stroke-1.5" />
							</div>
							<div class="stat-value">
								{{ formatNumber(rankings.data?.summary?.visible_members || 0) }}
							</div>
							<div class="stat-label">{{ __('Participantes') }}</div>
						</div>
						<div class="stat-card">
							<div class="stat-icon stat-icon--coins">
								<Coins class="h-5 w-5 stroke-1.5" />
							</div>
							<div class="stat-value">
								{{ formatNumber(rankings.data?.summary?.total_coins || 0) }}
							</div>
							<div class="stat-label">{{ __('Monedas totales') }}</div>
						</div>
						<div class="stat-card">
							<div class="stat-icon stat-icon--trophy">
								<Trophy class="h-5 w-5 stroke-1.5" />
							</div>
							<div class="stat-value">
								Top {{ rankings.data?.summary?.top_prize_slots || 3 }}
							</div>
							<div class="stat-label">{{ __('Premios') }}</div>
						</div>
					</div>
				</div>
			</section>

			<!-- ═══════════ YOUR RANKING CARD ═══════════ -->
			<section v-if="currentUser" class="my-ranking-card">
				<div class="my-ranking-header">
					<div class="my-ranking-user">
						<UserAvatar :user="currentUser" size="xl" />
						<div class="min-w-0">
							<div class="my-ranking-name">{{ currentUser.full_name }}</div>
							<div class="my-ranking-label">{{ __('Tu ranking') }}</div>
						</div>
					</div>
					<div v-if="currentUser.is_hidden" class="rank-badge rank-badge--hidden">
						<EyeOff class="h-3.5 w-3.5 stroke-1.5" />
						{{ __('Oculto') }}
					</div>
					<div v-else class="rank-badge rank-badge--active">
						#{{ currentUser.rank || '-' }}
					</div>
				</div>

				<div class="my-ranking-stats">
					<div class="my-stat my-stat--coins">
						<Coins class="h-5 w-5 stroke-1.5" />
						<div class="my-stat-data">
							<span class="my-stat-number">{{ formatNumber(currentUser.coins) }}</span>
							<span class="my-stat-label">{{ __('Monedas') }}</span>
						</div>
					</div>
					<div class="my-ranking-divider"></div>
					<div class="my-stat my-stat--level">
						<Sparkles class="h-5 w-5 stroke-1.5" />
						<div class="my-stat-data">
							<span class="my-stat-number">{{ currentUser.level }}</span>
							<span class="my-stat-label">{{ __('Nivel') }}</span>
						</div>
					</div>
				</div>

				<div
					v-if="currentUser.is_hidden"
					class="my-ranking-notice"
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
			</section>

			<!-- ═══════════ PODIUM TOP 3 ═══════════ -->
			<section v-if="topThree.length" class="podium-section">
				<div class="podium-title-bar">
					<Crown class="h-5 w-5 stroke-1.5" />
					<h2>{{ __('Top 3') }}</h2>
				</div>
				<div class="podium-grid">
					<router-link
						v-for="(entry, i) in podiumOrder"
						:key="entry.name"
						:to="profileRoute(entry)"
						class="podium-card"
						:class="[`podium-card--rank-${entry.rank}`, { 'podium-card--center': entry.rank === 1 }]"
					>
						<div class="podium-rank-circle" :class="`podium-rank--${entry.rank}`">
							<span v-if="entry.rank === 1">👑</span>
							<span v-else>{{ entry.rank }}</span>
						</div>
						<div class="podium-avatar-wrap">
							<div class="podium-avatar-ring" :class="`ring--rank-${entry.rank}`">
								<UserAvatar :user="entry" size="2xl" />
							</div>
						</div>
						<div class="podium-name">{{ entry.full_name }}</div>
						<div class="podium-level">{{ entry.level }}</div>
						<div class="podium-coins">
							<Coins class="h-4 w-4 stroke-1.5" />
							<span>{{ formatNumber(entry.coins) }}</span>
						</div>
						<div v-if="entry.highlights?.length" class="podium-highlights">
							<span
								v-for="highlight in entry.highlights.slice(0, 2)"
								:key="highlight"
								class="podium-tag"
							>
								{{ highlight }}
							</span>
						</div>
					</router-link>
				</div>
			</section>

			<!-- ═══════════ MAIN CONTENT GRID ═══════════ -->
			<div class="grid gap-6 lg:grid-cols-[1fr_340px]">
				<!-- LEADERBOARD TABLE -->
				<section class="leaderboard-section">
					<div class="leaderboard-header">
						<div>
							<h2 class="leaderboard-title">
								{{ __('Tabla de posiciones') }}
							</h2>
							<div class="leaderboard-subtitle">
								{{ __('Ordenada por monedas acumuladas') }}
							</div>
						</div>
						<div class="leaderboard-icon">
							<Trophy class="h-5 w-5 stroke-1.5" />
						</div>
					</div>

					<div v-if="rankings.loading" class="leaderboard-empty">
						<div class="loading-spinner"></div>
						<span>{{ __('Cargando rankings...') }}</span>
					</div>
					<div
						v-else-if="!leaderboard.length"
						class="leaderboard-empty"
					>
						<Trophy class="h-8 w-8 stroke-1 text-ink-gray-4" />
						<span>{{ __('Aun no hay actividad suficiente para mostrar rankings.') }}</span>
					</div>
					<div v-else class="overflow-x-auto">
						<table class="leaderboard-table">
							<thead>
								<tr>
									<th class="w-20">{{ __('Puesto') }}</th>
									<th>{{ __('Perfil') }}</th>
									<th>{{ __('Monedas') }}</th>
									<th>{{ __('Ganadas por') }}</th>
								</tr>
							</thead>
							<tbody>
								<tr
									v-for="entry in leaderboard"
									:key="entry.name"
									class="leaderboard-row"
									:class="{
										'leaderboard-row--self': entry.is_current_user,
										'leaderboard-row--top': entry.rank <= 3,
									}"
								>
									<td>
										<div
											class="rank-number"
											:class="rankClass(entry.rank)"
										>
											<Medal v-if="entry.rank <= 3" class="h-3.5 w-3.5 stroke-1.5" />
											<span v-else>{{ entry.rank }}</span>
										</div>
									</td>
									<td>
										<router-link
											:to="profileRoute(entry)"
											class="profile-cell"
										>
											<UserAvatar :user="entry" size="lg" />
											<div class="min-w-0">
												<div class="profile-name">
													{{ entry.full_name }}
												</div>
												<div class="profile-headline">
													{{ entry.headline || entry.level }}
												</div>
											</div>
										</router-link>
									</td>
									<td>
										<div class="coins-cell">
											<Coins class="h-4 w-4 stroke-1.5" />
											{{ formatNumber(entry.coins) }}
										</div>
									</td>
									<td>
										<div class="highlights-cell">
											<span
												v-for="highlight in entry.highlights"
												:key="highlight"
												class="highlight-tag"
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

				<!-- SIDEBAR -->
				<aside class="flex flex-col gap-6">
					<!-- PREMIOS -->
					<section class="sidebar-card">
						<div class="sidebar-card-header">
							<div class="sidebar-icon sidebar-icon--pink">
								<Award class="h-4 w-4 stroke-1.5" />
							</div>
							<h2 class="sidebar-title">{{ __('Premios') }}</h2>
						</div>
						<div class="rewards-list">
							<div
								v-for="(reward, i) in rankings.data?.rewards || []"
								:key="reward.place"
								class="reward-item"
							>
								<div class="reward-place" :class="`reward-place--${i + 1}`">
									#{{ reward.place }}
								</div>
								<div class="reward-info">
									<div class="reward-title">{{ reward.title }}</div>
									<div class="reward-desc">{{ reward.description }}</div>
								</div>
							</div>
						</div>
					</section>

					<!-- COMO GANAR MONEDAS -->
					<section class="sidebar-card">
						<div class="sidebar-card-header">
							<div class="sidebar-icon sidebar-icon--green">
								<BookOpen class="h-4 w-4 stroke-1.5" />
							</div>
							<h2 class="sidebar-title">{{ __('Como ganar monedas') }}</h2>
						</div>
						<div class="rules-list">
							<div
								v-for="rule in rankings.data?.rules || []"
								:key="rule.label"
								class="rule-item"
							>
								<span class="rule-label">{{ rule.label }}</span>
								<span class="rule-coins">
									<Coins class="h-3.5 w-3.5 stroke-1.5" />
									+{{ rule.coins }}
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
	Crown,
	EyeOff,
	Medal,
	RefreshCw,
	Sparkles,
	Trophy,
	Users,
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

/* Reorder for podium layout: 2nd, 1st, 3rd */
const podiumOrder = computed(() => {
	const t = topThree.value
	if (t.length < 3) return t
	return [t[1], t[0], t[2]]
})

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

const rankClass = (rank) => {
	if (rank === 1) return 'rank-number--gold'
	if (rank === 2) return 'rank-number--silver'
	if (rank === 3) return 'rank-number--bronze'
	return 'rank-number--default'
}

usePageMeta(() => {
	return {
		title: __('Rankings'),
		icon: brand.favicon,
	}
})
</script>

<style scoped>
/* ─── VARIABLES ─── */
:root {
	--gold: #f59e0b;
	--gold-light: #fef3c7;
	--gold-dark: #92400e;
	--silver: #94a3b8;
	--silver-light: #e2e8f0;
	--silver-dark: #475569;
	--bronze: #f97316;
	--bronze-light: #ffedd5;
	--bronze-dark: #9a3412;
}

/* ─── HERO SECTION ─── */
.rankings-hero {
	position: relative;
	overflow: hidden;
	border-radius: 16px;
	background: linear-gradient(135deg, #1e1b4b 0%, #312e81 40%, #4338ca 100%);
	padding: 2rem;
	color: white;
}

.hero-decoration {
	position: absolute;
	inset: 0;
	pointer-events: none;
	overflow: hidden;
}

.hero-orb {
	position: absolute;
	border-radius: 50%;
	filter: blur(60px);
	opacity: 0.3;
}
.hero-orb--1 {
	top: -40px;
	right: -20px;
	width: 200px;
	height: 200px;
	background: #f59e0b;
	animation: float 8s ease-in-out infinite;
}
.hero-orb--2 {
	bottom: -60px;
	left: 10%;
	width: 180px;
	height: 180px;
	background: #8b5cf6;
	animation: float 10s ease-in-out infinite reverse;
}
.hero-orb--3 {
	top: 30%;
	right: 30%;
	width: 100px;
	height: 100px;
	background: #ec4899;
	animation: float 6s ease-in-out infinite 1s;
}

@keyframes float {
	0%, 100% { transform: translateY(0) scale(1); }
	50% { transform: translateY(-20px) scale(1.05); }
}

.hero-content {
	position: relative;
	z-index: 1;
	display: grid;
	gap: 2rem;
}
@media (min-width: 1024px) {
	.hero-content {
		grid-template-columns: 1.2fr 0.8fr;
	}
}

.hero-text {
	display: flex;
	flex-direction: column;
	justify-content: center;
	gap: 0.75rem;
}

.hero-badge {
	display: inline-flex;
	align-items: center;
	gap: 0.5rem;
	width: fit-content;
	padding: 0.35rem 0.85rem;
	border-radius: 9999px;
	background: rgba(255, 255, 255, 0.12);
	backdrop-filter: blur(8px);
	border: 1px solid rgba(255, 255, 255, 0.15);
	font-size: 0.8rem;
	font-weight: 500;
	color: #fde68a;
}

.hero-title {
	font-size: 2.25rem;
	font-weight: 800;
	letter-spacing: -0.025em;
	line-height: 1.1;
	background: linear-gradient(135deg, #ffffff 0%, #e0e7ff 100%);
	-webkit-background-clip: text;
	-webkit-text-fill-color: transparent;
	background-clip: text;
}

.hero-subtitle {
	font-size: 1rem;
	line-height: 1.6;
	color: rgba(199, 210, 254, 0.85);
	max-width: 480px;
}

.hero-stats {
	display: grid;
	grid-template-columns: repeat(3, 1fr);
	gap: 0.75rem;
	align-self: center;
}
@media (max-width: 639px) {
	.hero-stats {
		grid-template-columns: repeat(2, 1fr);
	}
}

.stat-card {
	display: flex;
	flex-direction: column;
	align-items: center;
	gap: 0.5rem;
	padding: 1.25rem 0.75rem;
	border-radius: 12px;
	background: rgba(255, 255, 255, 0.08);
	backdrop-filter: blur(12px);
	border: 1px solid rgba(255, 255, 255, 0.1);
	text-align: center;
	transition: transform 0.2s ease, background 0.2s ease;
}
.stat-card:hover {
	transform: translateY(-2px);
	background: rgba(255, 255, 255, 0.12);
}

.stat-icon {
	display: grid;
	place-items: center;
	width: 36px;
	height: 36px;
	border-radius: 10px;
}
.stat-icon--users { background: rgba(99, 102, 241, 0.35); color: #c7d2fe; }
.stat-icon--coins { background: rgba(245, 158, 11, 0.35); color: #fde68a; }
.stat-icon--trophy { background: rgba(236, 72, 153, 0.35); color: #fbcfe8; }

.stat-value {
	font-size: 1.5rem;
	font-weight: 700;
	color: white;
}

.stat-label {
	font-size: 0.75rem;
	color: rgba(199, 210, 254, 0.7);
	text-transform: uppercase;
	letter-spacing: 0.05em;
	font-weight: 500;
}

/* ─── MY RANKING CARD ─── */
.my-ranking-card {
	border-radius: 14px;
	border: 1px solid var(--outline-gray-2, #e5e7eb);
	background: var(--surface-white, #fff);
	padding: 1.25rem;
	display: flex;
	flex-direction: column;
	gap: 1rem;
	transition: box-shadow 0.3s ease;
}
.my-ranking-card:hover {
	box-shadow: 0 4px 24px rgba(0, 0, 0, 0.06);
}

.my-ranking-header {
	display: flex;
	align-items: center;
	justify-content: space-between;
	gap: 1rem;
}

.my-ranking-user {
	display: flex;
	align-items: center;
	gap: 0.75rem;
	min-width: 0;
}

.my-ranking-name {
	font-weight: 600;
	color: var(--ink-gray-9, #111827);
	font-size: 1rem;
}
.my-ranking-label {
	font-size: 0.8rem;
	color: var(--ink-gray-5, #9ca3af);
}

.rank-badge {
	display: inline-flex;
	align-items: center;
	gap: 0.375rem;
	padding: 0.375rem 0.85rem;
	border-radius: 9999px;
	font-weight: 700;
	font-size: 0.875rem;
}
.rank-badge--active {
	background: linear-gradient(135deg, #ecfdf5, #d1fae5);
	color: #065f46;
	border: 1px solid #a7f3d0;
}
.rank-badge--hidden {
	background: #f3f4f6;
	color: #6b7280;
	border: 1px solid #e5e7eb;
}

.my-ranking-stats {
	display: flex;
	align-items: center;
	gap: 1.5rem;
	padding: 0.75rem 1rem;
	border-radius: 10px;
	background: var(--surface-gray-1, #f9fafb);
}
.my-ranking-divider {
	width: 1px;
	height: 28px;
	background: var(--outline-gray-2, #e5e7eb);
}

.my-stat {
	display: flex;
	align-items: center;
	gap: 0.625rem;
}
.my-stat--coins { color: #d97706; }
.my-stat--level { color: #2563eb; }

.my-stat-data {
	display: flex;
	flex-direction: column;
}
.my-stat-number {
	font-weight: 700;
	font-size: 1.125rem;
	line-height: 1.2;
	color: var(--ink-gray-9, #111827);
}
.my-stat-label {
	font-size: 0.7rem;
	text-transform: uppercase;
	letter-spacing: 0.05em;
	color: var(--ink-gray-5, #9ca3af);
	font-weight: 500;
}

.my-ranking-notice {
	display: flex;
	align-items: flex-start;
	gap: 0.5rem;
	padding: 0.75rem;
	border-radius: 8px;
	background: #fefce8;
	border: 1px solid #fef08a;
	font-size: 0.8rem;
	line-height: 1.4;
	color: #854d0e;
}

/* ─── PODIUM SECTION ─── */
.podium-section {
	border-radius: 14px;
	border: 1px solid var(--outline-gray-2, #e5e7eb);
	background: var(--surface-white, #fff);
	overflow: hidden;
}

.podium-title-bar {
	display: flex;
	align-items: center;
	gap: 0.5rem;
	padding: 1rem 1.25rem;
	border-bottom: 1px solid var(--outline-gray-2, #e5e7eb);
	color: #d97706;
}
.podium-title-bar h2 {
	font-size: 1rem;
	font-weight: 700;
	color: var(--ink-gray-9, #111827);
}

.podium-grid {
	display: grid;
	grid-template-columns: 1fr 1.15fr 1fr;
	gap: 0;
	padding: 1.5rem;
	align-items: end;
}
@media (max-width: 767px) {
	.podium-grid {
		grid-template-columns: 1fr;
		gap: 1rem;
		align-items: stretch;
	}
}

.podium-card {
	display: flex;
	flex-direction: column;
	align-items: center;
	gap: 0.5rem;
	padding: 1.5rem 1rem;
	border-radius: 14px;
	text-decoration: none;
	transition: transform 0.25s ease, box-shadow 0.25s ease;
	position: relative;
}
.podium-card:hover {
	transform: translateY(-4px);
	box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
}

.podium-card--rank-1 {
	background: linear-gradient(180deg, #fffbeb 0%, #fef3c7 100%);
	border: 1px solid #fde68a;
}
.podium-card--rank-2 {
	background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%);
	border: 1px solid #cbd5e1;
}
.podium-card--rank-3 {
	background: linear-gradient(180deg, #fff7ed 0%, #ffedd5 100%);
	border: 1px solid #fed7aa;
}
.podium-card--center {
	margin-top: -12px;
}
@media (max-width: 767px) {
	.podium-card--center {
		margin-top: 0;
	}
}

.podium-rank-circle {
	width: 36px;
	height: 36px;
	border-radius: 50%;
	display: grid;
	place-items: center;
	font-weight: 800;
	font-size: 0.95rem;
}
.podium-rank--1 {
	background: linear-gradient(135deg, #f59e0b, #eab308);
	color: white;
	box-shadow: 0 2px 12px rgba(245, 158, 11, 0.35);
	font-size: 1.1rem;
}
.podium-rank--2 {
	background: linear-gradient(135deg, #94a3b8, #64748b);
	color: white;
	box-shadow: 0 2px 12px rgba(148, 163, 184, 0.35);
}
.podium-rank--3 {
	background: linear-gradient(135deg, #f97316, #ea580c);
	color: white;
	box-shadow: 0 2px 12px rgba(249, 115, 22, 0.35);
}

.podium-avatar-wrap {
	margin: 0.5rem 0;
}

.podium-avatar-ring {
	border-radius: 50%;
	padding: 3px;
}
.ring--rank-1 {
	background: linear-gradient(135deg, #f59e0b, #eab308, #f59e0b);
	box-shadow: 0 0 20px rgba(245, 158, 11, 0.2);
}
.ring--rank-2 {
	background: linear-gradient(135deg, #94a3b8, #64748b, #94a3b8);
}
.ring--rank-3 {
	background: linear-gradient(135deg, #f97316, #ea580c, #f97316);
}

.podium-name {
	font-weight: 700;
	font-size: 0.95rem;
	color: var(--ink-gray-9, #111827);
	text-align: center;
	max-width: 100%;
	overflow: hidden;
	text-overflow: ellipsis;
	white-space: nowrap;
}

.podium-level {
	font-size: 0.8rem;
	color: var(--ink-gray-6, #6b7280);
}

.podium-coins {
	display: inline-flex;
	align-items: center;
	gap: 0.375rem;
	font-weight: 700;
	font-size: 1.1rem;
	color: #b45309;
}

.podium-highlights {
	display: flex;
	flex-wrap: wrap;
	gap: 0.375rem;
	justify-content: center;
	margin-top: 0.25rem;
}

.podium-tag {
	padding: 0.2rem 0.5rem;
	border-radius: 9999px;
	font-size: 0.65rem;
	font-weight: 500;
	background: rgba(0, 0, 0, 0.05);
	color: var(--ink-gray-7, #4b5563);
}

/* ─── LEADERBOARD TABLE ─── */
.leaderboard-section {
	border-radius: 14px;
	border: 1px solid var(--outline-gray-2, #e5e7eb);
	background: var(--surface-white, #fff);
	overflow: hidden;
}

.leaderboard-header {
	display: flex;
	align-items: center;
	justify-content: space-between;
	padding: 1.125rem 1.25rem;
	border-bottom: 1px solid var(--outline-gray-2, #e5e7eb);
}

.leaderboard-title {
	font-size: 1.05rem;
	font-weight: 700;
	color: var(--ink-gray-9, #111827);
}
.leaderboard-subtitle {
	font-size: 0.8rem;
	color: var(--ink-gray-5, #9ca3af);
	margin-top: 0.125rem;
}

.leaderboard-icon {
	display: grid;
	place-items: center;
	width: 36px;
	height: 36px;
	border-radius: 10px;
	background: #fef3c7;
	color: #d97706;
}

.leaderboard-empty {
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	gap: 0.75rem;
	padding: 3rem;
	color: var(--ink-gray-5, #9ca3af);
	font-size: 0.9rem;
}

.loading-spinner {
	width: 28px;
	height: 28px;
	border: 3px solid #e5e7eb;
	border-top-color: #6366f1;
	border-radius: 50%;
	animation: spin 0.7s linear infinite;
}
@keyframes spin {
	to { transform: rotate(360deg); }
}

.leaderboard-table {
	width: 100%;
	min-width: 720px;
	border-collapse: collapse;
}

.leaderboard-table thead {
	border-bottom: 1px solid var(--outline-gray-2, #e5e7eb);
	background: var(--surface-gray-1, #f9fafb);
}
.leaderboard-table thead tr th {
	padding: 0.75rem 1rem;
	text-align: left;
	font-size: 0.75rem;
	font-weight: 600;
	text-transform: uppercase;
	letter-spacing: 0.05em;
	color: var(--ink-gray-5, #9ca3af);
}

.leaderboard-row {
	border-bottom: 1px solid var(--outline-gray-1, #f3f4f6);
	transition: background 0.15s ease;
}
.leaderboard-row:hover {
	background: var(--surface-gray-1, #f9fafb);
}
.leaderboard-row--self {
	background: #eff6ff;
}
.leaderboard-row--self:hover {
	background: #dbeafe;
}

.leaderboard-row td {
	padding: 0.875rem 1rem;
}

.rank-number {
	display: grid;
	place-items: center;
	width: 34px;
	height: 34px;
	border-radius: 50%;
	font-size: 0.8rem;
	font-weight: 700;
}
.rank-number--gold {
	background: linear-gradient(135deg, #fef3c7, #fde68a);
	color: #92400e;
	box-shadow: 0 1px 6px rgba(245, 158, 11, 0.2);
}
.rank-number--silver {
	background: linear-gradient(135deg, #e2e8f0, #cbd5e1);
	color: #334155;
	box-shadow: 0 1px 6px rgba(148, 163, 184, 0.2);
}
.rank-number--bronze {
	background: linear-gradient(135deg, #ffedd5, #fed7aa);
	color: #9a3412;
	box-shadow: 0 1px 6px rgba(249, 115, 22, 0.2);
}
.rank-number--default {
	background: var(--surface-gray-2, #f3f4f6);
	color: var(--ink-gray-6, #6b7280);
}

.profile-cell {
	display: flex;
	align-items: center;
	gap: 0.75rem;
	text-decoration: none;
}
.profile-name {
	font-weight: 600;
	color: var(--ink-gray-9, #111827);
	overflow: hidden;
	text-overflow: ellipsis;
	white-space: nowrap;
}
.profile-headline {
	font-size: 0.8rem;
	color: var(--ink-gray-5, #9ca3af);
	overflow: hidden;
	text-overflow: ellipsis;
	white-space: nowrap;
}

.coins-cell {
	display: flex;
	align-items: center;
	gap: 0.375rem;
	font-weight: 700;
	color: #b45309;
}

.highlights-cell {
	display: flex;
	flex-wrap: wrap;
	gap: 0.375rem;
}

.highlight-tag {
	padding: 0.25rem 0.625rem;
	border-radius: 9999px;
	font-size: 0.7rem;
	font-weight: 500;
	background: var(--surface-gray-2, #f3f4f6);
	color: var(--ink-gray-7, #4b5563);
	transition: background 0.15s ease;
}
.leaderboard-row:hover .highlight-tag {
	background: #e5e7eb;
}

/* ─── SIDEBAR CARDS ─── */
.sidebar-card {
	border-radius: 14px;
	border: 1px solid var(--outline-gray-2, #e5e7eb);
	background: var(--surface-white, #fff);
	padding: 1.25rem;
	transition: box-shadow 0.3s ease;
}
.sidebar-card:hover {
	box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
}

.sidebar-card-header {
	display: flex;
	align-items: center;
	gap: 0.625rem;
	margin-bottom: 1rem;
}

.sidebar-icon {
	display: grid;
	place-items: center;
	width: 30px;
	height: 30px;
	border-radius: 8px;
}
.sidebar-icon--pink {
	background: #fce7f3;
	color: #db2777;
}
.sidebar-icon--green {
	background: #dcfce7;
	color: #16a34a;
}

.sidebar-title {
	font-weight: 700;
	font-size: 0.95rem;
	color: var(--ink-gray-9, #111827);
}

/* Rewards */
.rewards-list {
	display: flex;
	flex-direction: column;
	gap: 0.625rem;
}

.reward-item {
	display: flex;
	align-items: flex-start;
	gap: 0.75rem;
	padding: 0.875rem;
	border-radius: 10px;
	background: var(--surface-gray-1, #f9fafb);
	border: 1px solid transparent;
	transition: border-color 0.15s ease;
}
.reward-item:hover {
	border-color: var(--outline-gray-2, #e5e7eb);
}

.reward-place {
	display: grid;
	place-items: center;
	width: 32px;
	height: 32px;
	border-radius: 8px;
	font-weight: 800;
	font-size: 0.75rem;
	flex-shrink: 0;
}
.reward-place--1 {
	background: linear-gradient(135deg, #fef3c7, #fde68a);
	color: #92400e;
}
.reward-place--2 {
	background: linear-gradient(135deg, #e2e8f0, #cbd5e1);
	color: #334155;
}
.reward-place--3 {
	background: linear-gradient(135deg, #ffedd5, #fed7aa);
	color: #9a3412;
}

.reward-info {
	min-width: 0;
}
.reward-title {
	font-weight: 600;
	font-size: 0.85rem;
	color: var(--ink-gray-9, #111827);
}
.reward-desc {
	font-size: 0.8rem;
	line-height: 1.4;
	color: var(--ink-gray-6, #6b7280);
	margin-top: 0.125rem;
}

/* Rules */
.rules-list {
	display: flex;
	flex-direction: column;
	gap: 0.5rem;
}

.rule-item {
	display: flex;
	align-items: center;
	justify-content: space-between;
	gap: 0.75rem;
	padding: 0.625rem 0.75rem;
	border-radius: 8px;
	transition: background 0.15s ease;
}
.rule-item:hover {
	background: var(--surface-gray-1, #f9fafb);
}

.rule-label {
	font-size: 0.85rem;
	color: var(--ink-gray-7, #4b5563);
}

.rule-coins {
	display: inline-flex;
	align-items: center;
	gap: 0.25rem;
	padding: 0.25rem 0.625rem;
	border-radius: 9999px;
	font-size: 0.8rem;
	font-weight: 600;
	background: linear-gradient(135deg, #fefce8, #fef3c7);
	color: #92400e;
	border: 1px solid #fde68a;
	white-space: nowrap;
}
</style>
