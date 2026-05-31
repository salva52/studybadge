<template>
	<div class="space-y-8">

		<!-- ═══ 1. STAT CARDS (TU PROGRESO COMO ADMIN) ═══ -->
		<div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
			<div v-for="stat in statCards" :key="stat.label" class="ah-stat-card group">
				<div class="ah-stat-icon" :style="`--icon-bg: ${stat.bgColor}; --icon-color: ${stat.iconColor}`">
					<component :is="stat.icon" class="size-5" />
				</div>
				<div class="min-w-0">
					<div class="text-[10px] ah-text-muted font-bold uppercase tracking-wider">{{ stat.label }}</div>
					<div class="text-xl sm:text-2xl font-extrabold ah-text-primary mt-0.5 truncate">
						{{ stat.value }}
					</div>
				</div>
			</div>
		</div>

		<!-- ═══ 2. HERRAMIENTAS IA DISPONIBLES ═══ -->
		<div>
			<h3 class="ah-section-title">
				<div class="ah-section-icon bg-indigo-500/10 text-indigo-500"><Sparkles class="size-5" /></div>
				{{ __('Herramientas IA Disponibles') }}
			</h3>
			<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
				<!-- Herramienta 1 -->
				<div class="ah-tool-card group relative overflow-hidden flex flex-col justify-between">
					<div class="absolute -right-10 -top-10 w-32 h-32 bg-indigo-500/10 rounded-full blur-2xl group-hover:bg-indigo-500/20 transition-all"></div>
					<div class="relative z-10 p-6 flex flex-col h-full">
						<div class="rounded-xl bg-indigo-50 dark:bg-indigo-900/20 w-fit p-3 mb-4 ring-1 ring-indigo-100 dark:ring-indigo-800/50 group-hover:scale-110 transition-transform">
							<Wand2 class="size-6 text-indigo-600 dark:text-indigo-400" />
						</div>
						<h4 class="font-extrabold text-lg ah-text-primary mb-2">{{ __('Generador de Cursos IA') }}</h4>
						<p class="text-sm ah-text-muted leading-relaxed mb-5">
							{{ __('Crea la estructura, lecciones y contenido de tus cursos automáticamente usando nuestra Inteligencia Artificial.') }}
						</p>
						<router-link :to="{ name: 'Courses', query: { newCourse: '1' } }" class="ah-btn-outline w-full mt-auto">
							<Plus class="size-4" /> {{ __('Crear nuevo curso') }}
						</router-link>
					</div>
				</div>

				<!-- Herramienta 2 -->
				<div class="ah-tool-card group relative overflow-hidden flex flex-col justify-between">
					<div class="absolute -right-10 -top-10 w-32 h-32 bg-amber-500/10 rounded-full blur-2xl group-hover:bg-amber-500/20 transition-all"></div>
					<div class="relative z-10 p-6 flex flex-col h-full">
						<div class="rounded-xl bg-amber-50 dark:bg-amber-900/20 w-fit p-3 mb-4 ring-1 ring-amber-100 dark:ring-amber-800/50 group-hover:scale-110 transition-transform">
							<Bot class="size-6 text-amber-600 dark:text-amber-400" />
						</div>
						<h4 class="font-extrabold text-lg ah-text-primary mb-2">{{ __('Tutor IA Global') }}</h4>
						<p class="text-sm ah-text-muted leading-relaxed mb-5">
							{{ __('Configura el comportamiento del Tutor IA para que guíe a tus estudiantes de forma personalizada 24/7.') }}
						</p>
						<a href="/app/ai-tutor-settings" target="_blank" class="ah-btn-outline w-full mt-auto">
							<Settings class="size-4" /> {{ __('Configurar Tutor') }}
						</a>
					</div>
				</div>

				<!-- Herramienta 3 -->
				<div class="ah-tool-card group relative overflow-hidden flex flex-col justify-between">
					<div class="absolute -right-10 -top-10 w-32 h-32 bg-emerald-500/10 rounded-full blur-2xl group-hover:bg-emerald-500/20 transition-all"></div>
					<div class="relative z-10 p-6 flex flex-col h-full">
						<div class="rounded-xl bg-emerald-50 dark:bg-emerald-900/20 w-fit p-3 mb-4 ring-1 ring-emerald-100 dark:ring-emerald-800/50 group-hover:scale-110 transition-transform">
							<LineChart class="size-6 text-emerald-600 dark:text-emerald-400" />
						</div>
						<h4 class="font-extrabold text-lg ah-text-primary mb-2">{{ __('Analítica Avanzada') }}</h4>
						<p class="text-sm ah-text-muted leading-relaxed mb-5">
							{{ __('Revisa el progreso de tus grupos, evaluaciones pendientes y métricas de retención de los estudiantes.') }}
						</p>
						<router-link :to="{ name: 'Batches' }" class="ah-btn-outline w-full mt-auto">
							<BarChart2 class="size-4" /> {{ __('Ver Reportes') }}
						</router-link>
					</div>
				</div>
			</div>
		</div>

		<!-- ═══ 3. EVALUACIONES PRÓXIMAS ═══ -->
		<div v-if="evals?.data?.length">
			<h3 class="ah-section-title">
				<div class="ah-section-icon bg-amber-500/10 text-amber-600"><ClipboardCheck class="size-5" /></div>
				{{ __('Evaluaciones Próximas') }}
			</h3>
			<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
				<div
					v-for="evaluation in evals?.data"
					:key="evaluation.name"
					class="ah-card p-5 group cursor-pointer hover:border-amber-400/30"
					@click="redirectToProfile()"
				>
					<div class="flex items-center gap-2 text-[10px] font-bold uppercase tracking-wider text-amber-600 mb-3">
						<ClipboardCheck class="size-3.5" /> {{ __('Evaluación') }}
					</div>
					<div class="font-extrabold ah-text-primary text-lg leading-tight mb-4 group-hover:text-amber-600 transition-colors">
						{{ evaluation.course_title }}
					</div>
					<div class="space-y-2.5 mt-auto">
						<div class="ah-meta-row">
							<Calendar class="w-4 h-4 shrink-0 text-gray-400" />
							<span class="font-medium ah-text-primary text-sm">{{ dayjs(evaluation.date).format('DD MMM YYYY') }}</span>
						</div>
						<div class="ah-meta-row">
							<Clock class="w-4 h-4 shrink-0 text-gray-400" />
							<span class="font-medium ah-text-primary text-sm">{{ formatTime(evaluation.start_time) }}</span>
						</div>
						<div class="ah-meta-row bg-blue-50/50 dark:bg-blue-900/10">
							<User class="w-4 h-4 shrink-0 text-blue-500" />
							<span class="font-bold ah-text-primary text-sm line-clamp-1">{{ evaluation.member_name }}</span>
						</div>
					</div>
				</div>
			</div>
		</div>

		<!-- ═══ 4. CLASES EN VIVO PRÓXIMAS ═══ -->
		<div v-if="liveClasses?.data?.length">
			<h3 class="ah-section-title">
				<div class="ah-section-icon bg-red-500/10 text-red-500"><Video class="size-5" /></div>
				{{ __('Clases en Vivo Próximas') }}
			</h3>
			<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
				<div
					v-for="cls in liveClasses?.data"
					:key="cls.name"
					class="ah-card p-5 flex flex-col"
				>
					<div class="font-extrabold ah-text-primary text-lg leading-tight mb-2">
						{{ cls.title }}
					</div>
					<div class="text-sm ah-text-muted leading-relaxed mb-5 line-clamp-2">
						{{ cls.description }}
					</div>
					
					<div class="mt-auto space-y-2 mb-5">
						<div class="ah-meta-row">
							<Calendar class="w-4 h-4 shrink-0 text-gray-400" />
							<span class="font-medium ah-text-primary text-sm">{{ dayjs(cls.date).format('DD MMM YYYY') }}</span>
						</div>
						<div class="ah-meta-row">
							<Clock class="w-4 h-4 shrink-0 text-red-400" />
							<span class="font-medium ah-text-primary text-sm">{{ formatTime(cls.time) }} - {{ dayjs(getClassEnd(cls)).format('HH:mm A') }}</span>
						</div>
					</div>

					<div v-if="canAccessClass(cls)" class="flex items-center gap-2 mt-auto pt-4 border-t ah-border">
						<a
							v-if="user.data?.is_moderator || user.data?.is_evaluator"
							:href="cls.start_url"
							target="_blank"
							class="ah-btn-outline w-full"
						>
							<Monitor class="h-4 w-4" /> {{ __('Iniciar') }}
						</a>
						<a
							:href="cls.join_url"
							target="_blank"
							class="ah-btn-primary w-full"
						>
							<Video class="h-4 w-4" /> {{ __('Unirse') }}
						</a>
					</div>
					
					<div v-else-if="hasClassEnded(cls)" class="mt-auto pt-4 border-t ah-border">
						<div class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-gray-100 dark:bg-gray-800 text-gray-500 dark:text-gray-400 rounded-lg text-xs font-bold uppercase tracking-wider w-full justify-center">
							<Info class="w-4 h-4" /> {{ __('Finalizada') }}
						</div>
					</div>
				</div>
			</div>
		</div>

		<!-- ═══ 5. CURSOS DESTACADOS ═══ -->
		<div v-if="createdCourses.data?.length">
			<div class="flex items-center justify-between mb-6">
				<h3 class="ah-section-title mb-0">
					<div class="ah-section-icon bg-blue-500/10 text-blue-600"><BookOpen class="size-5" /></div>
					{{ __('Cursos destacados') }}
				</h3>
				<router-link :to="{ name: 'Courses' }" class="ah-link text-sm">
					{{ __('Ver todos') }} <MoveRight class="size-3.5" />
				</router-link>
			</div>
			<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5">
				<router-link
					v-for="course in createdCourses.data"
					:key="course.name"
					:to="{ name: 'CourseDetail', params: { courseName: course.name } }"
				>
					<CourseCard :course="course" />
				</router-link>
			</div>
		</div>

		<!-- ═══ 6. GRUPOS PRÓXIMOS ═══ -->
		<div v-if="createdBatches.data?.length">
			<div class="flex items-center justify-between mb-6">
				<h3 class="ah-section-title mb-0">
					<div class="ah-section-icon bg-purple-500/10 text-purple-600"><Users class="size-5" /></div>
					{{ __('Grupos Próximos') }}
				</h3>
				<router-link :to="{ name: 'Batches' }" class="ah-link text-sm">
					{{ __('Ver todos') }} <MoveRight class="size-3.5" />
				</router-link>
			</div>
			<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
				<router-link
					v-for="batch in createdBatches.data"
					:key="batch.name"
					:to="{ name: 'BatchDetail', params: { batchName: batch.name } }"
				>
					<BatchCard :batch="batch" />
				</router-link>
			</div>
		</div>

		<!-- ═══ EMPTY STATE ═══ -->
		<div
			v-if="!createdCourses.data?.length && !createdBatches.data?.length && !liveClasses?.data?.length && !evals?.data?.length"
			class="ah-empty-state"
		>
			<div class="ah-empty-icon mb-6">
				<GraduationCap class="size-12" />
			</div>
			<h2 class="text-2xl font-extrabold ah-text-primary mb-3">
				{{ __('Aún no hay contenido') }}
			</h2>
			<p class="text-base ah-text-muted max-w-md mx-auto leading-relaxed mb-8">
				{{ __('Parece que tu panel está vacío. Crea tu primer curso o programa evaluaciones para que aparezcan aquí.') }}
			</p>
			<router-link :to="{ name: 'Courses', query: { newCourse: '1' } }" class="ah-btn-primary text-base px-8 py-3">
				<Plus class="size-5" /> {{ __('Crear mi primer curso') }}
			</router-link>
		</div>
	</div>
