<template>
	<div
		v-if="course.title"
		class="flex flex-col h-full overflow-hidden text-ink-gray-9 sb-course-card bg-white dark:bg-gray-800 rounded-2xl shadow-md hover:shadow-xl hover:-translate-y-1 transition-all duration-300 border border-gray-100 dark:border-gray-700"
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
					class="flex items-center gap-x-1 text-[11px] font-bold tracking-wide uppercase text-amber-700 dark:text-amber-300 bg-amber-100 dark:bg-amber-900/30 border border-amber-200 dark:border-amber-800 px-2.5 py-1 rounded-full shadow-sm"
				>
					<Star class="size-3 stroke-2" />
					<span>{{ __('Más vendido') }}</span>
				</div>
				<div
					v-if="course.enable_certification || course.paid_certificate"
					class="flex items-center gap-x-1 text-[11px] font-bold tracking-wide uppercase text-blue-700 dark:text-blue-300 bg-blue-100 dark:bg-blue-900/30 border border-blue-200 dark:border-blue-800 px-2.5 py-1 rounded-full shadow-sm"
				>
					<GraduationCap class="size-3 stroke-2" />
					<span>{{ __('Certificado incluido') }}</span>
				</div>
				<div
					v-if="course.tags"
					v-for="tag in course.tags?.split(', ')"
					class="flex items-center text-[11px] font-bold tracking-wide uppercase text-green-700 dark:text-green-300 bg-green-100 dark:bg-green-900/30 border border-green-200 dark:border-green-800 px-2.5 py-1 rounded-full shadow-sm"
				>
					{{ tag }}
				</div>
			</div>
			<div
				v-if="!course.image"
				class="flex items-center justify-center text-white flex-1 font-extrabold my-auto px-5 text-center leading-6 h-full relative overflow-hidden"
				:class="
					course.title.length > 32
						? 'text-lg'
						: course.title.length > 20
						? 'text-xl'
						: 'text-2xl'
				"
			>
				<BookOpen class="absolute -right-6 -bottom-6 w-32 h-32 text-white/20 -rotate-12 transform" />
				<span class="z-10 relative drop-shadow-md">{{ course.title }}</span>
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
			<div class="flex items-center gap-2 mb-3 text-sm font-medium flex-wrap">
				<div v-if="course.lessons">
					<Tooltip :text="__('Lecciones')">
						<span class="flex items-center text-blue-700 dark:text-blue-300 bg-blue-50 dark:bg-blue-900/20 border border-blue-100 dark:border-blue-800 px-2 py-1 rounded-lg">
							<BookOpen class="h-3.5 w-3.5 stroke-2 me-1.5" />
							{{ course.lessons }}
						</span>
					</Tooltip>
				</div>

				<div v-if="course.enrollments">
					<Tooltip :text="__('Estudiantes inscritos')">
						<span class="flex items-center text-green-700 dark:text-green-300 bg-green-50 dark:bg-green-900/20 border border-green-100 dark:border-green-800 px-2 py-1 rounded-lg">
							<Users class="h-3.5 w-3.5 stroke-2 me-1.5" />
							{{ formatAmount(course.enrollments) }}
						</span>
					</Tooltip>
				</div>

				<div v-if="course.rating">
					<Tooltip :text="__('Calificación Promedio')">
						<span class="flex items-center text-amber-700 dark:text-amber-300 bg-amber-50 dark:bg-amber-900/20 border border-amber-100 dark:border-amber-800 px-2 py-1 rounded-lg">
							<Star class="h-3.5 w-3.5 stroke-2 me-1.5 text-amber-500 fill-amber-500" />
							{{ course.rating }}
						</span>
					</Tooltip>
				</div>

				<!-- Placeholders for Duration and Level (Custom fields to be added later) -->
				<div v-if="isPublic">
					<Tooltip :text="__('Duración aproximada')">
						<span class="flex items-center text-purple-700 dark:text-purple-300 bg-purple-50 dark:bg-purple-900/20 border border-purple-100 dark:border-purple-800 px-2 py-1 rounded-lg">
							<Clock class="h-3.5 w-3.5 stroke-2 me-1.5" />
							2 hrs
						</span>
					</Tooltip>
				</div>
				<div v-if="isPublic">
					<Tooltip :text="__('Nivel del curso')">
						<span class="flex items-center text-teal-700 dark:text-teal-300 bg-teal-50 dark:bg-teal-900/20 border border-teal-100 dark:border-teal-800 px-2 py-1 rounded-lg">
							<BarChart class="h-3.5 w-3.5 stroke-2 me-1.5" />
							Principiante
						</span>
					</Tooltip>
				</div>
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
			
			<div v-if="isPublic" class="mt-5 w-full">
				<button class="w-full py-2.5 bg-gray-50 hover:bg-[#007BFF] text-[#007BFF] hover:text-white dark:bg-gray-700 dark:text-blue-400 dark:hover:bg-[#007BFF] dark:hover:text-white font-bold rounded-xl transition-colors border border-gray-200 dark:border-gray-600 hover:border-[#007BFF]">
					Ver curso
				</button>
			</div>
		</div>
	</div>
</template>
<script setup>
import { Award, BookOpen, GraduationCap, Star, Users, Clock, BarChart } from 'lucide-vue-next'
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
	isPublic: {
		type: Boolean,
		default: false,
	}
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
