<template>
	<div class="student-home">
		<!-- HERO / WELCOME -->
		<section class="sh-hero-card">
			<div class="sh-hero-content">
				<div>
					<div class="sh-eyebrow">
						<Sparkles class="size-4" />
						{{ __('Tu espacio de aprendizaje') }}
					</div>

					<h1 class="sh-hero-title">
						{{ __('Hola') }}, {{ firstName }} 👋
					</h1>

					<p class="sh-hero-subtitle">
						{{ __('Sigue avanzando en tus cursos, practica con TutorIA y desbloquea certificados verificables para demostrar lo que aprendes.') }}
					</p>

					<div class="sh-hero-actions">
						<router-link :to="{ name: 'Courses' }" class="sh-btn-light">
							<BookOpen class="size-4" />
							{{ __('Explorar cursos') }}
						</router-link>

						<router-link :to="{ name: 'Practice' }" class="sh-btn-ghost-light">
							<MessageCircle class="size-4" />
							{{ __('Practicar con IA') }}
						</router-link>
					</div>
				</div>

				<div class="sh-hero-panel">
					<div class="sh-plan-pill" :class="{ active: billing.data?.active }">
						<Crown class="size-4" />
						{{ billing.data?.active ? __('StudyBadge Plus activo') : __('Plan gratuito') }}
					</div>

					<div class="sh-hero-panel-title">
						{{ billing.data?.active ? __('Tienes herramientas Plus desbloqueadas') : __('Desbloquea más herramientas con Plus') }}
					</div>

					<p class="sh-hero-panel-text">
						{{ billing.data?.active
							? __('Usa TutorIA, prompts, simulaciones y certificados para acelerar tu aprendizaje.')
							: __('Accede a TutorIA ilimitado, certificados, biblioteca de prompts y herramientas premium.')
						}}
					</p>

					<router-link :to="{ name: 'Plus' }" class="sh-btn-panel">
						{{ billing.data?.active ? __('Gestionar Plus') : __('Ver StudyBadge Plus') }}
						<MoveRight class="size-4" />
					</router-link>
				</div>
			</div>
		</section>

		<!-- STATS -->
		<section class="sh-stats-grid">
			<div v-for="stat in statCards" :key="stat.label" class="sh-stat-card">
				<div
					class="sh-stat-icon"
					:style="{
						backgroundColor: stat.bgColor,
						color: stat.iconColor,
					}"
				>
					<component :is="stat.icon" class="size-5" />
				</div>

				<div class="min-w-0">
					<div class="sh-stat-label">
						{{ stat.label }}
					</div>

					<div class="sh-stat-value">
						{{ stat.value }}
						<span v-if="stat.suffix" class="sh-stat-suffix">
							{{ stat.suffix }}
						</span>
					</div>
				</div>
			</div>
		</section>

		<!-- MAIN DASHBOARD -->
		<section class="sh-main-grid">
			<!-- CONTINUE COURSE -->
			<div class="sh-main-left">
				<div v-if="continueCourse" class="sh-continue-card">
					<div class="sh-continue-media" :class="{ empty: !continueCourse.image }">
						<div
							v-if="continueCourse.image"
							class="sh-continue-image"
							:style="{ backgroundImage: `url('${continueCourse.image}')` }"
						></div>

						<div v-else class="sh-continue-fallback">
							<BookOpen class="size-10" />
							<span>{{ __('StudyBadge') }}</span>
						</div>

						<div class="sh-mobile-progress">
							<div
								class="sh-mobile-progress-fill"
								:style="{ width: courseProgress(continueCourse) + '%' }"
							></div>
						</div>
					</div>

					<div class="sh-continue-body">
						<div class="sh-section-kicker">
							<PlayCircle class="size-4" />
							{{ __('Continúa donde lo dejaste') }}
						</div>

						<h2 class="sh-continue-title">
							{{ continueCourse.title }}
						</h2>

						<p class="sh-continue-desc">
							{{ continueCourse.short_introduction || __('Sigue aprendiendo y completa las próximas lecciones para avanzar en tu ruta.') }}
						</p>

						<div class="sh-progress-wrap">
							<div class="sh-progress-head">
								<span>{{ __('Progreso del curso') }}</span>
								<strong>{{ courseProgress(continueCourse) }}%</strong>
							</div>

							<div class="sh-progress-track">
								<div
									class="sh-progress-bar"
									:style="{ width: courseProgress(continueCourse) + '%' }"
								></div>
							</div>
						</div>

						<div class="sh-continue-actions">
							<router-link
								:to="{ name: 'CourseDetail', params: { courseName: continueCourse.name } }"
								class="sh-btn-primary"
							>
								{{ __('Continuar lección') }}
								<MoveRight class="size-4" />
							</router-link>

							<router-link :to="{ name: 'Courses' }" class="sh-btn-outline">
								{{ __('Ver cursos') }}
							</router-link>
						</div>
					</div>
				</div>

				<div v-else class="sh-start-card">
					<div class="sh-start-icon">
						<GraduationCap class="size-9" />
					</div>

					<h2>{{ __('Empieza tu primera ruta de aprendizaje') }}</h2>

					<p>
						{{ __('Explora cursos de IA, negocios digitales, productividad y habilidades prácticas. Elige uno y empieza a avanzar hoy.') }}
					</p>

					<router-link :to="{ name: 'Courses' }" class="sh-btn-primary">
						{{ __('Explorar cursos') }}
						<MoveRight class="size-4" />
					</router-link>
				</div>
			</div>

			<!-- QUICK ACTIONS -->
			<aside class="sh-main-right">
				<div class="sh-card sh-quick-card">
					<div class="sh-card-header">
						<div>
							<h3>{{ __('Acciones rápidas') }}</h3>
							<p>{{ __('Entra directo a las herramientas más útiles.') }}</p>
						</div>
					</div>

					<div class="sh-quick-list">
						<router-link :to="{ name: 'Practice' }" class="sh-quick-item">
							<div class="sh-quick-icon">
								<MessageCircle class="size-5" />
							</div>

							<div>
								<strong>{{ __('Practicar con TutorIA') }}</strong>
								<span>{{ __('Resuelve dudas y practica temas.') }}</span>
							</div>

							<ArrowUpRight class="size-4" />
						</router-link>

						<router-link :to="{ name: 'PromptLibrary' }" class="sh-quick-item">
							<div class="sh-quick-icon gold">
								<Zap class="size-5" />
							</div>

							<div>
								<strong>{{ __('Biblioteca de prompts') }}</strong>
								<span>{{ __('Prompts listos para estudiar y crear.') }}</span>
							</div>

							<ArrowUpRight class="size-4" />
						</router-link>

						<router-link
							v-if="profileUsername"
							:to="{ name: 'ProfileCertificates', params: { username: profileUsername } }"
							class="sh-quick-item"
						>
							<div class="sh-quick-icon green">
								<Award class="size-5" />
							</div>

							<div>
								<strong>{{ __('Mis certificados') }}</strong>
								<span>{{ __('Mira tus logros verificables.') }}</span>
							</div>

							<ArrowUpRight class="size-4" />
						</router-link>
					</div>
				</div>
			</aside>
		</section>

		<!-- LIVE CLASSES -->
		<section v-if="myLiveClasses.data?.length" class="sh-section">
			<div class="sh-section-head">
				<div>
					<div class="sh-section-kicker">
						<Video class="size-4" />
						{{ __('En vivo') }}
					</div>

					<h2>{{ __('Próximas clases en vivo') }}</h2>
				</div>
			</div>

			<div class="sh-live-grid">
				<div v-for="cls in myLiveClasses.data" :key="cls.name" class="sh-card sh-live-card">
					<div class="sh-live-top">
						<div class="sh-live-badge">
							<Video class="size-3.5" />
							{{ __('Clase') }}
						</div>
					</div>

					<h3>{{ cls.title }}</h3>

					<p>{{ cls.description }}</p>

					<div class="sh-live-meta">
						<div>
							<Calendar class="size-4" />
							<span>{{ dayjs(cls.date).format('DD MMM YYYY') }}</span>
						</div>

						<div>
							<Clock class="size-4" />
							<span>{{ formatTime(cls.time) }} - {{ dayjs(getClassEnd(cls)).format('hh:mm A') }}</span>
						</div>
					</div>

					<a
						v-if="canAccessClass(cls)"
						:href="cls.join_url"
						target="_blank"
						class="sh-btn-primary w-full"
					>
						<Video class="size-4" />
						{{ __('Unirse a clase') }}
					</a>

					<div v-else class="sh-live-disabled">
						{{ hasClassEnded(cls) ? __('Clase finalizada') : __('Disponible el día de la clase') }}
					</div>
				</div>
			</div>
		</section>

		<!-- MY COURSES -->
		<section v-if="remainingCourses.length" class="sh-section">
			<div class="sh-section-head">
				<div>
					<div class="sh-section-kicker">
						<BookOpen class="size-4" />
						{{ __('Tus cursos') }}
					</div>

					<h2>{{ __('Mis cursos') }}</h2>
				</div>

				<router-link :to="{ name: 'Courses' }" class="sh-link">
					{{ __('Ver todos') }}
					<MoveRight class="size-4" />
				</router-link>
			</div>

			<div class="sh-courses-grid">
				<router-link
					v-for="course in remainingCourses"
					:key="course.name"
					:to="{ name: 'CourseDetail', params: { courseName: course.name } }"
					class="sh-course-link"
				>
					<CourseCard :course="course" />
				</router-link>
			</div>
		</section>

		<!-- CERTIFICATES + PLUS -->
		<section class="sh-bottom-grid">
			<div class="sh-card sh-cert-card">
				<div class="sh-card-header">
					<div>
						<div class="sh-section-kicker">
							<Award class="size-4" />
							{{ __('Logros') }}
						</div>

						<h3>{{ __('Certificados y progreso') }}</h3>

						<p>
							{{ __('Completa cursos y evaluaciones para obtener certificados verificables de StudyBadge.') }}
						</p>
					</div>
				</div>

				<div class="sh-cert-content">
					<div class="sh-cert-icon" :class="{ active: certCount }">
						<Award class="size-9" />
					</div>

					<div>
						<h4>
							{{ certCount ? __('Tienes {0} certificado(s)').replace('{0}', certCount) : __('Aún no tienes certificados') }}
						</h4>

						<p>
							{{ certCount
								? __('Sigue completando cursos para sumar más logros a tu perfil.')
								: __('Completa tu primer curso elegible para desbloquear tu certificado.')
							}}
						</p>
					</div>
				</div>

				<router-link
					v-if="profileUsername"
					:to="{ name: 'ProfileCertificates', params: { username: profileUsername } }"
					class="sh-btn-outline"
				>
					{{ __('Ver mis certificados') }}
				</router-link>
			</div>

			<div class="sh-plus-card">
				<div class="sh-plus-content">
					<div class="sh-plus-badge">
						<Crown class="size-4" />
						{{ __('StudyBadge Plus') }}
					</div>

					<h3>
						{{ billing.data?.active ? __('Tu plan Plus está activo') : (hasExpiredTrial ? __('Renueva tu membresía Plus') : __('Aprende más rápido con Plus')) }}
					</h3>

					<p>
						{{ __('Desbloquea TutorIA ilimitado, prompts, simulaciones, generación de cursos y certificados incluidos en cursos elegibles.') }}
					</p>

					<ul class="sh-plus-list">
						<li>
							<CheckCircle2 class="size-4" />
							{{ __('TutorIA ilimitado') }}
						</li>

						<li>
							<CheckCircle2 class="size-4" />
							{{ __('Biblioteca de prompts') }}
						</li>

						<li>
							<CheckCircle2 class="size-4" />
							{{ __('Simulaciones tipo entrevista') }}
						</li>

						<li>
							<CheckCircle2 class="size-4" />
							{{ __('Certificados incluidos') }}
						</li>
					</ul>

					<div class="sh-plus-actions">
						<router-link :to="{ name: 'Practice' }" class="sh-btn-gold">
							<MessageCircle class="size-4" />
							{{ __('Practicar con IA') }}
						</router-link>

						<router-link :to="{ name: 'Plus' }" class="sh-btn-plus-outline">
							{{ billing.data?.active ? __('Gestionar mi Plus') : (hasExpiredTrial ? __('Renovar mi Plus') : __('Desbloquear Plus')) }}
						</router-link>
					</div>
				</div>
			</div>
		</section>

		<UpcomingEvaluations :forHome="true" />
	</div>