</template>

<script setup lang="ts">
import { computed, inject, markRaw } from 'vue'
import { Button, createResource, Tooltip } from 'frappe-ui'
import { useRouter } from 'vue-router'
import {
	Calendar,
	Clock,
	GraduationCap,
	Info,
	Monitor,
	MoveRight,
	Plus,
	Video,
	ClipboardCheck,
	User,
	BookOpen,
	Users,
	Sparkles,
	Bot,
	Settings,
	Wand2,
	LineChart,
	BarChart2,
	Layers
} from 'lucide-vue-next'
import { formatTime } from '@/utils'
import CourseCard from '@/components/CourseCard.vue'
import BatchCard from '@/pages/Batches/components/BatchCard.vue'

const user = inject<any>('$user')
const dayjs = inject<any>('$dayjs')
const router = useRouter()
const profileUsername = computed(
	() => user?.data?.username || user?.data?.name || user?.data?.email || ''
)

const props = defineProps<{
	liveClasses?: { data?: any[] }
	evals?: { data?: any[] }
}>()

const createdCourses = createResource({
	url: 'lms.lms.api.get_created_courses',
	auto: true,
})

const createdBatches = createResource({
	url: 'lms.lms.api.get_created_batches',
	auto: true,
})

const statCards = computed(() => [
	{
		icon: markRaw(BookOpen),
		label: __('Cursos Creados'),
		value: createdCourses.data?.length || 0,
		bgColor: 'rgba(59, 130, 246, 0.08)',
		iconColor: 'var(--sb-primary)',
	},
	{
		icon: markRaw(Users),
		label: __('Grupos Activos'),
		value: createdBatches.data?.length || 0,
		bgColor: 'rgba(139, 92, 246, 0.08)',
		iconColor: '#8b5cf6',
	},
	{
		icon: markRaw(ClipboardCheck),
		label: __('Eval. Pendientes'),
		value: props.evals?.data?.length || 0,
		bgColor: 'rgba(245, 158, 11, 0.08)',
		iconColor: '#f59e0b',
	},
	{
		icon: markRaw(Video),
		label: __('Clases Programadas'),
		value: props.liveClasses?.data?.length || 0,
		bgColor: 'rgba(239, 68, 68, 0.08)',
		iconColor: '#ef4444',
	},
])

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

