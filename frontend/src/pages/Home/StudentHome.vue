<template>
	<div class="space-y-10">

		<!-- ═══ 1. STAT CARDS ═══ -->
		<div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
			<div v-for="stat in statCards" :key="stat.label" class="sh-stat-card group">
				<div class="sh-stat-icon" :style="`--icon-bg: ${stat.bgColor}; --icon-color: ${stat.iconColor}`">
					<component :is="stat.icon" class="size-5" />
				</div>
				<div class="min-w-0">
					<div class="text-[10px] sh-text-muted font-bold uppercase tracking-wider">{{ stat.label }}</div>
					<div class="text-xl sm:text-2xl font-extrabold sh-text-primary mt-0.5 truncate">
						{{ stat.value }}
						<span v-if="stat.suffix" class="text-sm font-normal sh-text-muted">{{ stat.suffix }}</span>
					</div>
				</div>
			</div>
		</div>

		<!-- ═══ 2. CONTINUE WHERE YOU LEFT OFF ═══ -->
		<div v-if="continueCourse" class="sh-continue-card overflow-hidden">
			<div class="flex flex-col md:flex-row">
				<!-- Image Side -->
				<div class="w-full md:w-2/5 h-52 md:h-auto relative overflow-hidden">
					<div
						class="absolute inset-0 bg-cover bg-center transition-transform duration-700 group-hover:scale-105"
						:style="continueCourse.image
							? `background-image: url('${encodeURI(continueCourse.image)}')`
							: 'background: linear-gradient(135deg, #061B49, #0b2f73, #0d6efd)'
						"
					></div>
					<div class="absolute inset-0 bg-gradient-to-r from-black/20 to-transparent md:bg-gradient-to-l md:from-transparent md:to-transparent"></div>
					<!-- Progress overlay on mobile -->
					<div class="absolute bottom-0 left-0 right-0 md:hidden">
						<div class="h-1 bg-black/20">
							<div class="h-full bg-white/80 transition-all duration-500" :style="`width: ${continueCourse.membership?.progress || 0}%`"></div>
						</div>
					</div>
				</div>
				<!-- Content Side -->
				<div class="w-full md:w-3/5 p-7 sm:p-9 flex flex-col justify-center sh-card-bg">
					<div class="flex items-center gap-2 text-xs font-extrabold uppercase tracking-widest mb-3" style="color: var(--sb-primary);">
						<PlayCircle class="size-4" /> {{ __('Continúa donde lo dejaste') }}
					</div>
					<h2 class="text-xl sm:text-2xl font-extrabold sh-text-primary mb-2 leading-tight">{{ continueCourse.title }}</h2>
					<p class="sh-text-muted text-sm mb-6 line-clamp-2 leading-relaxed">{{ continueCourse.short_introduction }}</p>

					<!-- Progress Bar (desktop) -->
					<div class="hidden md:block mb-6">
						<div class="flex justify-between text-xs font-bold mb-2">
							<span class="sh-text-muted">{{ __('Progreso del curso') }}</span>
							<span style="color: var(--sb-primary);">{{ Math.ceil(continueCourse.membership?.progress || 0) }}%</span>
						</div>
						<div class="sh-progress-track">
							<div class="sh-progress-bar" :style="`width: ${continueCourse.membership?.progress || 0}%`"></div>
						</div>
					</div>

					<router-link
						:to="{ name: 'CourseDetail', params: { courseName: continueCourse.name } }"
						class="sh-btn-dark w-fit"
					>
						{{ __('Continuar lección') }} <MoveRight class="size-4" />
					</router-link>
				</div>
			</div>
		</div>

		<!-- ═══ 3. LIVE CLASSES ═══ -->
		<div v-if="myLiveClasses.data?.length">
			<h3 class="sh-section-title">
				<div class="sh-section-icon bg-red-500/10 text-red-500"><Video class="size-5" /></div>
				{{ __('Próximas Clases en Vivo') }}
			</h3>
			<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
				<div v-for="cls in myLiveClasses.data" :key="cls.name" class="sh-card p-5">
					<div class="font-bold sh-text-primary leading-tight mb-2">{{ cls.title }}</div>
					<div class="text-sm sh-text-muted leading-snug mb-5 line-clamp-2">{{ cls.description }}</div>
					<div class="mt-auto space-y-2 text-sm">
						<div class="sh-meta-row">
							<Calendar class="w-4 h-4 shrink-0" style="color: var(--sb-primary);" />
							<span class="font-medium sh-text-primary">{{ dayjs(cls.date).format('DD MMM YYYY') }}</span>
						</div>
						<div class="sh-meta-row">
							<Clock class="w-4 h-4 shrink-0 text-amber-500" />
							<span class="font-medium sh-text-primary">{{ formatTime(cls.time) }} - {{ dayjs(getClassEnd(cls)).format('HH:mm A') }}</span>
						</div>
						<a
							v-if="canAccessClass(cls)"
							:href="cls.join_url"
							target="_blank"
							class="sh-btn-primary w-full mt-3"
						>
							<Video class="size-4" /> {{ __('Unirse a clase') }}
						</a>
					</div>
				</div>
			</div>
		</div>

		<!-- ═══ 4. MY COURSES ═══ -->
		<div v-if="remainingCourses.length">
			<div class="flex items-center justify-between mb-6">
				<h3 class="sh-section-title mb-0">
					<div class="sh-section-icon bg-blue-500/10" style="color: var(--sb-primary);"><BookOpen class="size-5" /></div>
					{{ __('Mis Cursos') }}
				</h3>
				<router-link :to="{ name: 'Courses' }" class="sh-link text-sm">
					{{ __('Ver todos') }} <MoveRight class="size-3.5" />
				</router-link>
			</div>
			<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
				<router-link
					v-for="course in remainingCourses"
					:key="course.name"
					:to="{ name: 'CourseDetail', params: { courseName: course.name } }"
				>
					<CourseCard :course="course" />
				</router-link>
			</div>
		</div>

		<!-- ═══ 5. CERTIFICATES + PLUS PROMO ═══ -->
		<div class="grid grid-cols-1 lg:grid-cols-5 gap-6">

			<!-- Certificados -->
			<div class="lg:col-span-3">
				<h3 class="sh-section-title">
					<div class="sh-section-icon bg-amber-500/10 text-amber-500"><Award class="size-5" /></div>
					{{ __('Certificados y Logros') }}
				</h3>
				<div class="sh-card p-8 text-center">
					<div class="sh-empty-icon mx-auto mb-4" :class="certCount ? 'bg-amber-500/10 text-amber-500' : ''">
						<Award class="size-9" />
					</div>
					<h4 class="font-bold text-lg sh-text-primary mb-2">
						{{ certCount ? __('Tienes {0} certificado(s)').replace('{0}', certCount) : __('Aún no tienes certificados') }}
					</h4>
					<p class="sh-text-muted text-sm max-w-sm mx-auto mb-6 leading-relaxed">
						{{ __('Completa cursos y aprueba evaluaciones para obtener certificados verificables.') }}
					</p>
					<router-link
						:to="{ name: 'ProfileCertificates', params: { user: user.data?.name } }"
						class="sh-btn-outline inline-flex"
					>
						{{ __('Ver mis certificados') }}
					</router-link>
				</div>
			</div>

			<!-- Plus Promo -->
			<div class="lg:col-span-2">
				<h3 class="sh-section-title">
					<div class="sh-section-icon bg-blue-500/10" style="color: var(--sb-primary);"><Sparkles class="size-5" /></div>
					{{ __('Herramientas Pro') }}
				</h3>
				<div class="sh-plus-promo relative overflow-hidden h-full flex flex-col">
					<div class="absolute -top-16 -right-16 w-48 h-48 bg-blue-500/15 rounded-full blur-3xl"></div>
					<div class="absolute bottom-0 left-0 w-32 h-32 bg-amber-500/10 rounded-full blur-2xl"></div>
					<div class="relative z-10 p-7 flex flex-col flex-1">
						<Crown class="size-8 text-amber-400 mb-4 drop-shadow-md" />
						<h4 class="font-extrabold text-xl text-white mb-2">StudyBadge Plus</h4>
						<p class="text-blue-100/70 text-sm mb-6 flex-1 leading-relaxed">
							{{ __('Tutor IA ilimitado, certificados, herramientas de estudio premium y más.') }}
						</p>
						<ul class="space-y-2.5 mb-7 text-sm font-medium text-blue-50/90">
							<li class="flex items-center gap-2.5"><CheckCircle2 class="size-4 text-amber-400 shrink-0" /> {{ __('Tutor IA ilimitado') }}</li>
							<li class="flex items-center gap-2.5"><CheckCircle2 class="size-4 text-amber-400 shrink-0" /> {{ __('Generación de cursos') }}</li>
							<li class="flex items-center gap-2.5"><CheckCircle2 class="size-4 text-amber-400 shrink-0" /> {{ __('Certificados incluidos') }}</li>
						</ul>
						<router-link :to="{ name: 'Plus' }" class="sh-btn-gold w-full">
							{{ billing.data?.active ? __('Gestionar mi Plus') : __('Desbloquear Plus') }}
						</router-link>
					</div>
				</div>
			</div>
		</div>

		<UpcomingEvaluations :forHome="true" />
	</div>
