<template>
	<LayoutHeader>
		<template #left-header>
			<Breadcrumbs :items="breadcrumbs" />
		</template>
		<template #right-header>
			<Button
				v-if="activeTab === unreadTab && unreadCount > 0"
				class="notifications-header-action"
				@click="markAllAsRead.submit()"
				:loading="markAllAsRead.loading"
			>
				<CheckCheck class="size-4" />
				{{ __('Marcar todo como leído') }}
			</Button>
		</template>
	</LayoutHeader>

	<main class="notifications-page">
		<section class="notifications-hero">
			<div class="notifications-hero-content">
				<div class="notifications-hero-copy">
					<div class="notifications-eyebrow">
						<Sparkles class="size-4" />
						{{ __('Centro de actividad') }}
					</div>

					<h1 class="notifications-title">
						{{ __('Notificaciones') }}
					</h1>

					<p class="notifications-subtitle">
						{{ heroSubtitle }}
					</p>
				</div>

				<div class="notifications-hero-panel">
					<div class="notifications-panel-title">
						{{ __('Resumen rápido') }}
					</div>

					<div class="notifications-stats">
						<div class="notifications-stat">
							<div class="notifications-stat-icon">
								<Bell class="size-5" />
							</div>
							<div>
								<div class="notifications-stat-value">
									{{ unreadCount }}
								</div>
								<div class="notifications-stat-label">
									{{ __('No leídas') }}
								</div>
							</div>
						</div>

						<div class="notifications-stat">
							<div class="notifications-stat-icon gold">
								<CheckCheck class="size-5" />
							</div>
							<div>
								<div class="notifications-stat-value">
									{{ readCount }}
								</div>
								<div class="notifications-stat-label">
									{{ __('Leídas') }}
								</div>
							</div>
						</div>
					</div>

					<p class="notifications-panel-note">
						{{ __('Revisa novedades de cursos, grupos, comentarios y actividades desde un solo lugar.') }}
					</p>
				</div>
			</div>
		</section>

		<section class="notifications-shell">
			<div class="notifications-toolbar">
				<div class="notifications-tabs" role="tablist" :aria-label="__('Filtros de notificaciones')">
					<button
						v-for="tab in tabs"
						:key="tab.label"
						type="button"
						class="notifications-tab"
						:class="{ active: activeTab === tab.label }"
						@click="activeTab = tab.label"
						role="tab"
						:aria-selected="activeTab === tab.label"
					>
						<component :is="tab.icon" class="size-4" />
						<span>{{ tab.label }}</span>
						<span class="notifications-tab-count">{{ tab.count }}</span>
					</button>
				</div>

				<div class="notifications-toolbar-hint">
					<Circle class="size-2.5 fill-current" />
					{{ toolbarHint }}
				</div>
			</div>

			<TransitionGroup
				v-if="notifications?.length"
				name="notification-list"
				tag="div"
				class="notifications-list"
			>
				<article
					v-for="log in notifications"
					:key="log.name"
					class="notification-card"
					:class="{
						'is-unread': !log.read,
						'is-clickable': log.link,
					}"
					@click="navigateToPage(log)"
				>
					<div class="notification-avatar-wrap">
						<Avatar
							:image="log.from_user_details?.user_image"
							size="xl"
							:label="log.from_user_details?.full_name || __('Sistema')"
						/>
						<span v-if="!log.read" class="notification-unread-dot" />
					</div>

					<div class="notification-content">
						<div class="notification-main-row">
							<div class="notification-subject-wrap">
								<div class="notification-subject" v-html="log.subject" />
								<div class="notification-meta">
									<span>{{ log.from_user_details?.full_name || __('StudyBadge') }}</span>
									<span class="notification-meta-separator">•</span>
									<span>{{ dayjs(log.creation).fromNow() }}</span>
								</div>
							</div>

							<div class="notification-actions">
								<span v-if="log.link" class="notification-open-pill">
									{{ __('Abrir') }}
									<ArrowUpRight class="size-3.5" />
								</span>

								<Button
									v-if="!log.read"
									variant="ghost"
									class="notification-read-button"
									@click.stop="handleMarkAsRead(log.name)"
									:aria-label="__('Marcar como leído')"
								>
									<template #icon>
										<X class="size-4" />
									</template>
								</Button>
							</div>
						</div>

						<div
							v-if="isMentionOrComment(log)"
							v-html="log.email_content"
							class="notification-message-content"
						/>

						<div
							v-else-if="showDetails(log)"
							class="notification-detail-card"
							:class="{ 'has-media': hasEmbeddedMedia(log) }"
						>
							<div
								v-if="hasEmbeddedMedia(log)"
								class="notification-media"
							>
								<iframe
									v-if="log.document_type === 'LMS Course' && log.document_details.video_link"
									:src="`https://www.youtube.com/embed/${log.document_details.video_link}`"
									class="notification-video"
									allowfullscreen
								/>
								<video
									v-else-if="log.document_type === 'LMS Batch' && log.document_details.video_link"
									:src="log.document_details.video_link"
									class="notification-video"
									controls
								/>
							</div>

							<div class="notification-detail-body">
								<div class="notification-detail-badge">
									{{ getDocumentBadge(log) }}
								</div>

								<h3 class="notification-detail-title">
									{{ __(log.document_details.title) }}
								</h3>

								<p
									v-if="log.document_details.short_introduction"
									class="notification-detail-description"
								>
									{{ __(log.document_details.short_introduction) }}
								</p>

								<div class="notification-detail-meta">
									<div
										v-if="log.document_details.start_date"
										class="notification-detail-meta-item"
									>
										<Calendar class="size-3.5" />
										<span>{{ dayjs(log.document_details.start_date).format('DD MMM YYYY') }}</span>
									</div>

									<div
										v-if="log.document_details.start_time"
										class="notification-detail-meta-item"
									>
										<Clock class="size-3.5" />
										<span>
											{{ formatTime(log.document_details.start_time) }}
											{{ log.document_details.timezone }}
										</span>
									</div>
								</div>

								<div
									v-if="log.document_details.instructors?.length"
									class="notification-instructors"
								>
									<div
										v-for="instructor in log.document_details.instructors"
										:key="instructor.name || instructor.full_name"
										class="notification-instructor"
									>
										<Avatar
											:size="'sm'"
											:image="instructor.user_image"
											:label="instructor.full_name"
										/>
										<span>{{ instructor.full_name }}</span>
									</div>
								</div>
							</div>
						</div>
					</div>
				</article>
			</TransitionGroup>

			<div v-else class="notifications-empty-state">
				<div class="notifications-empty-icon">
					<Inbox class="size-9" />
				</div>

				<h2 class="notifications-empty-title">
					{{ emptyStateTitle }}
				</h2>

				<p class="notifications-empty-text">
					{{ emptyStateText }}
				</p>
			</div>
		</section>
	</main>
