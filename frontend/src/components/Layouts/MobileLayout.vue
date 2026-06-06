<template>
	<div class="mobile-layout">
		<div
			id="scrollContainer"
			ref="scrollContainer"
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

			<nav
				class="mobile-bottom-nav"
				:class="{
					'is-compact': isNavCompact && !showMenu && !navPressed,
					'is-expanded': showMenu || navPressed,
				}"
				aria-label="Navegación móvil"
				@pointerdown="pressNav"
				@pointerup="releaseNav"
				@pointercancel="releaseNav"
				@mouseleave="releaseNav"
			>
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
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
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
const scrollContainer = ref(null)
const isNavCompact = ref(false)
const navPressed = ref(false)
const isModerator = ref(false)
const isInstructor = ref(false)

let lastScrollTop = 0
let scrollTicking = false
let navPressTimeout = null

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
		isNavCompact.value = false

		setTimeout(() => {
			document.addEventListener('click', handleOutsideClick)
		}, 0)
	} else {
		document.removeEventListener('click', handleOutsideClick)
	}
})


const updateNavFromScroll = () => {
	const currentScrollTop = scrollContainer.value?.scrollTop || 0
	const delta = currentScrollTop - lastScrollTop

	if (currentScrollTop < 28 || delta < -5) {
		isNavCompact.value = false
	} else if (delta > 6 && currentScrollTop > 52) {
		isNavCompact.value = true
	}

	lastScrollTop = Math.max(currentScrollTop, 0)
	scrollTicking = false
}

const handleMobileScroll = () => {
	if (scrollTicking) return

	scrollTicking = true
	requestAnimationFrame(updateNavFromScroll)
}

const pressNav = () => {
	if (navPressTimeout) {
		clearTimeout(navPressTimeout)
	}

	navPressed.value = true
	isNavCompact.value = false
}

const releaseNav = () => {
	if (navPressTimeout) {
		clearTimeout(navPressTimeout)
	}

	navPressTimeout = setTimeout(() => {
		navPressed.value = false
	}, 140)
}

onMounted(() => {
	scrollContainer.value?.addEventListener('scroll', handleMobileScroll, {
		passive: true,
	})
})

