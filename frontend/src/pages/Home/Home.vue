<template>
	<div class="home-page w-full px-4 pb-12 pt-6 sm:px-6">
		<section v-if="isAdmin" class="home-admin-hero">
			<div class="home-admin-hero-content">
				<div class="home-admin-copy">
					<div class="home-admin-eyebrow">
						<Sparkles class="size-4" />
						{{ __('Panel de gestión') }}
					</div>

					<h1 class="home-admin-title">
						{{ __('Hola') }},
						{{ firstName }} 👋
					</h1>

					<p class="home-admin-subtitle">
						{{ adminSubtitle }}
					</p>

					<div class="home-admin-actions">
						<router-link :to="{ name: 'Courses' }" class="home-btn-light">
							<BookOpen class="size-4" />
							{{ __('Gestionar cursos') }}
						</router-link>

						<router-link :to="{ name: 'Courses' }" class="home-btn-ghost">
							<ArrowUpRight class="size-4" />
							{{ __('Ver catálogo') }}
						</router-link>
					</div>
				</div>

				<div class="home-admin-panel">
					<div class="home-admin-panel-title">
						{{ __('Resumen rápido') }}
					</div>

					<div class="home-admin-stats">
						<div class="home-admin-stat">
							<div class="home-admin-stat-icon">
								<Video class="size-5" />
							</div>

							<div>
								<div class="home-admin-stat-value">
									{{ adminLiveClasses.data?.length || 0 }}
								</div>
								<div class="home-admin-stat-label">
									{{ __('Clases en vivo') }}
								</div>
							</div>
						</div>

						<div class="home-admin-stat">
							<div class="home-admin-stat-icon gold">
								<ClipboardCheck class="size-5" />
							</div>

							<div>
								<div class="home-admin-stat-value">
									{{ adminEvals.data?.length || 0 }}
								</div>
								<div class="home-admin-stat-label">
									{{ __('Evaluaciones') }}
								</div>
							</div>
						</div>
					</div>

					<p class="home-admin-panel-note">
						{{ __('Revisa tus cursos, clases y evaluaciones desde un solo lugar.') }}
					</p>
				</div>
			</div>
		</section>

		<AdminHome
			v-if="isAdmin && currentTab === 'instructor'"
			:liveClasses="adminLiveClasses"
			:evals="adminEvals"
		/>

		<StudentHome
			v-else-if="currentTab === 'student'"
			:myLiveClasses="myLiveClasses"
		/>
	</div>
</template>

<script setup lang="ts">
import { computed, inject, onMounted, ref } from 'vue'
import { call, createResource, usePageMeta } from 'frappe-ui'
import { sessionStore } from '@/stores/session'
import { useRouter } from 'vue-router'
import {
	ArrowUpRight,
	BookOpen,
	ClipboardCheck,
	Sparkles,
	Video,
} from 'lucide-vue-next'
import StudentHome from '@/pages/Home/StudentHome.vue'
import AdminHome from '@/pages/Home/AdminHome.vue'

const user = inject<any>('$user')
const { brand } = sessionStore()
const router = useRouter()

const currentTab = ref<'student' | 'instructor'>('student')

const firstName = computed(() => {
	const name =
		user?.data?.first_name ||
		user?.data?.full_name ||
		user?.data?.name ||
		'StudyBadger'

	return String(name).split(' ')[0]
})

const isAdmin = computed(() => {
	return (
		user?.data?.is_moderator ||
		user?.data?.is_instructor ||
		user?.data?.is_evaluator
	)
})

const myLiveClasses = createResource({
	url: 'lms.lms.api.get_my_live_classes',
	auto: false,
})

const adminLiveClasses = createResource({
	url: 'lms.lms.api.get_admin_live_classes',
	auto: false,
})

const adminEvals = createResource({
	url: 'lms.lms.api.get_admin_evals',
	auto: false,
})

const isPersonaCaptured = async () => {
	const persona = await call('frappe.client.get_single_value', {
		doctype: 'LMS Settings',
		field: 'persona_captured',
	})

	return persona
}

const identifyUserPersona = async () => {
	if (user?.data?.is_system_manager && !user?.data?.developer_mode) {
		const personaCaptured = await isPersonaCaptured()

		if (personaCaptured) return

		const courseCount = await call('frappe.client.get_count', {
			doctype: 'LMS Course',
			filters: {
				title: ['not like', '%A guide to Frappe Learning%'],
			},
		})

		if (!courseCount) {
			router.push({ name: 'PersonaForm' })
		}
	}
}

const loadHomeData = () => {
	if (isAdmin.value) {
		currentTab.value = 'instructor'
		adminLiveClasses.reload()
		adminEvals.reload()
		return
	}

	currentTab.value = 'student'
	myLiveClasses.reload()
}

onMounted(() => {
	identifyUserPersona()
	loadHomeData()
})

const adminSubtitle = computed(() => {
	const liveCount = adminLiveClasses.data?.length || 0
	const evalCount = adminEvals.data?.length || 0

	const liveClassSuffix =
		liveCount === 1 ? __('clase en vivo') : __('clases en vivo')

	const evalSuffix =
		evalCount === 1 ? __('evaluación') : __('evaluaciones')

	if (liveCount > 0 && evalCount > 0) {
		return __('Tienes {0} {1} próximas y {2} {3} programadas.').format(
			liveCount,
			liveClassSuffix,
			evalCount,
			evalSuffix
		)
	}

	if (liveCount > 0) {
		return __('Tienes {0} {1} próximas.').format(
			liveCount,
			liveClassSuffix
		)
	}

	if (evalCount > 0) {
		return __('Tienes {0} {1} programadas.').format(
			evalCount,
			evalSuffix
		)
	}

	return __('Gestiona tus cursos, clases y evaluaciones desde tu panel de StudyBadge.')
})

