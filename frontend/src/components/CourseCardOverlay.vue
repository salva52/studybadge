<template>
	<div class="course-card-overlay">
		<iframe
			v-if="course.data.video_link"
			:src="video_link"
			class="course-card-video"
		/>
		<div class="course-card-body">
			<div v-if="course.data.paid_course" class="course-card-price">
				{{ course.data.price }}
			</div>
			<div v-if="!readOnlyMode">
				<div v-if="course.data.membership" class="space-y-2 mb-6">
					<router-link
						:to="{
							name: 'Lesson',
							params: {
								courseName: course.name,
								chapterNumber: course.data.current_lesson
									? course.data.current_lesson.split('-')[0]
									: 1,
								lessonNumber: course.data.current_lesson
									? course.data.current_lesson.split('-')[1]
									: 1,
							},
						}"
					>
						<Button variant="solid" size="md" class="w-full">
							<template #prefix>
								<BookText class="size-4 stroke-1.5" />
							</template>
							<span>
								{{ __('Continuar Aprendiendo') }}
							</span>
						</Button>
					</router-link>
					<CertificationLinks :courseName="course.data.name" class="w-full" />
				</div>
				<router-link
					v-else-if="course.data.paid_course && !isAdmin"
					:to="{
						name: 'Billing',
						params: {
							type: 'course',
							name: course.data.name,
						},
					}"
				>
					<Button variant="solid" size="md" class="w-full mb-6">
						<template #prefix>
							<CreditCard class="size-4 stroke-1.5" />
						</template>
						<span>
							{{ __('Comprar este curso') }}
						</span>
					</Button>
				</router-link>
				<Badge
					v-else-if="course.data.disable_self_learning && !isAdmin"
					theme="blue"
					size="lg"
					class="mb-4"
				>
					{{ __('Contacta al administrador para inscribirte en este curso.') }}
				</Badge>
				<Button
					v-else-if="!isAdmin"
					@click="enrollStudent()"
					variant="solid"
					class="w-full mb-6"
					size="md"
				>
					<template #prefix>
						<BookText class="size-4 stroke-1.5" />
					</template>
					<span>
						{{ __('Empezar a Aprender') }}
					</span>
				</Button>
				<Button
					v-if="canGetCertificate"
					@click="fetchCertificate()"
					variant="subtle"
					class="w-full mt-2"
					size="md"
				>
					<template #prefix>
						<GraduationCap class="size-4 stroke-1.5" />
					</template>
					{{ __('Obtener Certificado') }}
				</Button>
			</div>

			<div class="course-card-stats">
				<div class="course-card-stats-title">
					{{ __('Este curso incluye:') }}
				</div>
				<div class="course-card-stat-item">
					<BookOpen class="course-card-stat-icon" />
					<span>
						{{ course.data.lessons }}
						{{ course.data.lessons > 1 ? __('lecciones') : __('lección') }}
					</span>
				</div>
				<div class="course-card-stat-item">
					<Users class="course-card-stat-icon" />
					<span>
						{{ formatAmount(course.data.enrollments) }}
						{{
							course.data.enrollments > 1
								? __('estudiantes inscritos')
								: __('estudiante inscrito')
						}}
					</span>
				</div>
				<div
					v-if="parseInt(course.data.rating) > 0"
					class="course-card-stat-item"
				>
					<Star class="course-card-stat-icon fill-yellow-500 !text-transparent" />
					<span>
						{{ course.data.rating }} {{ __('calificación promedio') }}
					</span>
				</div>
				<div
					v-if="course.data.enable_certification"
					class="course-card-stat-item course-card-stat-highlight"
				>
					<GraduationCap class="course-card-stat-icon !text-green-600" />
					<span>
						{{ __('Certificado de Finalización') }}
					</span>
				</div>
				<div
					v-if="course.data.paid_certificate"
					class="course-card-stat-item course-card-stat-highlight"
				>
					<GraduationCap class="course-card-stat-icon !text-green-600" />
					<span>
						{{ __('Certificado con Evaluación') }}
					</span>
				</div>
			</div>
		</div>
	</div>
</template>
<script setup>
import {
	BookOpen,
	BookText,
	CreditCard,
	GraduationCap,
	Pencil,
	Star,
	TrendingUp,
	Users,
} from 'lucide-vue-next'
import { computed, inject, ref } from 'vue'
import { Badge, Button, call, createResource, toast } from 'frappe-ui'
import { formatAmount } from '@/utils/'
import { useRouter } from 'vue-router'
import CertificationLinks from '@/components/CertificationLinks.vue'
import { useTelemetry } from 'frappe-ui/frappe'

const router = useRouter()
const user = inject('$user')
const readOnlyMode = window.read_only_mode
const { capture } = useTelemetry()

const props = defineProps({
	course: {
		type: Object,
		default: null,
	},
})

