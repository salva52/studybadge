<template>
	<div
		v-if="course.title"
		class="group flex flex-col h-full overflow-hidden text-ink-gray-9 bg-white dark:bg-gray-800 rounded-3xl shadow-sm hover:shadow-xl hover:-translate-y-1.5 transition-all duration-300 border border-gray-100 dark:border-gray-700"
		style="min-height: 380px"
	>
		<!-- Image Section -->
		<div class="relative w-full h-48 overflow-hidden bg-gray-100">
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
			
			<!-- Optional Overlay for better text readability if no image -->
			<div v-if="!course.image" class="absolute inset-0 bg-black/20 mix-blend-multiply"></div>

			<!-- Badges -->
			<div class="absolute top-4 left-4 right-4 flex flex-wrap gap-2 z-10">
				<div
					v-if="course.featured"
					class="flex items-center gap-1.5 text-[10px] font-bold tracking-wider uppercase text-amber-900 bg-amber-400 border-none px-3 py-1.5 rounded-full shadow-md"
				>
					<Star class="size-3 fill-amber-900" />
					<span>{{ __('Más vendido') }}</span>
				</div>
				<div
					v-if="course.enable_certification || course.paid_certificate"
					class="flex items-center gap-1.5 text-[10px] font-bold tracking-wider uppercase text-blue-900 bg-blue-100/90 backdrop-blur-sm border border-blue-200/50 px-3 py-1.5 rounded-full shadow-sm"
				>
					<GraduationCap class="size-3 stroke-2" />
					<span>{{ __('Certificado') }}</span>
				</div>
				<div
					v-if="course.tags"
					v-for="tag in course.tags?.split(', ').slice(0, 2)"
					class="flex items-center text-[10px] font-bold tracking-wider uppercase text-gray-900 bg-white/90 backdrop-blur-sm border border-white/50 px-3 py-1.5 rounded-full shadow-sm"
				>
					{{ tag }}
				</div>
			</div>
			
			<div
				v-if="!course.image"
				class="absolute inset-0 flex items-center justify-center p-6 text-center z-10"
			>
				<BookOpen class="absolute -right-8 -bottom-8 w-40 h-40 text-white/10 -rotate-12 transform" />
				<span class="text-2xl font-extrabold text-white drop-shadow-lg leading-tight">{{ course.title }}</span>
			</div>
		</div>

		<!-- Recommendation Badge -->
		<div
			v-if="course.custom_recommended_by_studybadge"
			class="bg-gradient-to-r from-amber-50 to-amber-100/50 px-6 py-2 border-b border-amber-100"
		>
			<span class="text-xs font-bold text-amber-800 flex items-center gap-1.5">
				<Star class="size-3.5 text-amber-500 fill-amber-500" /> {{ __('Recomendado por StudyBadge') }}
			</span>
		</div>

		<!-- Content Section -->
		<div class="flex flex-col flex-auto p-6">
			<!-- Meta tags -->
			<div class="flex items-center gap-3 mb-4 text-xs font-semibold text-gray-500 flex-wrap">
				<div v-if="course.lessons" class="flex items-center gap-1.5 bg-gray-50 px-2.5 py-1 rounded-md">
					<BookOpen class="h-3.5 w-3.5 stroke-2" />
					{{ course.lessons }} {{ __('Lecc.') }}
				</div>
				<div v-if="course.enrollments" class="flex items-center gap-1.5 bg-gray-50 px-2.5 py-1 rounded-md">
					<Users class="h-3.5 w-3.5 stroke-2" />
					{{ formatAmount(course.enrollments) }}
				</div>
				<div v-if="course.rating" class="flex items-center gap-1.5 bg-amber-50 text-amber-700 px-2.5 py-1 rounded-md">
					<Star class="h-3.5 w-3.5 stroke-2 fill-amber-500 text-amber-500" />
					{{ course.rating }}
				</div>
			</div>

			<h3 class="text-xl font-bold text-gray-900 leading-snug mb-2 line-clamp-2 group-hover:text-[#0d6efd] transition-colors">
				{{ course.title }}
			</h3>

			<p class="text-sm text-gray-500 leading-relaxed mb-6 line-clamp-2">
				{{ course.short_introduction }}
			</p>

			<!-- Progress Bar (if enrolled) -->
			<div v-if="user && course.membership" class="mt-auto mb-6">
				<div class="flex justify-between items-end mb-2">
					<span class="text-xs font-bold text-gray-900">{{ __('Tu progreso') }}</span>
					<span class="text-xs font-bold text-[#0d6efd]">{{ Math.ceil(course.membership.progress) }}%</span>
				</div>
				<div class="h-2 w-full bg-gray-100 rounded-full overflow-hidden">
					<div class="h-full bg-[#0d6efd] rounded-full transition-all duration-500" :style="`width: ${course.membership.progress}%`"></div>
				</div>
			</div>

			<!-- Footer (Instructors & Price) -->
			<div class="flex items-center justify-between mt-auto pt-4 border-t border-gray-100" :class="{'mt-auto': !(user && course.membership)}">
				<div class="flex items-center gap-3">
					<div class="flex avatar-group overlap">
						<div class="h-8" :class="{ 'avatar-group overlap': course.instructors?.length > 1 }">
							<UserAvatar
								v-for="instructor in course.instructors"
								:user="instructor"
							/>
						</div>
					</div>
					<CourseInstructors :instructors="course.instructors" class="text-sm font-medium" />
				</div>

				<div class="flex items-center gap-x-2">
					<div v-if="course.paid_course" class="font-black text-gray-900 text-lg">
						{{ course.price }}
					</div>
					<div v-else class="text-xs font-bold text-green-600 bg-green-50 px-2 py-1 rounded-md uppercase tracking-wide">
						{{ __('Gratis') }}
					</div>
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
	return `linear-gradient(to top right, #08204e, ${colorMap[400]})`
})
</script>
<style>
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