onBeforeUnmount(() => {
	document.removeEventListener('click', handleOutsideClick)
	scrollContainer.value?.removeEventListener('scroll', handleMobileScroll)

	if (navPressTimeout) {
		clearTimeout(navPressTimeout)
	}
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
	--mobile-border: rgba(215, 226, 240, 0.78);
	--mobile-border-strong: rgba(185, 203, 227, 0.9);
	--mobile-gold: #f5b301;
	--mobile-red: #ef4444;
	--mobile-shadow: 0 24px 70px rgba(10, 34, 81, 0.16);
	--mobile-glass: rgba(255, 255, 255, 0.58);
	--mobile-glass-soft: rgba(255, 255, 255, 0.34);
	--mobile-glass-strong: rgba(255, 255, 255, 0.78);
	--mobile-glass-border: rgba(255, 255, 255, 0.66);
	--mobile-glass-shadow: 0 24px 70px rgba(10, 34, 81, 0.22),
		0 6px 18px rgba(10, 34, 81, 0.08),
		inset 0 1px 1px rgba(255, 255, 255, 0.74),
		inset 0 -1px 1px rgba(255, 255, 255, 0.22);
	--mobile-glass-blur: blur(28px) saturate(190%) contrast(105%);

	position: relative;
	display: flex;
	height: 100dvh;
	flex-direction: column;
	background:
		radial-gradient(circle at 12% 0%, rgba(245, 179, 1, 0.14), transparent 28%),
		radial-gradient(circle at 88% 12%, rgba(59, 130, 246, 0.14), transparent 30%),
		linear-gradient(180deg, #f8fbff 0%, var(--mobile-bg) 48%, #edf4ff 100%);
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
	--mobile-glass: rgba(9, 18, 32, 0.58);
	--mobile-glass-soft: rgba(15, 23, 42, 0.38);
	--mobile-glass-strong: rgba(30, 41, 59, 0.72);
	--mobile-glass-border: rgba(255, 255, 255, 0.16);
	--mobile-glass-shadow: 0 24px 70px rgba(0, 0, 0, 0.52),
		0 8px 24px rgba(0, 0, 0, 0.28),
		inset 0 1px 1px rgba(255, 255, 255, 0.18),
		inset 0 -1px 1px rgba(255, 255, 255, 0.08);
}

.mobile-scroll {
	flex: 1;
	overflow-y: auto;
	background: transparent;
	-webkit-overflow-scrolling: touch;
}

.mobile-scroll.menu-open {
	overflow: hidden;
}

.mobile-bottom-spacer {
	width: 100%;
	height: calc(106px + env(safe-area-inset-bottom));
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
	background:
		radial-gradient(circle at 50% 100%, rgba(255, 255, 255, 0.16), transparent 32%),
		rgba(2, 6, 23, 0.42);
	backdrop-filter: blur(14px) saturate(140%);
	-webkit-backdrop-filter: blur(14px) saturate(140%);
}

.mobile-sheet {
	position: fixed;
	left: 12px;
	right: 12px;
	bottom: calc(92px + env(safe-area-inset-bottom));
	z-index: 70;
	max-height: min(78dvh, 680px);
	overflow-y: auto;
	border: 1px solid var(--mobile-glass-border);
	border-radius: 34px;
	background:
		linear-gradient(145deg, rgba(255, 255, 255, 0.68), rgba(255, 255, 255, 0.34)),
		radial-gradient(circle at 15% 0%, rgba(255, 255, 255, 0.9), transparent 30%),
		var(--mobile-glass);
	color: var(--mobile-text);
	padding: 0.9rem;
	box-shadow: var(--mobile-glass-shadow);
	backdrop-filter: var(--mobile-glass-blur);
	-webkit-backdrop-filter: var(--mobile-glass-blur);
	scrollbar-width: none;
	isolation: isolate;
}

.mobile-sheet::before {
	content: "";
	position: sticky;
	top: -0.9rem;
	display: block;
	height: 1px;
	margin: -1px -0.9rem 0;
	background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.9), transparent);
	opacity: 0.8;
	pointer-events: none;
}

:global(:root[data-theme='dark']) .mobile-sheet {
	background:
		linear-gradient(145deg, rgba(15, 23, 42, 0.76), rgba(15, 23, 42, 0.42)),
		radial-gradient(circle at 15% 0%, rgba(96, 165, 250, 0.16), transparent 30%),
		var(--mobile-glass);
	color: #ffffff;
}

.mobile-sheet::-webkit-scrollbar {
	display: none;
}

.mobile-sheet-handle {
	width: 46px;
	height: 5px;
	margin: 0.35rem auto 0.95rem;
	border-radius: 999px;
	background: rgba(15, 23, 42, 0.22);
	box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.8);
}

:global(:root[data-theme='dark']) .mobile-sheet-handle {
	background: rgba(255, 255, 255, 0.26);
	box-shadow: none;
}

.mobile-sheet-header {
	display: flex;
	align-items: center;
	justify-content: space-between;
	gap: 1rem;
	padding: 0 0.25rem 0.85rem;
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
	font-size: 1.55rem;
	font-weight: 950;
	letter-spacing: -0.045em;
}

.mobile-sheet-close {
	display: grid;
	place-items: center;
	width: 42px;
	height: 42px;
	border: 1px solid var(--mobile-glass-border);
	border-radius: 18px;
	background: rgba(255, 255, 255, 0.38);
	color: var(--mobile-text);
	box-shadow:
		inset 0 1px 0 rgba(255, 255, 255, 0.72),
		0 10px 22px rgba(10, 34, 81, 0.08);
	cursor: pointer;
	transition:
		transform 0.18s ease,
		background 0.18s ease,
		border-color 0.18s ease;
}

