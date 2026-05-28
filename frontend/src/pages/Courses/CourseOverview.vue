<template>
	<div class="course-overview-page">
		<!-- Hero Section -->
		<div class="course-hero">
			<div class="course-hero-content">
				<div class="course-hero-left">
					<h1 class="course-hero-title">
						{{ course.data.title }}
					</h1>
					<p class="course-hero-subtitle">
						{{ course.data.short_introduction }}
					</p>
					<div class="course-hero-meta">
						<div
							v-if="parseInt(course.data.rating) > 0"
							class="course-hero-meta-item"
						>
							<Star class="size-4 text-transparent fill-yellow-400" />
							<span>{{ course.data.rating }}</span>
						</div>
						<div
							v-if="course.data.enrollment_count"
							class="course-hero-meta-item"
						>
							<Users class="size-4 opacity-70" />
							<span>{{ course.data.enrollment_count_formatted }} estudiantes</span>
						</div>
						<div class="course-hero-meta-item">
							<span
								class="h-6 me-1"
								:class="{
									'avatar-group overlap': course.data.instructors.length > 1,
								}"
							>
								<UserAvatar
									v-for="instructor in course.data.instructors"
									:user="instructor"
								/>
							</span>
							<CourseInstructors :instructors="course.data.instructors" />
						</div>
					</div>
					<div v-if="course.data.tags" class="course-hero-tags">
						<span
							v-for="tag in course.data.tags.split(', ')"
							class="course-tag"
						>
							{{ tag }}
						</span>
					</div>
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
   COURSE OVERVIEW — Page Layout
   ============================================== */

.course-overview-page {
	max-width: 100%;
	overflow-x: hidden;
}

/* ==============================================
   COURSE OVERVIEW — Hero Section
   ============================================== */

.course-hero {
	background: linear-gradient(135deg, var(--sb-dark, #061B49) 0%, #0D2B5E 50%, #1a3a6e 100%);
	padding: 2.5rem 2rem 2rem;
	position: relative;
	overflow: hidden;
}

.course-hero::before {
	content: '';
	position: absolute;
	top: -40%;
	right: -20%;
	width: 60%;
	height: 180%;
	background: radial-gradient(circle, rgba(245, 179, 1, 0.06) 0%, transparent 70%);
	pointer-events: none;
}

.course-hero::after {
	content: '';
	position: absolute;
	bottom: -30%;
	left: -5%;
	width: 30%;
	height: 60%;
	background: radial-gradient(circle, rgba(0, 123, 255, 0.08) 0%, transparent 70%);
	pointer-events: none;
}

.course-hero-content {
	max-width: 72rem;
	margin: 0 auto;
	position: relative;
	z-index: 1;
}

.course-hero-left {
	max-width: 65%;
}

@media (max-width: 768px) {
	.course-hero-left {
		max-width: 100%;
	}
	.course-hero {
		padding: 1.75rem 1.25rem 1.5rem;
	}
}

.course-hero-title {
	font-size: 1.75rem;
	font-weight: 800;
	color: #ffffff;
	line-height: 1.2;
	letter-spacing: -0.02em;
	margin: 0 0 0.75rem;
}

@media (min-width: 768px) {
	.course-hero-title {
		font-size: 2.25rem;
	}
}

.course-hero-subtitle {
	font-size: 1rem;
	line-height: 1.65;
	color: rgba(255, 255, 255, 0.82);
	margin: 0 0 1.25rem;
	max-width: 600px;
}

@media (min-width: 768px) {
	.course-hero-subtitle {
		font-size: 1.05rem;
	}
}

.course-hero-meta {
	display: flex;
	flex-wrap: wrap;
	align-items: center;
	gap: 1rem;
	color: rgba(255, 255, 255, 0.85);
	font-size: 0.875rem;
}

.course-hero-meta-item {
	display: flex;
	align-items: center;
	gap: 0.375rem;
}

.course-hero-meta-item .avatar {
	border: 2px solid rgba(255, 255, 255, 0.2) !important;
}

.course-hero-tags {
	display: flex;
	flex-wrap: wrap;
	gap: 0.5rem;
	margin-top: 1rem;
}

.course-tag {
	display: inline-block;
	padding: 0.2rem 0.75rem;
	font-size: 0.75rem;
	font-weight: 600;
	letter-spacing: 0.02em;
	color: rgba(255, 255, 255, 0.9);
	background: rgba(255, 255, 255, 0.12);
	border: 1px solid rgba(255, 255, 255, 0.1);
	border-radius: 20px;
	backdrop-filter: blur(4px);
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
		padding: 2rem 2rem;
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
	border-bottom: 2px solid rgba(0, 123, 255, 0.1);
}

.course-section-icon {
	width: 1.25rem;
	height: 1.25rem;
	color: var(--sb-primary, #007BFF);
	stroke-width: 2;
	flex-shrink: 0;
}

.course-section-title {
	font-size: 1.25rem;
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
   COURSE OVERVIEW — Dark Mode Overrides
   ============================================== */

:root[data-theme="dark"] .course-hero,
.dark .course-hero {
	background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #1a2744 100%);
}

:root[data-theme="dark"] .course-section-title,
.dark .course-section-title {
	color: #f3f4f6;
}

:root[data-theme="dark"] .course-section-header,
.dark .course-section-header {
	border-bottom-color: rgba(59, 130, 246, 0.15);
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
