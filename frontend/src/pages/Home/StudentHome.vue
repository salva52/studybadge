<template>
	<div class="space-y-12">
		<!-- 2. Tarjetas de resumen rápido -->
		<div class="grid grid-cols-2 md:grid-cols-4 gap-4">
			<div class="bg-white rounded-2xl p-5 border border-gray-100 shadow-sm flex items-center gap-4 hover:shadow-md transition-shadow">
				<div class="bg-blue-50 text-[#0d6efd] p-3 rounded-xl shrink-0">
					<BookOpen class="size-6" />
				</div>
				<div>
					<div class="text-xs text-gray-500 font-semibold uppercase tracking-wide">{{ __('Cursos activos') }}</div>
					<div class="text-2xl font-bold text-gray-900">{{ myCourses.data?.length || 0 }}</div>
				</div>
			</div>
			
			<div class="bg-white rounded-2xl p-5 border border-gray-100 shadow-sm flex items-center gap-4 hover:shadow-md transition-shadow">
				<div class="bg-amber-50 text-amber-500 p-3 rounded-xl shrink-0">
					<Award class="size-6" />
				</div>
				<div>
					<div class="text-xs text-gray-500 font-semibold uppercase tracking-wide">{{ __('Certificados') }}</div>
					<div class="text-2xl font-bold text-gray-900">{{ certCount || 0 }}</div>
				</div>
			</div>
			
			<div class="bg-white rounded-2xl p-5 border border-gray-100 shadow-sm flex items-center gap-4 hover:shadow-md transition-shadow">
				<div class="bg-green-50 text-green-500 p-3 rounded-xl shrink-0">
					<Zap class="size-6" />
				</div>
				<div>
					<div class="text-xs text-gray-500 font-semibold uppercase tracking-wide">{{ __('Racha actual') }}</div>
					<div class="text-2xl font-bold text-gray-900">{{ streakInfo.data?.current_streak || 0 }} <span class="text-base font-normal text-gray-400">{{ __('días') }}</span></div>
				</div>
			</div>
			
			<div class="bg-white rounded-2xl p-5 border border-gray-100 shadow-sm flex items-center gap-4 hover:shadow-md transition-shadow">
				<div class="p-3 rounded-xl shrink-0" :class="billing.data?.active ? 'bg-gradient-to-br from-amber-400 to-amber-200 text-white shadow-inner' : 'bg-gray-100 text-gray-500'">
					<Crown class="size-6" />
				</div>
				<div>
					<div class="text-xs text-gray-500 font-semibold uppercase tracking-wide">{{ __('Plan actual') }}</div>
					<div class="text-lg font-bold text-gray-900 truncate" :class="{'text-amber-500': billing.data?.active}">
						{{ billing.data?.active ? __('StudyBadge Plus') : __('Gratuito') }}
					</div>
				</div>
			</div>
		</div>

		<!-- 3. Continúa donde lo dejaste -->
		<div v-if="continueCourse" class="bg-white rounded-3xl border border-gray-100 shadow-sm overflow-hidden flex flex-col md:flex-row relative">
			<div class="w-full md:w-2/5 h-48 md:h-auto bg-cover bg-center" :style="continueCourse.image ? `background-image: url('${encodeURI(continueCourse.image)}')` : `background: linear-gradient(to top right, #08204e, #0d6efd)`">
			</div>
			<div class="w-full md:w-3/5 p-8 flex flex-col justify-center bg-gradient-to-l from-white to-white/95">
				<div class="flex items-center gap-2 text-sm font-bold text-[#0d6efd] mb-2 uppercase tracking-wider">
					<PlayCircle class="size-4" /> {{ __('Continúa donde lo dejaste') }}
				</div>
				<h2 class="text-2xl font-bold text-gray-900 mb-2">{{ continueCourse.title }}</h2>
				<p class="text-gray-500 text-sm mb-6 line-clamp-2">{{ continueCourse.short_introduction }}</p>
				
				<div class="mb-6">
					<div class="flex justify-between text-xs font-bold text-gray-700 mb-2">
						<span>{{ __('Progreso del curso') }}</span>
						<span>{{ Math.ceil(continueCourse.membership?.progress || 0) }}%</span>
					</div>
					<div class="h-2.5 w-full bg-gray-100 rounded-full overflow-hidden">
						<div class="h-full bg-[#0d6efd] rounded-full transition-all duration-500" :style="`width: ${continueCourse.membership?.progress || 0}%`"></div>
					</div>
				</div>
				
				<router-link
					:to="{ name: 'CourseDetail', params: { courseName: continueCourse.name } }"
					class="inline-flex items-center justify-center rounded-xl bg-gray-900 px-6 py-3 text-sm font-bold text-white shadow-md transition-transform hover:-translate-y-0.5 hover:bg-black w-fit"
				>
					{{ __('Continuar lección') }} <MoveRight class="size-4 ml-2" />
				</router-link>
			</div>
		</div>

		<!-- Próximas clases en vivo (Opcional, de la base original) -->
		<div v-if="myLiveClasses.data?.length">
			<div class="font-bold text-xl mb-4 text-gray-900 flex items-center gap-2">
				<Video class="size-5 text-[#0d6efd]" />
				{{ __('Próximas Clases en Vivo') }}
			</div>
			<div class="grid grid-cols-1 md:grid-cols-4 gap-5">
				<div v-for="cls in myLiveClasses.data" class="bg-white border border-gray-100 rounded-2xl hover:border-blue-200 p-5 shadow-sm transition-all hover:shadow-md">
					<div class="font-bold text-gray-900 leading-tight mb-2">{{ cls.title }}</div>
					<div class="text-sm text-gray-500 leading-snug mb-5">{{ cls.description }}</div>
					<div class="mt-auto space-y-3 text-sm text-gray-700">
						<div class="flex items-center gap-x-2 bg-gray-50 p-2 rounded-lg">
							<Calendar class="w-4 h-4 text-blue-500" />
							<span class="font-medium">{{ dayjs(cls.date).format('DD MMM YYYY') }}</span>
						</div>
						<div class="flex items-center gap-x-2 bg-gray-50 p-2 rounded-lg">
							<Clock class="w-4 h-4 text-amber-500" />
							<span class="font-medium">{{ formatTime(cls.time) }} - {{ dayjs(getClassEnd(cls)).format('HH:mm A') }}</span>
						</div>
						<div v-if="canAccessClass(cls)" class="flex items-center gap-x-2 text-ink-gray-9 mt-4">
							<a
								:href="cls.join_url"
								target="_blank"
								class="w-full cursor-pointer inline-flex items-center justify-center gap-2 transition-colors font-bold text-white bg-[#0d6efd] hover:bg-blue-700 h-10 px-4 rounded-xl shadow-sm"
							>
								<Video class="h-4 w-4" />
								{{ __('Unirse a clase') }}
							</a>
						</div>
					</div>
				</div>
			</div>
		</div>

		<!-- 4. Mis cursos -->
		<div v-if="remainingCourses.length" class="mt-12">
			<div class="flex items-center justify-between mb-6">
				<h3 class="font-bold text-2xl text-gray-900 flex items-center gap-2">
					<BookOpen class="size-6 text-[#0d6efd]" />
					{{ __('Mis Cursos') }}
				</h3>
				<router-link :to="{ name: 'Courses' }" class="flex items-center gap-x-1 text-sm font-bold text-[#0d6efd] hover:text-[#0b2f73] transition-colors">
					<span>{{ __('Ver todos') }}</span>
					<MoveRight class="size-4" />
				</router-link>
			</div>
			<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
				<router-link
					v-for="course in remainingCourses"
					:to="{ name: 'CourseDetail', params: { courseName: course.name } }"
				>
					<CourseCard :course="course" />
				</router-link>
			</div>
		</div>

		<div class="grid grid-cols-1 lg:grid-cols-3 gap-8 mt-12">
			
			<!-- 6. Certificados y logros -->
			<div class="lg:col-span-2">
				<h3 class="font-bold text-xl text-gray-900 flex items-center gap-2 mb-6">
					<Award class="size-5 text-amber-500" />
					{{ __('Certificados y Logros') }}
				</h3>
				<div class="bg-white border border-gray-100 rounded-3xl p-8 shadow-sm text-center">
					<div class="flex justify-center mb-4">
						<div class="bg-amber-50 p-4 rounded-full">
							<Award class="size-10 text-amber-400" />
						</div>
					</div>
					<h4 class="font-bold text-lg text-gray-900 mb-2">{{ certCount ? __('Tienes certificados desbloqueados') : __('Aún no tienes certificados') }}</h4>
					<p class="text-gray-500 text-sm max-w-sm mx-auto mb-6">
						{{ __('Completa cursos y aprueba tus evaluaciones para añadir certificaciones verificables a tu perfil profesional.') }}
					</p>
					<router-link :to="{ name: 'ProfileCertificates', params: { user: user.data?.name } }" class="inline-flex items-center justify-center rounded-xl border-2 border-gray-200 bg-white px-6 py-2.5 text-sm font-bold text-gray-700 hover:border-gray-300 hover:bg-gray-50 transition-colors">
						{{ __('Ver mis certificados') }}
					</router-link>
				</div>
			</div>

			<!-- 7. Herramientas IA / Plus -->
			<div class="lg:col-span-1">
				<h3 class="font-bold text-xl text-gray-900 flex items-center gap-2 mb-6">
					<Sparkles class="size-5 text-[#0d6efd]" />
					{{ __('Herramientas Pro') }}
				</h3>
				<div class="bg-gradient-to-br from-[#08204e] to-[#0b2f73] rounded-3xl p-8 text-white shadow-xl relative overflow-hidden h-full flex flex-col">
					<div class="absolute -top-12 -right-12 w-40 h-40 bg-blue-500 opacity-20 blur-2xl rounded-full"></div>
					<Crown class="size-8 text-amber-400 mb-4" />
					<h4 class="font-bold text-xl mb-2">StudyBadge Plus</h4>
					<p class="text-blue-100 text-sm mb-6 flex-1">
						{{ __('Desbloquea tutor IA ilimitado, todos los certificados, herramientas de estudio premium y más.') }}
					</p>
					<ul class="space-y-3 mb-8 text-sm font-medium text-blue-50">
						<li class="flex items-center gap-2"><CheckCircle2 class="size-4 text-amber-400" /> {{ __('Tutor IA ilimitado') }}</li>
						<li class="flex items-center gap-2"><CheckCircle2 class="size-4 text-amber-400" /> {{ __('Generación de cursos') }}</li>
						<li class="flex items-center gap-2"><CheckCircle2 class="size-4 text-amber-400" /> {{ __('Certificados incluidos') }}</li>
					</ul>
					<router-link
						:to="{ name: 'Plus' }"
						class="w-full flex items-center justify-center rounded-xl bg-gradient-to-r from-amber-400 to-yellow-500 px-4 py-3.5 text-sm font-bold text-amber-900 shadow-md transition-transform hover:-translate-y-0.5"
					>
						{{ billing.data?.active ? __('Gestionar mi Plus') : __('Desbloquear Plus') }}
					</router-link>
				</div>
			</div>

		</div>
		
		<UpcomingEvaluations :forHome="true" class="mt-12" />
		
	</div>
