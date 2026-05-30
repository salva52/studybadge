<template>
	<NoPermission v-if="!$user.data" />
	<div v-else-if="profile.data" class="pr-page min-h-screen pb-16">
		<header
			class="sticky group top-0 z-10 flex flex-col md:flex-row md:items-center justify-between border-b pr-header-bg pr-border px-4 py-3 sm:px-6"
		>
			<Breadcrumbs class="h-7" :items="breadcrumbs" />
			<Button v-if="isSessionUser()" class="invisible group-hover:visible" variant="ghost">
				<template #icon>
					<RefreshCcw
						class="w-4 h-4 stroke-1.5 pr-text-muted"
						@click="reloadUser()"
					/>
				</template>
			</Button>
		</header>
		
		<!-- Cover Image Section -->
		<div class="group relative h-[180px] md:h-[220px] w-full overflow-hidden">
			<img
				v-if="profile.data.cover_image"
				:src="profile.data.cover_image"
				class="h-full w-full object-cover object-center transition-transform duration-700 group-hover:scale-105"
			/>
			<div
				v-else
				class="h-full w-full bg-gradient-to-r from-blue-900 via-blue-800 to-indigo-900 pr-cover-fallback"
			>
				<div class="absolute inset-0 opacity-20" style="background-image: radial-gradient(circle at 2px 2px, white 1px, transparent 0); background-size: 24px 24px;"></div>
			</div>
			
			<!-- Edit Cover Button -->
			<div
				class="absolute bottom-4 right-4 opacity-0 transition-opacity focus-within:opacity-100 group-hover:opacity-100"
				v-if="isSessionUser()"
			>
				<EditCoverImage
					@select="(imageUrl) => coverImage.submit({ url: imageUrl })"
				>
					<template v-slot="{ togglePopover }">
						<button
							v-if="!readOnlyMode"
							class="pr-btn-glass"
							@click="togglePopover()"
						>
							<Edit class="w-4 h-4" /> {{ __('Cambiar portada') }}
						</button>
					</template>
				</EditCoverImage>
			</div>
		</div>

		<!-- Profile Info Section -->
		<div class="mx-auto -mt-16 max-w-5xl px-4 sm:px-6 md:px-8 relative z-10">
			<div class="flex flex-col md:flex-row items-start md:items-end gap-6 bg-white dark:bg-gray-900 p-6 rounded-3xl shadow-lg border border-gray-100 dark:border-gray-800">
				<div class="relative shrink-0">
					<img
						v-if="profile.data.user_image"
						:src="profile.data.user_image"
						class="object-cover h-28 w-28 md:h-32 md:w-32 rounded-full border-4 border-white dark:border-gray-900 shadow-md bg-white dark:bg-gray-800"
					/>
					<div
						v-else
						class="flex items-center justify-center h-28 w-28 md:h-32 md:w-32 rounded-full border-4 border-white dark:border-gray-900 shadow-md bg-gradient-to-br from-blue-100 to-blue-200 dark:from-gray-700 dark:to-gray-600 text-4xl font-bold text-blue-900 dark:text-gray-300"
					>
						{{ profile.data.full_name.charAt(0).toUpperCase() }}
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
						<div class="absolute bottom-2 right-2 p-1 bg-white dark:bg-gray-900 rounded-full shadow-sm">
							<div
								class="rounded-full p-1"
								:class="
									profile.data.open_to === 'Work'
										? 'bg-green-500 text-white'
										: 'bg-purple-500 text-white'
								"
							>
								<BadgeCheckIcon class="size-4" />
							</div>
						</div>
					</Tooltip>
				</div>
				<div class="flex-1 w-full pb-2">
					<div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
						<div>
							<h2 class="text-2xl md:text-3xl font-extrabold pr-text-primary tracking-tight flex items-center flex-wrap gap-2">
								{{ profile.data.full_name }}
								<span
									v-if="profile.data.is_plus"
									class="inline-flex items-center gap-1.5 rounded-full bg-gradient-to-r from-amber-200 to-yellow-400 px-3 py-1 text-[11px] font-extrabold uppercase tracking-widest text-amber-900 shadow-sm"
								>
									<Crown class="size-3.5 fill-amber-900" />
									Plus PRO
								</span>
							</h2>
							<p class="text-base font-medium pr-text-muted mt-1.5 max-w-2xl">
								{{ profile.data.headline || __('Estudiante en StudyBadge') }}
							</p>
							
							<div
								v-if="profile.data.is_plus"
								class="mt-4 flex flex-wrap gap-2"
							>
								<span class="pr-plus-perk"><Award class="size-3 text-amber-600" /> {{ __('Certificados') }}</span>
								<span class="pr-plus-perk"><Sparkles class="size-3 text-amber-600" /> {{ __('Tutor IA') }}</span>
								<span class="pr-plus-perk"><Calendar class="size-3 text-amber-600" /> {{ __('Calendario') }}</span>
							</div>
							
							<div class="flex items-center gap-x-4 mt-5">
								<a
									v-if="profile.data.twitter"
									class="pr-social-link"
									@click="navigateTo(profile.data.twitter)"
								>
									<Twitter class="size-4" />
								</a>
								<a
									v-if="profile.data.linkedin"
									class="pr-social-link"
									@click="navigateTo(profile.data.linkedin)"
								>
									<Linkedin class="size-4" />
								</a>
								<a
									v-if="profile.data.github"
									class="pr-social-link"
									@click="navigateTo(profile.data.github)"
								>
									<Github class="size-4" />
								</a>
							</div>
						</div>
						
						<button
							v-if="isSessionUser() && !readOnlyMode"
							class="pr-btn-outline shrink-0 mt-2 md:mt-0"
							@click="editProfile()"
						>
							<Edit class="w-4 h-4" />
							{{ __('Editar Perfil') }}
						</button>
					</div>
				</div>
			</div>

			<!-- Navigation Tabs -->
			<div class="mt-8 mb-6 border-b pr-border">
				<TabButtons
					class="pr-tabs"
					:buttons="getTabButtons()"
					v-model="activeTab"
				/>
			</div>
			
			<!-- Tab Content -->
			<div class="pr-content-area">
				<router-view :profile="profile" :key="profile.data?.name" />
			</div>
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
import { computed, inject, watch, ref, onMounted, watchEffect } from 'vue'
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
	Calendar
} from 'lucide-vue-next'
import { useRoute, useRouter } from 'vue-router'
import { convertToTitleCase } from '@/utils'
import UserAvatar from '@/components/UserAvatar.vue'
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

