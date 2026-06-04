<template>
	<div class="mobile-layout">
		<div
			id="scrollContainer"
			class="mobile-scroll"
			:class="{ 'menu-open': showMenu }"
		>
			<slot />

			<div v-if="showBottomSpacer" class="mobile-bottom-spacer"></div>
		</div>

		<div v-if="sidebarSettings.data" class="mobile-nav-layer">
			<Transition name="mobile-overlay">
				<div
					v-if="showMenu"
					class="mobile-menu-overlay"
					@click="showMenu = false"
				></div>
			</Transition>

			<Transition name="mobile-sheet">
				<div v-if="showMenu" ref="menu" class="mobile-sheet">
					<div class="mobile-sheet-handle"></div>

					<div class="mobile-sheet-header">
						<div>
							<p>{{ __('StudyBadge') }}</p>
							<h2>{{ __('Menú') }}</h2>
						</div>

						<button class="mobile-sheet-close" @click="showMenu = false">
							<component :is="icons['X']" class="size-5" />
						</button>
					</div>

					<div v-if="user" class="mobile-user-card">
						<div class="mobile-user-avatar">
							<component :is="icons['UserRound']" class="size-5" />
						</div>

						<div class="mobile-user-copy">
							<strong>{{ userLabel }}</strong>
							<span>{{ __('Tu espacio de aprendizaje') }}</span>
						</div>

						<div class="mobile-user-badge">
							{{ isInstructor || isModerator ? __('Pro') : __('Estudiante') }}
						</div>
					</div>

					<div class="mobile-sheet-section">
						<div class="mobile-section-title">
							{{ __('Accesos rápidos') }}
						</div>

						<div class="mobile-quick-grid">
							<button
								v-for="link in quickSheetLinks"
								:key="link.label"
								class="mobile-quick-card"
								:class="{ active: isActive(link) }"
								@click="handleClick(link); showMenu = false"
							>
								<div class="mobile-quick-icon">
									<component
										:is="icons[link.icon] || icons['Circle']"
										class="size-5"
									/>
								</div>

								<span>{{ __(link.label) }}</span>
							</button>
						</div>
					</div>

					<div v-if="otherLinks.length" class="mobile-sheet-section">
						<div class="mobile-section-title">
							{{ __('Más opciones') }}
						</div>

						<div class="mobile-link-list">
							<button
								v-for="link in otherLinks"
								:key="link.label"
								class="mobile-sheet-link"
								:class="{
									active: isActive(link),
									danger: link.label === 'Cerrar sesión',
								}"
								@click="handleClick(link); showMenu = false"
							>
								<div class="mobile-sheet-link-icon">
									<component
										:is="icons[link.icon] || icons['Circle']"
										class="size-5"
									/>
								</div>

								<div class="mobile-sheet-link-copy">
									<strong>{{ __(link.label) }}</strong>
									<span>{{ getLinkDescription(link) }}</span>
								</div>

								<component :is="icons['ChevronRight']" class="size-4" />
							</button>
						</div>
					</div>
				</div>
			</Transition>

			<nav class="mobile-bottom-nav" aria-label="Navegación móvil">
				<button
					v-for="tab in visibleBottomTabs"
					:key="tab.label"
					class="mobile-nav-item"
					:class="{ active: isActive(tab) }"
					@click="handleClick(tab)"
				>
					<span class="mobile-nav-icon">
						<component
							:is="icons[tab.icon] || icons['Circle']"
							class="size-5"
						/>
					</span>

					<span class="mobile-nav-label">
						{{ getShortLabel(tab) }}
					</span>
				</button>

				<button
					class="mobile-nav-item mobile-more-button"
					:class="{ active: showMenu }"
					@click.stop="toggleMenu"
				>
					<span class="mobile-nav-icon">
						<component
							:is="showMenu ? icons['X'] : icons['Menu']"
							class="size-5"
						/>
					</span>

					<span class="mobile-nav-label">
						{{ __('Más') }}
					</span>
				</button>
			</nav>
		</div>
	</div>
</template>

