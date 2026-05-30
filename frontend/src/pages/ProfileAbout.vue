<template>
	<div class="mb-10">
		<h2 class="mb-4 text-xl font-extrabold pr-text-primary flex items-center gap-2">
			{{ __('Acerca de mí') }}
		</h2>
		<div
			v-if="profile.data.bio"
			v-html="
				DOMPurify.sanitize(decodeEntities(profile.data.bio), {
					ALLOWED_TAGS: [
						'b',
						'i',
						'em',
						'strong',
						'a',
						'p',
						'br',
						'ul',
						'ol',
						'li',
						'img',
					],
					ALLOWED_ATTR: ['href', 'target', 'rel', 'src'],
				})
			"
			class="pr-bio-content ProseMirror prose prose-table:table-fixed prose-td:p-2 prose-th:p-2 prose-td:border prose-th:border prose-td:border-outline-gray-2 prose-th:border-outline-gray-2 prose-td:relative prose-th:relative prose-th:bg-surface-gray-2 prose-sm max-w-none !whitespace-normal"
		></div>
		<div v-else class="pr-empty-state">
			<div class="pr-empty-icon">
				<User class="size-6" />
			</div>
			<p class="font-medium pr-text-primary">{{ __('Aún no hay una biografía') }}</p>
			<p class="text-sm pr-text-muted mt-1">{{ __('Este usuario no ha completado esta información.') }}</p>
		</div>
	</div>

	<div class="mb-10" v-if="badges.data?.length">
		<h2 class="mb-6 text-xl font-extrabold pr-text-primary flex items-center gap-2">
			{{ __('Insignias y Logros') }}
		</h2>
		<div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-5">
			<div v-for="badge in badges.data">
				<Popover trigger="hover" :leaveDelay="Number(0.01)">
					<template #target>
						<div class="pr-badge-card group relative">
							<div class="pr-badge-image-wrap group-hover:scale-105 transition-transform">
								<img
									:src="badge.badge_image"
									:alt="badge.badge"
									class="h-[80px] drop-shadow-md"
								/>
							</div>
							<div
								v-if="badge.count > 1"
								class="absolute -top-2 -right-2 bg-blue-600 text-white shadow-md w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold ring-2 ring-white dark:ring-gray-800"
							>
								{{ badge.count }}
							</div>
							<div class="mt-3 text-center">
								<div class="font-bold text-sm pr-text-primary line-clamp-2 leading-tight">{{ badge.badge }}</div>
							</div>
						</div>
					</template>
					<template #body-main>
						<div class="w-[280px] bg-white dark:bg-gray-800 rounded-xl overflow-hidden shadow-xl border border-gray-100 dark:border-gray-700">
							<div class="bg-gray-50 dark:bg-gray-900/50 py-6 border-b border-gray-100 dark:border-gray-700">
								<img
									:src="badge.badge_image"
									:alt="badge.badge"
									class="h-[140px] mx-auto drop-shadow-lg"
								/>
							</div>
							<div class="p-5">
								<div class="text-lg font-extrabold pr-text-primary mb-2 leading-tight">
									{{ badge.badge }}
								</div>
								<div class="text-sm pr-text-muted leading-relaxed mb-4">
									{{ badge.badge_description }}
								</div>
								<div class="bg-gray-50 dark:bg-gray-900 rounded-lg p-3 mb-4">
									<div class="text-[10px] uppercase tracking-wider font-bold pr-text-muted mb-0.5">
										{{ __('Obtenido el') }}
									</div>
									<div class="text-sm font-semibold pr-text-primary flex items-center gap-2">
										<Calendar class="size-3.5" /> {{ dayjs(badge.issued_on).format('DD MMM YYYY') }}
									</div>
								</div>
								
								<div
									v-if="user.data?.name == profile.data?.name"
									class="flex flex-col border-t border-gray-100 dark:border-gray-700 pt-4"
								>
									<span class="text-[10px] uppercase tracking-wider font-bold pr-text-muted mb-2">
										{{ __('Compartir logro') }}
									</span>
									<div class="flex items-center gap-2">
										<button class="pr-btn-social" @click="shareOnSocial(badge, 'LinkedIn')">
											<LinkedinIcon class="h-4 w-4" /> {{ __('LinkedIn') }}
										</button>
										<button class="pr-btn-social" @click="shareOnSocial(badge, 'Twitter')">
											<Twitter class="h-4 w-4" /> {{ __('Twitter') }}
										</button>
									</div>
								</div>
							</div>
						</div>
					</template>
				</Popover>
			</div>
		</div>
	</div>
