<template>
	<div class="w-full px-4 sm:px-6 pt-6 pb-12 font-sans bg-[#f5f7fb] min-h-screen">
		<!-- New Hero Section -->
		<div class="bg-[#08204e] rounded-3xl p-8 sm:p-10 text-white relative overflow-hidden mb-8 shadow-lg">
			<!-- background decorations -->
			<div class="absolute -top-24 -right-24 w-96 h-96 bg-[#0b2f73] opacity-50 blur-3xl rounded-full"></div>
			<div class="relative z-10 flex flex-col md:flex-row justify-between items-center gap-8">
				<div class="space-y-4 max-w-2xl">
					<h1 class="text-3xl sm:text-4xl font-bold tracking-tight">
						{{ __('Hola') }}, {{ user.data?.full_name?.split(' ')[0] || user.data?.full_name }} 👋
					</h1>
					<p class="text-lg text-blue-100 font-medium">
						{{ subtitle }}
					</p>
					<div class="flex flex-wrap gap-3 pt-2" v-if="!isAdmin">
						<router-link
							:to="{ name: 'Courses' }"
							class="inline-flex items-center justify-center rounded-xl bg-[#0d6efd] px-6 py-3 text-sm font-bold text-white shadow-md transition-colors hover:bg-[#0b2f73]"
						>
							{{ __('Continuar aprendiendo') }}
						</router-link>
						<router-link
							:to="{ name: 'Courses' }"
							class="inline-flex items-center justify-center rounded-xl bg-white/10 px-6 py-3 text-sm font-bold text-white backdrop-blur-sm transition-colors hover:bg-white/20"
						>
							{{ __('Explorar cursos') }}
						</router-link>
					</div>
				</div>
				<div class="hidden md:flex gap-6 items-center" v-if="!isAdmin">
					<!-- Mini Stats in Hero -->
					<div class="text-center cursor-pointer hover:scale-105 transition-transform" @click="showStreakModal = true">
						<div class="text-4xl font-black text-amber-400 drop-shadow-sm">{{ streakInfo.data?.current_streak || 0 }}</div>
						<div class="text-xs uppercase tracking-wider text-blue-200 font-bold mt-1 flex justify-center items-center gap-1">{{ __('Racha') }} 🔥</div>
					</div>
					<div class="w-px h-16 bg-white/20"></div>
					<div class="text-center">
						<div class="text-4xl font-black text-white drop-shadow-sm">{{ evalCount || 0 }}</div>
						<div class="text-xs uppercase tracking-wider text-blue-200 font-bold mt-1 flex justify-center items-center gap-1">{{ __('Evals') }} 📝</div>
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
