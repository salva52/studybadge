<template>
	<div
		v-if="course.title"
		class="cc-root group"
	>
		<!-- Image Section -->
		<div class="relative w-full h-48 overflow-hidden cc-image-wrap">
			<div
				class="absolute inset-0 w-full h-full bg-cover bg-center bg-no-repeat transition-transform duration-500 group-hover:scale-105"
				:style="
					course.image
						? { backgroundImage: `url('${encodeURI(course.image)}')` }
						: {
								backgroundImage: gradientColor,
								backgroundBlendMode: 'screen',
						  }
				"
			></div>

			<!-- Overlay for no-image cards -->
			<div v-if="!course.image" class="absolute inset-0 bg-black/15"></div>

			<!-- Badges -->
			<div class="absolute top-3.5 left-3.5 right-3.5 flex flex-wrap gap-1.5 z-10">
				<div v-if="course.featured" class="cc-badge-featured">
					<Star class="size-3 fill-amber-900" />
					<span>{{ __('Más vendido') }}</span>
				</div>
				<div v-if="course.enable_certification || course.paid_certificate" class="cc-badge-cert">
					<GraduationCap class="size-3 stroke-2" />
					<span>{{ __('Certificado') }}</span>
				</div>
				<div
					v-if="course.tags"
					v-for="tag in course.tags?.split(', ').slice(0, 2)"
					class="cc-badge-tag"
				>
					{{ tag }}
				</div>
			</div>

			<!-- Title overlay for no-image cards -->
			<div v-if="!course.image" class="absolute inset-0 flex items-center justify-center p-6 text-center z-10">
				<BookOpen class="absolute -right-8 -bottom-8 w-36 h-36 text-white/8 -rotate-12 transform" />
				<span class="text-xl sm:text-2xl font-extrabold text-white drop-shadow-lg leading-tight relative z-10">{{ course.title }}</span>
			</div>
		</div>

		<!-- Recommendation Badge -->
		<div v-if="course.custom_recommended_by_studybadge" class="cc-recommended">
			<Star class="size-3.5 text-amber-500 fill-amber-500 shrink-0" />
			<span>{{ __('Recomendado por StudyBadge') }}</span>
		</div>

		<!-- Content Section -->
		<div class="flex flex-col flex-auto p-5 sm:p-6">
			<!-- Meta pills -->
			<div class="flex items-center gap-2 mb-3 text-xs font-semibold flex-wrap">
				<div v-if="course.lessons" class="cc-meta-pill">
					<BookOpen class="h-3 w-3 stroke-2" />
					{{ course.lessons }} {{ __('Lecc.') }}
				</div>
				<div v-if="course.enrollments" class="cc-meta-pill">
					<Users class="h-3 w-3 stroke-2" />
					{{ formatAmount(course.enrollments) }}
				</div>
				<div v-if="course.rating" class="cc-meta-pill cc-meta-rating">
					<Star class="h-3 w-3 stroke-2 fill-amber-500 text-amber-500" />
					{{ course.rating }}
				</div>
			</div>

			<!-- Title -->
			<h3 class="cc-title group-hover:text-[color:var(--sb-primary)] transition-colors">
				{{ course.title }}
			</h3>

			<!-- Description -->
			<p class="cc-description">{{ course.short_introduction }}</p>

			<!-- Progress Bar -->
			<div v-if="user && course.membership" class="mt-auto mb-5">
				<div class="flex justify-between items-end mb-1.5">
					<span class="text-[11px] font-bold cc-text-primary">{{ __('Tu progreso') }}</span>
					<span class="text-[11px] font-bold" style="color: var(--sb-primary);">{{ Math.ceil(course.membership.progress) }}%</span>
				</div>
				<div class="cc-progress-track">
					<div class="cc-progress-bar" :style="`width: ${course.membership.progress}%`"></div>
				</div>
			</div>

			<!-- Footer -->
			<div class="flex items-center justify-between mt-auto pt-4 cc-footer-border" :class="{'mt-auto': !(user && course.membership)}">
				<div class="flex items-center gap-2.5">
					<div class="flex avatar-group overlap">
						<div class="h-7" :class="{ 'avatar-group overlap': course.instructors?.length > 1 }">
							<UserAvatar v-for="instructor in course.instructors" :user="instructor" />
						</div>
					</div>
					<CourseInstructors :instructors="course.instructors" class="text-xs font-medium" />
				</div>
				<div class="flex items-center gap-x-2">
					<div v-if="course.paid_course" class="font-extrabold cc-text-primary text-base">{{ course.price }}</div>
					<div v-else class="cc-free-badge">{{ __('Gratis') }}</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import { Award, BookOpen, GraduationCap, Star, Users } from 'lucide-vue-next'
