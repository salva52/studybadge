<template>
	<div
		class="sb-sidebar-app"
		:class="{ 'is-collapsed': sidebarStore.isSidebarCollapsed }"
	>
		<div class="sb-sidebar-top">
			<UserDropdown :isCollapsed="sidebarStore.isSidebarCollapsed" />
		</div>

		<div class="sb-sidebar-scroll">
			<div v-if="sidebarSettings.data" class="sb-nav-groups">
				<section
					v-for="link in sidebarLinks"
					:key="link.label"
					class="sb-nav-section"
				>
					<div
						v-if="!link.hideLabel && !sidebarStore.isSidebarCollapsed"
						class="sb-section-label"
					>
						<span>{{ __(link.label) }}</span>
					</div>

					<nav class="sb-link-list">
						<div
							v-for="item in link.items"
							:key="item.label || item.route || item.name"
							class="sb-link-shell"
						>
							<SidebarLink
								:link="item"
								:isCollapsed="sidebarStore.isSidebarCollapsed"
							/>
						</div>
					</nav>
				</section>
			</div>

			<section
				v-if="sidebarSettings.data?.web_pages?.length || isModerator"
				class="sb-more-section"
			>
				<div
					class="sb-more-toggle"
					:class="{ collapsed: sidebarStore.isSidebarCollapsed }"
					@click="toggleWebPages"
				>
					<div class="sb-more-title">
						<span class="sb-more-icon">
							<ChevronRight
								class="size-4 transition-transform"
								:class="{
									'rotate-90': !sidebarStore.isWebpagesCollapsed,
									'rtl:rotate-180': sidebarStore.isWebpagesCollapsed,
								}"
							/>
						</span>

						<span v-if="!sidebarStore.isSidebarCollapsed">
							{{ __('Más') }}
						</span>
					</div>

					<Button
						v-if="isModerator && !readOnlyMode && !sidebarStore.isSidebarCollapsed"
						class="sb-add-page"
						variant="ghost"
						@click.stop="openPageModal()"
					>
						<template #icon>
							<Plus class="size-4 stroke-1.5" />
						</template>
					</Button>
				</div>

				<div
					v-if="sidebarSettings.data?.web_pages?.length"
					class="sb-web-pages"
					:class="{ hidden: sidebarStore.isWebpagesCollapsed }"
				>
					<div
						v-for="link in sidebarSettings.data.web_pages"
						:key="link.name || link.label || link.route"
						class="sb-link-shell"
					>
						<SidebarLink
							:link="link"
							:isCollapsed="sidebarStore.isSidebarCollapsed"
							:showControls="isModerator ? true : false"
							@openModal="openPageModal"
							@deletePage="deletePage"
						/>
					</div>
				</div>
			</section>
		</div>

		<div class="sb-sidebar-bottom">
			<div
				v-if="readOnlyMode && !sidebarStore.isSidebarCollapsed"
				class="sb-readonly-card"
			>
				<CircleAlert class="size-4" />
				<p>
					{{
						__(
							'Este sitio se está actualizando. No podrás realizar cambios temporalmente.'
						)
					}}
				</p>
			</div>

			<router-link
				v-if="
					isStudent &&
					!profileIsComplete &&
					profileUsername &&
					!sidebarStore.isSidebarCollapsed
				"
				:to="{
					name: 'Profile',
					params: {
						username: profileUsername,
					},
				}"
				class="sb-profile-card"
			>
				<div class="sb-profile-icon">
					<User class="size-4" />
				</div>

				<div class="sb-profile-copy">
					<strong>{{ __('Completa tu perfil') }}</strong>
					<span>{{ __('Muestra tus habilidades y certificados.') }}</span>
				</div>

				<ChevronsRight class="size-4" />
			</router-link>

			<Tooltip
				v-if="
					isStudent &&
					!profileIsComplete &&
					profileUsername &&
					sidebarStore.isSidebarCollapsed
				"
				:text="__('Completa tu perfil')"
			>
				<router-link
					:to="{
						name: 'Profile',
						params: {
							username: profileUsername,
						},
					}"
					class="sb-bottom-icon"
				>
					<User class="size-4" />
				</router-link>
			</Tooltip>

			<TrialBanner
				v-if="
					userResource.data?.is_system_manager && userResource.data?.is_fc_site
				"
				:isSidebarCollapsed="sidebarStore.isSidebarCollapsed"
			/>

			<GettingStartedBanner
				v-if="showOnboarding && !isOnboardingStepsCompleted"
				:isSidebarCollapsed="sidebarStore.isSidebarCollapsed"
				appName="learning"
			/>

			<div
				class="sb-bottom-actions"
				:class="{ collapsed: sidebarStore.isSidebarCollapsed }"
			>
				<Tooltip v-if="readOnlyMode && sidebarStore.isSidebarCollapsed">
					<CircleAlert class="sb-action-icon" />

					<template #body>
						<div
							class="max-w-[30ch] rounded bg-surface-gray-7 px-2 py-1 text-center text-p-xs text-ink-white shadow-xl"
						>
							{{
								__(
									'Este sitio se está actualizando. No podrás realizar cambios temporalmente.'
								)
							}}
						</div>
					</template>
				</Tooltip>

				<Tooltip :text="__('Tutor IA')">
					<button
						class="sb-tutor-button"
						:class="{ active: sidebarStore.isTutorOpen }"
						@click="sidebarStore.isTutorOpen = !sidebarStore.isTutorOpen"
					>
						<Bot class="size-4" />

						<span v-if="!sidebarStore.isSidebarCollapsed">
							{{ __('Tutor IA') }}
						</span>
					</button>
				</Tooltip>

				<Tooltip
					:text="
						sidebarStore.isSidebarCollapsed ? __('Expandir') : __('Colapsar')
					"
				>
					<button class="sb-collapse-button" @click="toggleSidebar()">
						<CollapseSidebar
							class="size-4 duration-300 stroke-1.5 ease-in-out"
							:style="{
								transform:
									isRtl !== sidebarStore.isSidebarCollapsed
										? 'rotateY(180deg)'
										: '',
							}"
						/>
					</button>
				</Tooltip>
			</div>
		</div>

		<HelpModal
			data-testid="onboarding-help-modal"
			v-if="showOnboarding && showHelpModal"
			v-model="showHelpModal"
			v-model:articles="articles"
			appName="learning"
			title="StudyBadge"
			:logo="LMSLogo"
			:afterSkip="(step) => capture('onboarding_step_skipped_' + step)"
			:afterSkipAll="() => capture('onboarding_steps_skipped')"
			:afterReset="(step) => capture('onboarding_step_reset_' + step)"
			:afterResetAll="() => capture('onboarding_steps_reset')"
			docsLink="https://docs.frappe.io/learning"
		/>

		<IntermediateStepModal
			v-model="showIntermediateModal"
			:currentStep="currentStep"
		/>
	</div>

	<CommandPalette v-model="settingsStore.isCommandPaletteOpen" />

	<PageModal
		v-model="showPageModal"
		v-model:reloadSidebar="sidebarSettings"
		:page="pageToEdit"
	/>