</template>
<script setup>
import { inject } from 'vue'
import { createResource, Popover, Button } from 'frappe-ui'
import { X, LinkedinIcon, Twitter, User, Calendar } from 'lucide-vue-next'
import { sessionStore } from '@/stores/session'
import { decodeEntities } from '@/utils'
import DOMPurify from 'dompurify'
import { getLmsRoute } from '@/utils/basePath'

const dayjs = inject('$dayjs')
const user = inject('$user')
const { branding } = sessionStore()

const props = defineProps({
	profile: {
		type: Object,
		required: true,
	},
})

const badges = createResource({
	url: 'lms.lms.api.get_badges',
	params: {
		member: props.profile.data.name,
	},
	auto: true,
	transform(data) {
		let finalBadges = []
		let groupedBadges = Object.groupBy(data, ({ badge }) => badge)
		for (let badge in groupedBadges) {
			let badgeData = groupedBadges[badge][0]
			badgeData.count = groupedBadges[badge].length
			finalBadges.push(badgeData)
		}
		return finalBadges
	},
})

const shareOnSocial = (badge, medium) => {
	let shareUrl
	const url = encodeURIComponent(
		`${window.location.origin}${getLmsRoute(
			`user/${props.profile.data?.username}`
		)}`
	)
	const summary = __(
		'Me alegra compartir que he obtenido la insignia {0} el {1} en {2}'
	).format(
		badge.badge,
		dayjs(badge.issued_on).format('DD MMM YYYY'),
		branding.data?.app_name
	)

	if (medium == 'LinkedIn')
		shareUrl = `https://www.linkedin.com/shareArticle?mini=true&url=${url}&text=${summary}`
	else if (medium == 'Twitter')
		shareUrl = `https://twitter.com/intent/tweet?text=${summary}&url=${url}`

	window.open(shareUrl, '_blank')
}
</script>

<style scoped>
/* Text Colors */
.pr-text-primary { color: #111827; }
.pr-text-muted { color: #6b7280; }
:root[data-theme="dark"] .pr-text-primary { color: #f3f4f6; }
:root[data-theme="dark"] .pr-text-muted { color: #9ca3af; }

/* Bio Content */
.pr-bio-content {
	font-size: 15px;
	line-height: 1.7;
	color: #374151;
}
:root[data-theme="dark"] .pr-bio-content {
	color: #d1d5db;
}

/* Empty State */
.pr-empty-state {
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	padding: 40px 20px;
	background: rgba(0, 0, 0, 0.02);
	border: 1px dashed rgba(0, 0, 0, 0.1);
	border-radius: 16px;
	text-align: center;
}
:root[data-theme="dark"] .pr-empty-state {
	background: rgba(255, 255, 255, 0.02);
	border-color: rgba(255, 255, 255, 0.1);
}

.pr-empty-icon {
	width: 56px;
	height: 56px;
	border-radius: 16px;
	background: rgba(0, 0, 0, 0.05);
	display: flex;
	align-items: center;
	justify-content: center;
	color: #9ca3af;
	margin-bottom: 12px;
}
:root[data-theme="dark"] .pr-empty-icon {
	background: rgba(255, 255, 255, 0.05);
	color: #6b7280;
}

/* Badges */
.pr-badge-card {
	background: var(--sb-bg);
	border: 1px solid rgba(0, 0, 0, 0.05);
	border-radius: 16px;
	padding: 20px 16px;
	display: flex;
	flex-direction: column;
	align-items: center;
	cursor: pointer;
	transition: all 0.2s ease;
}
:root[data-theme="dark"] .pr-badge-card {
	border-color: rgba(255, 255, 255, 0.05);
}
.pr-badge-card:hover {
	background: var(--sb-white);
	box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
	transform: translateY(-2px);
}
:root[data-theme="dark"] .pr-badge-card:hover {
	box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
}

/* Social Buttons */
.pr-btn-social {
	flex: 1;
	display: inline-flex;
	align-items: center;
	justify-content: center;
	gap: 6px;
	padding: 8px;
	font-size: 12px;
	font-weight: 600;
	color: #374151;
	background: rgba(0, 0, 0, 0.03);
	border-radius: 8px;
	transition: all 0.2s;
}
.pr-btn-social:hover {
	background: rgba(0, 0, 0, 0.06);
	color: #111827;
}
:root[data-theme="dark"] .pr-btn-social {
	color: #d1d5db;
	background: rgba(255, 255, 255, 0.05);
}
:root[data-theme="dark"] .pr-btn-social:hover {
	background: rgba(255, 255, 255, 0.1);
	color: #fff;
}
</style>