import { sessionStore } from '@/stores/session'
import { Tooltip } from 'frappe-ui'
import { formatAmount } from '@/utils'
import { theme } from '@/utils/theme'
import { computed } from 'vue'
import CourseInstructors from '@/components/CourseInstructors.vue'
import UserAvatar from '@/components/UserAvatar.vue'
import colors from '@/utils/frappe-ui-colors.json'

const { user } = sessionStore()

const props = defineProps({
	course: {
		type: Object,
		default: null,
	},
})

const gradientColor = computed(() => {
	let themeMode = theme.value === 'dark' ? 'darkMode' : 'lightMode'
	let color = props.course?.card_gradient?.toLowerCase() || 'blue'
	let colorMap = colors[themeMode][color] || colors[themeMode]['blue']
	return `linear-gradient(to top right, #061B49, ${colorMap[400]})`
})
</script>

<style>
/* ═══════════════════════════════════════
   COURSE CARD — Light & Dark Support
   ═══════════════════════════════════════ */

.cc-root {
	display: flex;
	flex-direction: column;
	height: 100%;
	min-height: 370px;
	overflow: hidden;
	background: var(--sb-white);
	border: 1px solid rgba(6, 27, 73, 0.05);
	border-radius: 22px;
	box-shadow: 0 1px 3px rgba(6, 27, 73, 0.03), 0 2px 8px rgba(6, 27, 73, 0.02);
	transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.cc-root:hover {
	transform: translateY(-4px);
	box-shadow: 0 8px 32px rgba(6, 27, 73, 0.1), 0 2px 8px rgba(6, 27, 73, 0.05);
	border-color: rgba(59, 130, 246, 0.12);
}

:root[data-theme="dark"] .cc-root {
	border-color: rgba(255, 255, 255, 0.06);
	box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2), 0 2px 8px rgba(0, 0, 0, 0.12);
}

:root[data-theme="dark"] .cc-root:hover {
	box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35), 0 2px 8px rgba(0, 0, 0, 0.2);
	border-color: rgba(59, 130, 246, 0.2);
}