const redirectToProfile = () => {
	if (!profileUsername.value) return
	router.push({
		name: 'ProfileEvaluationSchedule',
		params: { username: profileUsername.value },
	})
}
</script>

<style scoped>
/* ═══════════════════════════════════════
   TEXT TOKENS & BORDERS
   ═══════════════════════════════════════ */

.ah-text-primary { color: #111827; }
.ah-text-muted { color: #6b7280; }
:root[data-theme="dark"] .ah-text-primary { color: #f3f4f6; }
:root[data-theme="dark"] .ah-text-muted { color: #9ca3af; }

.ah-border { border-color: rgba(6, 27, 73, 0.05); }
:root[data-theme="dark"] .ah-border { border-color: rgba(255, 255, 255, 0.05); }

/* ═══════════════════════════════════════
   SECTION TITLES
   ═══════════════════════════════════════ */

.ah-section-title {
	display: flex;
	align-items: center;
	gap: 12px;
	font-size: 1.25rem;
	font-weight: 800;
	color: #111827;
	margin-bottom: 1.25rem;
}

:root[data-theme="dark"] .ah-section-title {
	color: #f3f4f6;
}

.ah-section-icon {
	display: flex;
	align-items: center;
	justify-content: center;
	width: 36px;
	height: 36px;
	border-radius: 10px;
	flex-shrink: 0;
}

/* ═══════════════════════════════════════
   STAT CARDS
   ═══════════════════════════════════════ */

.ah-stat-card {
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

.ah-stat-card:hover {
	box-shadow: 0 4px 16px rgba(6, 27, 73, 0.08);
	transform: translateY(-1px);
}

:root[data-theme="dark"] .ah-stat-card {
	border-color: rgba(255, 255, 255, 0.05);
	box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
}

:root[data-theme="dark"] .ah-stat-card:hover {
	box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
}

.ah-stat-icon {
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
   CARDS & TOOL CARDS
   ═══════════════════════════════════════ */

.ah-card, .ah-tool-card {
	background: var(--sb-white);
	border: 1px solid rgba(6, 27, 73, 0.05);
	border-radius: 20px;
	box-shadow: 0 1px 3px rgba(6, 27, 73, 0.03), 0 4px 12px rgba(6, 27, 73, 0.02);
	transition: all 0.2s ease;
}

.ah-card:hover, .ah-tool-card:hover {
	transform: translateY(-2px);
	box-shadow: 0 8px 24px rgba(6, 27, 73, 0.08);
}

:root[data-theme="dark"] .ah-card,
:root[data-theme="dark"] .ah-tool-card {
	border-color: rgba(255, 255, 255, 0.05);
	box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2), 0 4px 12px rgba(0, 0, 0, 0.12);
}

:root[data-theme="dark"] .ah-card:hover,
:root[data-theme="dark"] .ah-tool-card:hover {
	box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
}

/* ═══════════════════════════════════════
   META ROWS
   ═══════════════════════════════════════ */

.ah-meta-row {
	display: flex;
	align-items: center;
	gap: 8px;
	padding: 8px 12px;
	border-radius: 12px;
	background: rgba(0, 0, 0, 0.02);
}

:root[data-theme="dark"] .ah-meta-row {
	background: rgba(255, 255, 255, 0.04);
}

/* ═══════════════════════════════════════
   BUTTONS
   ═══════════════════════════════════════ */

.ah-btn-primary {
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

.ah-btn-primary:hover {
	transform: translateY(-1px);
	box-shadow: 0 4px 16px rgba(13, 110, 253, 0.35);
}

.ah-btn-outline {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	gap: 8px;
	padding: 10px 18px;
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

.ah-btn-outline:hover {
	background: rgba(0, 0, 0, 0.03);
	border-color: rgba(0, 0, 0, 0.15);
}

:root[data-theme="dark"] .ah-btn-outline {
	color: #d1d5db;
	border-color: rgba(255, 255, 255, 0.1);
}

:root[data-theme="dark"] .ah-btn-outline:hover {
	background: rgba(255, 255, 255, 0.05);
	border-color: rgba(255, 255, 255, 0.18);
}

/* ═══════════════════════════════════════
   LINKS
   ═══════════════════════════════════════ */

.ah-link {
	display: inline-flex;
	align-items: center;
	gap: 4px;
	font-weight: 700;
	color: var(--sb-primary);
	text-decoration: none;
	transition: color 0.15s ease;
}

.ah-link:hover {
	color: var(--sb-medium);
}

/* ═══════════════════════════════════════
   EMPTY STATE
   ═══════════════════════════════════════ */

.ah-empty-state {
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	padding: 60px 20px;
	text-align: center;
	background: var(--sb-white);
	border: 1px dashed rgba(6, 27, 73, 0.1);
	border-radius: 24px;
	margin-top: 40px;
}

:root[data-theme="dark"] .ah-empty-state {
	border-color: rgba(255, 255, 255, 0.1);
}

.ah-empty-icon {
	display: flex;
	align-items: center;
	justify-content: center;
	width: 80px;
	height: 80px;
	border-radius: 24px;
	background: rgba(0, 0, 0, 0.03);
	color: #d1d5db;
}

:root[data-theme="dark"] .ah-empty-icon {
	background: rgba(255, 255, 255, 0.05);
	color: #4b5563;
}
</style>