</template>

<script setup lang="ts">
import { computed, inject, markRaw, onMounted, ref } from 'vue'
import { call, createResource } from 'frappe-ui'
import { formatTime } from '@/utils'
import {
	ArrowUpRight,
	Award,
	BookOpen,
	Calendar,
	CheckCircle2,
	Clock,
	Crown,
	GraduationCap,
	MessageCircle,
	MoveRight,
	PlayCircle,
	Sparkles,
	Video,
	Zap,
} from 'lucide-vue-next'
import CourseCard from '@/components/CourseCard.vue'
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

const streakInfo = createResource({
	url: 'lms.lms.api.get_streak_info',
	auto: true,
})

const billing = createResource({
	url: 'lms.lms.subscriptions.get_plus_billing',
	auto: true,
})

const hasExpiredTrial = computed(() => {
	const sub = billing.data?.subscription
	if (!sub) return false
	return !billing.data?.active
})

const certCount = ref(0)

const firstName = computed(() => {
	const name =
		user?.data?.first_name ||
		user?.data?.full_name ||
		user?.data?.name ||
		'StudyBadger'

	return String(name).split(' ')[0]
})

const profileUsername = computed(() => {
	return user?.data?.username || user?.data?.name || user?.data?.email || ''
})

const fetchCertCount = () => {
	if (!user?.data?.name) return

	call('frappe.client.get_count', {
		doctype: 'LMS Certificate',
		filters: {
			member: user.data.name,
		},
	})
		.then((data: any) => {
			certCount.value = data || 0
		})
		.catch(() => {
			certCount.value = 0
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
		bgColor: 'rgba(10, 34, 81, 0.08)',
		iconColor: '#0a2251',
	},
	{
		icon: markRaw(Award),
		label: __('Certificados'),
		value: certCount.value || 0,
		suffix: null,
		bgColor: 'rgba(245, 179, 1, 0.14)',
		iconColor: '#b77900',
	},
	{
		icon: markRaw(Zap),
		label: __('Racha actual'),
		value: streakInfo.data?.current_streak || 0,
		suffix: __('días'),
		bgColor: 'rgba(22, 163, 74, 0.1)',
		iconColor: '#16a34a',
	},
	{
		icon: markRaw(Crown),
		label: __('Plan actual'),
		value: billing.data?.active ? 'Plus' : __('Gratis'),
		suffix: null,
		bgColor: billing.data?.active
			? 'rgba(245, 179, 1, 0.14)'
			: 'rgba(100, 116, 139, 0.1)',
		iconColor: billing.data?.active ? '#b77900' : '#64748b',
	},
])