/* Text */
.cc-text-primary { color: #111827; }
:root[data-theme="dark"] .cc-text-primary { color: #f3f4f6; }

.cc-title {
	font-size: 1.125rem;
	font-weight: 800;
	line-height: 1.35;
	color: #111827;
	margin-bottom: 6px;
	display: -webkit-box;
	-webkit-line-clamp: 2;
	-webkit-box-orient: vertical;
	overflow: hidden;
}

:root[data-theme="dark"] .cc-title { color: #f3f4f6; }

.cc-description {
	font-size: 0.8125rem;
	line-height: 1.6;
	color: #6b7280;
	margin-bottom: 1.25rem;
	display: -webkit-box;
	-webkit-line-clamp: 2;
	-webkit-box-orient: vertical;
	overflow: hidden;
}

:root[data-theme="dark"] .cc-description { color: #9ca3af; }

/* Image */
.cc-image-wrap {
	background: rgba(0, 0, 0, 0.04);
}

:root[data-theme="dark"] .cc-image-wrap {
	background: rgba(255, 255, 255, 0.04);
}

/* Badges */
.cc-badge-featured {
	display: flex;
	align-items: center;
	gap: 5px;
	font-size: 10px;
	font-weight: 800;
	letter-spacing: 0.05em;
	text-transform: uppercase;
	color: #78350f;
	background: #fbbf24;
	padding: 4px 10px;
	border-radius: 100px;
	box-shadow: 0 2px 6px rgba(0,0,0,0.15);
}

.cc-badge-cert {
	display: flex;
	align-items: center;
	gap: 5px;
	font-size: 10px;
	font-weight: 800;
	letter-spacing: 0.05em;
	text-transform: uppercase;
	color: #1e40af;
	background: rgba(219, 234, 254, 0.92);
	backdrop-filter: blur(6px);
	padding: 4px 10px;
	border-radius: 100px;
	border: 1px solid rgba(147, 197, 253, 0.4);
}

.cc-badge-tag {
	display: flex;
	align-items: center;
	font-size: 10px;
	font-weight: 800;
	letter-spacing: 0.05em;
	text-transform: uppercase;
	color: #111827;
	background: rgba(255, 255, 255, 0.88);
	backdrop-filter: blur(6px);
	padding: 4px 10px;
	border-radius: 100px;
	border: 1px solid rgba(255, 255, 255, 0.4);
}

/* Meta pills */
.cc-meta-pill {
	display: flex;
	align-items: center;
	gap: 5px;
	padding: 3px 8px;
	border-radius: 6px;
	color: #6b7280;
	background: rgba(0, 0, 0, 0.03);
}

:root[data-theme="dark"] .cc-meta-pill {
	background: rgba(255, 255, 255, 0.06);
	color: #9ca3af;
}

.cc-meta-rating {
	background: rgba(245, 158, 11, 0.06);
	color: #b45309;
}

:root[data-theme="dark"] .cc-meta-rating {
	background: rgba(245, 158, 11, 0.1);
	color: #fbbf24;
}

/* Recommendation */
.cc-recommended {
	display: flex;
	align-items: center;
	gap: 6px;
	padding: 6px 20px;
	font-size: 11px;
	font-weight: 700;
	color: #92400e;
	background: linear-gradient(135deg, rgba(254, 243, 199, 0.6), rgba(252, 211, 77, 0.15));
	border-bottom: 1px solid rgba(245, 158, 11, 0.15);
}

:root[data-theme="dark"] .cc-recommended {
	background: rgba(245, 158, 11, 0.08);
	color: #fbbf24;
	border-color: rgba(245, 158, 11, 0.12);
}

/* Progress */
.cc-progress-track {
	height: 5px;
	width: 100%;
	background: rgba(0, 0, 0, 0.04);
	border-radius: 100px;
	overflow: hidden;
}

:root[data-theme="dark"] .cc-progress-track {
	background: rgba(255, 255, 255, 0.08);
}

.cc-progress-bar {
	height: 100%;
	background: linear-gradient(90deg, var(--sb-primary), var(--sb-medium));
	border-radius: 100px;
	transition: width 0.5s ease;
}

/* Footer */
.cc-footer-border {
	border-top: 1px solid rgba(0, 0, 0, 0.04);
}

:root[data-theme="dark"] .cc-footer-border {
	border-color: rgba(255, 255, 255, 0.06);
}

.cc-free-badge {
	font-size: 10px;
	font-weight: 800;
	text-transform: uppercase;
	letter-spacing: 0.04em;
	color: #059669;
	background: rgba(16, 185, 129, 0.08);
	padding: 3px 8px;
	border-radius: 6px;
}

:root[data-theme="dark"] .cc-free-badge {
	background: rgba(16, 185, 129, 0.12);
	color: #34d399;
}

/* Avatar group (global, not scoped) */
.avatar-group {
	display: inline-flex;
	align-items: center;
}

.avatar-group .avatar {
	transition: margin 0.1s ease-in-out;
}

.avatar-group.overlap .avatar + .avatar {
	margin-inline-start: calc(-8px);
}
</style>