</template>

<script setup>
import { getSidebarLinks } from '@/utils'
import { usersStore } from '@/stores/user'
import { sessionStore } from '@/stores/session'
import { useSidebar } from '@/stores/sidebar'
import { useSettings } from '@/stores/settings'
import { Button, call, createResource, Tooltip, toast } from 'frappe-ui'
import PageModal from '@/components/Modals/PageModal.vue'
import LMSLogo from '@/components/Icons/LMSLogo.vue'
import { useRouter } from 'vue-router'
import {
	ref,
	onMounted,
	inject,
	watch,
	reactive,
	markRaw,
	h,
	onUnmounted,
	computed,
} from 'vue'
import {
	BookOpen,
	CircleAlert,
	ChevronRight,
	ChevronsRight,
	CircleHelp,
	FolderTree,
	FileText,
	Plus,
	User,
	UserPlus,
	Users,
	BookText,
	Bot,
} from 'lucide-vue-next'
import {
	TrialBanner,
	HelpModal,
	GettingStartedBanner,
	useOnboarding,
	showHelpModal,
	minimize,
	IntermediateStepModal,
	useTelemetry,
} from 'frappe-ui/frappe'
import InviteIcon from '@/components/Icons/InviteIcon.vue'
import UserDropdown from '@/components/Sidebar/UserDropdown.vue'
import CollapseSidebar from '@/components/Icons/CollapseSidebar.vue'
import SidebarLink from '@/components/Sidebar/SidebarLink.vue'
import CommandPalette from '@/components/CommandPalette/CommandPalette.vue'