</template>
<script setup lang="ts">
import { computed, inject, ref, onMounted } from 'vue'
import { call, createResource, Tooltip } from 'frappe-ui'
import { formatTime } from '@/utils'
import {
	Calendar,
	Clock,
	Info,
	Monitor,
	MoveRight,
	Video,
	BookOpen,
	Award,
	Zap,
	Crown,
	PlayCircle,
	Sparkles,
	CheckCircle2
} from 'lucide-vue-next'
import CourseCard from '@/components/CourseCard.vue'
import BatchCard from '@/pages/Batches/components/BatchCard.vue'
import UpcomingEvaluations from '@/components/UpcomingEvaluations.vue'

const dayjs = inject<any>('$dayjs')
const user = inject<any>('$user')

const props = defineProps<{
	myLiveClasses: any
}>()

const myCourses = createResource({
	url: 'lms.lms.api.get_my_courses',
	auto: true,
})

const myBatches = createResource({
	url: 'lms.lms.api.get_my_batches',
	auto: true,
})

const streakInfo = createResource({
	url: 'lms.lms.api.get_streak_info',
	auto: true,
})

const billing = createResource({
	url: 'lms.lms.subscriptions.get_plus_billing',
	auto: true,
})

const certCount = ref(0)
const fetchCertCount = () => {
	call('frappe.client.get_count', {
		doctype: 'LMS Certificate',
		filters: {
			member: user?.data?.name,
		},
	}).then((data: any) => {
		certCount.value = data
	})
}

onMounted(() => {
	fetchCertCount()
})

const continueCourse = computed(() => {
	if (!myCourses.data?.length) return null
	// Asumimos que el primer curso está en progreso si tiene membresía
	const course = myCourses.data[0]
	if (course.membership) return course
	return null
})

const remainingCourses = computed(() => {
	if (!myCourses.data?.length) return []
	if (continueCourse.value) return myCourses.data.slice(1)
	return myCourses.data
})

const getClassEnd = (cls: { date: string; time: string; duration: number }) => {
	const classStart = new Date(`${cls.date}T${cls.time}`)
	return new Date(classStart.getTime() + cls.duration * 60000)
}

const canAccessClass = (cls: {
	date: string
	time: string
	duration: number
}) => {
	if (cls.date < dayjs().format('YYYY-MM-DD')) return false
	if (cls.date > dayjs().format('YYYY-MM-DD')) return false
	if (hasClassEnded(cls)) return false
	return true
}

const hasClassEnded = (cls: {
	date: string
	time: string
	duration: number
}) => {
	const classEnd = getClassEnd(cls)
	const now = new Date()
	return now > classEnd
}
</script>