</template>

<script setup>
import {
	Avatar,
	Breadcrumbs,
	Button,
	createListResource,
	createResource,
	getCachedResource,
	usePageMeta,
} from 'frappe-ui'
import { computed, inject, onMounted, onUnmounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import {
	ArrowUpRight,
	Bell,
	Calendar,
	CheckCheck,
	Circle,
	Clock,
	Inbox,
	Sparkles,
	X,
} from 'lucide-vue-next'
import { sessionStore } from '../stores/session'
import { formatTime } from '@/utils/'
import LayoutHeader from '@/components/Layouts/LayoutHeader.vue'

const { brand } = sessionStore()
const dayjs = inject('$dayjs')
const user = inject('$user')
const socket = inject('$socket')
const router = useRouter()

const unreadTab = 'No leídas'
const readTab = 'Leídas'
const activeTab = ref(unreadTab)

const unReadNotifications = createListResource({
	doctype: 'Notification Log',
	url: 'lms.lms.api.get_notifications',
	filters: {
		read: 0,
	},
	auto: Boolean(user?.data),
	cache: 'Unread Notifications',
})

const readNotifications = createListResource({
	doctype: 'Notification Log',
	url: 'lms.lms.api.get_notifications',
	filters: {
		read: 1,
	},
	auto: Boolean(user?.data),
	cache: 'Read Notifications',
})

const notifications = computed(() => {
	return activeTab.value === unreadTab
		? unReadNotifications.data || []
		: readNotifications.data || []
})

const unreadCount = computed(() => unReadNotifications.data?.length || 0)
const readCount = computed(() => readNotifications.data?.length || 0)

const tabs = computed(() => [
	{
		label: unreadTab,
		count: unreadCount.value,
		icon: Bell,
	},
	{
		label: readTab,
		count: readCount.value,
		icon: CheckCheck,
	},
])

const heroSubtitle = computed(() => {
	if (unreadCount.value > 0) {
		return __('Tienes {0} notificaciones pendientes. Revisa lo importante y mantén tu aprendizaje al día.').format(unreadCount.value)
	}

	return __('Todo está bajo control. Aquí aparecerán las novedades de tus cursos, grupos, comentarios y evaluaciones.')
})

const toolbarHint = computed(() => {
	return activeTab.value === unreadTab
		? __('Mostrando actualizaciones pendientes')
		: __('Mostrando historial de notificaciones')
})

const emptyStateTitle = computed(() => {
	return activeTab.value === unreadTab
		? __('No hay notificaciones no leídas')
		: __('No hay notificaciones leídas')
})

const emptyStateText = computed(() => {
	return activeTab.value === unreadTab
		? __('¡Estás al día! Cuando llegue una nueva actualización, la verás aquí.')
		: __('Las notificaciones que marques como leídas aparecerán en este espacio.')
})

const refreshSidebarCount = () => {
	getCachedResource('Unread Notifications Count')?.reload()
}

const markAsRead = createResource({
	url: 'frappe.desk.doctype.notification_log.notification_log.mark_as_read',
	makeParams(values) {
		return {
			docname: values.name,
		}
	},
	onSuccess() {
		unReadNotifications.reload()
		readNotifications.reload()
		refreshSidebarCount()
	},
})

const markAllAsRead = createResource({
	url: 'frappe.desk.doctype.notification_log.notification_log.mark_all_as_read',
	onSuccess() {
		unReadNotifications.reload()
		readNotifications.reload()
		refreshSidebarCount()
	},
})

const handleMarkAsRead = (logName) => {
	if (!logName) return
	markAsRead.submit({ name: logName })
}

const navigateToPage = (log) => {
	if (!log?.link) return

	if (!log.read) {
		handleMarkAsRead(log.name)
	}

	const link = String(log.link).split('/')

	if (link[2] === 'courses') {
		router.push({
			name: 'CourseDetail',
			params: { courseName: link[3] },
		})
		return
	}

	if (link.includes('batches')) {
		router.push({
			name: link.includes('details') ? 'BatchDetail' : 'Batch',
			params: { batchName: link.pop() },
		})
		return
	}

	if (link.includes('assignment-submission')) {
		router.push({
			name: 'AssignmentSubmission',
			params: {
				submissionName: link[4],
				assignmentID: link[3],
			},
		})
	}
}

const isMentionOrComment = (log) => {
	const subject = String(log?.subject || '')

	return (
		log?.type === 'Mention' ||
		subject.includes('mentioned you') ||
		subject.includes('comment')
	)
}

const showDetails = (log) => {
	return (
		['LMS Course', 'LMS Batch'].includes(log?.document_type) &&
		Boolean(log?.document_details)
	)
}

const hasEmbeddedMedia = (log) => {
	return Boolean(log?.document_details?.video_link)
}

const getDocumentBadge = (log) => {
	if (log?.document_type === 'LMS Course') return __('Nuevo curso')
	if (log?.document_type === 'LMS Batch') return __('Nuevo grupo')
	return __('Actualización')
}

onMounted(() => {
	if (!user?.data) {
		router.push({ name: 'Courses' })
		return
	}

	socket?.on('publish_lms_notifications', () => {
		unReadNotifications.reload()
		readNotifications.reload()
		refreshSidebarCount()
	})
})

onUnmounted(() => {
	socket?.off('publish_lms_notifications')
})

const breadcrumbs = computed(() => {
	return [
		{
			label: __('Notificaciones'),
			route: {
				name: 'Notifications',
			},
		},
	]
})

usePageMeta(() => {
	return {
		title: __('Notificaciones'),
		icon: brand.favicon,
	}
})
</script>

<style scoped>
.notifications-page {
	min-height: 100vh;
	background: var(--sb-bg, #f5f8fc);
	padding: 1.5rem 1rem 3rem;
}

.notifications-page,
.notifications-page * {
	box-sizing: border-box;
}

.notifications-header-action {
	display: inline-flex !important;
	align-items: center;
	gap: 0.45rem;
	border-radius: 999px !important;
	background: #0a2251 !important;
	color: #ffffff !important;
	font-weight: 900 !important;
	box-shadow: 0 12px 24px rgba(10, 34, 81, 0.16);
}

/* HERO */

.notifications-hero {
	position: relative;
	max-width: 1180px;
	margin: 0 auto 1.25rem;
	overflow: hidden;
	border-radius: 30px;
	background: #0a2251;
	color: #ffffff;
	box-shadow: 0 24px 60px rgba(10, 34, 81, 0.16);
}

.notifications-hero::before,
.notifications-hero::after {
	content: '';
	position: absolute;
	pointer-events: none;
	border-radius: 999px;
}

.notifications-hero::before {
	top: -120px;
	right: -100px;
	width: 310px;
	height: 310px;
	background: rgba(245, 179, 1, 0.18);
	filter: blur(2px);
}

.notifications-hero::after {
	bottom: -150px;
	left: 38%;
	width: 280px;
	height: 280px;
	background: rgba(255, 255, 255, 0.1);
}

.notifications-hero-content {
	position: relative;
	z-index: 1;
	display: grid;
	grid-template-columns: minmax(0, 1fr) 390px;
	gap: 2rem;
	align-items: center;
	padding: 2rem;
}

.notifications-hero-copy {
	min-width: 0;
}

.notifications-eyebrow {
	display: inline-flex;
	align-items: center;
	gap: 0.5rem;
	width: fit-content;
	margin-bottom: 1rem;
	border: 1px solid rgba(255, 255, 255, 0.18);
	border-radius: 999px;
	background: rgba(255, 255, 255, 0.1);
	padding: 0.45rem 0.75rem;
	color: rgba(255, 255, 255, 0.9);
	font-size: 0.75rem;
	font-weight: 900;
	letter-spacing: 0.06em;
	text-transform: uppercase;
}

.notifications-title {
	margin: 0;
	max-width: 760px;
	color: #ffffff;
	font-size: clamp(2.1rem, 5vw, 3.8rem);
	font-weight: 950;
	letter-spacing: -0.055em;
	line-height: 1.02;
}

.notifications-subtitle {
	margin: 1rem 0 0;
	max-width: 700px;
	color: rgba(255, 255, 255, 0.78);
	font-size: 1rem;
	line-height: 1.75;
}

.notifications-hero-panel {
	border: 1px solid rgba(255, 255, 255, 0.16);
	border-radius: 24px;
	background: rgba(255, 255, 255, 0.08);
	padding: 1.25rem;
	backdrop-filter: blur(16px);
}

.notifications-panel-title {
	color: rgba(255, 255, 255, 0.82);
	font-size: 0.78rem;
	font-weight: 900;
	letter-spacing: 0.08em;
	text-transform: uppercase;
}

.notifications-stats {
	display: grid;
	gap: 0.85rem;
	margin-top: 1rem;
}

.notifications-stat {
	display: flex;
	align-items: center;
	gap: 0.85rem;
	border-radius: 18px;
	background: rgba(255, 255, 255, 0.1);
	padding: 0.9rem;
}

.notifications-stat-icon {
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

.notifications-stat-icon.gold {
	background: #f5b301;
	color: #3b2a00;
}

.notifications-stat-value {
	color: #ffffff;
	font-size: 1.6rem;
	font-weight: 950;
	letter-spacing: -0.04em;
	line-height: 1;
}

.notifications-stat-label {
	margin-top: 0.2rem;
	color: rgba(255, 255, 255, 0.72);
	font-size: 0.78rem;
	font-weight: 800;
}

.notifications-panel-note {
	margin: 1rem 0 0;
	color: rgba(255, 255, 255, 0.72);
	font-size: 0.85rem;
	line-height: 1.6;
}

/* CONTENT */

.notifications-shell {
	max-width: 1180px;
	margin: 0 auto;
}

.notifications-toolbar {
	display: flex;
	align-items: center;
	justify-content: space-between;
	gap: 1rem;
	margin-bottom: 1rem;
	border: 1px solid rgba(10, 34, 81, 0.08);
	border-radius: 22px;
	background: rgba(255, 255, 255, 0.78);
	padding: 0.65rem;
	box-shadow: 0 14px 35px rgba(10, 34, 81, 0.08);
	backdrop-filter: blur(14px);
}

.notifications-tabs {
	display: inline-flex;
	gap: 0.45rem;
	border-radius: 18px;
	background: #eef4fb;
	padding: 0.35rem;
}

.notifications-tab {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	gap: 0.5rem;
	min-height: 40px;
	border: 0;
	border-radius: 14px;
	background: transparent;
	padding: 0.55rem 0.85rem;
	color: #56657a;
	font-size: 0.88rem;
	font-weight: 900;
	white-space: nowrap;
	transition: 0.18s ease;
}

.notifications-tab:hover {
	color: #0a2251;
	background: rgba(255, 255, 255, 0.7);
}

.notifications-tab.active {
	background: #ffffff;
	color: #0a2251;
	box-shadow: 0 10px 24px rgba(10, 34, 81, 0.1);
}

.notifications-tab-count {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	min-width: 1.45rem;
	height: 1.45rem;
	border-radius: 999px;
	background: rgba(10, 34, 81, 0.08);
	padding: 0 0.45rem;
	font-size: 0.72rem;
	font-weight: 950;
}

.notifications-tab.active .notifications-tab-count {
	background: #0a2251;
	color: #ffffff;
}

.notifications-toolbar-hint {
	display: inline-flex;
	align-items: center;
	gap: 0.5rem;
	padding: 0 0.75rem;
	color: #6b7890;
	font-size: 0.82rem;
	font-weight: 800;
}

.notifications-toolbar-hint svg {
	color: #f5b301;
}

/* LIST */

.notifications-list {
	display: grid;
	gap: 0.85rem;
}

.notification-card {
	position: relative;
	display: grid;
	grid-template-columns: auto minmax(0, 1fr);
	gap: 1rem;
	border: 1px solid rgba(10, 34, 81, 0.08);
	border-radius: 24px;
	background: #ffffff;
	padding: 1rem;
	box-shadow: 0 12px 32px rgba(10, 34, 81, 0.07);
	transition:
		transform 0.18s ease,
		box-shadow 0.18s ease,
		border-color 0.18s ease,
		background 0.18s ease;
}

.notification-card::before {
	content: '';
	position: absolute;
	inset: 0 auto 0 0;
	width: 4px;
	border-radius: 24px 0 0 24px;
	background: transparent;
	transition: 0.18s ease;
}

.notification-card.is-unread {
	border-color: rgba(10, 34, 81, 0.16);
	background: linear-gradient(180deg, #ffffff 0%, #f9fcff 100%);
}

.notification-card.is-unread::before {
	background: #f5b301;
}

.notification-card.is-clickable {
	cursor: pointer;
}

.notification-card.is-clickable:hover {
	transform: translateY(-2px);
	border-color: rgba(10, 34, 81, 0.22);
	box-shadow: 0 20px 44px rgba(10, 34, 81, 0.12);
}

.notification-avatar-wrap {
	position: relative;
	flex: 0 0 auto;
}

.notification-unread-dot {
	position: absolute;
	right: -2px;
	bottom: 3px;
	width: 0.8rem;
	height: 0.8rem;
	border: 2px solid #ffffff;
	border-radius: 999px;
	background: #f5b301;
	box-shadow: 0 0 0 4px rgba(245, 179, 1, 0.14);
}

.notification-content {
	min-width: 0;
}

.notification-main-row {
	display: flex;
	align-items: flex-start;
	justify-content: space-between;
	gap: 1rem;
}

.notification-subject-wrap {
	min-width: 0;
}

.notification-subject {
	color: #10233f;
	font-size: 0.95rem;
	font-weight: 850;
	line-height: 1.45;
}

.notification-subject :deep(a) {
	color: #0a2251;
	font-weight: 950;
	text-decoration: none;
}

.notification-meta {
	display: flex;
	align-items: center;
	flex-wrap: wrap;
	gap: 0.4rem;
	margin-top: 0.25rem;
	color: #738098;
	font-size: 0.78rem;
	font-weight: 750;
}

.notification-meta-separator {
	color: #b8c2d1;
}

.notification-actions {
	display: inline-flex;
	align-items: center;
	gap: 0.45rem;
	flex: 0 0 auto;
}

.notification-open-pill {
	display: inline-flex;
	align-items: center;
	gap: 0.25rem;
	border: 1px solid rgba(10, 34, 81, 0.08);
	border-radius: 999px;
	background: #f3f7fc;
	padding: 0.35rem 0.55rem;
	color: #0a2251;
	font-size: 0.72rem;
	font-weight: 900;
	transition: 0.18s ease;
}

.notification-card:hover .notification-open-pill {
	background: #0a2251;
	color: #ffffff;
}

.notification-read-button {
	width: 2rem !important;
	height: 2rem !important;
	border-radius: 999px !important;
	color: #64748b !important;
}

.notification-read-button:hover {
	background: rgba(10, 34, 81, 0.08) !important;
	color: #0a2251 !important;
}

.notification-message-content {
	margin-top: 0.85rem;
	max-height: 6.8rem;
	overflow: hidden;
	border: 1px solid rgba(10, 34, 81, 0.06);
	border-radius: 18px;
	background: #f6f9fd;
	padding: 0.85rem 1rem;
	color: #4d5c72;
	font-size: 0.88rem;
	line-height: 1.65;
}

.notification-message-content :deep(p) {
	margin: 0;
}

.notification-message-content :deep(a) {
	color: #0a2251;
	font-weight: 900;
	text-decoration: none;
}

/* DETAILS */

.notification-detail-card {
	display: grid;
	grid-template-columns: 1fr;
	gap: 0;
	margin-top: 0.9rem;
	overflow: hidden;
	border: 1px solid rgba(10, 34, 81, 0.08);
	border-radius: 20px;
	background: #f7faff;
}

.notification-detail-card.has-media {
	grid-template-columns: minmax(220px, 300px) minmax(0, 1fr);
}

.notification-media {
	min-height: 190px;
	background: #061832;
}

.notification-video {
	display: block;
	width: 100%;
	height: 100%;
	min-height: 190px;
	border: 0;
	object-fit: cover;
}

.notification-detail-body {
	padding: 1rem;
}

.notification-detail-badge {
	display: inline-flex;
	align-items: center;
	width: fit-content;
	margin-bottom: 0.7rem;
	border-radius: 999px;
	background: rgba(245, 179, 1, 0.14);
	padding: 0.35rem 0.6rem;
	color: #705000;
	font-size: 0.72rem;
	font-weight: 950;
	letter-spacing: 0.03em;
	text-transform: uppercase;
}

.notification-detail-title {
	margin: 0;
	color: #0f2342;
	font-size: 1rem;
	font-weight: 950;
	letter-spacing: -0.02em;
	line-height: 1.35;
}

.notification-detail-description {
	margin: 0.45rem 0 0;
	color: #5d6b80;
	font-size: 0.88rem;
	line-height: 1.65;
}

.notification-detail-meta {
	display: flex;
	flex-wrap: wrap;
	gap: 0.55rem;
	margin-top: 0.9rem;
}

.notification-detail-meta-item {
	display: inline-flex;
	align-items: center;
	gap: 0.4rem;
	border-radius: 999px;
	background: #ffffff;
	padding: 0.45rem 0.65rem;
	color: #40516a;
	font-size: 0.78rem;
	font-weight: 850;
	box-shadow: 0 8px 18px rgba(10, 34, 81, 0.06);
}

.notification-detail-meta-item svg {
	color: #0a2251;
}

.notification-instructors {
	display: flex;
	flex-wrap: wrap;
	gap: 0.5rem;
	margin-top: 0.9rem;
}

.notification-instructor {
	display: inline-flex;
	align-items: center;
	gap: 0.45rem;
	border: 1px solid rgba(10, 34, 81, 0.08);
	border-radius: 999px;
	background: #ffffff;
	padding: 0.35rem 0.65rem 0.35rem 0.35rem;
	color: #263850;
	font-size: 0.78rem;
	font-weight: 900;
}

/* EMPTY */

.notifications-empty-state {
	display: flex;
	min-height: 380px;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	border: 1px solid rgba(10, 34, 81, 0.08);
	border-radius: 28px;
	background: #ffffff;
	padding: 3rem 1.25rem;
	text-align: center;
	box-shadow: 0 16px 42px rgba(10, 34, 81, 0.08);
}

.notifications-empty-icon {
	display: flex;
	align-items: center;
	justify-content: center;
	width: 78px;
	height: 78px;
	margin-bottom: 1.1rem;
	border-radius: 26px;
	background: linear-gradient(180deg, rgba(10, 34, 81, 0.1), rgba(10, 34, 81, 0.04));
	color: #0a2251;
}

.notifications-empty-title {
	margin: 0;
	color: #0f2342;
	font-size: 1.15rem;
	font-weight: 950;
	letter-spacing: -0.02em;
}

.notifications-empty-text {
	margin: 0.55rem 0 0;
	max-width: 520px;
	color: #68768c;
	font-size: 0.92rem;
	line-height: 1.7;
}

/* ANIMATION */

.notification-list-enter-active,
.notification-list-leave-active {
	transition: all 0.18s ease;
}

.notification-list-enter-from,
.notification-list-leave-to {
	opacity: 0;
	transform: translateY(8px);
}

/* DARK MODE */

:global(:root[data-theme='dark']) .notifications-page {
	background: #07111f;
}

:global(:root[data-theme='dark']) .notifications-header-action {
	background: #f5b301 !important;
	color: #2d2100 !important;
	box-shadow: 0 12px 24px rgba(0, 0, 0, 0.3);
}

:global(:root[data-theme='dark']) .notifications-hero {
	box-shadow: 0 24px 60px rgba(0, 0, 0, 0.34);
}

:global(:root[data-theme='dark']) .notifications-toolbar {
	border-color: rgba(255, 255, 255, 0.08);
	background: rgba(12, 25, 45, 0.9);
	box-shadow: 0 18px 45px rgba(0, 0, 0, 0.25);
}

:global(:root[data-theme='dark']) .notifications-tabs {
	background: rgba(255, 255, 255, 0.06);
}

:global(:root[data-theme='dark']) .notifications-tab {
	color: rgba(255, 255, 255, 0.68);
}

:global(:root[data-theme='dark']) .notifications-tab:hover {
	background: rgba(255, 255, 255, 0.08);
	color: #ffffff;
}

:global(:root[data-theme='dark']) .notifications-tab.active {
	background: #ffffff;
	color: #0a2251;
}

:global(:root[data-theme='dark']) .notifications-toolbar-hint {
	color: rgba(255, 255, 255, 0.62);
}

:global(:root[data-theme='dark']) .notification-card,
:global(:root[data-theme='dark']) .notifications-empty-state {
	border-color: rgba(255, 255, 255, 0.08);
	background: #0c192d;
	box-shadow: 0 18px 45px rgba(0, 0, 0, 0.26);
}

:global(:root[data-theme='dark']) .notification-card.is-unread {
	border-color: rgba(245, 179, 1, 0.24);
	background: linear-gradient(180deg, #0d1b31 0%, #0a1729 100%);
}

:global(:root[data-theme='dark']) .notification-unread-dot {
	border-color: #0c192d;
}

:global(:root[data-theme='dark']) .notification-subject,
:global(:root[data-theme='dark']) .notification-detail-title,
:global(:root[data-theme='dark']) .notifications-empty-title {
	color: #ffffff;
}

:global(:root[data-theme='dark']) .notification-meta,
:global(:root[data-theme='dark']) .notification-detail-description,
:global(:root[data-theme='dark']) .notifications-empty-text {
	color: rgba(255, 255, 255, 0.62);
}

:global(:root[data-theme='dark']) .notification-open-pill {
	border-color: rgba(255, 255, 255, 0.08);
	background: rgba(255, 255, 255, 0.06);
	color: #ffffff;
}

:global(:root[data-theme='dark']) .notification-card:hover .notification-open-pill {
	background: #f5b301;
	color: #2d2100;
}

:global(:root[data-theme='dark']) .notification-message-content,
:global(:root[data-theme='dark']) .notification-detail-card {
	border-color: rgba(255, 255, 255, 0.08);
	background: rgba(255, 255, 255, 0.04);
	color: rgba(255, 255, 255, 0.72);
}

:global(:root[data-theme='dark']) .notification-detail-meta-item,
:global(:root[data-theme='dark']) .notification-instructor {
	border-color: rgba(255, 255, 255, 0.08);
	background: rgba(255, 255, 255, 0.06);
	color: rgba(255, 255, 255, 0.78);
	box-shadow: none;
}

:global(:root[data-theme='dark']) .notification-detail-meta-item svg,
:global(:root[data-theme='dark']) .notifications-empty-icon {
	color: #f5b301;
}

:global(:root[data-theme='dark']) .notifications-empty-icon {
	background: rgba(245, 179, 1, 0.12);
}

/* RESPONSIVE */

@media (max-width: 1100px) {
	.notifications-hero-content {
		grid-template-columns: 1fr;
	}

	.notifications-hero-panel {
		max-width: 620px;
	}
}

@media (max-width: 760px) {
	.notifications-page {
		padding: 1rem 0.85rem 2.5rem;
	}

	.notifications-hero {
		border-radius: 24px;
	}

	.notifications-hero-content {
		gap: 1.25rem;
		padding: 1.25rem;
	}

	.notifications-toolbar {
		align-items: stretch;
		flex-direction: column;
	}

	.notifications-tabs {
		display: grid;
		grid-template-columns: 1fr 1fr;
		width: 100%;
	}

	.notifications-tab {
		width: 100%;
	}

	.notifications-toolbar-hint {
		justify-content: center;
		padding: 0.2rem 0 0.35rem;
	}

	.notification-card {
		grid-template-columns: 1fr;
		gap: 0.75rem;
		border-radius: 22px;
	}

	.notification-avatar-wrap {
		display: none;
	}

	.notification-main-row {
		gap: 0.75rem;
	}

	.notification-open-pill {
		display: none;
	}

	.notification-detail-card {
		grid-template-columns: 1fr;
	}

	.notification-media,
	.notification-video {
		min-height: 210px;
	}
}

@media (max-width: 480px) {
	.notifications-title {
		font-size: 2rem;
	}

	.notifications-subtitle {
		font-size: 0.92rem;
		line-height: 1.65;
	}

	.notifications-stats {
		grid-template-columns: 1fr;
	}

	.notifications-tab {
		font-size: 0.78rem;
		padding-inline: 0.55rem;
	}

	.notification-actions {
		align-self: flex-start;
	}

	.notification-message-content {
		font-size: 0.84rem;
	}
}
</style>