const video_link = computed(() => {
	if (props.course.data.video_link) {
		return 'https://www.youtube.com/embed/' + props.course.data.video_link
	}
	return null
})

function enrollStudent() {
	if (!user.data) {
		toast.warning(__('You need to login first to enroll for this course'))
		setTimeout(() => {
			window.location.href = `/login?redirect-to=${window.location.pathname}`
		}, 500)
	} else {
		call('frappe.client.insert', {
			doc: {
				doctype: 'LMS Enrollment',
				course: props.course.data.name,
				member: user.data.name,
			},
		})
			.then(() => {
				capture('enrolled_in_course', {
					course: props.course.data.name,
				})
				toast.success(__('You have been enrolled in this course'))
				setTimeout(() => {
					router.push({
						name: 'Lesson',
						params: {
							courseName: props.course.data.name,
							chapterNumber: 1,
							lessonNumber: 1,
						},
					})
				}, 1000)
			})
			.catch((err) => {
				toast.warning(__(err.messages?.[0] || err))
				console.error(err)
			})
	}
}

const is_instructor = () => {
	let user_is_instructor = false
	props.course.data.instructors.forEach((instructor) => {
		if (!user_is_instructor && instructor.name == user.data?.name) {
			user_is_instructor = true
		}
	})
	return user_is_instructor
}

const canGetCertificate = computed(() => {
	if (
		props.course.data?.enable_certification &&
		props.course.data?.membership?.progress >= 100
	) {
		return true
	}
	return false
})

const certificate = createResource({
	url: 'lms.lms.doctype.lms_certificate.lms_certificate.create_certificate',
	makeParams(values) {
		return {
			course: values.course,
		}
	},
	onSuccess(data) {
		window.open(
			`/api/method/frappe.utils.print_format.download_pdf?doctype=LMS+Certificate&name=${
				data.name
			}&format=${encodeURIComponent(data.template)}`,
			'_blank'
		)
	},
})

const fetchCertificate = () => {
	certificate.submit({
		course: props.course.data?.name,
		member: user.data?.name,
	})
}

const isAdmin = computed(() => {
	return user.data?.is_moderator || is_instructor()
})
</script>
<style>
.course-card-overlay {
	border-radius: var(--sb-radius, 12px);
	box-shadow: var(--sb-shadow-card, 0 2px 12px rgba(6, 27, 73, 0.08));
	border: 1px solid rgba(6, 27, 73, 0.06);
	background: white;
	overflow: hidden;
	min-width: 280px;
	max-width: 380px;
}

.course-card-video {
	border-radius: var(--sb-radius, 12px) var(--sb-radius, 12px) 0 0;
	min-height: 14rem;
	width: 100%;
	border: none;
}

.course-card-body {
	padding: 1.25rem;
}

.course-card-price {
	font-size: 1.75rem;
	font-weight: 700;
	color: var(--sb-dark, #061B49);
	margin-bottom: 0.75rem;
}

.course-card-stats {
	background: rgba(6, 27, 73, 0.025);
	border-radius: 10px;
	padding: 1rem 1.1rem;
	border: 1px solid rgba(6, 27, 73, 0.04);
}

.course-card-stats-title {
	font-size: 0.8125rem;
	font-weight: 600;
	color: var(--sb-dark, #061B49);
	margin-bottom: 0.75rem;
	text-transform: uppercase;
	letter-spacing: 0.04em;
}

.course-card-stat-item {
	display: flex;
	align-items: center;
	gap: 0.5rem;
	font-size: 0.875rem;
	color: #4b5563;
	padding: 0.35rem 0;
}

.course-card-stat-icon {
	width: 1rem;
	height: 1rem;
	stroke-width: 1.5;
	color: var(--sb-primary, #007BFF);
	flex-shrink: 0;
}

.course-card-stat-highlight {
	font-weight: 600;
	color: var(--sb-dark, #061B49);
}

/* Dark mode */
:root[data-theme="dark"] .course-card-overlay,
.dark .course-card-overlay {
	background: #1f2937;
	border-color: rgba(255, 255, 255, 0.06);
}

:root[data-theme="dark"] .course-card-price,
.dark .course-card-price {
	color: #f3f4f6;
}

:root[data-theme="dark"] .course-card-stats,
.dark .course-card-stats {
	background: rgba(255, 255, 255, 0.04);
	border-color: rgba(255, 255, 255, 0.06);
}

:root[data-theme="dark"] .course-card-stats-title,
.dark .course-card-stats-title {
	color: #f3f4f6;
}

:root[data-theme="dark"] .course-card-stat-item,
.dark .course-card-stat-item {
	color: #d1d5db;
}

:root[data-theme="dark"] .course-card-stat-highlight,
.dark .course-card-stat-highlight {
	color: #f3f4f6;
}
</style>
