<template>
	<NoPermission v-if="!$user.data" />

	<div v-else-if="profile.data" class="profile-page min-h-screen pb-16">
		<header class="profile-topbar sticky top-0 z-20 border-b px-4 py-3 sm:px-6">
			<div class="mx-auto flex max-w-6xl items-center justify-between gap-3">
				<Breadcrumbs class="min-w-0" :items="breadcrumbs" />

				<Button
					v-if="isSessionUser()"
					variant="ghost"
					class="profile-refresh-button"
					@click="reloadUser()"
				>
					<template #icon>
						<RefreshCcw class="size-4 stroke-1.5" />
					</template>
				</Button>
			</div>
		</header>

		<main>
			<section class="profile-cover group relative h-[220px] w-full overflow-hidden md:h-[280px]">
				<img
					v-if="profile.data.cover_image"
					:src="profile.data.cover_image"
					class="h-full w-full object-cover object-center transition duration-700 group-hover:scale-[1.02]"
				/>

				<div v-else class="cover-fallback h-full w-full">
					<div class="cover-pattern"></div>
				</div>

				<div
					v-if="isSessionUser() && !readOnlyMode"
					class="absolute bottom-4 right-4 opacity-100 transition sm:opacity-0 sm:group-hover:opacity-100"
				>
					<EditCoverImage
						@select="(imageUrl) => coverImage.submit({ url: imageUrl })"
					>
						<template v-slot="{ togglePopover }">
							<button class="cover-edit-button" @click="togglePopover()">
								<Edit class="size-4" />
								{{ __('Cambiar portada') }}
							</button>
						</template>
					</EditCoverImage>
				</div>
			</section>

			<section class="relative z-10 mx-auto -mt-14 max-w-6xl px-4 sm:px-6 md:-mt-16">
				<div class="profile-card">
					<div class="flex flex-col gap-5 md:flex-row md:items-end md:justify-between">
						<div class="flex min-w-0 flex-col gap-5 sm:flex-row sm:items-end">
							<div class="relative shrink-0">
								<img
									v-if="profile.data.user_image"
									:src="profile.data.user_image"
									class="profile-avatar object-cover"
								/>

								<div v-else class="profile-avatar profile-avatar-fallback">
									{{ profileInitial }}
								</div>

								<Tooltip
									v-if="profile.data.open_to"
									:text="
										profile.data.open_to === 'Work'
											? __('Open to Work')
											: __('Hiring')
									"
									placement="right"
								>
									<div class="profile-open-badge">
										<div
											class="profile-open-badge-inner"
											:class="
												profile.data.open_to === 'Work'
													? 'is-work'
													: 'is-hiring'
											"
										>
											<BadgeCheckIcon class="size-4" />
										</div>
									</div>
								</Tooltip>
							</div>

							<div class="min-w-0 pb-1">
								<div class="flex flex-wrap items-center gap-2">
									<h2 class="profile-name">
										{{ profile.data.full_name }}
									</h2>

									<span v-if="profile.data.is_plus" class="plus-badge">
										<Crown class="size-3.5 fill-current" />
										{{ __('Plus') }}
									</span>
								</div>

								<p class="profile-headline">
									{{
										profile.data.headline ||
										(user.data?.is_instructor
											? __('Instructor en StudyBadge')
											: __('Estudiante en StudyBadge'))
									}}
								</p>

								<div class="profile-meta-row">
									<span class="profile-pill">
										<Award class="size-3.5" />
										{{ __('Perfil público') }}
									</span>

									<span v-if="profile.data.is_plus" class="profile-pill premium">
										<Sparkles class="size-3.5" />
										{{ __('StudyBadge Plus') }}
									</span>

									<span v-if="profile.data.open_to" class="profile-pill">
										<BadgeCheckIcon class="size-3.5" />
										{{
											profile.data.open_to === 'Work'
												? __('Open to Work')
												: __('Hiring')
										}}
									</span>
								</div>

								<div
									v-if="
										profile.data.twitter ||
										profile.data.linkedin ||
										profile.data.github
									"
									class="profile-social-row"
								>
									<button
										v-if="profile.data.twitter"
										class="social-button"
										:title="__('Twitter')"
										@click="navigateTo(profile.data.twitter)"
									>
										<Twitter class="size-4" />
									</button>

									<button
										v-if="profile.data.linkedin"
										class="social-button"
										:title="__('LinkedIn')"
										@click="navigateTo(profile.data.linkedin)"
									>
										<Linkedin class="size-4" />
									</button>

									<button
										v-if="profile.data.github"
										class="social-button"
										:title="__('GitHub')"
										@click="navigateTo(profile.data.github)"
									>
										<Github class="size-4" />
									</button>
								</div>
							</div>
						</div>

						<div class="flex w-full flex-col gap-3 sm:w-auto sm:flex-row md:items-center">
							<button
								v-if="isSessionUser() && !readOnlyMode"
								class="profile-edit-button"
								@click="editProfile()"
							>
								<Edit class="size-4" />
								{{ __('Editar perfil') }}
							</button>
						</div>
					</div>

					<div class="profile-stats">
						<div class="stat-card">
							<p>{{ __('Estado') }}</p>
							<strong>
								{{
									profile.data.open_to
										? profile.data.open_to === 'Work'
											? __('Open to Work')
											: __('Hiring')
										: __('Activo')
								}}
							</strong>
						</div>

						<div class="stat-card">
							<p>{{ __('Cuenta') }}</p>
							<strong>
								{{ profile.data.is_plus ? __('Plus') : __('Free') }}
							</strong>
						</div>

						<div class="stat-card">
							<p>{{ __('Rol') }}</p>
							<strong>
								{{
									user.data?.is_instructor
										? __('Instructor')
										: __('Estudiante')
								}}
							</strong>
						</div>
					</div>
				</div>

				<div class="profile-tabs-wrap">
					<TabButtons
						class="profile-tabs"
						:buttons="getTabButtons()"
						v-model="activeTab"
					/>
				</div>

				<div class="profile-content-card">
					<router-view :profile="profile" :key="profile.data?.name" />
				</div>
			</section>
		</main>
	</div>

	<div v-else class="profile-loading min-h-screen">
		<div class="loading-card">
			<div class="loading-dot"></div>
			<p>{{ __('Cargando perfil...') }}</p>
		</div>
	</div>

	<EditProfile
		v-if="showProfileModal"
		v-model="showProfileModal"
		v-model:reloadProfile="profile"
		:profile="profile"
	/>
