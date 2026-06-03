<template>
	<div class="relative flex h-[100dvh] flex-col">
		<div
			class="flex flex-1 flex-col overflow-y-auto bg-sb-bg"
			id="scrollContainer"
		>
			<slot />
			<!-- Espaciador para la barra de navegación móvil (previene que el contenido quede oculto) -->
			<div v-if="!['AISessions', 'AISessionRoom', 'AISessionChat'].includes(router?.currentRoute?.value?.name)" class="h-28 shrink-0 w-full"></div>
		</div>

		<div class="relative z-20">
			<!-- Dropdown menu -->
			<Transition
				enter-active-class="transition duration-300 ease-out"
				enter-from-class="transform translate-y-8 opacity-0 scale-95"
				enter-to-class="transform translate-y-0 opacity-100 scale-100"
				leave-active-class="transition duration-200 ease-in"
				leave-from-class="transform translate-y-0 opacity-100 scale-100"
				leave-to-class="transform translate-y-8 opacity-0 scale-95"
			>
				<div
					class="fixed bottom-[4.5rem] right-4 w-64 max-h-[75vh] overflow-y-auto scrollbar-hide rounded-2xl bg-white/95 p-2 backdrop-blur-xl shadow-[0_10px_40px_-10px_rgba(0,0,0,0.15)] ring-1 ring-black/5"
					v-if="showMenu"
					ref="menu"
				>
					<div
						v-for="(link, index) in otherLinks"
						:key="link.label"
					>
						<div v-if="link.label === 'Referidos' && index !== 0" class="my-1.5 border-t border-gray-100"></div>
						<div v-if="link.label === 'Cerrar sesión' || link.label === 'Iniciar sesión'" class="my-1.5 border-t border-gray-100"></div>
						
						<div
							class="flex cursor-pointer items-center gap-3 rounded-xl px-3 py-2.5 transition-all hover:bg-gray-50 active:scale-95 active:bg-gray-100"
							@click="handleClick(link); showMenu = false"
						>
							<div class="flex h-9 w-9 items-center justify-center rounded-lg bg-blue-50 text-blue-600">
								<component
									:is="icons[link.icon]"
									class="h-[18px] w-[18px] stroke-[1.8]"
								/>
							</div>
							<div class="text-[0.95rem] font-semibold text-gray-700">{{ link.label }}</div>
						</div>
					</div>
				</div>
			</Transition>

			<!-- Fixed menu -->
			<div
				v-if="sidebarSettings.data"
				class="standalone:pb-4 fixed bottom-0 start-0 z-10 flex w-full items-center justify-around border-t border-outline-gray-2 bg-surface-white"
			>
				<button
					v-for="tab in sidebarLinks"
					:key="tab.label"
					:class="isVisible(tab) ? 'block' : 'hidden'"
					class="flex flex-col items-center justify-center py-3 transition active:scale-95"
					@click="handleClick(tab)"
				>
					<component
						:is="icons[tab.icon]"
						class="h-6 w-6 stroke-1.5"
						:class="[isActive(tab) ? 'text-sb-primary' : 'text-ink-gray-5']"
					/>
				</button>
				<button @click="toggleMenu">
					<component
						:is="icons['List']"
						class="h-6 w-6 stroke-1.5 text-ink-gray-5"
					/>
				</button>
			</div>
		</div>
	</div>
</template>
<script setup>
import { getSidebarLinks } from '@/utils'
import { useRouter } from 'vue-router'
import { call } from 'frappe-ui'
import { computed, ref, watch } from 'vue'
import { sessionStore } from '@/stores/session'
import { useSettings } from '@/stores/settings'
import { usersStore } from '@/stores/user'
import * as icons from 'lucide-vue-next'

const { logout, user } = sessionStore()
let { isLoggedIn } = sessionStore()
const { sidebarSettings } = useSettings()
const router = useRouter()
let { userResource } = usersStore()
const sidebarLinks = ref([])
const otherLinks = ref([])
const showMenu = ref(false)
const menu = ref(null)
const isModerator = ref(false)
const isInstructor = ref(false)
const profileUsername = computed(
	() =>
		userResource.data?.username ||
		userResource.data?.name ||
		userResource.data?.email ||
		''
)

const handleOutsideClick = (e) => {
	if (menu.value && !menu.value.contains(e.target)) {
		showMenu.value = false
	}
}