const { user } = sessionStore()
const { userResource } = usersStore()
const sidebarStore = useSidebar()
const socket = inject('$socket')
const unreadCount = ref(0)
const sidebarLinks = ref(null)
const { capture } = useTelemetry()
const showPageModal = ref(false)
const isModerator = ref(false)
const isInstructor = ref(false)
const pageToEdit = ref(null)
const { sidebarSettings, activeTab, isSettingsOpen, programs } = useSettings()
const settingsStore = useSettings()
const showOnboarding = ref(false)
const showIntermediateModal = ref(false)
const currentStep = ref({})
const router = useRouter()
let onboardingDetails
let isOnboardingStepsCompleted = false

const readOnlyMode = window.read_only_mode
const isRtl = document.documentElement.dir === 'rtl'

const profileUsername = computed(
	() =>
		userResource.data?.username ||
		userResource.data?.name ||
		userResource.data?.email ||
		''
)

const iconProps = {
	strokeWidth: 1.5,
	width: 16,
	height: 16,
}

onMounted(() => {
	setUpOnboarding()
	addKeyboardShortcut()
	updateSidebarLinks()

	socket?.on?.('publish_lms_notifications', () => {
		unreadNotifications.reload()
	})
})

const updateSidebarLinksVisibility = () => {
	sidebarSettings.reload(
		{},
		{
			onSuccess(data) {
				if (!sidebarLinks.value) return

				Object.keys(data).forEach((key) => {
					if (!parseInt(data[key])) {
						sidebarLinks.value.forEach((link) => {
							link.items = link.items.filter(
								(item) => item.label.toLowerCase().split(' ').join('_') !== key
							)
						})
					}
				})
			},
		}
	)
}

const addKeyboardShortcut = () => {
	window.addEventListener('keydown', (e) => {
		if (
			e.key === 'k' &&
			(e.ctrlKey || e.metaKey) &&
			!e.target.classList.contains('ProseMirror')
		) {
			toggleCommandPalette()
			e.preventDefault()
		}
	})
}

const toggleCommandPalette = () => {
	settingsStore.isCommandPaletteOpen = !settingsStore.isCommandPaletteOpen
}

const unreadNotifications = createResource({
	cache: 'Unread Notifications Count',
	url: 'frappe.client.get_count',
	makeParams() {
		return {
			doctype: 'Notification Log',
			filters: {
				for_user: user,
				read: 0,
			},
		}
	},
	onSuccess(data) {
		unreadCount.value = data
		updateUnreadCount()
	},
	auto: user ? true : false,
})

const updateUnreadCount = () => {
	sidebarLinks.value?.forEach((link) => {
		link.items.forEach((item) => {
			if (item.label === 'Notifications') {
				item.count = unreadCount.value || 0
			}
		})
	})
}

const openPageModal = (link) => {
	showPageModal.value = true
	pageToEdit.value = link
}

const deletePage = (link) => {
	call('lms.lms.api.delete_documents', {
		doctype: 'LMS Sidebar Item',
		documents: [link.name],
	}).then(() => {
		sidebarSettings.reload()
		toast.success(__('Page deleted successfully'))
	})
}

const toggleSidebar = () => {
	sidebarStore.isSidebarCollapsed = !sidebarStore.isSidebarCollapsed
	localStorage.setItem(
		'isSidebarCollapsed',
		JSON.stringify(sidebarStore.isSidebarCollapsed)
	)
}

const toggleWebPages = () => {
	sidebarStore.isWebpagesCollapsed = !sidebarStore.isWebpagesCollapsed
	localStorage.setItem(
		'isWebpagesCollapsed',
		JSON.stringify(sidebarStore.isWebpagesCollapsed)
	)
}

const getFirstCourse = async () => {
	const firstCourse = localStorage.getItem('firstCourse')
	if (firstCourse) return firstCourse

	return await call('lms.lms.onboarding.get_first_course')
}

const getFirstBatch = async () => {
	const firstBatch = localStorage.getItem('firstBatch')
	if (firstBatch) return firstBatch

	return await call('lms.lms.onboarding.get_first_batch')
}