</template>

<script setup lang="ts">
import { computed, inject, ref, onMounted, markRaw } from 'vue'
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

const statCards = computed(() => [
	{
		icon: markRaw(BookOpen),
		label: __('Cursos activos'),
		value: myCourses.data?.length || 0,
		suffix: null,
		bgColor: 'rgba(59, 130, 246, 0.08)',
		iconColor: 'var(--sb-primary)',
	},
	{
		icon: markRaw(Award),
		label: __('Certificados'),
		value: certCount.value || 0,
		suffix: null,
		bgColor: 'rgba(245, 158, 11, 0.08)',
		iconColor: '#f59e0b',
	},
	{
		icon: markRaw(Zap),
		label: __('Racha actual'),
		value: streakInfo.data?.current_streak || 0,
		suffix: __('días'),
		bgColor: 'rgba(16, 185, 129, 0.08)',
		iconColor: '#10b981',
	},
	{
		icon: markRaw(Crown),
		label: __('Plan actual'),
		value: billing.data?.active ? 'Plus' : __('Gratuito'),
		suffix: null,
		bgColor: billing.data?.active ? 'rgba(245, 179, 1, 0.12)' : 'rgba(107, 114, 128, 0.08)',
		iconColor: billing.data?.active ? '#f5b301' : '#6b7280',
	},
])