</template>

<script setup>
import {
	Breadcrumbs,
	Button,
	call,
	createResource,
	TabButtons,
	Tooltip,
	toast,
	usePageMeta,
} from 'frappe-ui'
import { computed, inject, watch, ref, onMounted } from 'vue'
import { sessionStore } from '@/stores/session'
import {
	BadgeCheckIcon,
	Crown,
	Edit,
	Github,
	Linkedin,
	RefreshCcw,
	Twitter,
	Award,
	Sparkles,
} from 'lucide-vue-next'
import { useRoute, useRouter } from 'vue-router'
import { convertToTitleCase } from '@/utils'
import NoPermission from '@/components/NoPermission.vue'
import EditProfile from '@/components/Modals/EditProfile.vue'
import EditCoverImage from '@/components/Modals/EditCoverImage.vue'

const { user, brand } = sessionStore()
const $user = inject('$user')
const route = useRoute()
const router = useRouter()

const activeTab = ref('')
const showProfileModal = ref(false)
const readOnlyMode = window.read_only_mode

const props = defineProps({
	username: {
		type: String,
		required: true,
	},
})

const profile = createResource({
	url: 'lms.lms.api.get_profile_details',
	makeParams() {
		return {
			username: props.username,
		}
	},
})

const coverImage = createResource({
	url: 'frappe.client.set_value',
	makeParams(values) {
		return {
			doctype: 'User',
			name: profile.data?.name,
			fieldname: 'cover_image',
			value: values.url,
		}
	},
	onSuccess() {
		profile.reload()
		toast.success(__('Portada actualizada'))
	},
	onError(err) {
		toast.error(err.messages?.[0] || __('No se pudo actualizar la portada'))
		console.error(err)
	},
})

const profileInitial = computed(() => {
	return profile.data?.full_name?.charAt(0)?.toUpperCase() || 'S'
})

const breadcrumbs = computed(() => {
	return [
		{
			label: __('Directorio'),
		},
		{
			label: profile.data?.full_name,
			route: {
				name: 'Profile',
				params: {
					username: props.username || user.doc?.username,
				},
			},
		},
	]
})