const steps = reactive([
	{
		name: 'create_first_course',
		title: __('Crea tu primer curso'),
		icon: markRaw(h(BookOpen, iconProps)),
		completed: false,
		onClick: () => {
			minimize.value = true
			router.push({
				name: 'Courses',
			})
		},
	},
	{
		name: 'create_first_chapter',
		title: __('Agrega tu primer capítulo'),
		icon: markRaw(h(FolderTree, iconProps)),
		completed: false,
		dependsOn: 'create_first_course',
		onClick: async () => {
			minimize.value = true
			const course = await getFirstCourse()

			if (course) {
				router.push({
					name: 'CourseDetail',
					params: { courseName: course },
					hash: '#settings',
				})
			} else {
				router.push({ name: 'Courses', query: { newCourse: '1' } })
			}
		},
	},
	{
		name: 'create_first_lesson',
		title: __('Agrega tu primera lección'),
		icon: markRaw(h(FileText, iconProps)),
		completed: false,
		dependsOn: 'create_first_chapter',
		onClick: async () => {
			minimize.value = true
			const course = await getFirstCourse()

			if (course) {
				router.push({
					name: 'CourseDetail',
					params: { courseName: course },
					hash: '#settings',
				})
			} else {
				router.push({ name: 'Courses', query: { newCourse: '1' } })
			}
		},
	},
	{
		name: 'create_first_quiz',
		title: __('Crea tu primera evaluación'),
		icon: markRaw(h(CircleHelp, iconProps)),
		completed: false,
		dependsOn: 'create_first_course',
		onClick: () => {
			minimize.value = true
			router.push({ name: 'Quizzes' })
		},
	},
	{
		name: 'invite_students',
		title: __('Invita a tu equipo y estudiantes'),
		icon: markRaw(h(InviteIcon, iconProps)),
		completed: false,
		onClick: () => {
			minimize.value = true
			activeTab.value = 'Members'
			isSettingsOpen.value = true
		},
	},
	{
		name: 'create_first_batch',
		title: __('Crea tu primer grupo'),
		icon: markRaw(h(Users, iconProps)),
		completed: false,
		onClick: () => {
			minimize.value = true
			router.push({ name: 'Batches' })
		},
	},
	{
		name: 'add_batch_student',
		title: __('Agrega estudiantes a tu grupo'),
		icon: markRaw(h(UserPlus, iconProps)),
		completed: false,
		dependsOn: 'create_first_batch',
		onClick: async () => {
			minimize.value = true
			const batch = await getFirstBatch()

			if (batch) {
				router.push({
					name: 'Batch',
					params: {
						batchName: batch,
					},
				})
			} else {
				router.push({ name: 'Batch' })
			}
		},
	},
	{
		name: 'add_batch_course',
		title: __('Agrega cursos a tu grupo'),
		icon: markRaw(h(BookText, iconProps)),
		completed: false,
		dependsOn: 'create_first_batch',
		onClick: async () => {
			minimize.value = true
			const batch = await getFirstBatch()

			if (batch) {
				router.push({
					name: 'Batch',
					params: {
						batchName: batch,
					},
					hash: '#courses',
				})
			} else {
				router.push({ name: 'Batch' })
			}
		},
	},
])

const articles = ref([
	{
		title: __('Introduction'),
		opened: false,
		subArticles: [
			{ name: 'introduction', title: __('Introduction') },
			{ name: 'setting-up', title: __('Setting up') },
		],
	},
	{
		title: __('Creating a course'),
		opened: false,
		subArticles: [
			{ name: 'create-a-course', title: __('Create a course') },
			{ name: 'add-a-chapter', title: __('Add a chapter') },
			{ name: 'add-a-lesson', title: __('Add a lesson') },
		],
	},
	{
		title: __('Creating a batch'),
		opened: false,
		subArticles: [
			{ name: 'create-a-batch', title: __('Create a batch') },
			{ name: 'create-a-live-class', title: __('Create a live class') },
		],
	},
	{
		title: __('Learning Paths'),
		opened: false,
		subArticles: [{ name: 'add-a-program', title: __('Add a program') }],
	},
	{
		title: __('Assessments'),
		opened: false,
		subArticles: [
			{ name: 'quizzes', title: __('Quizzes') },
			{ name: 'assignments', title: __('Assignments') },
		],
	},
	{
		title: __('Certification'),
		opened: false,
		subArticles: [
			{ name: 'issue-a-certificate', title: __('Issue a Certificate') },
			{
				name: 'custom-certificate-templates',
				title: __('Custom Certificate Templates'),
			},
		],
	},
	{
		title: __('Monetization'),
		opened: false,
		subArticles: [
			{
				name: 'setting-up-payment-gateway',
				title: __('Setting up payment gateway'),
			},
		],
	},
	{
		title: __('Settings'),
		opened: false,
		subArticles: [{ name: 'roles', title: __('Roles') }],
	},
])