const continueCourse = computed(() => {
	if (!myCourses.data?.length) return null

	const courseWithProgress = myCourses.data.find((course: any) => {
		return course.membership && Number(course.membership.progress || 0) > 0
	})

	return courseWithProgress || myCourses.data[0]
})

const remainingCourses = computed(() => {
	if (!myCourses.data?.length) return []

	if (!continueCourse.value) return myCourses.data

	return myCourses.data.filter((course: any) => course.name !== continueCourse.value.name)
})

const courseProgress = (course: any) => {
	const progress = Number(course?.membership?.progress || 0)
	return Math.min(Math.max(Math.ceil(progress), 0), 100)
}

const getClassEnd = (cls: { date: string; time: string; duration: number }) => {
	const classStart = new Date(`${cls.date}T${cls.time}`)
	return new Date(classStart.getTime() + cls.duration * 60000)
}

const hasClassEnded = (cls: { date: string; time: string; duration: number }) => {
	const classEnd = getClassEnd(cls)
	const now = new Date()
	return now > classEnd
}

const canAccessClass = (cls: { date: string; time: string; duration: number }) => {
	if (!dayjs) return false

	const today = dayjs().format('YYYY-MM-DD')

	if (cls.date < today) return false
	if (cls.date > today) return false
	if (hasClassEnded(cls)) return false

	return true
}
</script>