.mobile-sheet-close:hover {
	border-color: rgba(255, 255, 255, 0.88);
	background: rgba(255, 255, 255, 0.62);
	transform: translateY(-1px) scale(1.02);
}

:global(:root[data-theme='dark']) .mobile-sheet-close {
	background: rgba(255, 255, 255, 0.08);
}

:global(:root[data-theme='dark']) .mobile-sheet-close:hover {
	background: rgba(255, 255, 255, 0.14);
}

.mobile-user-card {
	display: grid;
	grid-template-columns: 44px minmax(0, 1fr) auto;
	gap: 0.75rem;
	align-items: center;
	margin-bottom: 0.8rem;
	border: 1px solid rgba(255, 255, 255, 0.54);
	border-radius: 24px;
	background:
		linear-gradient(135deg, rgba(255, 255, 255, 0.58), rgba(255, 255, 255, 0.26)),
		rgba(255, 255, 255, 0.32);
	padding: 0.85rem;
	box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.62);
}

:global(:root[data-theme='dark']) .mobile-user-card {
	border-color: rgba(255, 255, 255, 0.12);
	background: rgba(255, 255, 255, 0.07);
}

.mobile-user-avatar {
	display: grid;
	place-items: center;
	width: 44px;
	height: 44px;
	border-radius: 18px;
	background:
		linear-gradient(135deg, rgba(10, 34, 81, 0.14), rgba(59, 130, 246, 0.08)),
		rgba(255, 255, 255, 0.45);
	color: var(--mobile-primary);
	box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.78);
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
	border: 1px solid rgba(245, 179, 1, 0.24);
	border-radius: 999px;
	background: rgba(245, 179, 1, 0.16);
	padding: 0.38rem 0.55rem;
	color: #9a6700;
	font-size: 0.68rem;
	font-weight: 950;
	box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.44);
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
	border: 1px solid rgba(255, 255, 255, 0.52);
	border-radius: 22px;
	background:
		linear-gradient(135deg, rgba(255, 255, 255, 0.52), rgba(255, 255, 255, 0.18)),
		rgba(255, 255, 255, 0.28);
	padding: 0.85rem;
	color: var(--mobile-text);
	text-align: left;
	box-shadow:
		inset 0 1px 0 rgba(255, 255, 255, 0.68),
		0 12px 28px rgba(10, 34, 81, 0.08);
	cursor: pointer;
	transition:
		transform 0.18s ease,
		background 0.18s ease,
		border-color 0.18s ease,
		box-shadow 0.18s ease;
}

.mobile-quick-card.active,
.mobile-quick-card:hover {
	border-color: rgba(10, 34, 81, 0.22);
	background:
		linear-gradient(135deg, rgba(255, 255, 255, 0.7), rgba(245, 179, 1, 0.14)),
		rgba(10, 34, 81, 0.055);
	box-shadow:
		inset 0 1px 0 rgba(255, 255, 255, 0.75),
		0 16px 34px rgba(10, 34, 81, 0.12);
	transform: translateY(-2px);
}

:global(:root[data-theme='dark']) .mobile-quick-card {
	border-color: rgba(255, 255, 255, 0.1);
	background: rgba(255, 255, 255, 0.06);
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
	border-radius: 17px;
	background:
		linear-gradient(135deg, rgba(10, 34, 81, 0.12), rgba(59, 130, 246, 0.08)),
		rgba(255, 255, 255, 0.38);
	color: var(--mobile-primary);
	box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.72);
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
	border: 1px solid rgba(255, 255, 255, 0.5);
	border-radius: 20px;
	background:
		linear-gradient(135deg, rgba(255, 255, 255, 0.5), rgba(255, 255, 255, 0.18)),
		rgba(255, 255, 255, 0.26);
	padding: 0.75rem;
	color: var(--mobile-text);
	text-align: left;
	box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.62);
	cursor: pointer;
	transition:
		transform 0.18s ease,
		background 0.18s ease,
		border-color 0.18s ease,
		box-shadow 0.18s ease;
}