onMounted(() => {
	if ($user.data) profile.reload()
	setActiveTab()
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
	},
})

const setActiveTab = () => {
	let fragments = route.path.split('/')
	let sections = ['certificates', 'roles', 'slots', 'schedule']
	sections.forEach((section) => {
		if (fragments.includes(section)) {
			activeTab.value = convertToTitleCase(section)
		}
	})
	if (!activeTab.value) activeTab.value = 'About'
}

watchEffect(() => {
	if (activeTab.value) {
		let route = {
			About: { name: 'ProfileAbout' },
			Certificates: { name: 'ProfileCertificates' },
			Roles: { name: 'ProfileRoles' },
			Slots: { name: 'ProfileEvaluator' },
			Schedule: { name: 'ProfileEvaluationSchedule' },
		}[activeTab.value]
		router.push(route)
	}
})

watch(
	() => props.username,
	() => {
		profile.reload()
	}
)

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
	let buttons = [
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
	window.open(url, '_blank')
}

const breadcrumbs = computed(() => {
	let crumbs = [
		{
			label: __('Directorio'),
		},
		{
			label: profile.data?.full_name,
			route: {
				name: 'Profile',
				params: {
					username: user.doc?.username,
				},
			},
		},
	]
	return crumbs
})

usePageMeta(() => {
	return {
		title: profile.data?.full_name,
		icon: brand.favicon,
	}
})
</script>