usePageMeta(() => {
	return {
		title: __('Inicio'),
		icon: brand.favicon,
	}
})
</script>

<style scoped>
.home-page {
	min-height: 100vh;
	background: var(--sb-bg, #f5f8fc);
}

/* ADMIN HERO */

.home-admin-hero {
	margin-bottom: 2rem;
	overflow: hidden;
	border-radius: 28px;
	background: #0a2251;
	color: #ffffff;
	box-shadow: 0 24px 60px rgba(10, 34, 81, 0.16);
}

.home-admin-hero-content {
	display: grid;
	grid-template-columns: minmax(0, 1fr) 360px;
	gap: 2rem;
	align-items: center;
	padding: 2rem;
}

.home-admin-copy {
	min-width: 0;
}

.home-admin-eyebrow {
	display: inline-flex;
	align-items: center;
	gap: 0.5rem;
	width: fit-content;
	margin-bottom: 1rem;
	border-radius: 999px;
	border: 1px solid rgba(255, 255, 255, 0.18);
	background: rgba(255, 255, 255, 0.1);
	padding: 0.45rem 0.75rem;
	color: rgba(255, 255, 255, 0.88);
	font-size: 0.75rem;
	font-weight: 900;
	letter-spacing: 0.06em;
	text-transform: uppercase;
}

.home-admin-title {
	margin: 0;
	max-width: 720px;
	color: #ffffff;
	font-size: clamp(2rem, 5vw, 3.75rem);
	font-weight: 950;
	letter-spacing: -0.055em;
	line-height: 1.02;
}

.home-admin-subtitle {
	margin: 1rem 0 0;
	max-width: 680px;
	color: rgba(255, 255, 255, 0.78);
	font-size: 1rem;
	line-height: 1.75;
}

.home-admin-actions {
	display: flex;
	flex-wrap: wrap;
	gap: 0.75rem;
	margin-top: 1.5rem;
}

.home-admin-panel {
	border: 1px solid rgba(255, 255, 255, 0.16);
	border-radius: 24px;
	background: rgba(255, 255, 255, 0.08);
	padding: 1.25rem;
}

.home-admin-panel-title {
	color: rgba(255, 255, 255, 0.82);
	font-size: 0.78rem;
	font-weight: 900;
	letter-spacing: 0.08em;
	text-transform: uppercase;
}

.home-admin-stats {
	display: grid;
	gap: 0.85rem;
	margin-top: 1rem;
}

.home-admin-stat {
	display: flex;
	align-items: center;
	gap: 0.85rem;
	border-radius: 18px;
	background: rgba(255, 255, 255, 0.1);
	padding: 0.9rem;
}

.home-admin-stat-icon {
	display: flex;
	align-items: center;
	justify-content: center;
	width: 44px;
	height: 44px;
	border-radius: 16px;
	background: #ffffff;
	color: #0a2251;
	flex: 0 0 auto;
}

.home-admin-stat-icon.gold {
	background: #f5b301;
	color: #3b2a00;
}

.home-admin-stat-value {
	color: #ffffff;
	font-size: 1.6rem;
	font-weight: 950;
	letter-spacing: -0.04em;
	line-height: 1;
}

.home-admin-stat-label {
	margin-top: 0.2rem;
	color: rgba(255, 255, 255, 0.7);
	font-size: 0.78rem;
	font-weight: 800;
}

.home-admin-panel-note {
	margin: 1rem 0 0;
	color: rgba(255, 255, 255, 0.72);
	font-size: 0.85rem;
	line-height: 1.6;
}

/* BUTTONS */

.home-btn-light,
.home-btn-ghost {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	gap: 0.5rem;
	border-radius: 999px;
	padding: 0.8rem 1.1rem;
	font-size: 0.9rem;
	font-weight: 900;
	text-decoration: none;
	transition: 0.18s ease;
}

.home-btn-light {
	background: #ffffff;
	color: #0a2251;
	box-shadow: 0 14px 28px rgba(0, 0, 0, 0.18);
}

.home-btn-light:hover {
	transform: translateY(-1px);
	background: #f8fbff;
}

.home-btn-ghost {
	border: 1px solid rgba(255, 255, 255, 0.28);
	background: rgba(255, 255, 255, 0.08);
	color: #ffffff;
}

.home-btn-ghost:hover {
	transform: translateY(-1px);
	background: rgba(255, 255, 255, 0.14);
}

:global(:root[data-theme='dark']) .home-page {
	background: #07111f;
}

:global(:root[data-theme='dark']) .home-admin-hero {
	box-shadow: 0 24px 60px rgba(0, 0, 0, 0.34);
}

/* RESPONSIVE */

@media (max-width: 1100px) {
	.home-admin-hero-content {
		grid-template-columns: 1fr;
	}

	.home-admin-panel {
		max-width: 560px;
	}
}

@media (max-width: 640px) {
	.home-page {
		padding-inline: 1rem;
	}

	.home-admin-hero-content {
		padding: 1.25rem;
	}

	.home-admin-actions {
		flex-direction: column;
	}

	.home-btn-light,
	.home-btn-ghost {
		width: 100%;
	}
}
</style>