.mobile-sheet-link:hover,
.mobile-sheet-link.active {
	border-color: rgba(10, 34, 81, 0.22);
	background:
		linear-gradient(135deg, rgba(255, 255, 255, 0.68), rgba(245, 179, 1, 0.12)),
		rgba(10, 34, 81, 0.055);
	box-shadow:
		inset 0 1px 0 rgba(255, 255, 255, 0.7),
		0 12px 28px rgba(10, 34, 81, 0.09);
	transform: translateY(-1px);
}

:global(:root[data-theme='dark']) .mobile-sheet-link {
	border-color: rgba(255, 255, 255, 0.1);
	background: rgba(255, 255, 255, 0.06);
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
	border-radius: 18px;
	background:
		linear-gradient(135deg, rgba(10, 34, 81, 0.12), rgba(59, 130, 246, 0.08)),
		rgba(255, 255, 255, 0.36);
	color: var(--mobile-primary);
	box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.68);
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

.mobile-bottom-nav {
	position: fixed;
	left: 12px;
	right: 12px;
	bottom: calc(12px + env(safe-area-inset-bottom));
	z-index: 80;
	display: grid;
	grid-template-columns: repeat(5, minmax(0, 1fr));
	gap: 0.28rem;
	min-height: 72px;
	border: 1px solid var(--mobile-glass-border);
	border-radius: 34px;
	background:
		radial-gradient(circle at 12% 0%, rgba(255, 255, 255, 0.95), transparent 28%),
		radial-gradient(circle at 84% 120%, rgba(245, 179, 1, 0.2), transparent 34%),
		linear-gradient(135deg, rgba(255, 255, 255, 0.68), rgba(255, 255, 255, 0.28)),
		var(--mobile-glass);
	padding: 0.42rem;
	box-shadow: var(--mobile-glass-shadow);
	backdrop-filter: var(--mobile-glass-blur);
	-webkit-backdrop-filter: var(--mobile-glass-blur);
	isolation: isolate;
	overflow: hidden;
	transform: translateZ(0);
	transform-origin: bottom center;
	transition:
		left 0.34s cubic-bezier(0.22, 1, 0.36, 1),
		right 0.34s cubic-bezier(0.22, 1, 0.36, 1),
		bottom 0.34s cubic-bezier(0.22, 1, 0.36, 1),
		min-height 0.34s cubic-bezier(0.22, 1, 0.36, 1),
		border-radius 0.34s cubic-bezier(0.22, 1, 0.36, 1),
		padding 0.34s cubic-bezier(0.22, 1, 0.36, 1),
		transform 0.34s cubic-bezier(0.22, 1, 0.36, 1),
		opacity 0.24s ease,
		box-shadow 0.34s ease;
}

.mobile-bottom-nav::before {
	content: "";
	position: absolute;
	inset: 1px 1px auto;
	height: 46%;
	border-radius: inherit;
	background:
		linear-gradient(180deg, rgba(255, 255, 255, 0.72), rgba(255, 255, 255, 0)),
		radial-gradient(circle at 28% 12%, rgba(255, 255, 255, 0.95), transparent 32%);
	opacity: 0.78;
	pointer-events: none;
	z-index: -1;
}

.mobile-bottom-nav::after {
	content: "";
	position: absolute;
	inset: 0;
	border-radius: inherit;
	background:
		linear-gradient(115deg, transparent 0%, rgba(255, 255, 255, 0.5) 36%, transparent 48%),
		radial-gradient(circle at 78% 24%, rgba(255, 255, 255, 0.48), transparent 28%);
	mix-blend-mode: screen;
	opacity: 0.46;
	pointer-events: none;
	transform: translateX(-16%);
	transition: transform 0.42s ease, opacity 0.24s ease;
}