<style scoped>
/* ═══════════════════════════════════════
   PROFILE STYLES
   ═══════════════════════════════════════ */

.pr-page {
	background: var(--sb-bg);
}

.pr-header-bg {
	background: var(--sb-white);
}

.pr-border {
	border-color: rgba(6, 27, 73, 0.05);
}
:root[data-theme="dark"] .pr-border {
	border-color: rgba(255, 255, 255, 0.05);
}

/* Text Colors */
.pr-text-primary { color: #111827; }
.pr-text-muted { color: #6b7280; }
:root[data-theme="dark"] .pr-text-primary { color: #f3f4f6; }
:root[data-theme="dark"] .pr-text-muted { color: #9ca3af; }

/* Buttons */
.pr-btn-glass {
	display: inline-flex;
	align-items: center;
	gap: 6px;
	padding: 8px 16px;
	font-size: 13px;
	font-weight: 700;
	color: #fff;
	background: rgba(0, 0, 0, 0.5);
	backdrop-filter: blur(8px);
	border: 1px solid rgba(255, 255, 255, 0.2);
	border-radius: 10px;
	transition: all 0.2s ease;
	cursor: pointer;
}
.pr-btn-glass:hover {
	background: rgba(0, 0, 0, 0.7);
	transform: translateY(-1px);
}

.pr-btn-outline {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	gap: 6px;
	padding: 10px 20px;
	font-size: 14px;
	font-weight: 700;
	color: #374151;
	background: transparent;
	border: 2px solid rgba(0, 0, 0, 0.08);
	border-radius: 12px;
	cursor: pointer;
	transition: all 0.15s ease;
}
.pr-btn-outline:hover {
	background: rgba(0, 0, 0, 0.03);
	border-color: rgba(0, 0, 0, 0.15);
}
:root[data-theme="dark"] .pr-btn-outline {
	color: #d1d5db;
	border-color: rgba(255, 255, 255, 0.1);
}
:root[data-theme="dark"] .pr-btn-outline:hover {
	background: rgba(255, 255, 255, 0.05);
	border-color: rgba(255, 255, 255, 0.18);
}

/* Plus Perks */
.pr-plus-perk {
	display: inline-flex;
	align-items: center;
	gap: 4px;
	padding: 4px 10px;
	border-radius: 6px;
	font-size: 11px;
	font-weight: 700;
	text-transform: uppercase;
	letter-spacing: 0.05em;
	color: #92400e;
	background: rgba(245, 158, 11, 0.1);
	border: 1px solid rgba(245, 158, 11, 0.2);
}
:root[data-theme="dark"] .pr-plus-perk {
	color: #fbbf24;
	background: rgba(245, 158, 11, 0.15);
	border-color: rgba(245, 158, 11, 0.3);
}

/* Social Links */
.pr-social-link {
	display: flex;
	align-items: center;
	justify-content: center;
	width: 36px;
	height: 36px;
	border-radius: 50%;
	background: rgba(0, 0, 0, 0.04);
	color: #4b5563;
	transition: all 0.2s ease;
	cursor: pointer;
}
.pr-social-link:hover {
	background: #0d6efd;
	color: #fff;
	transform: translateY(-2px);
}
:root[data-theme="dark"] .pr-social-link {
	background: rgba(255, 255, 255, 0.05);
	color: #9ca3af;
}
:root[data-theme="dark"] .pr-social-link:hover {
	background: #0d6efd;
	color: #fff;
}

/* Content Area */
.pr-content-area {
	background: var(--sb-white);
	border-radius: 20px;
	padding: 24px;
	border: 1px solid rgba(6, 27, 73, 0.05);
	box-shadow: 0 1px 3px rgba(6, 27, 73, 0.03);
}
:root[data-theme="dark"] .pr-content-area {
	border-color: rgba(255, 255, 255, 0.05);
	box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
}

/* Tabs Override */
.pr-tabs :deep(button) {
	font-weight: 600;
}
</style>