const continueCourse = computed(() => {
	if (!myCourses.data?.length) return null
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

const canAccessClass = (cls: { date: string; time: string; duration: number }) => {
	if (cls.date < dayjs().format('YYYY-MM-DD')) return false
	if (cls.date > dayjs().format('YYYY-MM-DD')) return false
	if (hasClassEnded(cls)) return false
	return true
}

const hasClassEnded = (cls: { date: string; time: string; duration: number }) => {
	const classEnd = getClassEnd(cls)
	const now = new Date()
	return now > classEnd
}
</script>

<style scoped>
/* ═══════════════════════════════════════
   TEXT TOKENS
   ═══════════════════════════════════════ */

.sh-text-primary { color: #111827; }
.sh-text-muted { color: #6b7280; }
:root[data-theme="dark"] .sh-text-primary { color: #f3f4f6; }
:root[data-theme="dark"] .sh-text-muted { color: #9ca3af; }

/* ═══════════════════════════════════════
   CARDS
   ═══════════════════════════════════════ */

.sh-card {
	background: var(--sb-white);
	border: 1px solid rgba(6, 27, 73, 0.05);
	border-radius: 20px;
	box-shadow: 0 1px 3px rgba(6, 27, 73, 0.03), 0 4px 12px rgba(6, 27, 73, 0.02);
	transition: all 0.2s ease;
}

:root[data-theme="dark"] .sh-card {
	border-color: rgba(255, 255, 255, 0.05);
	box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2), 0 4px 12px rgba(0, 0, 0, 0.12);
}

.sh-card-bg {
	background: var(--sb-white);
}

/* ═══════════════════════════════════════
   STAT CARDS
   ═══════════════════════════════════════ */

.sh-stat-card {
	display: flex;
	align-items: center;
	gap: 14px;
	padding: 18px 20px;
	background: var(--sb-white);
	border: 1px solid rgba(6, 27, 73, 0.05);
	border-radius: 18px;
	box-shadow: 0 1px 3px rgba(6, 27, 73, 0.03);
	transition: all 0.2s ease;
}

.sh-stat-card:hover {
	box-shadow: 0 4px 16px rgba(6, 27, 73, 0.08);
	transform: translateY(-1px);
}

:root[data-theme="dark"] .sh-stat-card {
	border-color: rgba(255, 255, 255, 0.05);
	box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
}

:root[data-theme="dark"] .sh-stat-card:hover {
	box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
}

.sh-stat-icon {
	display: flex;
	align-items: center;
	justify-content: center;
	width: 44px;
	height: 44px;
	border-radius: 14px;
	background: var(--icon-bg);
	color: var(--icon-color);
	flex-shrink: 0;
}

/* ═══════════════════════════════════════
   CONTINUE CARD
   ═══════════════════════════════════════ */

.sh-continue-card {
	background: var(--sb-white);
	border: 1px solid rgba(6, 27, 73, 0.05);
	border-radius: 24px;
	box-shadow: 0 2px 8px rgba(6, 27, 73, 0.04), 0 8px 24px rgba(6, 27, 73, 0.04);
	overflow: hidden;
}

:root[data-theme="dark"] .sh-continue-card {
	border-color: rgba(255, 255, 255, 0.05);
	box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2), 0 8px 24px rgba(0, 0, 0, 0.15);
}

/* ═══════════════════════════════════════
   PROGRESS BAR
   ═══════════════════════════════════════ */

.sh-progress-track {
	height: 6px;
	width: 100%;
	background: rgba(0, 0, 0, 0.05);
	border-radius: 100px;
	overflow: hidden;
}

:root[data-theme="dark"] .sh-progress-track {
	background: rgba(255, 255, 255, 0.08);
}

.sh-progress-bar {
	height: 100%;
	background: linear-gradient(90deg, var(--sb-primary), var(--sb-medium));
	border-radius: 100px;
	transition: width 0.5s ease;
}

/* ═══════════════════════════════════════
   META ROWS
   ═══════════════════════════════════════ */

.sh-meta-row {
	display: flex;
	align-items: center;
	gap: 8px;
	padding: 6px 10px;
	border-radius: 10px;
	background: rgba(0, 0, 0, 0.02);
}

:root[data-theme="dark"] .sh-meta-row {
	background: rgba(255, 255, 255, 0.04);
}

/* ═══════════════════════════════════════
   SECTION TITLES
   ═══════════════════════════════════════ */

.sh-section-title {
	display: flex;
	align-items: center;
	gap: 12px;
	font-size: 1.25rem;
	font-weight: 800;
	color: #111827;
	margin-bottom: 1.25rem;
}

:root[data-theme="dark"] .sh-section-title {
	color: #f3f4f6;
}

.sh-section-icon {
	display: flex;
	align-items: center;
	justify-content: center;
	width: 36px;
	height: 36px;
	border-radius: 10px;
	flex-shrink: 0;
}

/* ═══════════════════════════════════════
   EMPTY ICON
   ═══════════════════════════════════════ */

.sh-empty-icon {
	display: flex;
	align-items: center;
	justify-content: center;
	width: 68px;
	height: 68px;
	border-radius: 22px;
	background: rgba(0, 0, 0, 0.03);
	color: #d1d5db;
}

:root[data-theme="dark"] .sh-empty-icon {
	background: rgba(255, 255, 255, 0.05);
	color: #4b5563;
}

/* ═══════════════════════════════════════
   PLUS PROMO CARD
   ═══════════════════════════════════════ */

.sh-plus-promo {
	background: linear-gradient(145deg, #061B49 0%, #0b2f73 50%, #0a2259 100%);
	border-radius: 24px;
	box-shadow: 0 4px 24px rgba(6, 27, 73, 0.2);
}

:root[data-theme="dark"] .sh-plus-promo {
	box-shadow: 0 4px 24px rgba(0, 0, 0, 0.4);
}

/* ═══════════════════════════════════════
   BUTTONS
   ═══════════════════════════════════════ */

.sh-btn-primary {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	gap: 8px;
	padding: 10px 18px;
	border-radius: 12px;
	font-size: 14px;
	font-weight: 700;
	color: #fff;
	background: linear-gradient(135deg, #0d6efd, #0b5ed7);
	border: none;
	cursor: pointer;
	transition: all 0.2s ease;
	box-shadow: 0 2px 8px rgba(13, 110, 253, 0.25);
	text-decoration: none;
}

.sh-btn-primary:hover {
	transform: translateY(-1px);
	box-shadow: 0 4px 16px rgba(13, 110, 253, 0.35);
}

.sh-btn-dark {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	gap: 8px;
	padding: 12px 24px;
	border-radius: 14px;
	font-size: 14px;
	font-weight: 700;
	color: #fff;
	background: #111827;
	border: none;
	cursor: pointer;
	transition: all 0.2s ease;
	box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
	text-decoration: none;
}

:root[data-theme="dark"] .sh-btn-dark {
	background: rgba(255, 255, 255, 0.1);
	border: 1px solid rgba(255, 255, 255, 0.12);
}

.sh-btn-dark:hover {
	transform: translateY(-1px);
	background: #000;
	box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);
}

:root[data-theme="dark"] .sh-btn-dark:hover {
	background: rgba(255, 255, 255, 0.15);
}

.sh-btn-outline {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	gap: 8px;
	padding: 10px 20px;
	border-radius: 12px;
	font-size: 14px;
	font-weight: 700;
	color: #374151;
	background: transparent;
	border: 2px solid rgba(0, 0, 0, 0.08);
	cursor: pointer;
	transition: all 0.15s ease;
	text-decoration: none;
}

.sh-btn-outline:hover {
	background: rgba(0, 0, 0, 0.03);
	border-color: rgba(0, 0, 0, 0.15);
}

:root[data-theme="dark"] .sh-btn-outline {
	color: #d1d5db;
	border-color: rgba(255, 255, 255, 0.1);
}

:root[data-theme="dark"] .sh-btn-outline:hover {
	background: rgba(255, 255, 255, 0.05);
	border-color: rgba(255, 255, 255, 0.18);
}

.sh-btn-gold {
	display: flex;
	align-items: center;
	justify-content: center;
	gap: 8px;
	padding: 14px 20px;
	border-radius: 14px;
	font-size: 14px;
	font-weight: 800;
	color: #78350f;
	background: linear-gradient(135deg, #fbbf24, #f59e0b);
	border: none;
	cursor: pointer;
	transition: all 0.2s ease;
	box-shadow: 0 2px 12px rgba(245, 158, 11, 0.3);
	text-decoration: none;
}

.sh-btn-gold:hover {
	transform: translateY(-1px);
	box-shadow: 0 4px 20px rgba(245, 158, 11, 0.4);
}

/* ═══════════════════════════════════════
   LINKS
   ═══════════════════════════════════════ */

.sh-link {
	display: inline-flex;
	align-items: center;
	gap: 4px;
	font-weight: 700;
	color: var(--sb-primary);
	text-decoration: none;
	transition: color 0.15s ease;
}

.sh-link:hover {
	color: var(--sb-medium);
}
</style>