watch(showMenu, (val) => {
	if (val) {
		setTimeout(() => {
			document.addEventListener('click', handleOutsideClick)
		}, 0)
	} else {
		document.removeEventListener('click', handleOutsideClick)
	}
})

const destructureSidebarLinks = () => {
	let links = []
	sidebarLinks.value.forEach((link) => {
		link.items?.forEach((item) => {
			links.push(item)
		})
	})
	sidebarLinks.value = links
}

const filterLinksToShow = (data) => {
	Object.keys(data).forEach((key) => {
		if (!parseInt(data[key])) {
			sidebarLinks.value = sidebarLinks.value.filter(
				(link) => link.label.toLowerCase().split(' ').join('_') !== key
			)
		}
	})
}

const addOtherLinks = () => {
	if (user) {
		addLink('Referidos', 'Gift', 'Referrals')
		addLink('Notificaciones', 'Bell', 'Notifications')
		addLink('Perfil', 'UserRound')
		addLink('Cerrar sesión', 'LogOut')
	} else {
		addLink('Iniciar sesión', 'LogIn')
	}
}

const addLink = (label, icon, to = '') => {
	if (otherLinks.value.some((link) => link.label === label)) return
	otherLinks.value.push({
		label: label,
		icon: icon,
		to: to,
	})
}

const updateSidebarLinks = () => {
	sidebarLinks.value = getSidebarLinks(true)
	destructureSidebarLinks()
	otherLinks.value = []
	sidebarSettings.reload(
		{},
		{
			onSuccess: async (data) => {
				filterLinksToShow(data)
				await addPrograms()
				if (isModerator.value || isInstructor.value) {
					addQuizzes()
					addAssignments()
					addProgrammingExercises()
				}
				addOtherLinks()

				if (sidebarLinks.value.length > 3) {
					const extraLinks = sidebarLinks.value.slice(3)
					sidebarLinks.value = sidebarLinks.value.slice(0, 3)
					
					const mappedExtra = extraLinks.map(link => ({
						label: link.label,
						icon: link.icon,
						to: link.to,
						activeFor: link.activeFor
					}))
					
					otherLinks.value = [...mappedExtra, ...otherLinks.value]
				}
			},
		}
	)
}

const addQuizzes = () => {
	addLink('Quizzes', 'CircleHelp', 'Quizzes')
}

const addAssignments = () => {
	addLink('Assignments', 'Pencil', 'Assignments')
}

const addProgrammingExercises = () => {
	addLink('Programming Exercises', 'Code', 'ProgrammingExercises')
}

const addPrograms = async () => {
	if (sidebarLinks.value.some((link) => link.label === 'Programs')) return
	let canAddProgram = await checkIfCanAddProgram()
	if (!canAddProgram) return
	let activeFor = ['Programs', 'ProgramDetail']
	let index = 1

	sidebarLinks.value.splice(index, 0, {
		label: 'Programs',
		icon: 'Route',
		to: 'Programs',
		activeFor: activeFor,
	})
}

watch(
	userResource,
	async () => {
		await userResource.promise
		if (userResource.data) {
			isModerator.value = userResource.data.is_moderator
			isInstructor.value = userResource.data.is_instructor
		}
		updateSidebarLinks()
	},
	{ immediate: true }
)

const checkIfCanAddProgram = async () => {
	if (!userResource.data) return false
	if (isModerator.value || isInstructor.value) {
		return true
	}
	const programs = await call('lms.lms.utils.get_programs')
	return programs.enrolled.length > 0 || programs.published.length > 0
}

let isActive = (tab) => {
	return tab.activeFor?.includes(router.currentRoute.value.name)
}

const handleClick = (tab) => {
	if (tab.label == 'Iniciar sesión') window.location.href = '/login'
	else if (tab.label == 'Cerrar sesión')
		logout.submit().then(() => {
			isLoggedIn = false
		})
	else if (tab.label == 'Perfil' && profileUsername.value)
		router.push({
			name: 'Profile',
			params: {
				username: profileUsername.value,
			},
		})
	else router.push({ name: tab.to })
}

const isVisible = (tab) => {
	if (tab.label == 'Iniciar sesión') return !isLoggedIn
	else if (tab.label == 'Cerrar sesión') return isLoggedIn
	else return true
}

const toggleMenu = () => {
	showMenu.value = !showMenu.value
}
</script>