<style scoped>
.student-home {
	--sh-primary: #0a2251;
	--sh-primary-hover: #12356f;
	--sh-primary-soft: #eaf1fb;
	--sh-primary-soft-2: #f4f8fd;
	--sh-gold: #f5b301;
	--sh-gold-soft: #fff7db;
	--sh-green: #16a34a;
	--sh-green-soft: #ecfdf3;
	--sh-bg: #f5f8fc;
	--sh-card: #ffffff;
	--sh-text: #0f172a;
	--sh-muted: #64748b;
	--sh-soft: #94a3b8;
	--sh-border: #d7e2f0;
	--sh-border-strong: #b9cbe3;
	--sh-shadow-sm: 0 8px 22px rgba(10, 34, 81, 0.08);
	--sh-shadow-md: 0 18px 45px rgba(10, 34, 81, 0.12);
	--sh-shadow-lg: 0 28px 70px rgba(10, 34, 81, 0.16);

	display: flex;
	flex-direction: column;
	gap: 1.75rem;
	color: var(--sh-text);
}

:global(:root[data-theme='dark']) .student-home {
	--sh-bg: #07111f;
	--sh-card: #101a2b;
	--sh-text: #f8fafc;
	--sh-muted: #cbd5e1;
	--sh-soft: #94a3b8;
	--sh-border: rgba(255, 255, 255, 0.1);
	--sh-border-strong: rgba(255, 255, 255, 0.16);
	--sh-primary-soft: rgba(255, 255, 255, 0.06);
	--sh-primary-soft-2: rgba(255, 255, 255, 0.04);
	--sh-shadow-sm: 0 8px 22px rgba(0, 0, 0, 0.22);
	--sh-shadow-md: 0 18px 45px rgba(0, 0, 0, 0.28);
	--sh-shadow-lg: 0 28px 70px rgba(0, 0, 0, 0.34);
}