onMounted(() => {
	if ($user.data) profile.reload()
	setActiveTab()
})

watch(
	() => props.username,
	() => {
		profile.reload()
	}
)

watch(
	() => route.path,
	() => {
		setActiveTab()
	}
)

watch(activeTab, (tab) => {
	if (!tab) return

	const params = { username: props.username }

	const routes = {
		About: { name: 'ProfileAbout', params },
		Certificates: { name: 'ProfileCertificates', params },
		Roles: { name: 'ProfileRoles', params },
		Slots: { name: 'ProfileEvaluator', params },
		Schedule: { name: 'ProfileEvaluationSchedule', params },
	}

	const targetRoute = routes[tab]

	if (targetRoute && route.name !== targetRoute.name) {
		router.push(targetRoute)
	}
})

const setActiveTab = () => {
	const fragments = route.path.split('/')
	const sections = ['certificates', 'roles', 'slots', 'schedule']

	let matchedSection = ''

	sections.forEach((section) => {
		if (fragments.includes(section)) {
			matchedSection = convertToTitleCase(section)
		}
	})

	activeTab.value = matchedSection || 'About'
}

const editProfile = () => {
	showProfileModal.value = true
}

const isSessionUser = () => {
	return $user.data?.email === profile.data?.name
}

const currentUserHasHigherAccess = () => {
	return $user.data?.is_evaluator || $user.data?.is_moderator
}

const isEvaluatorOrModerator = () => {
	return (
		profile.data?.roles?.includes('Batch Evaluator') ||
		profile.data?.roles?.includes('Moderator')
	)
}

const getTabButtons = () => {
	const buttons = [
		{ label: __('Acerca de mí'), value: 'About' },
		{ label: __('Certificados'), value: 'Certificates' },
	]

	if ($user.data?.is_moderator) {
		buttons.push({ label: __('Roles'), value: 'Roles' })
	}

	if (currentUserHasHigherAccess() && isEvaluatorOrModerator()) {
		buttons.push({ label: __('Horarios'), value: 'Slots' })
		buttons.push({ label: __('Calendario'), value: 'Schedule' })
	}

	return buttons
}

const reloadUser = () => {
	call('frappe.sessions.clear')
		.then(() => {
			$user.reload().then(() => {
				profile.reload()
				toast.success(__('Session refreshed successfully'))
			})
		})
		.catch((err) => {
			toast.error(__('Failed to refresh session'))
			console.error(err)
		})
}

const navigateTo = (url) => {
	if (!url) return

	const safeUrl = url.startsWith('http') ? url : `https://${url}`
	window.open(safeUrl, '_blank', 'noopener,noreferrer')
}

usePageMeta(() => {
	return {
		title: profile.data?.full_name,
		icon: brand.favicon,
	}
})
</script>

<style scoped>
.profile-page {
	--sb-primary: #0a2251;
	--sb-primary-hover: #11336f;
	--sb-primary-soft: #eef3fb;
	--sb-primary-soft-2: #f5f8fd;
	--sb-bg: #f4f7fb;
	--sb-card: #ffffff;
	--sb-card-muted: #f8fafd;
	--sb-border: #dbe4f0;
	--sb-border-strong: #c7d5e8;
	--sb-text: #0f172a;
	--sb-muted: #64748b;
	--sb-soft-muted: #94a3b8;
	--sb-shadow: 0 18px 45px rgba(10, 34, 81, 0.1);
	--sb-shadow-soft: 0 8px 26px rgba(10, 34, 81, 0.07);
	--sb-radius-xl: 24px;
	--sb-radius-lg: 18px;

	background: var(--sb-bg);
	color: var(--sb-text);
}

:global(:root[data-theme='dark']) .profile-page {
	--sb-bg: #08111f;
	--sb-card: #101827;
	--sb-card-muted: #0c1423;
	--sb-border: rgba(255, 255, 255, 0.08);
	--sb-border-strong: rgba(255, 255, 255, 0.14);
	--sb-text: #f8fafc;
	--sb-muted: #b6c2d2;
	--sb-soft-muted: #7f8da3;
	--sb-primary-soft: rgba(10, 34, 81, 0.45);
	--sb-primary-soft-2: rgba(255, 255, 255, 0.04);
	--sb-shadow: 0 18px 45px rgba(0, 0, 0, 0.24);
	--sb-shadow-soft: 0 8px 26px rgba(0, 0, 0, 0.18);
}

