<template>
	<div class="home-page w-full px-4 sm:px-6 pt-6 pb-12 min-h-screen">

		<!-- Hero Section -->
		<div class="home-hero relative overflow-hidden mb-8">
			<div class="home-hero-glow-1"></div>
			<div class="home-hero-glow-2"></div>
			<div class="home-hero-grid"></div>
			<div class="relative z-10 p-8 sm:p-10">
				<div class="flex flex-col md:flex-row justify-between items-center gap-8">
					<div class="space-y-4 max-w-2xl">
						<h1 class="text-3xl sm:text-4xl font-extrabold tracking-tight text-white leading-tight">
							{{ __('Hola') }}, {{ user.data?.full_name?.split(' ')[0] || user.data?.full_name }} 👋
						</h1>
						<p class="text-base sm:text-lg text-blue-100/80 font-medium leading-relaxed">
							{{ subtitle }}
						</p>
						<div class="flex flex-wrap gap-3 pt-2" v-if="!isAdmin">
							<router-link
								:to="{ name: 'Courses' }"
								class="home-btn-primary"
							>
								{{ __('Continuar aprendiendo') }}
							</router-link>
							<router-link
								:to="{ name: 'Courses' }"
								class="home-btn-ghost"
							>
								{{ __('Explorar cursos') }}
							</router-link>
						</div>
					</div>

					<!-- Mini Stats in Hero -->
					<div class="hidden md:flex gap-5 items-center" v-if="!isAdmin">
						<div class="home-hero-stat cursor-pointer hover:scale-105 transition-transform" @click="showStreakModal = true">
							<div class="text-3xl font-black text-amber-400 drop-shadow-md">{{ streakInfo.data?.current_streak || 0 }}</div>
							<div class="flex items-center justify-center gap-1.5 text-[10px] uppercase tracking-widest text-blue-200/70 font-bold mt-1">
								<Flame class="size-3 text-amber-400" /> {{ __('Racha') }}
							</div>
						</div>
						<div class="w-px h-10 bg-white/10"></div>
						<div class="home-hero-stat">
							<div class="text-3xl font-black text-white drop-shadow-md">{{ evalCount || 0 }}</div>
							<div class="flex items-center justify-center gap-1.5 text-[10px] uppercase tracking-widest text-blue-200/70 font-bold mt-1">
								<ClipboardCheck class="size-3 text-blue-300" /> {{ __('Evaluaciones') }}
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>

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
	<Streak v-model="showStreakModal" :streakInfo="streakInfo" />
</template>

<script setup lang="ts">
import { computed, inject, onMounted, ref } from 'vue'
import { call, createResource, usePageMeta } from 'frappe-ui'
import { sessionStore } from '@/stores/session'
import { useRouter } from 'vue-router'
import { Flame, ClipboardCheck } from 'lucide-vue-next'
import StudentHome from '@/pages/Home/StudentHome.vue'
import AdminHome from '@/pages/Home/AdminHome.vue'
import Streak from '@/pages/Home/Streak.vue'

const user = inject<any>('$user')
const { brand } = sessionStore()
const router = useRouter()
const evalCount = ref(0)
const currentTab = ref<'student' | 'instructor'>('student')
const showStreakModal = ref(false)

const fetchEvalCount = () => {
	call('frappe.client.get_count', {
		doctype: 'LMS Certificate Request',
		filters: {
			member: user?.data?.name,
			status: 'Upcoming',
			date: ['>=', inject<any>('$dayjs')().format('YYYY-MM-DD')],
		},
	}).then((data: any) => {
		evalCount.value = data
	})
}

const isAdmin = computed(() => {
	return (
		user.data?.is_moderator ||
		user.data?.is_instructor ||
		user.data?.is_evaluator
	)
})

const isPersonaCaptured = async () => {
	let persona = await call('frappe.client.get_single_value', {
		doctype: 'LMS Settings',
		field: 'persona_captured',
	})
	return persona
}