.sh-hero-card {
	overflow: hidden;
	border: 1px solid rgba(255, 255, 255, 0.16);
	border-radius: 28px;
	background: var(--sh-primary);
	color: #ffffff;
	box-shadow: var(--sh-shadow-lg);
}

.sh-hero-content {
	display: grid;
	grid-template-columns: minmax(0, 1fr) 360px;
	gap: 2rem;
	align-items: center;
	padding: 2rem;
}

.sh-eyebrow,
.sh-section-kicker {
	display: inline-flex;
	align-items: center;
	gap: 0.5rem;
	width: fit-content;
	font-size: 0.75rem;
	font-weight: 900;
	letter-spacing: 0.06em;
	text-transform: uppercase;
}

.sh-eyebrow {
	margin-bottom: 1rem;
	color: rgba(255, 255, 255, 0.82);
}

.sh-hero-title {
	margin: 0;
	max-width: 720px;
	font-size: clamp(2rem, 5vw, 3.75rem);
	font-weight: 950;
	letter-spacing: -0.055em;
	line-height: 1.02;
	color: #ffffff;
}

.sh-hero-subtitle {
	margin: 1rem 0 0;
	max-width: 680px;
	color: rgba(255, 255, 255, 0.78);
	font-size: 1rem;
	line-height: 1.75;
}

.sh-hero-actions {
	display: flex;
	flex-wrap: wrap;
	gap: 0.75rem;
	margin-top: 1.5rem;
}

.sh-hero-panel {
	border: 1px solid rgba(255, 255, 255, 0.16);
	border-radius: 24px;
	background: rgba(255, 255, 255, 0.08);
	padding: 1.25rem;
}

.sh-plan-pill {
	display: inline-flex;
	align-items: center;
	gap: 0.45rem;
	width: fit-content;
	border-radius: 999px;
	background: rgba(255, 255, 255, 0.1);
	padding: 0.45rem 0.7rem;
	color: rgba(255, 255, 255, 0.9);
	font-size: 0.75rem;
	font-weight: 900;
}

.sh-plan-pill.active {
	background: var(--sh-gold);
	color: #3b2a00;
}

.sh-hero-panel-title {
	margin-top: 1rem;
	color: #ffffff;
	font-size: 1.2rem;
	font-weight: 900;
	letter-spacing: -0.03em;
	line-height: 1.18;
}

.sh-hero-panel-text {
	margin: 0.65rem 0 1.25rem;
	color: rgba(255, 255, 255, 0.74);
	font-size: 0.9rem;
	line-height: 1.6;
}

.sh-btn-light,
.sh-btn-ghost-light,
.sh-btn-primary,
.sh-btn-outline,
.sh-btn-panel,
.sh-btn-gold,
.sh-btn-plus-outline {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	gap: 0.5rem;
	border-radius: 999px;
	font-size: 0.9rem;
	font-weight: 900;
	text-decoration: none;
	transition: 0.18s ease;
}

.sh-btn-light {
	background: #ffffff;
	color: var(--sh-primary);
	padding: 0.8rem 1.1rem;
	box-shadow: 0 14px 28px rgba(0, 0, 0, 0.18);
}

.sh-btn-light:hover {
	transform: translateY(-1px);
	background: #f8fbff;
}

.sh-btn-ghost-light {
	border: 1px solid rgba(255, 255, 255, 0.28);
	background: rgba(255, 255, 255, 0.08);
	color: #ffffff;
	padding: 0.8rem 1.1rem;
}

.sh-btn-ghost-light:hover {
	transform: translateY(-1px);
	background: rgba(255, 255, 255, 0.14);
}

.sh-btn-panel {
	width: 100%;
	background: #ffffff;
	color: var(--sh-primary);
	padding: 0.75rem 1rem;
}

.sh-stats-grid {
	display: grid;
	grid-template-columns: repeat(4, minmax(0, 1fr));
	gap: 1rem;
}

.sh-stat-card,
.sh-card,
.sh-continue-card,
.sh-start-card {
	border: 1px solid var(--sh-border);
	background: var(--sh-card);
	box-shadow: var(--sh-shadow-sm);
}

.sh-stat-card {
	display: flex;
	align-items: center;
	gap: 0.9rem;
	border-radius: 20px;
	padding: 1rem 1.1rem;
	transition: 0.18s ease;
}

.sh-stat-card:hover {
	transform: translateY(-2px);
	border-color: var(--sh-border-strong);
	box-shadow: var(--sh-shadow-md);
}

.sh-stat-icon {
	display: flex;
	align-items: center;
	justify-content: center;
	width: 46px;
	height: 46px;
	border-radius: 16px;
	flex: 0 0 auto;
}

