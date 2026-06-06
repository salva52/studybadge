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

		<div class="mobile-nav-layer">
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

					<div v-if="isUserLoggedIn" class="mobile-user-card">
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
								:key="link.key"
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

					<div
						v-for="group in mobileSheetGroups"
						:key="group.title"
						class="mobile-sheet-section"
					>
						<div class="mobile-section-title">
							{{ __(group.title) }}
						</div>

						<div class="mobile-link-list">
							<button
								v-for="link in group.links"
								:key="link.key"
								class="mobile-sheet-link"
								:class="{
									active: isActive(link),
									danger: link.key === 'logout',
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
					:key="tab.key"
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
const showMenu = ref(false)
const menu = ref(null)
const isModerator = ref(false)
const isInstructor = ref(false)

const fullScreenRoutes = ['AISessions', 'AISessionRoom', 'AISessionChat']

const showBottomSpacer = computed(() => {
	return !fullScreenRoutes.includes(router?.currentRoute?.value?.name)
})

const unwrap = (value) => {
	if (value && typeof value === 'object' && 'value' in value) {
		return value.value
	}

	return value
}

const currentUser = computed(() => {
	return userResource.data || unwrap(user) || null
})

const isUserLoggedIn = computed(() => {
	return Boolean(isLoggedIn || currentUser.value)
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

const mobileNavConfig = [
	{
		key: 'inicio',
		label: 'Inicio',
		shortLabel: 'Inicio',
		icon: 'Home',
		to: 'Home',
		path: '/',
		aliases: ['Home', 'Inicio'],
		activeFor: ['Home'],
	},
	{
		key: 'buscar',
		label: 'Buscar',
		shortLabel: 'Buscar',
		icon: 'Search',
		to: 'Search',
		path: '/search',
		aliases: ['Search', 'Buscar'],
		activeFor: ['Search'],
	},
	{
		key: 'notificaciones',
		label: 'Notificaciones',
		shortLabel: 'Notif.',
		icon: 'Bell',
		to: 'Notifications',
		path: '/notifications',
		aliases: ['Notifications', 'Notificaciones'],
		activeFor: ['Notifications'],
	},
	{
		key: 'referidos',
		label: 'Referidos',
		shortLabel: 'Referidos',
		icon: 'Gift',
		to: 'Referrals',
		path: '/referrals',
		aliases: ['Referrals', 'Referidos', 'Referidos StudyBadge'],
		activeFor: ['Referrals'],
	},
	{
		key: 'cursos',
		label: 'Cursos',
		shortLabel: 'Cursos',
		icon: 'BookOpen',
		to: 'Courses',
		path: '/courses',
		aliases: ['Courses', 'Cursos'],
		activeFor: ['Courses', 'CourseDetail', 'Lesson'],
	},
	{
		key: 'sesiones-ia',
		label: 'Sesiones IA',
		shortLabel: 'IA',
		icon: 'MessagesSquare',
		to: 'AISessions',
		path: '/ai-sessions',
		aliases: ['AISessions', 'AI Sessions', 'Sesiones IA', 'Sesiones de IA'],
		activeFor: ['AISessions', 'AISessionRoom', 'AISessionChat'],
	},
	{
		key: 'calendario-ia',
		label: 'Calendario IA',
		shortLabel: 'Agenda',
		icon: 'CalendarDays',
		to: 'StudyCalendar',
		path: '/study-calendar',
		aliases: ['StudyCalendar', 'Calendario IA', 'Coach IA Plus'],
		activeFor: ['StudyCalendar'],
	},
	{
		key: 'estudio-ia',
		label: 'Estudio IA',
		shortLabel: 'Estudio',
		icon: 'Sparkles',
		to: 'Study',
		path: '/study',
		aliases: ['Study', 'Estudio IA', 'AI Study', 'Estudiar con IA'],
		activeFor: ['Study', 'AIStudy'],
	},
	{
		key: 'grupos',
		label: 'Grupos',
		shortLabel: 'Grupos',
		icon: 'UsersRound',
		to: 'Groups',
		path: '/groups',
		aliases: ['Groups', 'Grupos'],
		activeFor: ['Groups', 'GroupDetail'],
	},
	{
		key: 'simulaciones-ia',
		label: 'Simulaciones IA',
		shortLabel: 'Simular',
		icon: 'BrainCircuit',
		to: 'Practice',
		path: '/practice',
		aliases: ['Practice', 'Practicar', 'Simulaciones IA', 'Simulations', 'AI Simulations'],
		activeFor: ['Practice', 'Simulation', 'AISimulations'],
	},
	{
		key: 'biblioteca-prompts',
		label: 'Biblioteca de prompts',
		shortLabel: 'Prompts',
		icon: 'Library',
		to: 'PromptLibrary',
		path: '/prompt-library',
		aliases: ['Prompt Library', 'Biblioteca de prompts', 'Prompts', 'Biblioteca'],
		activeFor: ['PromptLibrary', 'Prompts'],
	},
	{
		key: 'plus',
		label: 'StudyBadge Plus',
		shortLabel: 'Plus',
		icon: 'BadgeCheck',
		to: 'StudyBadgePlus',
		path: '/plus',
		aliases: ['StudyBadge Plus', 'Plus', 'Subscription', 'Billing'],
		activeFor: ['StudyBadgePlus', 'Plus', 'Billing'],
	},
	{
		key: 'rankings',
		label: 'Rankings',
		shortLabel: 'Ranking',
		icon: 'Trophy',
		to: 'Rankings',
		path: '/rankings',
		aliases: ['Rankings', 'Ranking', 'Leaderboard'],
		activeFor: ['Rankings', 'Leaderboard'],
	},
	{
		key: 'ayuda',
		label: 'Ayuda',
		shortLabel: 'Ayuda',
		icon: 'CircleHelp',
		to: 'Help',
		path: '/help',
		aliases: ['Help', 'Ayuda', 'Support', 'Soporte'],
		activeFor: ['Help', 'Support'],
	},
]

const bottomNavKeys = ['inicio', 'buscar', 'cursos', 'sesiones-ia']
const quickNavKeys = [
	'calendario-ia',
	'estudio-ia',
	'simulaciones-ia',
	'biblioteca-prompts',
	'plus',
]

const secondaryGroups = [
	{
		title: 'Aprendizaje',
		keys: ['notificaciones', 'referidos', 'grupos', 'rankings'],
	},
	{
		title: 'Más opciones',
		keys: ['ayuda'],
	},
]

const normalize = (value = '') => {
	return String(value)
		.toLowerCase()
		.normalize('NFD')
		.replace(/[\u0300-\u036f]/g, '')
		.replace(/[^a-z0-9]/g, '')
}

const flattenSidebarLinks = (links = []) => {
	const result = []

	links.forEach((link) => {
		if (link.items?.length) {
			link.items.forEach((item) => result.push(item))
		} else {
			result.push(link)
		}
	})

	return result.filter(Boolean)
}

const filterLinksToShow = (links, data = {}) => {
	let filteredLinks = [...links]

	Object.keys(data || {}).forEach((key) => {
		if (!parseInt(data[key])) {
			filteredLinks = filteredLinks.filter(
				(link) => normalize(link.label) !== normalize(key)
			)
		}
	})

	return filteredLinks.filter((link) => normalize(link.label) !== 'programs')
}

const linkMatchesConfig = (link, config) => {
	const aliases = [config.label, config.to, ...(config.aliases || [])].map(normalize)

	return (
		aliases.includes(normalize(link.label)) ||
		aliases.includes(normalize(link.to))
	)
}

const resolveNavItem = (config) => {
	const found = sidebarLinks.value.find((link) => linkMatchesConfig(link, config))

	return {
		...config,
		label: config.label,
		icon: config.icon,
		to: found?.to || config.to,
		path: found?.path || found?.route || config.path,
		href: found?.href || config.href,
		activeFor: [
			...(config.activeFor || []),
			...(found?.activeFor || []),
			found?.to,
		].filter(Boolean),
	}
}

const getNavItemByKey = (key) => {
	const config = mobileNavConfig.find((item) => item.key === key)
	return config ? resolveNavItem(config) : null
}

const getNavItemsByKeys = (keys) => {
	return keys
		.map((key) => getNavItemByKey(key))
		.filter(Boolean)
}

const visibleBottomTabs = computed(() => {
	return getNavItemsByKeys(bottomNavKeys).filter((tab) => isVisible(tab))
})

const quickSheetLinks = computed(() => {
	return getNavItemsByKeys(quickNavKeys).filter((tab) => isVisible(tab))
})

const accountLinks = computed(() => {
	const links = []

	if (isUserLoggedIn.value) {
		links.push({
			key: 'perfil',
			label: 'Perfil',
			shortLabel: 'Perfil',
			icon: 'UserRound',
			action: 'profile',
			activeFor: ['Profile', 'ProfileCertificates'],
		})

		links.push({
			key: 'logout',
			label: 'Cerrar sesión',
			shortLabel: 'Salir',
			icon: 'LogOut',
			action: 'logout',
		})
	} else {
		links.push({
			key: 'login',
			label: 'Iniciar sesión',
			shortLabel: 'Login',
			icon: 'LogIn',
			action: 'login',
		})
	}

	return links
})

const mobileSheetGroups = computed(() => {
	const groups = secondaryGroups
		.map((group) => ({
			title: group.title,
			links: getNavItemsByKeys(group.keys).filter((link) => isVisible(link)),
		}))
		.filter((group) => group.links.length)

	groups.push({
		title: 'Cuenta',
		links: accountLinks.value,
	})

	return groups
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

const updateSidebarLinks = () => {
	const baseLinks = flattenSidebarLinks(getSidebarLinks(true))
	sidebarLinks.value = baseLinks.filter((link) => normalize(link.label) !== 'programs')

	if (!sidebarSettings?.reload) return

	sidebarSettings.reload(
		{},
		{
			onSuccess: (data) => {
				sidebarLinks.value = filterLinksToShow(baseLinks, data)
			},
		}
	)
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

const isActive = (tab) => {
	const route = router.currentRoute.value
	const routeName = route.name
	const routePath = route.path || ''

	if (tab.activeFor?.includes(routeName)) return true
	if (tab.to && tab.to === routeName) return true

	if (tab.path) {
		if (tab.path === '/') return routePath === '/'
		return routePath.startsWith(tab.path)
	}

	return false
}

const safePush = async (tab) => {
	if (tab.href) {
		window.location.href = tab.href
		return
	}

	if (tab.to && router.hasRoute?.(tab.to)) {
		await router.push({ name: tab.to })
		return
	}

	if (tab.path) {
		await router.push(tab.path)
	}
}

const handleClick = async (tab) => {
	if (tab.action === 'login' || tab.label === 'Iniciar sesión') {
		window.location.href = '/login'
		return
	}

	if (tab.action === 'logout' || tab.label === 'Cerrar sesión') {
		logout.submit().then(() => {
			isLoggedIn = false
		})
		return
	}

	if (tab.action === 'profile' || tab.label === 'Perfil') {
		if (profileUsername.value) {
			router.push({
				name: 'Profile',
				params: {
					username: profileUsername.value,
				},
			})
		}

		return
	}

	try {
		await safePush(tab)
	} catch {
		if (tab.path) {
			window.location.href = tab.path
		}
	}
}

const isVisible = (tab) => {
	if (tab.key === 'login') return !isUserLoggedIn.value
	if (tab.key === 'logout') return isUserLoggedIn.value

	return true
}

const toggleMenu = () => {
	showMenu.value = !showMenu.value
}

const getShortLabel = (tab) => {
	return __(tab.shortLabel || tab.label)
}

const getLinkDescription = (link) => {
	const map = {
		Inicio: __('Vuelve al panel principal.'),
		Buscar: __('Encuentra cursos, sesiones y contenido.'),
		Notificaciones: __('Revisa avisos y actualizaciones.'),
		Referidos: __('Invita personas y revisa tus recompensas.'),
		Cursos: __('Explora tus cursos y lecciones.'),
		'Sesiones IA': __('Continúa tus conversaciones de estudio.'),
		'Estudio IA': __('Estudia con herramientas inteligentes.'),
		Grupos: __('Participa en comunidades de aprendizaje.'),
		'Simulaciones IA': __('Practica con escenarios y ejercicios.'),
		'Biblioteca de prompts': __('Guarda y reutiliza prompts útiles.'),
		'StudyBadge Plus': __('Accede a beneficios y funciones premium.'),
		Rankings: __('Mira tu posición y progreso.'),
		Ayuda: __('Resuelve dudas sobre la plataforma.'),
		Perfil: __('Edita tu información y certificados.'),
		'Cerrar sesión': __('Salir de tu cuenta.'),
		'Iniciar sesión': __('Accede a tu cuenta.'),
	}

	return map[link.label] || __('Abrir sección.')
}
</script>

<style scoped>
.mobile-layout {
	--mobile-primary: #0a2251;
	--mobile-primary-hover: #12356f;
	--mobile-bg: #f5f8fc;
	--mobile-card: #ffffff;
	--mobile-card-soft: #f8fafc;
	--mobile-text: #0f172a;
	--mobile-muted: #64748b;
	--mobile-soft: #94a3b8;
	--mobile-border: #d7e2f0;
	--mobile-border-strong: #b9cbe3;
	--mobile-gold: #f5b301;
	--mobile-red: #ef4444;
	--mobile-shadow: 0 24px 70px rgba(10, 34, 81, 0.16);

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
	--mobile-card-soft: #111d31;
	--mobile-text: #f8fafc;
	--mobile-muted: #cbd5e1;
	--mobile-soft: #94a3b8;
	--mobile-border: rgba(255, 255, 255, 0.1);
	--mobile-border-strong: rgba(255, 255, 255, 0.18);
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
	height: calc(100px + env(safe-area-inset-bottom));
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
	bottom: calc(96px + env(safe-area-inset-bottom));
	z-index: 70;
	max-height: min(78dvh, 680px);
	overflow-y: auto;
	border: 1px solid var(--mobile-border);
	border-radius: 28px;
	background: var(--mobile-card);
	color: var(--mobile-text);
	padding: 0.85rem;
	box-shadow: var(--mobile-shadow);
	scrollbar-width: none;
}

:global(:root[data-theme='dark']) .mobile-sheet {
	background: #07111f;
	color: #ffffff;
}

.mobile-sheet::-webkit-scrollbar {
	display: none;
}

.mobile-sheet-handle {
	width: 44px;
	height: 5px;
	margin: 0.25rem auto 0.9rem;
	border-radius: 999px;
	background: var(--mobile-border-strong);
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
	color: var(--mobile-muted);
	font-size: 0.72rem;
	font-weight: 950;
	letter-spacing: 0.08em;
	text-transform: uppercase;
}

.mobile-sheet-header h2 {
	margin: 0.2rem 0 0;
	color: var(--mobile-text);
	font-size: 1.5rem;
	font-weight: 950;
	letter-spacing: -0.045em;
}

.mobile-sheet-close {
	display: grid;
	place-items: center;
	width: 42px;
	height: 42px;
	border: 1px solid var(--mobile-border);
	border-radius: 16px;
	background: var(--mobile-card-soft);
	color: var(--mobile-text);
	cursor: pointer;
	transition: 0.18s ease;
}

.mobile-sheet-close:hover {
	border-color: var(--mobile-border-strong);
	background: rgba(10, 34, 81, 0.06);
}

:global(:root[data-theme='dark']) .mobile-sheet-close:hover {
	background: rgba(255, 255, 255, 0.08);
}

.mobile-user-card {
	display: grid;
	grid-template-columns: 44px minmax(0, 1fr) auto;
	gap: 0.75rem;
	align-items: center;
	margin-bottom: 0.8rem;
	border: 1px solid var(--mobile-border);
	border-radius: 22px;
	background: var(--mobile-card-soft);
	padding: 0.85rem;
}

.mobile-user-avatar {
	display: grid;
	place-items: center;
	width: 44px;
	height: 44px;
	border-radius: 16px;
	background: rgba(10, 34, 81, 0.08);
	color: var(--mobile-primary);
}

:global(:root[data-theme='dark']) .mobile-user-avatar {
	background: rgba(147, 197, 253, 0.14);
	color: #bfdbfe;
}

.mobile-user-copy {
	min-width: 0;
}

.mobile-user-copy strong {
	display: block;
	overflow: hidden;
	color: var(--mobile-text);
	font-size: 0.95rem;
	font-weight: 950;
	text-overflow: ellipsis;
	white-space: nowrap;
}

.mobile-user-copy span {
	display: block;
	margin-top: 0.15rem;
	color: var(--mobile-muted);
	font-size: 0.78rem;
}

.mobile-user-badge {
	border-radius: 999px;
	background: rgba(245, 179, 1, 0.16);
	padding: 0.38rem 0.55rem;
	color: #9a6700;
	font-size: 0.68rem;
	font-weight: 950;
}

:global(:root[data-theme='dark']) .mobile-user-badge {
	color: #fde68a;
}

.mobile-sheet-section {
	margin-top: 0.85rem;
}

.mobile-section-title {
	margin-bottom: 0.55rem;
	padding: 0 0.2rem;
	color: var(--mobile-soft);
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
	min-height: 100px;
	flex-direction: column;
	align-items: flex-start;
	justify-content: space-between;
	border: 1px solid var(--mobile-border);
	border-radius: 20px;
	background: var(--mobile-card-soft);
	padding: 0.85rem;
	color: var(--mobile-text);
	text-align: left;
	cursor: pointer;
	transition: 0.18s ease;
}

.mobile-quick-card.active,
.mobile-quick-card:hover {
	border-color: rgba(10, 34, 81, 0.26);
	background: rgba(10, 34, 81, 0.055);
	transform: translateY(-1px);
}

:global(:root[data-theme='dark']) .mobile-quick-card.active,
:global(:root[data-theme='dark']) .mobile-quick-card:hover {
	border-color: rgba(147, 197, 253, 0.32);
	background: rgba(147, 197, 253, 0.15);
}

.mobile-quick-icon {
	display: grid;
	place-items: center;
	width: 40px;
	height: 40px;
	border-radius: 15px;
	background: rgba(10, 34, 81, 0.08);
	color: var(--mobile-primary);
}

:global(:root[data-theme='dark']) .mobile-quick-icon {
	background: rgba(255, 255, 255, 0.1);
	color: #bfdbfe;
}

.mobile-quick-card span {
	display: block;
	color: var(--mobile-text);
	font-size: 0.86rem;
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
	border: 1px solid var(--mobile-border);
	border-radius: 18px;
	background: var(--mobile-card-soft);
	padding: 0.75rem;
	color: var(--mobile-text);
	text-align: left;
	cursor: pointer;
	transition: 0.18s ease;
}

.mobile-sheet-link:hover,
.mobile-sheet-link.active {
	border-color: rgba(10, 34, 81, 0.26);
	background: rgba(10, 34, 81, 0.055);
	transform: translateY(-1px);
}

:global(:root[data-theme='dark']) .mobile-sheet-link:hover,
:global(:root[data-theme='dark']) .mobile-sheet-link.active {
	border-color: rgba(147, 197, 253, 0.28);
	background: rgba(147, 197, 253, 0.13);
}

.mobile-sheet-link.danger {
	color: var(--mobile-red);
}

:global(:root[data-theme='dark']) .mobile-sheet-link.danger {
	color: #fecaca;
}

.mobile-sheet-link-icon {
	display: grid;
	place-items: center;
	width: 44px;
	height: 44px;
	border-radius: 16px;
	background: rgba(10, 34, 81, 0.08);
	color: var(--mobile-primary);
}

:global(:root[data-theme='dark']) .mobile-sheet-link-icon {
	background: rgba(255, 255, 255, 0.09);
	color: #bfdbfe;
}

.mobile-sheet-link.danger .mobile-sheet-link-icon {
	background: rgba(239, 68, 68, 0.1);
	color: var(--mobile-red);
}

:global(:root[data-theme='dark']) .mobile-sheet-link.danger .mobile-sheet-link-icon {
	background: rgba(239, 68, 68, 0.14);
	color: #fecaca;
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
	color: var(--mobile-muted);
	font-size: 0.75rem;
	line-height: 1.35;
	text-overflow: ellipsis;
	white-space: nowrap;
}

/* =========================================
   ESTILOS LIQUID GLASS / NAVBAR
   ========================================= */
.mobile-bottom-nav {
	position: fixed;
	left: 16px; /* Ligeramente más metido para dar el efecto de pastilla flotante */
	right: 16px;
	bottom: calc(16px + env(safe-area-inset-bottom));
	z-index: 80;
	display: grid;
	grid-template-columns: repeat(5, minmax(0, 1fr));
	gap: 0.35rem;
	border-radius: 36px;
	padding: 0.5rem;

	/* Efecto Transparente / Liquid Glass */
	background: rgba(255, 255, 255, 0.15); /* Muy transparente */
	backdrop-filter: blur(35px) saturate(250%); /* Alto desenfoque para colores vibrantes de fondo */
	-webkit-backdrop-filter: blur(35px) saturate(250%);

	/* Reflejos en los bordes del cristal */
	border: 1px solid rgba(255, 255, 255, 0.35);
	box-shadow: 
		0 12px 40px -12px rgba(10, 34, 81, 0.2), 
		inset 0 1px 0 rgba(255, 255, 255, 0.8), 
		inset 0 -1px 0 rgba(255, 255, 255, 0.1);
}

:global(:root[data-theme='dark']) .mobile-bottom-nav {
	background: rgba(10, 17, 31, 0.35);
	border: 1px solid rgba(255, 255, 255, 0.15);
	box-shadow: 
		0 12px 40px -12px rgba(0, 0, 0, 0.5), 
		inset 0 1px 0 rgba(255, 255, 255, 0.15), 
		inset 0 -1px 0 rgba(0, 0, 0, 0.3);
}

.mobile-nav-item {
	position: relative;
	display: flex;
	min-width: 0;
	min-height: 56px;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	gap: 0.35rem;
	border: 0;
	border-radius: 22px;
	background: transparent;
	color: var(--mobile-muted);
	cursor: pointer;

	/* Transición elástica y líquida usando curva bezier */
	transition: transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1), background-color 0.2s ease, color 0.2s ease;
	will-change: transform;
}

/* Física "Líquida" al presionar (se hunde) */
.mobile-nav-item:active {
	transform: scale(0.88);
}

/* Estado activo: Pastilla Frost y sobresale sutilmente */
.mobile-nav-item.active {
	background: rgba(255, 255, 255, 0.4);
	color: var(--mobile-primary);
	transform: scale(1.05);
	box-shadow: 
		inset 0 1px 2px rgba(255, 255, 255, 0.6), 
		0 2px 10px rgba(0, 0, 0, 0.05);
}

:global(:root[data-theme='dark']) .mobile-nav-item.active {
	background: rgba(255, 255, 255, 0.15);
	color: #ffffff;
	box-shadow: 
		inset 0 1px 2px rgba(255, 255, 255, 0.1), 
		0 2px 10px rgba(0, 0, 0, 0.2);
}

.mobile-nav-icon {
	display: grid;
	place-items: center;
	height: 22px;
	transition: transform 0.3s ease;
}

/* Sube el ícono un poquito si está activo */
.mobile-nav-item.active .mobile-nav-icon {
	transform: translateY(-2px);
}

.mobile-nav-label {
	display: block;
	max-width: 100%;
	overflow: hidden;
	padding: 0 0.1rem;
	font-size: 0.62rem;
	font-weight: 800;
	line-height: 1;
	text-overflow: ellipsis;
	white-space: nowrap;
	opacity: 0.8;
	transition: opacity 0.3s ease;
}

.mobile-nav-item.active .mobile-nav-label {
	opacity: 1;
}

.mobile-more-button.active {
	background: rgba(10, 34, 81, 0.8);
	color: #ffffff;
	backdrop-filter: blur(10px);
}

:global(:root[data-theme='dark']) .mobile-more-button.active {
	background: rgba(255, 255, 255, 0.8);
	color: #07111f;
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
		left: 10px;
		right: 10px;
		border-radius: 30px;
	}

	.mobile-nav-label {
		font-size: 0.58rem;
	}

	.mobile-sheet {
		left: 6px;
		right: 6px;
	}
}
</style>