.mobile-bottom-nav.is-expanded,
.mobile-bottom-nav:active {
	left: 10px;
	right: 10px;
	bottom: calc(14px + env(safe-area-inset-bottom));
	min-height: 76px;
	border-radius: 36px;
	box-shadow:
		0 30px 80px rgba(10, 34, 81, 0.26),
		0 12px 28px rgba(10, 34, 81, 0.12),
		inset 0 1px 1px rgba(255, 255, 255, 0.78);
	transform: translateY(-3px) scale(1.012);
}

.mobile-bottom-nav.is-expanded::after,
.mobile-bottom-nav:active::after {
	opacity: 0.72;
	transform: translateX(12%);
}

.mobile-bottom-nav.is-compact {
	left: 54px;
	right: 54px;
	bottom: calc(10px + env(safe-area-inset-bottom));
	min-height: 54px;
	border-radius: 999px;
	padding: 0.32rem;
	opacity: 0.94;
	box-shadow:
		0 18px 48px rgba(10, 34, 81, 0.2),
		inset 0 1px 1px rgba(255, 255, 255, 0.62);
	transform: translateY(5px) scale(0.965);
}

:global(:root[data-theme='dark']) .mobile-bottom-nav {
	background:
		radial-gradient(circle at 18% 0%, rgba(96, 165, 250, 0.2), transparent 32%),
		radial-gradient(circle at 84% 120%, rgba(245, 179, 1, 0.12), transparent 34%),
		linear-gradient(135deg, rgba(15, 23, 42, 0.76), rgba(15, 23, 42, 0.4)),
		var(--mobile-glass);
}

:global(:root[data-theme='dark']) .mobile-bottom-nav::before {
	background:
		linear-gradient(180deg, rgba(255, 255, 255, 0.16), rgba(255, 255, 255, 0)),
		radial-gradient(circle at 28% 12%, rgba(255, 255, 255, 0.18), transparent 32%);
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
	border: 1px solid transparent;
	border-radius: 23px;
	background: transparent;
	color: var(--mobile-muted);
	cursor: pointer;
	-webkit-tap-highlight-color: transparent;
	transition:
		min-height 0.28s cubic-bezier(0.22, 1, 0.36, 1),
		border-radius 0.28s cubic-bezier(0.22, 1, 0.36, 1),
		transform 0.18s ease,
		background 0.18s ease,
		border-color 0.18s ease,
		color 0.18s ease;
}

.mobile-nav-item::before {
	content: "";
	position: absolute;
	inset: 5px 8px auto;
	height: 32%;
	border-radius: inherit;
	background: linear-gradient(180deg, rgba(255, 255, 255, 0.68), transparent);
	opacity: 0;
	pointer-events: none;
	transition: opacity 0.18s ease;
}

.mobile-nav-item:hover,
.mobile-nav-item:focus-visible {
	color: var(--mobile-primary);
	transform: translateY(-1px);
}

.mobile-nav-item.active {
	border-color: rgba(255, 255, 255, 0.54);
	background:
		linear-gradient(145deg, rgba(255, 255, 255, 0.7), rgba(255, 255, 255, 0.24)),
		linear-gradient(135deg, rgba(10, 34, 81, 0.14), rgba(245, 179, 1, 0.1));
	color: var(--mobile-primary);
	box-shadow:
		inset 0 1px 0 rgba(255, 255, 255, 0.82),
		0 10px 24px rgba(10, 34, 81, 0.12);
}

.mobile-nav-item.active::before {
	opacity: 1;
}

:global(:root[data-theme='dark']) .mobile-nav-item:hover,
:global(:root[data-theme='dark']) .mobile-nav-item:focus-visible {
	color: #ffffff;
}

:global(:root[data-theme='dark']) .mobile-nav-item.active {
	border-color: rgba(255, 255, 255, 0.16);
	background:
		linear-gradient(145deg, rgba(255, 255, 255, 0.13), rgba(255, 255, 255, 0.05)),
		rgba(147, 197, 253, 0.14);
	color: #ffffff;
	box-shadow:
		inset 0 1px 0 rgba(255, 255, 255, 0.18),
		0 10px 24px rgba(0, 0, 0, 0.24);
}