.sh-stat-label {
	color: var(--sh-muted);
	font-size: 0.68rem;
	font-weight: 900;
	text-transform: uppercase;
	letter-spacing: 0.08em;
}

.sh-stat-value {
	margin-top: 0.15rem;
	color: var(--sh-text);
	font-size: 1.55rem;
	font-weight: 950;
	letter-spacing: -0.04em;
	line-height: 1;
}

.sh-stat-suffix {
	margin-left: 0.25rem;
	color: var(--sh-muted);
	font-size: 0.85rem;
	font-weight: 700;
	letter-spacing: 0;
}

.sh-main-grid {
	display: grid;
	grid-template-columns: minmax(0, 1fr) 360px;
	gap: 1.5rem;
	align-items: stretch;
}

.sh-continue-card {
	display: grid;
	grid-template-columns: 38% minmax(0, 1fr);
	overflow: hidden;
	border-radius: 28px;
}

.sh-continue-media {
	position: relative;
	min-height: 320px;
	background: var(--sh-primary);
}

.sh-continue-image {
	position: absolute;
	inset: 0;
	background-size: cover;
	background-position: center;
}

.sh-continue-fallback {
	position: absolute;
	inset: 0;
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	gap: 0.8rem;
	color: #ffffff;
	font-size: 0.9rem;
	font-weight: 900;
}

.sh-mobile-progress {
	position: absolute;
	left: 0;
	right: 0;
	bottom: 0;
	height: 5px;
	background: rgba(255, 255, 255, 0.18);
}

.sh-mobile-progress-fill {
	height: 100%;
	background: #ffffff;
	transition: width 0.5s ease;
}

.sh-continue-body {
	display: flex;
	flex-direction: column;
	justify-content: center;
	padding: 1.7rem;
}

.sh-section-kicker {
	margin-bottom: 0.65rem;
	color: var(--sh-primary);
}

.sh-continue-title {
	margin: 0;
	color: var(--sh-text);
	font-size: clamp(1.45rem, 3vw, 2rem);
	font-weight: 950;
	letter-spacing: -0.045em;
	line-height: 1.08;
}

.sh-continue-desc {
	margin: 0.8rem 0 1.4rem;
	color: var(--sh-muted);
	font-size: 0.95rem;
	line-height: 1.7;
}

.sh-progress-wrap {
	margin-bottom: 1.4rem;
}

.sh-progress-head {
	display: flex;
	align-items: center;
	justify-content: space-between;
	margin-bottom: 0.55rem;
	color: var(--sh-muted);
	font-size: 0.8rem;
	font-weight: 800;
}

.sh-progress-head strong {
	color: var(--sh-primary);
}

.sh-progress-track {
	overflow: hidden;
	height: 8px;
	border-radius: 999px;
	background: var(--sh-primary-soft);
}

.sh-progress-bar {
	height: 100%;
	border-radius: inherit;
	background: var(--sh-primary);
	transition: width 0.5s ease;
}

.sh-continue-actions {
	display: flex;
	flex-wrap: wrap;
	gap: 0.75rem;
}

.sh-btn-primary {
	background: var(--sh-primary);
	color: #ffffff;
	padding: 0.8rem 1.05rem;
	box-shadow: 0 12px 26px rgba(10, 34, 81, 0.2);
}

.sh-btn-primary:hover {
	transform: translateY(-1px);
	background: var(--sh-primary-hover);
}

.sh-btn-outline {
	border: 1px solid var(--sh-border-strong);
	background: transparent;
	color: var(--sh-primary);
	padding: 0.78rem 1rem;
}

.sh-btn-outline:hover {
	transform: translateY(-1px);
	background: var(--sh-primary-soft);
	border-color: var(--sh-primary);
}

:global(:root[data-theme='dark']) .sh-btn-outline {
	color: #ffffff;
}

.sh-start-card {
	display: flex;
	min-height: 330px;
	flex-direction: column;
	align-items: flex-start;
	justify-content: center;
	border-radius: 28px;
	padding: 2rem;
}

.sh-start-icon {
	display: flex;
	align-items: center;
	justify-content: center;
	width: 74px;
	height: 74px;
	border-radius: 24px;
	background: var(--sh-primary-soft);
	color: var(--sh-primary);
	margin-bottom: 1.2rem;
}

.sh-start-card h2 {
	margin: 0;
	color: var(--sh-text);
	font-size: clamp(1.5rem, 4vw, 2.25rem);
	font-weight: 950;
	letter-spacing: -0.045em;
	line-height: 1.08;
}

