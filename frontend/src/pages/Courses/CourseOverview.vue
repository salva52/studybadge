<template>
	<div class="course-overview-page">
		<!-- Header Section -->
		<div class="course-header-section">
			<div class="course-header-content">
				<h1 class="course-header-title">
					{{ course.data.title }}
				</h1>
				<p class="course-header-subtitle">
					{{ course.data.short_introduction }}
				</p>
				<div class="course-header-meta">
					<div
						v-if="parseInt(course.data.rating) > 0"
						class="course-meta-pill"
					>
						<Star class="size-3.5 text-transparent fill-yellow-500" />
						<span>{{ course.data.rating }}</span>
					</div>
					<div
						v-if="course.data.enrollment_count"
						class="course-meta-pill"
					>
						<Users class="size-3.5" />
						<span>{{ course.data.enrollment_count_formatted }} estudiantes</span>
					</div>
					<div class="course-meta-pill course-meta-instructor">
						<UserAvatar
							v-for="instructor in course.data.instructors"
							:user="instructor"
							class="course-meta-avatar"
						/>
						<CourseInstructors :instructors="course.data.instructors" />
					</div>
				</div>
				<div v-if="course.data.tags" class="course-header-tags">
					<span
						v-for="tag in course.data.tags.split(', ')"
						class="course-tag-pill"
					>
						{{ tag }}
					</span>
				</div>
			</div>
		</div>

		<!-- Main Content -->
		<div class="course-overview-body">
			<div class="course-overview-main">
				<!-- Mobile Card -->
				<div class="md:hidden mb-6">
					<CourseCardOverlay :course="course" />
				</div>

				<!-- Description -->
				<section v-if="course.data.description" class="course-section">
					<div class="course-section-header">
						<BookOpen class="course-section-icon" />
						<h2 class="course-section-title">{{ __('Acerca de este curso') }}</h2>
					</div>
					<div
						v-html="course.data.description"
						class="course-description ProseMirror prose prose-table:table-fixed prose-td:p-2 prose-th:p-2 prose-td:border prose-th:border prose-td:border-outline-gray-2 prose-th:border-outline-gray-2 prose-td:relative prose-th:relative prose-th:bg-surface-gray-2 prose-sm max-w-none !whitespace-normal"
					></div>
				</section>

				<!-- Course Outline -->
				<section class="course-section">
					<div class="course-section-header">
						<ListOrdered class="course-section-icon" />
						<h2 class="course-section-title">{{ __('Contenido del curso') }}</h2>
					</div>
					<CourseOutline
						:title="''"
						:courseName="course.data.name"
						:showOutline="true"
						:getProgress="course.data.membership ? true : false"
					/>
				</section>

				<!-- Reviews -->
				<section class="course-section">
					<CourseReviews
						:courseName="course.data.name"
						:avg_rating="course.data.rating"
						:membership="course.data.membership || null"
					/>
				</section>
			</div>

			<!-- Desktop Sidebar -->
			<aside class="course-overview-sidebar">
				<div class="course-sidebar-sticky">
					<CourseCardOverlay :course="course" />
				</div>
			</aside>
		</div>

		<RelatedCourses :courseName="course.data.name" />
	</div>
</template>
<script setup lang="ts">
import { Star, Users, BookOpen, ListOrdered } from 'lucide-vue-next'
import { Badge, Tooltip } from 'frappe-ui'
import CourseCardOverlay from '@/components/CourseCardOverlay.vue'
import CourseOutline from '@/components/CourseOutline.vue'
import CourseReviews from '@/components/CourseReviews.vue'
import UserAvatar from '@/components/UserAvatar.vue'
import CourseInstructors from '@/components/CourseInstructors.vue'
import RelatedCourses from '@/components/RelatedCourses.vue'

const props = defineProps<{
	course: any
}>()
</script>
<style>
/* ==============================================
   COURSE OVERVIEW — Page
   ============================================== */

.course-overview-page {
	max-width: 100%;
	overflow-x: hidden;
}

/* ==============================================
   COURSE OVERVIEW — Header (clean, no hero)
   ============================================== */

.course-header-section {
	padding: 2rem 1.5rem 1.5rem;
	border-bottom: 1px solid rgba(6, 27, 73, 0.06);
}

@media (min-width: 768px) {
	.course-header-section {
		padding: 2.5rem 2.5rem 2rem;
	}
}

.course-header-content {
	max-width: 72rem;
	margin: 0 auto;
}