.mobile-nav-item.active::after {
	content: "";
	position: absolute;
	top: 7px;
	width: 5px;
	height: 5px;
	border-radius: 999px;
	background: var(--mobile-gold);
	box-shadow: 0 0 12px rgba(245, 179, 1, 0.72);
}

.mobile-bottom-nav.is-compact .mobile-nav-item {
	min-height: 42px;
	border-radius: 999px;
	gap: 0;
}

.mobile-bottom-nav.is-compact .mobile-nav-item.active::after {
	top: 5px;
	width: 4px;
	height: 4px;
}

.mobile-nav-icon {
	display: grid;
	place-items: center;
	height: 22px;
	transition:
		transform 0.24s cubic-bezier(0.22, 1, 0.36, 1),
		filter 0.18s ease;
}

.mobile-nav-item.active .mobile-nav-icon,
.mobile-nav-item:hover .mobile-nav-icon {
	filter: drop-shadow(0 4px 8px rgba(10, 34, 81, 0.18));
	transform: translateY(-1px) scale(1.06);
}

.mobile-bottom-nav.is-compact .mobile-nav-icon {
	transform: scale(1.03);
}

.mobile-nav-label {
	display: block;
	max-width: 100%;
	overflow: hidden;
	padding: 0 0.1rem;
	font-size: 0.66rem;
	font-weight: 900;
	letter-spacing: -0.01em;
	line-height: 1;
	text-overflow: ellipsis;
	white-space: nowrap;
	transition:
		opacity 0.2s ease,
		transform 0.24s ease,
		max-height 0.24s ease,
		margin 0.24s ease;
}

.mobile-bottom-nav.is-compact .mobile-nav-label {
	max-height: 0;
	margin-top: -0.25rem;
	opacity: 0;
	transform: translateY(6px) scale(0.92);
}

.mobile-bottom-nav.is-expanded .mobile-nav-label,
.mobile-bottom-nav:active .mobile-nav-label {
	opacity: 1;
	transform: translateY(0) scale(1);
}

.mobile-more-button.active {
	border-color: rgba(255, 255, 255, 0.62);
	background:
		linear-gradient(145deg, rgba(10, 34, 81, 0.96), rgba(18, 53, 111, 0.86)),
		radial-gradient(circle at 30% 0%, rgba(255, 255, 255, 0.28), transparent 32%);
	color: #ffffff;
	box-shadow:
		0 12px 26px rgba(10, 34, 81, 0.22),
		inset 0 1px 0 rgba(255, 255, 255, 0.26);
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
		transform 0.28s cubic-bezier(0.22, 1, 0.36, 1),
		opacity 0.24s ease;
}

.mobile-sheet-enter-from,
.mobile-sheet-leave-to {
	opacity: 0;
	transform: translateY(28px) scale(0.96);
}

@media (prefers-reduced-motion: reduce) {
	.mobile-bottom-nav,
	.mobile-bottom-nav::after,
	.mobile-nav-item,
	.mobile-nav-icon,
	.mobile-nav-label,
	.mobile-sheet,
	.mobile-sheet-close,
	.mobile-quick-card,
	.mobile-sheet-link {
		transition: none;
	}
}

@media (max-width: 360px) {
	.mobile-bottom-nav {
		left: 8px;
		right: 8px;
		border-radius: 28px;
	}

	.mobile-bottom-nav.is-expanded,
	.mobile-bottom-nav:active {
		left: 6px;
		right: 6px;
	}

	.mobile-bottom-nav.is-compact {
		left: 38px;
		right: 38px;
	}

	.mobile-nav-label {
		font-size: 0.61rem;
	}

	.mobile-sheet {
		left: 8px;
		right: 8px;
		border-radius: 30px;
	}
}
</style>