.sh-start-card p {
	margin: 0.85rem 0 1.5rem;
	max-width: 560px;
	color: var(--sh-muted);
	line-height: 1.7;
}

.sh-card {
	border-radius: 24px;
}

.sh-quick-card {
	padding: 1.25rem;
	height: 100%;
}

.sh-card-header h3 {
	margin: 0;
	color: var(--sh-text);
	font-size: 1.2rem;
	font-weight: 950;
	letter-spacing: -0.035em;
}

.sh-card-header p {
	margin: 0.35rem 0 0;
	color: var(--sh-muted);
	font-size: 0.9rem;
	line-height: 1.6;
}

.sh-quick-list {
	display: grid;
	gap: 0.8rem;
	margin-top: 1.2rem;
}

.sh-quick-item {
	display: grid;
	grid-template-columns: 46px minmax(0, 1fr) 20px;
	gap: 0.8rem;
	align-items: center;
	border: 1px solid var(--sh-border);
	border-radius: 18px;
	background: var(--sh-primary-soft-2);
	padding: 0.9rem;
	color: inherit;
	text-decoration: none;
	transition: 0.18s ease;
}

.sh-quick-item:hover {
	transform: translateY(-1px);
	border-color: var(--sh-primary);
	background: var(--sh-primary-soft);
}

.sh-quick-icon {
	display: flex;
	align-items: center;
	justify-content: center;
	width: 46px;
	height: 46px;
	border-radius: 16px;
	background: var(--sh-primary);
	color: #ffffff;
}

.sh-quick-icon.gold {
	background: var(--sh-gold);
	color: #3b2a00;
}

.sh-quick-icon.green {
	background: var(--sh-green);
	color: #ffffff;
}

.sh-quick-item strong {
	display: block;
	color: var(--sh-text);
	font-size: 0.9rem;
	font-weight: 900;
	line-height: 1.25;
}

.sh-quick-item span {
	display: block;
	margin-top: 0.18rem;
	color: var(--sh-muted);
	font-size: 0.78rem;
	line-height: 1.4;
}

.sh-section {
	display: flex;
	flex-direction: column;
	gap: 1rem;
}

.sh-section-head {
	display: flex;
	align-items: end;
	justify-content: space-between;
	gap: 1rem;
}

.sh-section-head h2 {
	margin: 0;
	color: var(--sh-text);
	font-size: 1.4rem;
	font-weight: 950;
	letter-spacing: -0.04em;
}

.sh-link {
	display: inline-flex;
	align-items: center;
	gap: 0.35rem;
	color: var(--sh-primary);
	font-size: 0.9rem;
	font-weight: 900;
	text-decoration: none;
}

.sh-link:hover {
	color: var(--sh-primary-hover);
}

.sh-live-grid {
	display: grid;
	grid-template-columns: repeat(4, minmax(0, 1fr));
	gap: 1rem;
}

.sh-live-card {
	display: flex;
	flex-direction: column;
	padding: 1.1rem;
}

.sh-live-badge {
	display: inline-flex;
	align-items: center;
	gap: 0.35rem;
	width: fit-content;
	border-radius: 999px;
	background: rgba(239, 68, 68, 0.1);
	color: #dc2626;
	padding: 0.35rem 0.6rem;
	font-size: 0.72rem;
	font-weight: 900;
}

.sh-live-card h3 {
	margin: 0.9rem 0 0;
	color: var(--sh-text);
	font-size: 1rem;
	font-weight: 900;
	line-height: 1.25;
}

.sh-live-card p {
	margin: 0.5rem 0 1rem;
	color: var(--sh-muted);
	font-size: 0.86rem;
	line-height: 1.55;
	flex: 1;
}

.sh-live-meta {
	display: grid;
	gap: 0.55rem;
	margin-bottom: 1rem;
}

.sh-live-meta div {
	display: flex;
	align-items: center;
	gap: 0.45rem;
	color: var(--sh-muted);
	font-size: 0.82rem;
	font-weight: 750;
}

.sh-live-meta svg {
	color: var(--sh-primary);
}

.sh-live-disabled {
	border-radius: 999px;
	background: var(--sh-primary-soft);
	color: var(--sh-muted);
	padding: 0.75rem 1rem;
	text-align: center;
	font-size: 0.82rem;
	font-weight: 800;
}

.sh-courses-grid {
	display: grid;
	grid-template-columns: repeat(3, minmax(0, 1fr));
	gap: 1.2rem;
}

.sh-course-link {
	display: block;
	text-decoration: none;
}

.sh-bottom-grid {
	display: grid;
	grid-template-columns: minmax(0, 1.15fr) minmax(340px, 0.85fr);
	gap: 1.5rem;
	align-items: stretch;
}