.course-header-title {
	font-size: 1.75rem;
	font-weight: 800;
	color: var(--sb-dark, #061B49);
	line-height: 1.2;
	letter-spacing: -0.025em;
	margin: 0 0 0.625rem;
}

@media (min-width: 768px) {
	.course-header-title {
		font-size: 2.125rem;
	}
}

.course-header-subtitle {
	font-size: 1rem;
	line-height: 1.65;
	color: #6b7280;
	margin: 0 0 1.25rem;
	max-width: 680px;
}

/* Meta pills row */
.course-header-meta {
	display: flex;
	flex-wrap: wrap;
	align-items: center;
	gap: 0.5rem;
}

.course-meta-pill {
	display: inline-flex;
	align-items: center;
	gap: 0.35rem;
	padding: 0.3rem 0.75rem;
	background: #f3f4f6;
	border-radius: 20px;
	font-size: 0.8125rem;
	font-weight: 500;
	color: #374151;
	border: 1px solid rgba(6, 27, 73, 0.04);
}

.course-meta-pill svg {
	color: #6b7280;
}

.course-meta-instructor {
	gap: 0.5rem;
	padding-left: 0.3rem;
}

.course-meta-instructor .avatar {
	width: 22px !important;
	height: 22px !important;
}

.course-meta-avatar {
	width: 22px !important;
	height: 22px !important;
	flex-shrink: 0;
}

/* Tags */
.course-header-tags {
	display: flex;
	flex-wrap: wrap;
	gap: 0.375rem;
	margin-top: 0.875rem;
}

.course-tag-pill {
	display: inline-block;
	padding: 0.2rem 0.65rem;
	font-size: 0.6875rem;
	font-weight: 600;
	text-transform: uppercase;
	letter-spacing: 0.04em;
	color: var(--sb-primary, #007BFF);
	background: rgba(0, 123, 255, 0.06);
	border: 1px solid rgba(0, 123, 255, 0.12);
	border-radius: 6px;
}

/* ==============================================
   COURSE OVERVIEW — Body Layout
   ============================================== */

.course-overview-body {
	display: flex;
	gap: 2rem;
	max-width: 72rem;
	margin: 0 auto;
	padding: 2rem 1.25rem;
}

@media (min-width: 768px) {
	.course-overview-body {
		padding: 2rem 2.5rem;
	}
}

.course-overview-main {
	flex: 1;
	min-width: 0;
}

.course-overview-sidebar {
	display: none;
}

@media (min-width: 768px) {
	.course-overview-sidebar {
		display: block;
		width: 340px;
		flex-shrink: 0;
	}
}

.course-sidebar-sticky {
	position: sticky;
	top: 70px;
}

/* ==============================================
   COURSE OVERVIEW — Sections
   ============================================== */

.course-section {
	margin-bottom: 2.5rem;
}

.course-section-header {
	display: flex;
	align-items: center;
	gap: 0.625rem;
	margin-bottom: 1.25rem;
	padding-bottom: 0.75rem;
	border-bottom: 2px solid rgba(0, 123, 255, 0.08);
}

.course-section-icon {
	width: 1.25rem;
	height: 1.25rem;
	color: var(--sb-primary, #007BFF);
	stroke-width: 2;
	flex-shrink: 0;
}

.course-section-title {
	font-size: 1.2rem;
	font-weight: 700;
	color: var(--sb-dark, #061B49);
	margin: 0;
	letter-spacing: -0.01em;
}

/* ==============================================
   COURSE OVERVIEW — Description
   ============================================== */

.course-description {
	font-size: 1rem;
	line-height: 1.8;
	color: #374151;
}

.course-description p {
	margin-bottom: 1rem;
}

.course-description ul,
.course-description ol {
	padding-left: 1.25rem;
	margin: 0.75rem 0;
}

.course-description li {
	line-height: 1.8;
	margin-bottom: 0.375rem;
}

.course-description li::marker {
	color: var(--sb-primary, #007BFF);
}

.course-description strong,
.course-description b {
	color: var(--sb-dark, #061B49);
	font-weight: 600;
}

/* ==============================================
   Dark Mode
   ============================================== */

:root[data-theme="dark"] .course-header-section,
.dark .course-header-section {
	border-bottom-color: rgba(255, 255, 255, 0.06);
}

:root[data-theme="dark"] .course-header-title,
.dark .course-header-title {
	color: #f3f4f6;
}

:root[data-theme="dark"] .course-header-subtitle,
.dark .course-header-subtitle {
	color: #9ca3af;
}

:root[data-theme="dark"] .course-meta-pill,
.dark .course-meta-pill {
	background: rgba(255, 255, 255, 0.06);
	color: #d1d5db;
	border-color: rgba(255, 255, 255, 0.06);
}

:root[data-theme="dark"] .course-meta-pill svg,
.dark .course-meta-pill svg {
	color: #9ca3af;
}

:root[data-theme="dark"] .course-tag-pill,
.dark .course-tag-pill {
	color: #60a5fa;
	background: rgba(59, 130, 246, 0.1);
	border-color: rgba(59, 130, 246, 0.15);
}

:root[data-theme="dark"] .course-section-title,
.dark .course-section-title {
	color: #f3f4f6;
}

:root[data-theme="dark"] .course-section-header,
.dark .course-section-header {
	border-bottom-color: rgba(59, 130, 246, 0.12);
}

:root[data-theme="dark"] .course-description,
.dark .course-description {
	color: #d1d5db;
}

:root[data-theme="dark"] .course-description strong,
:root[data-theme="dark"] .course-description b,
.dark .course-description strong,
.dark .course-description b {
	color: #f3f4f6;
}
</style>