.profile-topbar {
	background: rgba(255, 255, 255, 0.92);
	border-color: var(--sb-border);
	backdrop-filter: blur(14px);
}

:global(:root[data-theme='dark']) .profile-topbar {
	background: rgba(8, 17, 31, 0.9);
}

.profile-refresh-button {
	color: var(--sb-muted);
}

.profile-refresh-button:hover {
	color: var(--sb-primary);
	background: var(--sb-primary-soft);
}

.profile-cover {
	background: var(--sb-primary);
}

.cover-fallback {
	position: relative;
	background: var(--sb-primary);
	color: #ffffff;
}

.cover-pattern {
	position: absolute;
	inset: 0;
	opacity: 0.22;
	background-image:
		linear-gradient(rgba(255, 255, 255, 0.08) 1px, transparent 1px),
		linear-gradient(90deg, rgba(255, 255, 255, 0.08) 1px, transparent 1px);
	background-size: 28px 28px;
}


.cover-edit-button {
	display: inline-flex;
	align-items: center;
	gap: 8px;
	border-radius: 999px;
	border: 1px solid rgba(255, 255, 255, 0.3);
	background: rgba(15, 23, 42, 0.74);
	padding: 9px 14px;
	font-size: 13px;
	font-weight: 700;
	color: #ffffff;
	box-shadow: 0 10px 25px rgba(0, 0, 0, 0.18);
	backdrop-filter: blur(12px);
	transition: 0.18s ease;
}

.cover-edit-button:hover {
	background: rgba(15, 23, 42, 0.9);
	transform: translateY(-1px);
}

.profile-card {
	border: 1px solid var(--sb-border);
	border-radius: var(--sb-radius-xl);
	background: var(--sb-card);
	padding: 22px;
	box-shadow: var(--sb-shadow);
}

@media (min-width: 768px) {
	.profile-card {
		padding: 28px;
	}
}

.profile-avatar {
	width: 112px;
	height: 112px;
	border-radius: 999px;
	border: 5px solid var(--sb-card);
	background: var(--sb-card-muted);
	box-shadow: 0 16px 32px rgba(10, 34, 81, 0.16);
}

@media (min-width: 768px) {
	.profile-avatar {
		width: 132px;
		height: 132px;
	}
}

.profile-avatar-fallback {
	display: flex;
	align-items: center;
	justify-content: center;
	background: var(--sb-primary-soft);
	color: var(--sb-primary);
	font-size: 44px;
	font-weight: 800;
}

.profile-open-badge {
	position: absolute;
	right: 8px;
	bottom: 8px;
	border-radius: 999px;
	background: var(--sb-card);
	padding: 4px;
	box-shadow: 0 6px 18px rgba(10, 34, 81, 0.18);
}

.profile-open-badge-inner {
	display: flex;
	align-items: center;
	justify-content: center;
	border-radius: 999px;
	padding: 5px;
}

.profile-open-badge-inner.is-work {
	background: #22c55e;
	color: #ffffff;
}

.profile-open-badge-inner.is-hiring {
	background: #8b5cf6;
	color: #ffffff;
}

.profile-name {
	max-width: 100%;
	overflow-wrap: anywhere;
	font-size: clamp(26px, 4vw, 40px);
	font-weight: 800;
	letter-spacing: -0.04em;
	line-height: 1.08;
	color: var(--sb-text);
}

.profile-headline {
	margin-top: 8px;
	max-width: 680px;
	font-size: 15px;
	font-weight: 500;
	line-height: 1.6;
	color: var(--sb-muted);
}

.plus-badge {
	display: inline-flex;
	align-items: center;
	gap: 6px;
	border-radius: 999px;
	border: 1px solid #f3d77a;
	background: #fff7d6;
	padding: 5px 10px;
	font-size: 11px;
	font-weight: 800;
	letter-spacing: 0.05em;
	text-transform: uppercase;
	color: #8a5a00;
}

.profile-meta-row {
	margin-top: 16px;
	display: flex;
	flex-wrap: wrap;
	align-items: center;
	gap: 8px;
}