<script setup>
import { getSidebarLinks } from '@/utils'
import { useRouter } from 'vue-router'
import { call } from 'frappe-ui'
import { computed, onBeforeUnmount, ref, watch } from 'vue'
import { sessionStore } from '@/stores/session'
import { useSettings } from '@/stores/settings'
import { usersStore } from '@/stores/user'
import * as icons from 'lucide-vue-next'

const { logout, user } = sessionStore()
let { isLoggedIn } = sessionStore()
const { sidebarSettings } = useSettings()
const router = useRouter()
const { userResource } = usersStore()

const sidebarLinks = ref([])
const otherLinks = ref([])
const showMenu = ref(false)
const menu = ref(null)
const isModerator = ref(false)
const isInstructor = ref(false)

const fullScreenRoutes = ['AISessions', 'AISessionRoom', 'AISessionChat']

const showBottomSpacer = computed(() => {
	return !fullScreenRoutes.includes(router?.currentRoute?.value?.name)
})

const profileUsername = computed(() => {
	return (
		userResource.data?.username ||
		userResource.data?.name ||
		userResource.data?.email ||
		''
	)
})

const userLabel = computed(() => {
	return (
		userResource.data?.first_name ||
		userResource.data?.full_name ||
		userResource.data?.username ||
		userResource.data?.name ||
		'StudyBadger'
	)
})

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

onBeforeUnmount(() => {
	document.removeEventListener('click', handleOutsideClick)
})

const destructureSidebarLinks = () => {
	const links = []

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
		label,
		icon,
		to,
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

				const bottomTabs = pickBottomTabs(sidebarLinks.value)
				const bottomLabels = bottomTabs.map((item) => item.label)

				const extraLinks = sidebarLinks.value
					.filter((link) => !bottomLabels.includes(link.label))
					.map((link) => ({
						label: link.label,
						icon: link.icon,
						to: link.to,
						activeFor: link.activeFor,
					}))

				sidebarLinks.value = bottomTabs
				otherLinks.value = [...extraLinks]

				addOtherLinks()
			},
		}
	)
}

