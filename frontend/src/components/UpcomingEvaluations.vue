<template>
	<div v-if="!forHome || (forHome && upcoming_evals.data?.length)">
		<div class="flex items-center justify-between mb-4">
			<div>
				<div class="text-lg text-ink-gray-9 font-semibold">
					{{ __('Próximas evaluaciones') }}
				</div>
				<div v-if="!forHome" class="mt-1 text-sm text-ink-gray-6">
					{{ __('Agenda tu evaluación final para obtener tu certificado.') }}
				</div>
			</div>
			<Button v-if="canScheduleEvals" @click="openEvalModal">
				<template #prefix>
					<Calendar class="w-4 h-4 stroke-1.5" />
				</template>
				{{ __('Programar evaluación') }}
			</Button>
		</div>
		<div
			v-if="endDate && !endDateHasPassed"
			class="text-sm leading-5 bg-surface-amber-1 text-ink-amber-3 p-2 rounded-md mb-4"
		>
			{{ __('El último día para programar tus evaluaciones es ') }}
			<span class="font-medium">
				{{ dayjs(endDate).format('DD MMMM YYYY') }} </span
			>.
			{{ __('Asegúrate de reservar tu horario antes de esa fecha.') }}
		</div>
		<div
			v-else-if="endDateHasPassed"
			class="text-sm leading-5 bg-surface-red-1 text-ink-red-3 p-2 rounded-md mb-4"
		>
			{{
				__(
					'El plazo para programar evaluaciones ya pasó. Contacta al instructor para recibir ayuda.'
				)
			}}
		</div>
		<div v-if="upcoming_evals.data?.length">
			<div
				class="grid gap-4"
				:class="forHome ? 'grid-cols-1 md:grid-cols-4' : 'grid-cols-1'"
			>
				<div v-for="evl in upcoming_evals.data">
					<div
						class="border hover:border-outline-gray-3 text-ink-gray-7 rounded-md p-3"
					>
						<div class="flex justify-between mb-3">
							<span class="font-semibold text-ink-gray-9 leading-5">
								{{ evl.course_title }}
							</span>
							<Dropdown
								v-if="evl.date > dayjs().format()"
								:options="[
									{
										label: __('Cancel'),
										icon: Ban,
										onClick() {
											cancelEvaluation(evl)
										},
									},
								]"
								placement="left"
								side="left"
							>
								<template v-slot="{ open }">
									<Button variant="ghost">
										<template #icon>
											<EllipsisVertical class="w-4 h-4 stroke-1.5" />
										</template>
									</Button>
								</template>
							</Dropdown>
						</div>
						<div class="flex items-center mb-2">
							<Calendar class="w-4 h-4 stroke-1.5" />
							<span class="ms-2">
								{{ dayjs(evl.date).format('DD MMMM YYYY') }}
							</span>
						</div>
						<div class="flex items-center mb-2">
							<Clock class="w-4 h-4 stroke-1.5" />
							<span class="ms-2">
								{{ formatTime(evl.start_time) }}
							</span>
						</div>
						<div class="flex items-center">
							<GraduationCap class="w-4 h-4 stroke-1.5" />
							<span class="ms-2">
								{{ evl.evaluator_name }}
							</span>
						</div>
						<div
							v-if="evl.google_meet_link"
							class="flex items-center justify-between gap-x-2 mt-4"
						>
							<Button @click="openEvalCall(evl)" class="w-full">
								<template #prefix>
									<HeadsetIcon class="w-4 h-4 stroke-1.5" />
								</template>
								{{ __('Entrar a la llamada') }}
							</Button>
						</div>
					</div>
				</div>
			</div>
		</div>
		<div v-else-if="!endDateHasPassed" class="cert-empty-state">
			<div class="cert-empty-icon">
				<Calendar class="w-6 h-6 stroke-1.5" />
			</div>
			<div class="min-w-0">
				<div class="font-semibold text-ink-gray-9">
					{{ __('Tu certificado está listo para el siguiente paso') }}
				</div>
				<div class="mt-1 text-sm leading-5 text-ink-gray-6">
					{{ __('Programa una evaluación con el equipo de StudyBadge y completa tu certificación.') }}
				</div>
			</div>
			<Button
				v-if="canScheduleEvals"
				class="cert-empty-action"
				@click="openEvalModal"
			>
				<template #prefix>
					<GraduationCap class="w-4 h-4 stroke-1.5" />
				</template>
				{{ __('Programar ahora') }}
			</Button>
		</div>
	</div>
	<EvaluationModal
		:batch="batch"
		:endDate="endDate"
		:courses="courses"
		v-model="showEvalModal"
		v-model:reloadEvals="upcoming_evals"
	/>