.profile-pill {
	display: inline-flex;
	align-items: center;
	gap: 6px;
	border-radius: 999px;
	border: 1px solid var(--sb-border);
	background: var(--sb-card-muted);
	padding: 7px 11px;
	font-size: 12px;
	font-weight: 700;
	color: var(--sb-muted);
}

.profile-pill.premium {
	border-color: #f3d77a;
	background: #fff9e8;
	color: #946300;
}

:global(:root[data-theme='dark']) .profile-pill.premium {
	background: rgba(245, 158, 11, 0.13);
	color: #facc15;
	border-color: rgba(250, 204, 21, 0.22);
}

.profile-social-row {
	margin-top: 18px;
	display: flex;
	align-items: center;
	gap: 8px;
}

.social-button {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	width: 38px;
	height: 38px;
	border-radius: 999px;
	border: 1px solid var(--sb-border);
	background: var(--sb-card-muted);
	color: var(--sb-muted);
	transition: 0.18s ease;
}

.social-button:hover {
	border-color: var(--sb-primary);
	background: var(--sb-primary);
	color: #ffffff;
	transform: translateY(-1px);
	box-shadow: 0 10px 24px rgba(10, 34, 81, 0.18);
}

.profile-edit-button {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	gap: 8px;
	width: 100%;
	border-radius: 999px;
	border: 1px solid var(--sb-primary);
	background: var(--sb-primary);
	padding: 10px 16px;
	font-size: 14px;
	font-weight: 800;
	color: #ffffff;
	box-shadow: 0 12px 26px rgba(10, 34, 81, 0.18);
	transition: 0.18s ease;
}

@media (min-width: 640px) {
	.profile-edit-button {
		width: auto;
	}
}

.profile-edit-button:hover {
	background: var(--sb-primary-hover);
	border-color: var(--sb-primary-hover);
	transform: translateY(-1px);
}

.profile-stats {
	margin-top: 24px;
	display: grid;
	grid-template-columns: 1fr;
	gap: 12px;
	border-top: 1px solid var(--sb-border);
	padding-top: 18px;
}

@media (min-width: 640px) {
	.profile-stats {
		grid-template-columns: repeat(3, minmax(0, 1fr));
	}
}

.stat-card {
	border: 1px solid var(--sb-border);
	border-radius: var(--sb-radius-lg);
	background: var(--sb-card-muted);
	padding: 14px 16px;
}

.stat-card p {
	font-size: 12px;
	font-weight: 700;
	color: var(--sb-soft-muted);
}

.stat-card strong {
	margin-top: 4px;
	display: block;
	font-size: 15px;
	font-weight: 800;
	color: var(--sb-text);
}

.profile-tabs-wrap {
	margin-top: 26px;
	border-bottom: 1px solid var(--sb-border);
}

.profile-tabs {
	padding-bottom: 0;
}

.profile-tabs :deep(button) {
	font-weight: 750;
	color: var(--sb-muted);
}

.profile-tabs :deep(button[aria-selected='true']),
.profile-tabs :deep(.active) {
	color: var(--sb-primary);
}

.profile-content-card {
	margin-top: 18px;
	border: 1px solid var(--sb-border);
	border-radius: var(--sb-radius-xl);
	background: var(--sb-card);
	padding: 20px;
	box-shadow: var(--sb-shadow-soft);
}

@media (min-width: 768px) {
	.profile-content-card {
		padding: 26px;
	}
}

.profile-loading {
	display: flex;
	align-items: center;
	justify-content: center;
	background: #f4f7fb;
	padding: 24px;
}

.loading-card {
	display: flex;
	align-items: center;
	gap: 10px;
	border: 1px solid #dbe4f0;
	border-radius: 18px;
	background: #ffffff;
	padding: 16px 18px;
	box-shadow: 0 12px 32px rgba(10, 34, 81, 0.08);
	color: #0a2251;
	font-size: 14px;
	font-weight: 700;
}

.loading-dot {
	width: 10px;
	height: 10px;
	border-radius: 999px;
	background: #0a2251;
	animation: pulse-dot 1.2s ease-in-out infinite;
}

@keyframes pulse-dot {
	0%,
	100% {
		opacity: 0.35;
		transform: scale(0.9);
	}
	50% {
		opacity: 1;
		transform: scale(1);
	}
}
</style>