const setUpOnboarding = () => {
	if (userResource.data?.is_system_manager) {
		onboardingDetails = useOnboarding('learning')
		onboardingDetails.setUp(steps)
		isOnboardingStepsCompleted = onboardingDetails.isOnboardingStepsCompleted
		showOnboarding.value = true
	}
}

watch(userResource, async () => {
	await userResource.promise

	if (userResource.data) {
		isModerator.value = userResource.data.is_moderator
		isInstructor.value = userResource.data.is_instructor
		await programs.reload()
		setUpOnboarding()
	}

	updateSidebarLinks()
})

watch(settingsStore.settings, () => {
	updateSidebarLinks()
})

const updateSidebarLinks = () => {
	sidebarLinks.value = getSidebarLinks()
	updateSidebarLinksVisibility()
	updateUnreadCount()
}

const isStudent = computed(() => {
	return userResource.data?.is_student
})

const profileIsComplete = computed(() => {
	return (
		userResource.data?.user_image &&
		userResource.data?.headline &&
		userResource.data?.bio
	)
})

onUnmounted(() => {
	socket?.off?.('publish_lms_notifications')
})
</script>

<style scoped>
.sb-sidebar-app {
	--sb-sidebar-bg: #07111f;
	--sb-sidebar-bg-2: #0b1730;
	--sb-sidebar-card: rgba(255, 255, 255, 0.075);
	--sb-sidebar-card-hover: rgba(255, 255, 255, 0.12);
	--sb-sidebar-border: rgba(255, 255, 255, 0.1);
	--sb-sidebar-border-strong: rgba(255, 255, 255, 0.16);
	--sb-sidebar-text: #f8fafc;
	--sb-sidebar-muted: rgba(226, 232, 240, 0.68);
	--sb-sidebar-soft: rgba(226, 232, 240, 0.46);
	--sb-sidebar-blue: #93c5fd;
	--sb-sidebar-gold: #f5b301;
	--sb-sidebar-green: #22c55e;

	position: relative;
	display: flex;
	height: 100%;
	min-height: 100vh;
	flex-direction: column;
	justify-content: space-between;
	width: 17rem;
	overflow: hidden;
	background: var(--sb-sidebar-bg);
	color: var(--sb-sidebar-text);
	border-right: 1px solid var(--sb-sidebar-border);
	transition:
		width 0.26s ease,
		background 0.2s ease;
}

.sb-sidebar-app::before {
	content: "";
	position: absolute;
	inset: 0;
	pointer-events: none;
	background-image:
		linear-gradient(rgba(255, 255, 255, 0.035) 1px, transparent 1px),
		linear-gradient(90deg, rgba(255, 255, 255, 0.035) 1px, transparent 1px);
	background-size: 28px 28px;
	opacity: 0.32;
}

.sb-sidebar-app::after {
	content: "";
	position: absolute;
	top: -120px;
	right: -120px;
	width: 260px;
	height: 260px;
	border-radius: 999px;
	background: rgba(37, 99, 235, 0.16);
	filter: blur(36px);
	pointer-events: none;
}

.sb-sidebar-app.is-collapsed {
	width: 4.25rem;
}

.sb-sidebar-top,
.sb-sidebar-scroll,
.sb-sidebar-bottom {
	position: relative;
	z-index: 1;
}

.sb-sidebar-top {
	flex: 0 0 auto;
	padding: 0.75rem 0.65rem 0.4rem;
}

.sb-sidebar-scroll {
	flex: 1;
	min-height: 0;
	overflow-y: auto;
	overflow-x: hidden;
	padding: 0.35rem 0.65rem 0.75rem;
	scrollbar-width: thin;
	scrollbar-color: rgba(148, 163, 184, 0.35) transparent;
}

.sb-sidebar-scroll::-webkit-scrollbar {
	width: 6px;
}

.sb-sidebar-scroll::-webkit-scrollbar-track {
	background: transparent;
}

.sb-sidebar-scroll::-webkit-scrollbar-thumb {
	border-radius: 999px;
	background: rgba(148, 163, 184, 0.35);
}

.sb-nav-groups {
	display: flex;
	flex-direction: column;
	gap: 0.35rem;
}