.sh-cert-card {
	display: flex;
	flex-direction: column;
	gap: 1.25rem;
	padding: 1.4rem;
}

.sh-cert-content {
	display: flex;
	align-items: center;
	gap: 1rem;
	border: 1px solid var(--sh-border);
	border-radius: 22px;
	background: var(--sh-primary-soft-2);
	padding: 1rem;
}

.sh-cert-icon {
	display: flex;
	align-items: center;
	justify-content: center;
	width: 72px;
	height: 72px;
	border-radius: 24px;
	background: var(--sh-primary-soft);
	color: var(--sh-soft);
	flex: 0 0 auto;
}

.sh-cert-icon.active {
	background: var(--sh-gold-soft);
	color: #b77900;
}

.sh-cert-content h4 {
	margin: 0;
	color: var(--sh-text);
	font-size: 1rem;
	font-weight: 950;
}

.sh-cert-content p {
	margin: 0.35rem 0 0;
	color: var(--sh-muted);
	font-size: 0.88rem;
	line-height: 1.55;
}

.sh-plus-card {
	overflow: hidden;
	border-radius: 28px;
	background: var(--sh-primary);
	color: #ffffff;
	box-shadow: var(--sh-shadow-lg);
}

.sh-plus-content {
	display: flex;
	flex-direction: column;
	height: 100%;
	padding: 1.5rem;
}

.sh-plus-badge {
	display: inline-flex;
	align-items: center;
	gap: 0.45rem;
	width: fit-content;
	border-radius: 999px;
	background: var(--sh-gold);
	color: #3b2a00;
	padding: 0.45rem 0.7rem;
	font-size: 0.75rem;
	font-weight: 950;
}

.sh-plus-card h3 {
	margin: 1rem 0 0;
	color: #ffffff;
	font-size: 1.55rem;
	font-weight: 950;
	letter-spacing: -0.045em;
	line-height: 1.08;
}

.sh-plus-card p {
	margin: 0.75rem 0 1.2rem;
	color: rgba(255, 255, 255, 0.74);
	font-size: 0.92rem;
	line-height: 1.65;
}

.sh-plus-list {
	display: grid;
	gap: 0.65rem;
	margin: 0 0 1.4rem;
	padding: 0;
	list-style: none;
}

.sh-plus-list li {
	display: flex;
	align-items: center;
	gap: 0.55rem;
	color: rgba(255, 255, 255, 0.9);
	font-size: 0.88rem;
	font-weight: 800;
}

.sh-plus-list svg {
	color: var(--sh-gold);
	flex: 0 0 auto;
}

.sh-plus-actions {
	display: grid;
	gap: 0.7rem;
	margin-top: auto;
}

.sh-btn-gold {
	background: var(--sh-gold);
	color: #3b2a00;
	padding: 0.85rem 1rem;
}

.sh-btn-gold:hover {
	transform: translateY(-1px);
	background: #ffc533;
}

.sh-btn-plus-outline {
	border: 1px solid rgba(255, 255, 255, 0.22);
	background: rgba(255, 255, 255, 0.08);
	color: #ffffff;
	padding: 0.82rem 1rem;
}

.sh-btn-plus-outline:hover {
	transform: translateY(-1px);
	background: rgba(255, 255, 255, 0.14);
}

@media (max-width: 1180px) {
	.sh-hero-content,
	.sh-main-grid,
	.sh-bottom-grid {
		grid-template-columns: 1fr;
	}

	.sh-hero-panel {
		max-width: 560px;
	}

	.sh-live-grid {
		grid-template-columns: repeat(2, minmax(0, 1fr));
	}
}

@media (max-width: 900px) {
	.sh-stats-grid,
	.sh-courses-grid {
		grid-template-columns: repeat(2, minmax(0, 1fr));
	}

	.sh-continue-card {
		grid-template-columns: 1fr;
	}

	.sh-continue-media {
		min-height: 220px;
	}
}

@media (max-width: 640px) {
	.student-home {
		gap: 1.25rem;
	}

	.sh-hero-content {
		padding: 1.25rem;
	}

	.sh-hero-actions,
	.sh-continue-actions {
		flex-direction: column;
	}

	.sh-btn-light,
	.sh-btn-ghost-light,
	.sh-btn-primary,
	.sh-btn-outline {
		width: 100%;
	}

	.sh-stats-grid,
	.sh-live-grid,
	.sh-courses-grid {
		grid-template-columns: 1fr;
	}

	.sh-section-head {
		align-items: flex-start;
		flex-direction: column;
	}

	.sh-cert-content {
		align-items: flex-start;
		flex-direction: column;
	}
}
</style>