const pickBottomTabs = (links) => {
	const priority = [
		'Home',
		'Inicio',
		'Courses',
		'Cursos',
		'Practice',
		'Practicar',
		'Prompt Library',
		'Prompts',
		'Certificates',
		'Certificados',
	]

	const selected = []

	priority.forEach((label) => {
		const found = links.find((link) => link.label === label)

		if (found && !selected.some((item) => item.label === found.label)) {
			selected.push(found)
		}
	})

	links.forEach((link) => {
		if (selected.length >= 4) return
		if (!selected.some((item) => item.label === link.label)) {
			selected.push(link)
		}
	})

	return selected.slice(0, 4)
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

	const canAddProgram = await checkIfCanAddProgram()

	if (!canAddProgram) return

	sidebarLinks.value.splice(1, 0, {
		label: 'Programs',
		icon: 'Route',
		to: 'Programs',
		activeFor: ['Programs', 'ProgramDetail'],
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

const isActive = (tab) => {
	return tab.activeFor?.includes(router.currentRoute.value.name)
}

const handleClick = (tab) => {
	if (tab.label === 'Iniciar sesión') {
		window.location.href = '/login'
		return
	}

	if (tab.label === 'Cerrar sesión') {
		logout.submit().then(() => {
			isLoggedIn = false
		})
		return
	}

	if (tab.label === 'Perfil' && profileUsername.value) {
		router.push({
			name: 'Profile',
			params: {
				username: profileUsername.value,
			},
		})
		return
	}

	if (tab.to) {
		router.push({ name: tab.to })
	}
}

const isVisible = (tab) => {
	if (tab.label === 'Iniciar sesión') return !isLoggedIn
	if (tab.label === 'Cerrar sesión') return isLoggedIn

	return true
}

const visibleBottomTabs = computed(() => {
	return sidebarLinks.value.filter((tab) => isVisible(tab)).slice(0, 4)
})

const quickSheetLinks = computed(() => {
	return sidebarLinks.value.filter((tab) => isVisible(tab)).slice(0, 4)
})

const toggleMenu = () => {
	showMenu.value = !showMenu.value
}

const getShortLabel = (tab) => {
	const map = {
		Home: __('Inicio'),
		Inicio: __('Inicio'),
		Courses: __('Cursos'),
		Cursos: __('Cursos'),
		Practice: __('IA'),
		Practicar: __('IA'),
		'Prompt Library': __('Prompts'),
		Prompts: __('Prompts'),
		Certificates: __('Cert.'),
		Certificados: __('Cert.'),
		Programs: __('Rutas'),
		Quizzes: __('Tests'),
		Assignments: __('Tareas'),
		Notifications: __('Notif.'),
		Notificaciones: __('Notif.'),
	}

	return map[tab.label] || __(tab.label)
}

const getLinkDescription = (link) => {
	const map = {
		Referidos: __('Invita amigos y gana recompensas.'),
		Notificaciones: __('Revisa avisos y actualizaciones.'),
		Perfil: __('Edita tu información y certificados.'),
		'Cerrar sesión': __('Salir de tu cuenta.'),
		'Iniciar sesión': __('Accede a tu cuenta.'),
		Quizzes: __('Gestiona evaluaciones rápidas.'),
		Assignments: __('Revisa tareas y entregas.'),
		'Programming Exercises': __('Ejercicios de programación.'),
		Programs: __('Rutas y programas de aprendizaje.'),
		Courses: __('Explora cursos disponibles.'),
		Cursos: __('Explora cursos disponibles.'),
	}

	return map[link.label] || __('Abrir sección')
}
</script>

<style scoped>
.mobile-layout {
	--mobile-primary: #0a2251;
	--mobile-primary-hover: #12356f;
	--mobile-bg: #f5f8fc;
	--mobile-card: #ffffff;
	--mobile-text: #0f172a;
	--mobile-muted: #64748b;
	--mobile-soft: #94a3b8;
	--mobile-border: #d7e2f0;
	--mobile-gold: #f5b301;
	--mobile-green: #16a34a;
	--mobile-shadow: 0 24px 70px rgba(10, 34, 81, 0.18);

	position: relative;
	display: flex;
	height: 100dvh;
	flex-direction: column;
	background: var(--mobile-bg);
	color: var(--mobile-text);
	overflow: hidden;
}

:global(:root[data-theme='dark']) .mobile-layout {
	--mobile-bg: #07111f;
	--mobile-card: #101a2b;
	--mobile-text: #f8fafc;
	--mobile-muted: #cbd5e1;
	--mobile-soft: #94a3b8;
	--mobile-border: rgba(255, 255, 255, 0.1);
	--mobile-shadow: 0 24px 70px rgba(0, 0, 0, 0.34);
}

.mobile-scroll {
	flex: 1;
	overflow-y: auto;
	background: var(--mobile-bg);
	-webkit-overflow-scrolling: touch;
}

.mobile-scroll.menu-open {
	overflow: hidden;
}

.mobile-bottom-spacer {
	width: 100%;
	height: calc(96px + env(safe-area-inset-bottom));
	flex-shrink: 0;
}

.mobile-nav-layer {
	position: relative;
	z-index: 50;
}

.mobile-menu-overlay {
	position: fixed;
	inset: 0;
	z-index: 60;
	background: rgba(2, 6, 23, 0.52);
	backdrop-filter: blur(8px);
}

.mobile-sheet {
	position: fixed;
	left: 10px;
	right: 10px;
	bottom: calc(82px + env(safe-area-inset-bottom));
	z-index: 70;
	max-height: min(74dvh, 640px);
	overflow-y: auto;
	border: 1px solid rgba(255, 255, 255, 0.14);
	border-radius: 28px;
	background: #07111f;
	color: #ffffff;
	padding: 0.8rem;
	box-shadow: 0 30px 90px rgba(0, 0, 0, 0.42);
	scrollbar-width: none;
}

.mobile-sheet::-webkit-scrollbar {
	display: none;
}

.mobile-sheet-handle {
	width: 44px;
	height: 5px;
	margin: 0.25rem auto 0.9rem;
	border-radius: 999px;
	background: rgba(255, 255, 255, 0.22);
}

.mobile-sheet-header {
	display: flex;
	align-items: center;
	justify-content: space-between;
	gap: 1rem;
	padding: 0 0.25rem 0.8rem;
}

.mobile-sheet-header p {
	margin: 0;
	color: rgba(226, 232, 240, 0.62);
	font-size: 0.72rem;
	font-weight: 950;
	letter-spacing: 0.08em;
	text-transform: uppercase;
}

.mobile-sheet-header h2 {
	margin: 0.2rem 0 0;
	color: #ffffff;
	font-size: 1.5rem;
	font-weight: 950;
	letter-spacing: -0.045em;
}

.mobile-sheet-close {
	display: grid;
	place-items: center;
	width: 42px;
	height: 42px;
	border: 1px solid rgba(255, 255, 255, 0.12);
	border-radius: 16px;
	background: rgba(255, 255, 255, 0.08);
	color: #ffffff;
	cursor: pointer;
}

.mobile-user-card {
	display: grid;
	grid-template-columns: 44px minmax(0, 1fr) auto;
	gap: 0.75rem;
	align-items: center;
	margin-bottom: 0.75rem;
	border: 1px solid rgba(255, 255, 255, 0.1);
	border-radius: 22px;
	background: rgba(255, 255, 255, 0.07);
	padding: 0.85rem;
}

.mobile-user-avatar {
	display: grid;
	place-items: center;
	width: 44px;
	height: 44px;
	border-radius: 16px;
	background: rgba(147, 197, 253, 0.14);
	color: #bfdbfe;
}

.mobile-user-copy {
	min-width: 0;
}

.mobile-user-copy strong {
	display: block;
	overflow: hidden;
	color: #ffffff;
	font-size: 0.95rem;
	font-weight: 950;
	text-overflow: ellipsis;
	white-space: nowrap;
}

.mobile-user-copy span {
	display: block;
	margin-top: 0.15rem;
	color: rgba(226, 232, 240, 0.62);
	font-size: 0.78rem;
}

.mobile-user-badge {
	border-radius: 999px;
	background: rgba(245, 179, 1, 0.16);
	padding: 0.38rem 0.55rem;
	color: #fde68a;
	font-size: 0.68rem;
	font-weight: 950;
}

.mobile-sheet-section {
	margin-top: 0.8rem;
}

.mobile-section-title {
	margin-bottom: 0.55rem;
	padding: 0 0.2rem;
	color: rgba(226, 232, 240, 0.5);
	font-size: 0.68rem;
	font-weight: 950;
	letter-spacing: 0.08em;
	text-transform: uppercase;
}

.mobile-quick-grid {
	display: grid;
	grid-template-columns: repeat(2, minmax(0, 1fr));
	gap: 0.65rem;
}

.mobile-quick-card {
	display: flex;
	min-height: 96px;
	flex-direction: column;
	align-items: flex-start;
	justify-content: space-between;
	border: 1px solid rgba(255, 255, 255, 0.1);
	border-radius: 20px;
	background: rgba(255, 255, 255, 0.07);
	padding: 0.85rem;
	color: #ffffff;
	text-align: left;
	cursor: pointer;
	transition: 0.18s ease;
}

.mobile-quick-card.active,
.mobile-quick-card:hover {
	border-color: rgba(147, 197, 253, 0.32);
	background: rgba(147, 197, 253, 0.15);
}

.mobile-quick-icon {
	display: grid;
	place-items: center;
	width: 40px;
	height: 40px;
	border-radius: 15px;
	background: rgba(255, 255, 255, 0.1);
	color: #bfdbfe;
}

.mobile-quick-card span {
	display: block;
	color: #ffffff;
	font-size: 0.85rem;
	font-weight: 900;
	line-height: 1.2;
}

.mobile-link-list {
	display: grid;
	gap: 0.5rem;
}

.mobile-sheet-link {
	display: grid;
	grid-template-columns: 44px minmax(0, 1fr) 18px;
	gap: 0.75rem;
	align-items: center;
	width: 100%;
	border: 1px solid rgba(255, 255, 255, 0.08);
	border-radius: 18px;
	background: rgba(255, 255, 255, 0.055);
	padding: 0.75rem;
	color: #ffffff;
	text-align: left;
	cursor: pointer;
	transition: 0.18s ease;
}

.mobile-sheet-link:hover,
.mobile-sheet-link.active {
	border-color: rgba(147, 197, 253, 0.28);
	background: rgba(147, 197, 253, 0.13);
}

.mobile-sheet-link.danger {
	color: #fecaca;
}

.mobile-sheet-link.danger .mobile-sheet-link-icon {
	background: rgba(239, 68, 68, 0.14);
	color: #fecaca;
}

.mobile-sheet-link-icon {
	display: grid;
	place-items: center;
	width: 44px;
	height: 44px;
	border-radius: 16px;
	background: rgba(255, 255, 255, 0.09);
	color: #bfdbfe;
}

.mobile-sheet-link-copy {
	min-width: 0;
}

.mobile-sheet-link-copy strong {
	display: block;
	color: currentColor;
	font-size: 0.9rem;
	font-weight: 950;
	line-height: 1.2;
}

.mobile-sheet-link-copy span {
	display: block;
	margin-top: 0.18rem;
	overflow: hidden;
	color: rgba(226, 232, 240, 0.58);
	font-size: 0.75rem;
	line-height: 1.35;
	text-overflow: ellipsis;
	white-space: nowrap;
}

.mobile-bottom-nav {
	position: fixed;
	left: 10px;
	right: 10px;
	bottom: calc(10px + env(safe-area-inset-bottom));
	z-index: 80;
	display: grid;
	grid-template-columns: repeat(5, minmax(0, 1fr));
	gap: 0.25rem;
	border: 1px solid rgba(255, 255, 255, 0.12);
	border-radius: 26px;
	background: rgba(7, 17, 31, 0.94);
	padding: 0.42rem;
	box-shadow: 0 20px 60px rgba(0, 0, 0, 0.35);
	backdrop-filter: blur(20px);
}

.mobile-nav-item {
	position: relative;
	display: flex;
	min-width: 0;
	min-height: 58px;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	gap: 0.25rem;
	border: 0;
	border-radius: 19px;
	background: transparent;
	color: rgba(226, 232, 240, 0.58);
	cursor: pointer;
	transition: 0.18s ease;
}

.mobile-nav-item.active {
	background: rgba(255, 255, 255, 0.1);
	color: #ffffff;
}

.mobile-nav-item.active::before {
	content: "";
	position: absolute;
	top: 7px;
	width: 5px;
	height: 5px;
	border-radius: 999px;
	background: var(--mobile-gold);
}

.mobile-nav-icon {
	display: grid;
	place-items: center;
	height: 22px;
}

.mobile-nav-label {
	display: block;
	max-width: 100%;
	overflow: hidden;
	padding: 0 0.1rem;
	font-size: 0.66rem;
	font-weight: 850;
	line-height: 1;
	text-overflow: ellipsis;
	white-space: nowrap;
}

.mobile-more-button.active {
	background: var(--mobile-primary);
	color: #ffffff;
}

.mobile-overlay-enter-active,
.mobile-overlay-leave-active {
	transition: opacity 0.2s ease;
}

.mobile-overlay-enter-from,
.mobile-overlay-leave-to {
	opacity: 0;
}

.mobile-sheet-enter-active,
.mobile-sheet-leave-active {
	transition:
		transform 0.24s ease,
		opacity 0.24s ease;
}

.mobile-sheet-enter-from,
.mobile-sheet-leave-to {
	opacity: 0;
	transform: translateY(24px) scale(0.96);
}

@media (max-width: 360px) {
	.mobile-bottom-nav {
		left: 6px;
		right: 6px;
		border-radius: 22px;
	}

	.mobile-nav-label {
		font-size: 0.61rem;
	}

	.mobile-sheet {
		left: 6px;
		right: 6px;
	}
}
</style>