.sb-nav-section {
	padding: 0.15rem 0;
}

.sb-section-label {
	display: flex;
	align-items: center;
	margin: 0.8rem 0 0.35rem;
	padding: 0 0.55rem;
	color: var(--sb-sidebar-soft);
	font-size: 0.68rem;
	font-weight: 950;
	letter-spacing: 0.08em;
	text-transform: uppercase;
}

.sb-link-list {
	display: flex;
	flex-direction: column;
	gap: 0.18rem;
}

.sb-link-shell {
	min-width: 0;
}

/* Mejoras visuales para SidebarLink sin tocar su componente interno */
.sb-sidebar-app :deep(a),
.sb-sidebar-app :deep(button) {
	-webkit-tap-highlight-color: transparent;
}

.sb-sidebar-app :deep(.router-link-active),
.sb-sidebar-app :deep(.router-link-exact-active) {
	font-weight: 800;
}

.sb-sidebar-app :deep(.text-ink-gray-7),
.sb-sidebar-app :deep(.text-ink-gray-8),
.sb-sidebar-app :deep(.text-ink-gray-9) {
	color: rgba(255, 255, 255, 0.84) !important;
}

.sb-sidebar-app :deep(.text-ink-gray-5),
.sb-sidebar-app :deep(.text-ink-gray-6) {
	color: rgba(226, 232, 240, 0.62) !important;
}

.sb-sidebar-app :deep(.hover\:bg-surface-gray-2:hover),
.sb-sidebar-app :deep(.hover\:bg-surface-gray-3:hover) {
	background-color: rgba(255, 255, 255, 0.08) !important;
}

.sb-sidebar-app :deep(.bg-surface-gray-2),
.sb-sidebar-app :deep(.bg-surface-gray-3) {
	background-color: rgba(255, 255, 255, 0.08) !important;
}

.sb-sidebar-app :deep(.stroke-1\.5) {
	stroke-width: 1.8;
}

.sb-more-section {
	margin-top: 0.65rem;
	border-top: 1px solid rgba(255, 255, 255, 0.075);
	padding-top: 0.75rem;
}

.sb-more-toggle {
	display: flex;
	align-items: center;
	justify-content: space-between;
	gap: 0.5rem;
	min-height: 38px;
	border-radius: 14px;
	padding: 0 0.35rem 0 0.45rem;
	color: var(--sb-sidebar-muted);
	cursor: pointer;
	transition: 0.18s ease;
}

.sb-more-toggle:hover {
	background: rgba(255, 255, 255, 0.07);
	color: #ffffff;
}

.sb-more-toggle.collapsed {
	justify-content: center;
	padding: 0;
}

.sb-more-title {
	display: flex;
	align-items: center;
	gap: 0.45rem;
	min-width: 0;
	font-size: 0.8rem;
	font-weight: 850;
}

.sb-more-icon {
	display: grid;
	place-items: center;
	width: 28px;
	height: 28px;
	border-radius: 10px;
	color: rgba(255, 255, 255, 0.72);
}

.sb-add-page {
	color: rgba(255, 255, 255, 0.74);
}

.sb-web-pages {
	display: flex;
	flex-direction: column;
	gap: 0.18rem;
	margin-top: 0.35rem;
}

.sb-sidebar-bottom {
	flex: 0 0 auto;
	display: flex;
	flex-direction: column;
	gap: 0.55rem;
	padding: 0.65rem;
	border-top: 1px solid rgba(255, 255, 255, 0.075);
	background: rgba(0, 0, 0, 0.08);
}

.sb-readonly-card {
	display: flex;
	align-items: flex-start;
	gap: 0.55rem;
	border: 1px solid rgba(251, 191, 36, 0.24);
	border-radius: 16px;
	background: rgba(251, 191, 36, 0.1);
	padding: 0.75rem;
	color: #fde68a;
}

.sb-readonly-card p {
	margin: 0;
	font-size: 0.75rem;
	line-height: 1.45;
}

.sb-profile-card {
	display: grid;
	grid-template-columns: 38px minmax(0, 1fr) 18px;
	gap: 0.7rem;
	align-items: center;
	border: 1px solid rgba(147, 197, 253, 0.2);
	border-radius: 18px;
	background: rgba(147, 197, 253, 0.09);
	padding: 0.75rem;
	color: #ffffff;
	text-decoration: none;
	transition: 0.18s ease;
}