</template>
<script setup>
import {
	Ban,
	Calendar,
	Clock,
	GraduationCap,
	HeadsetIcon,
	EllipsisVertical,
} from 'lucide-vue-next'
import { inject, ref, getCurrentInstance, computed } from 'vue'
import { formatTime } from '@/utils'
import { Button, createListResource, call, Dropdown, toast } from 'frappe-ui'
import EvaluationModal from '@/components/Modals/EvaluationModal.vue'

const dayjs = inject('$dayjs')
const user = inject('$user')
const showEvalModal = ref(false)
const app = getCurrentInstance()
const { $dialog } = app.appContext.config.globalProperties

const props = defineProps({
	batch: {
		type: String,
		default: null,
	},
	courses: {
		type: Array,
		default: [],
	},
	endDate: {
		type: String,
		default: null,
	},
	forHome: {
		type: Boolean,
		default: false,
	},
})

const upcoming_evals = createListResource({
	doctype: 'LMS Certificate Request',
	filters: {
		course: props.courses?.length
			? ['in', props.courses.map((course) => course.course)]
			: undefined,
		batch_name: props.batch || undefined,
		status: 'Upcoming',
		member: user?.data?.name,
		date: ['>=', dayjs().format('YYYY-MM-DD')],
	},
	fields: [
		'name',
		'date',
		'start_time',
		'evaluator_name',
		'course_title',
		'member',
		'member_name',
		'google_meet_link',
	],
	orderBy: 'date',
	auto: true,
})

function openEvalModal() {
	showEvalModal.value = true
}

const openEvalCall = (evl) => {
	window.open(evl.google_meet_link, '_blank')
}

const evaluationCourses = computed(() => {
	return props.courses.filter((course) => {
		return course.evaluator && course.evaluator != ''
	})
})

const canScheduleEvals = computed(() => {
	return (
		upcoming_evals.data?.length != evaluationCourses.value?.length &&
		!props.forHome &&
		!endDateHasPassed.value
	)
})

const endDateHasPassed = computed(() => {
	return dayjs().isSameOrAfter(dayjs(props.endDate))
})

const cancelEvaluation = (evl) => {
	$dialog({
		title: __('Confirm Cancellation?'),
		message: __(
			'Are you sure you want to cancel this evaluation? This action cannot be undone.'
		),
		actions: [
			{
				label: __('Cancel'),
				theme: 'red',
				variant: 'solid',
				onClick(close) {
					call('lms.lms.api.cancel_evaluation', { evaluation: evl })
						.then(() => {
							upcoming_evals.reload()
							toast.success(__('Evaluation cancelled successfully'))
						})
						.catch((err) => {
							toast.error(__(err.messages?.[0] || err))
							console.error(err)
						})
					close()
				},
			},
		],
	})
}
</script>

<style scoped>
.cert-empty-state {
	display: flex;
	align-items: center;
	gap: 14px;
	border: 1px solid rgba(10, 35, 81, 0.1);
	border-radius: 8px;
	background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
	padding: 18px;
	box-shadow: 0 8px 24px rgba(10, 35, 81, 0.06);
}

.cert-empty-icon {
	display: flex;
	align-items: center;
	justify-content: center;
	width: 44px;
	height: 44px;
	flex-shrink: 0;
	border-radius: 8px;
	background: #0a2351;
	color: white;
}

.cert-empty-action {
	margin-left: auto;
	flex-shrink: 0;
}

:root[data-theme='dark'] .cert-empty-state {
	border-color: rgba(255, 255, 255, 0.08);
	background: rgba(255, 255, 255, 0.03);
	box-shadow: none;
}

@media (max-width: 640px) {
	.cert-empty-state {
		align-items: flex-start;
		flex-direction: column;
	}

	.cert-empty-action {
		margin-left: 0;
		width: 100%;
	}
}
</style>
