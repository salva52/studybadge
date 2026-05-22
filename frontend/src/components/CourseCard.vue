<template>
	<div
		v-if="course.title"
		class="flex flex-col h-full overflow-hidden text-ink-gray-9 sb-course-card bg-white"
		style="min-height: 350px"
	>
		<div
			class="w-[100%] h-[168px] bg-cover bg-center bg-no-repeat"
			:style="
				course.image
					? { backgroundImage: `url('${encodeURI(course.image)}')` }
					: {
							backgroundImage: gradientColor,
							backgroundBlendMode: 'screen',
					  }
			"
		>
			<div class="flex items-center flex-wrap relative top-4 px-3 w-fit gap-1.5">
				<div
					v-if="course.featured"
					class="flex items-center gap-x-1 text-[11px] font-bold tracking-wide uppercase text-amber-700 bg-amber-100 border border-amber-200 px-2.5 py-1 rounded-full shadow-sm"
				>
					<Star class="size-3 stroke-2" />
					<span>{{ __('Más vendido') }}</span>
				</div>
				<div
					v-if="course.enable_certification || course.paid_certificate"
					class="flex items-center gap-x-1 text-[11px] font-bold tracking-wide uppercase text-blue-700 bg-blue-100 border border-blue-200 px-2.5 py-1 rounded-full shadow-sm"
				>
					<GraduationCap class="size-3 stroke-2" />
					<span>{{ __('Certificado incluido') }}</span>
				</div>
				<div
					v-if="course.tags"
					v-for="tag in course.tags?.split(', ')"
					class="flex items-center text-[11px] font-bold tracking-wide uppercase text-emerald-700 bg-emerald-100 border border-emerald-200 px-2.5 py-1 rounded-full shadow-sm"
				>
					{{ tag }}
				</div>
			</div>
			<div
				v-if="!course.image"
				class="flex items-center justify-center text-white flex-1 font-extrabold my-auto px-5 text-center leading-6 h-full"
				:class="
					course.title.length > 32
						? 'text-lg'
						: course.title.length > 20
						? 'text-xl'
						: 'text-2xl'
				"
			>
				{{ course.title }}
			</div>
		</div>
		<div
			v-if="course.custom_recommended_by_studybadge"
			class="px-5 pt-3 pb-0"
		>
			<span class="sb-recommended-badge">
				⭐ {{ __('Recomendado por StudyBadge') }}
			</span>
		</div>
		<div class="flex flex-col flex-auto p-5 border-0">
			<div class="flex items-center justify-between mb-2">
				<div v-if="course.lessons">
					<Tooltip :text="__('Lessons')">
						<span class="flex items-center">
							<BookOpen class="h-4 w-4 stroke-1.5 me-1" />
							{{ course.lessons }}
						</span>
					</Tooltip>
				</div>

				<div v-if="course.enrollments">
					<Tooltip :text="__('Enrolled Students')">
						<span class="flex items-center">
							<Users class="h-4 w-4 stroke-1.5 me-1" />
							{{ formatAmount(course.enrollments) }}
						</span>
					</Tooltip>
				</div>

				<div v-if="course.rating">
					<Tooltip :text="__('Average Rating')">
						<span class="flex items-center">
							<Star class="h-4 w-4 stroke-1.5 me-1" />
							{{ course.rating }}
						</span>
					</Tooltip>
				</div>

				<Tooltip v-if="course.featured" :text="__('Featured')">
					<Award class="size-4 stroke-2 text-ink-amber-3" />
				</Tooltip>
			</div>

			<div
				v-if="course.image"
				class="font-semibold leading-6"
				:class="course.title.length > 32 ? 'text-lg' : 'text-xl'"
			>
				{{ course.title }}
			</div>

			<div class="short-introduction text-sm text-ink-gray-7">
				{{ course.short_introduction }}
			</div>

			<ProgressBar
				v-if="user && course.membership"
				:progress="course.membership.progress"
			/>

			<div v-if="user && course.membership" class="text-sm mt-2 mb-4">
				{{ Math.ceil(course.membership.progress) }}% {{ __('completed') }}
			</div>

			<div class="flex items-center justify-between mt-auto">
				<div class="flex avatar-group overlap">
					<div
						class="h-6 me-1"
						:class="{ 'avatar-group overlap': course.instructors.length > 1 }"
					>
						<UserAvatar
							v-for="instructor in course.instructors"
							:user="instructor"
						/>
					</div>
					<CourseInstructors :instructors="course.instructors" />
				</div>

				<div class="flex items-center gap-x-2">
					<div v-if="course.paid_course" class="font-semibold">
						{{ course.price }}
					</div>

					<Tooltip
						v-if="course.paid_certificate || course.enable_certification"
						:text="__('Get Certified')"
					>
						<GraduationCap class="size-5 stroke-1.5 text-ink-gray-7" />
					</Tooltip>
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
import { computed, watch } from 'vue'
import CourseInstructors from '@/components/CourseInstructors.vue'
import UserAvatar from '@/components/UserAvatar.vue'
import ProgressBar from '@/components/ProgressBar.vue'
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
	let color = props.course.card_gradient?.toLowerCase() || 'blue'
	let colorMap = colors[themeMode][color]
	return `linear-gradient(to top right, black, ${colorMap[400]})`
})
</script>
<style>
.course-card-pills {
	background: #ffffff;
	margin-left: 0;
	margin-right: 0.5rem;
	padding: 3.5px 8px;
	font-size: 11px;
	text-align: center;
	letter-spacing: 0.011em;
	text-transform: uppercase;
	font-weight: 600;
	width: fit-content;
}

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

.short-introduction {
	display: -webkit-box;
	-webkit-line-clamp: 2;
	-webkit-box-orient: vertical;
	text-overflow: ellipsis;
	width: 100%;
	overflow: hidden;
	margin: 0.25rem 0 1.25rem;
	line-height: 1.6;
}
</style>