.sb-profile-card:hover {
	transform: translateY(-1px);
	border-color: rgba(147, 197, 253, 0.32);
	background: rgba(147, 197, 253, 0.14);
}

.sb-profile-icon {
	display: grid;
	place-items: center;
	width: 38px;
	height: 38px;
	border-radius: 14px;
	background: rgba(255, 255, 255, 0.1);
	color: #bfdbfe;
	flex: 0 0 auto;
}

.sb-profile-copy {
	min-width: 0;
}

.sb-profile-copy strong {
	display: block;
	color: #ffffff;
	font-size: 0.82rem;
	font-weight: 950;
	line-height: 1.2;
}

.sb-profile-copy span {
	display: block;
	margin-top: 0.15rem;
	color: rgba(226, 232, 240, 0.68);
	font-size: 0.72rem;
	line-height: 1.35;
}

.sb-bottom-icon {
	display: grid;
	place-items: center;
	width: 40px;
	height: 40px;
	margin: 0 auto;
	border: 1px solid var(--sb-sidebar-border);
	border-radius: 14px;
	background: rgba(255, 255, 255, 0.07);
	color: #bfdbfe;
	transition: 0.18s ease;
}

.sb-bottom-icon:hover {
	background: rgba(255, 255, 255, 0.13);
	color: #ffffff;
}

.sb-bottom-actions {
	display: flex;
	align-items: center;
	justify-content: space-between;
	gap: 0.5rem;
	margin-top: 0.15rem;
}

.sb-bottom-actions.collapsed {
	flex-direction: column;
	justify-content: center;
}

.sb-tutor-button,
.sb-collapse-button {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	gap: 0.5rem;
	border: 1px solid var(--sb-sidebar-border);
	border-radius: 999px;
	background: rgba(255, 255, 255, 0.075);
	color: rgba(255, 255, 255, 0.78);
	cursor: pointer;
	transition: 0.18s ease;
}

.sb-tutor-button {
	min-height: 40px;
	padding: 0 0.85rem;
	font-size: 0.82rem;
	font-weight: 900;
}

.is-collapsed .sb-tutor-button {
	width: 40px;
	height: 40px;
	padding: 0;
	border-radius: 14px;
}

.sb-tutor-button:hover,
.sb-tutor-button.active,
.sb-collapse-button:hover {
	border-color: rgba(147, 197, 253, 0.28);
	background: rgba(147, 197, 253, 0.13);
	color: #ffffff;
}

.sb-tutor-button.active {
	box-shadow: 0 0 0 4px rgba(147, 197, 253, 0.08);
}

.sb-collapse-button {
	width: 40px;
	height: 40px;
	flex: 0 0 auto;
	border-radius: 14px;
}

.sb-action-icon {
	color: rgba(255, 255, 255, 0.66);
	cursor: pointer;
}

/* Ajustes para banners de Frappe dentro del sidebar */
.sb-sidebar-app :deep(.rounded-md),
.sb-sidebar-app :deep(.rounded-lg),
.sb-sidebar-app :deep(.rounded-xl) {
	border-radius: 16px;
}

.sb-sidebar-app :deep(.bg-white) {
	background-color: rgba(255, 255, 255, 0.08) !important;
}

.sb-sidebar-app :deep(.border) {
	border-color: rgba(255, 255, 255, 0.1) !important;
}

/* Estado colapsado */
.is-collapsed .sb-sidebar-top {
	padding-inline: 0.45rem;
}

.is-collapsed .sb-sidebar-scroll {
	padding-inline: 0.45rem;
}

.is-collapsed .sb-section-label {
	display: none;
}

.is-collapsed .sb-nav-groups {
	align-items: center;
}

.is-collapsed .sb-nav-section,
.is-collapsed .sb-link-list,
.is-collapsed .sb-link-shell {
	width: 100%;
}

.is-collapsed .sb-more-section {
	width: 100%;
}

.is-collapsed .sb-sidebar-bottom {
	align-items: center;
	padding-inline: 0.45rem;
}

/* Dark mode ya es el modo base, pero esto evita conflictos si el theme global cambia */
:global(:root[data-theme='light']) .sb-sidebar-app {
	background: #07111f;
	color: #ffffff;
}

@media (max-width: 768px) {
	.sb-sidebar-app {
		width: 17rem;
	}

	.sb-sidebar-app.is-collapsed {
		width: 4.25rem;
	}
}
</style>