const identifyUserPersona = async () => {
	if (user.data?.is_system_manager && !user.data?.developer_mode) {
		let personaCaptured = await isPersonaCaptured()
		if (personaCaptured) return
		let courseCount = await call('frappe.client.get_count', {
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

onMounted(() => {
	identifyUserPersona()
	if (isAdmin.value) {
		currentTab.value = 'instructor'
	} else {
		currentTab.value = 'student'
		fetchEvalCount()
	}
})

const myLiveClasses = createResource({
	url: 'lms.lms.api.get_my_live_classes',
	auto: !isAdmin.value ? true : false,
})

const adminLiveClasses = createResource({
	url: 'lms.lms.api.get_admin_live_classes',
	auto: isAdmin.value ? true : false,
})

const adminEvals = createResource({
	url: 'lms.lms.api.get_admin_evals',
	auto: isAdmin.value ? true : false,
})

const streakInfo = createResource({
	url: 'lms.lms.api.get_streak_info',
	auto: true,
})

const subtitle = computed(() => {
	if (isAdmin.value) {
		let liveClassSuffix =
			adminLiveClasses.data?.length > 1 ? __('clases en vivo') : __('clase en vivo')
		let evalSuffix =
			adminEvals.data?.length > 1 ? __('evaluaciones') : __('evaluación')
		if (adminLiveClasses.data?.length > 0 && adminEvals.data?.length > 0) {
			return __('Tienes {0} {1} próximas y {2} {3} programadas.').format(
				adminLiveClasses.data.length,
				liveClassSuffix,
				adminEvals.data.length,
				evalSuffix
			)
		} else if (adminLiveClasses.data?.length > 0) {
			return __('Tienes {0} {1} próximas.').format(
				adminLiveClasses.data.length,
				liveClassSuffix
			)
		} else if (adminEvals.data?.length > 0) {
			return __('Tienes {0} {1} programadas.').format(
				adminEvals.data.length,
				evalSuffix
			)
		}
		return __('Gestiona tus cursos y grupos de un vistazo')
	} else {
		let liveClassSuffix =
			myLiveClasses.data?.length > 1 ? __('clases en vivo') : __('clase en vivo')
		let evalSuffix = evalCount.value > 1 ? __('evaluaciones') : __('evaluación')
		if (myLiveClasses.data?.length > 0 && evalCount.value > 0) {
			return __('Tienes {0} {1} próximas y {2} {3} programadas.').format(
				myLiveClasses.data.length,
				liveClassSuffix,
				evalCount.value,
				evalSuffix
			)
		} else if (myLiveClasses.data?.length > 0) {
			return __('Tienes {0} {1} próximas.').format(
				myLiveClasses.data.length,
				liveClassSuffix
			)
		} else if (evalCount.value > 0) {
			return __('Tienes {0} {1} programadas.').format(
				evalCount.value,
				evalSuffix
			)
		}
		return __('Sigue aprendiendo y completa tu próximo curso')
	}
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
	background: var(--sb-bg);
}

/* ═══════════════════════════════════════
   HERO
   ═══════════════════════════════════════ */

.home-hero {
	background: linear-gradient(145deg, #061B49 0%, #0b2f73 40%, #0a2259 100%);
	border-radius: 24px;
	box-shadow: 0 4px 24px rgba(6, 27, 73, 0.15), 0 1px 3px rgba(6, 27, 73, 0.08);
}

:root[data-theme="dark"] .home-hero {
	box-shadow: 0 4px 24px rgba(0, 0, 0, 0.4), 0 1px 3px rgba(0, 0, 0, 0.2);
}

.home-hero-glow-1 {
	position: absolute;
	top: -100px;
	right: -60px;
	width: 360px;
	height: 360px;
	background: radial-gradient(circle, rgba(59, 130, 246, 0.2), transparent 70%);
	border-radius: 50%;
	filter: blur(50px);
}

.home-hero-glow-2 {
	position: absolute;
	bottom: -80px;
	left: -40px;
	width: 260px;
	height: 260px;
	background: radial-gradient(circle, rgba(245, 179, 1, 0.1), transparent 70%);
	border-radius: 50%;
	filter: blur(40px);
}

.home-hero-grid {
	position: absolute;
	inset: 0;
	background-image:
		linear-gradient(rgba(255,255,255,0.025) 1px, transparent 1px),
		linear-gradient(90deg, rgba(255,255,255,0.025) 1px, transparent 1px);
	background-size: 40px 40px;
	border-radius: 24px;
}

.home-hero-stat {
	text-align: center;
	padding: 8px 16px;
}

/* ═══════════════════════════════════════
   BUTTONS
   ═══════════════════════════════════════ */

.home-btn-primary {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	gap: 8px;
	padding: 12px 24px;
	border-radius: 14px;
	font-size: 14px;
	font-weight: 700;
	color: #fff;
	background: linear-gradient(135deg, #0d6efd, #0b5ed7);
	box-shadow: 0 2px 12px rgba(13, 110, 253, 0.3);
	transition: all 0.2s ease;
	text-decoration: none;
}

.home-btn-primary:hover {
	transform: translateY(-1px);
	box-shadow: 0 4px 20px rgba(13, 110, 253, 0.4);
	background: linear-gradient(135deg, #0b5ed7, #084298);
}

.home-btn-ghost {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	gap: 8px;
	padding: 12px 24px;
	border-radius: 14px;
	font-size: 14px;
	font-weight: 700;
	color: #fff;
	background: rgba(255, 255, 255, 0.08);
	border: 1px solid rgba(255, 255, 255, 0.1);
	backdrop-filter: blur(8px);
	transition: all 0.2s ease;
	text-decoration: none;
}

.home-btn-ghost:hover {
	background: rgba(255, 255, 255, 0.14);
	border-color: rgba(255, 255, 255, 0.18);
}
</style>
