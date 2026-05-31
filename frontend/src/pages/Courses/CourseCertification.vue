<template>
	<header
		class="sticky top-0 z-10 flex items-center justify-between border-b bg-surface-white px-3 py-2.5 sm:px-5"
	>
		<Breadcrumbs class="h-7" :items="breadcrumbs" />
	</header>
	<div class="p-5">
		<div v-if="certificate.data && Object.keys(certificate.data).length">
			<div class="text-lg text-ink-gray-9 font-semibold mb-1">
				{{ __('Certificación') }}
			</div>
			<div class="text-ink-gray-9 text-sm">
				{{ __('Tu certificado ya fue emitido. Haz clic en la tarjeta para abrirlo.') }}
			</div>
			<div
				class="border p-3 w-fit min-w-60 rounded-md space-y-2 hover:bg-surface-gray-1 cursor-pointer mt-5"
				@click="openCertificate(certificate.data)"
			>
				<div class="text-ink-gray-9 font-semibold">
					{{ courseTitle }}
				</div>
				<div class="text-sm text-ink-gray-7 font-medium">
					{{ __('Emitido el') }}:
					{{ dayjs(certificate.data.issue_date).format('DD MMM YYYY') }}
				</div>
			</div>
		</div>
		<div v-else class="auto-cert-card">
			<div class="auto-cert-icon">
				<GraduationCap class="size-6" />
			</div>
			<div class="min-w-0 flex-1">
				<div class="text-lg font-semibold text-ink-gray-9">
					{{
						courseProgress >= 100
							? __('Estamos preparando tu certificado')
							: __('Completa el curso para emitir tu certificado')
					}}
				</div>
				<div class="mt-2 text-sm leading-5 text-ink-gray-6">
					{{
						courseProgress >= 100
							? __('Ya tienes acceso a la certificación. Si no aparece en unos segundos, actualiza esta pantalla.')
							: __('Cuando llegues al 100%, StudyBadge emitirá tu certificado automáticamente si ya pagaste el certificado o tienes Plus activo.')
					}}
				</div>
				<div class="mt-4 flex flex-wrap items-center gap-3">
					<div class="rounded-md bg-blue-50 px-3 py-1 text-sm font-semibold text-[#0a2351]">
						{{ Math.floor(courseProgress) }}% {{ __('completado') }}
					</div>
					<button class="auto-cert-button" @click="fetchCertificationDetails">
						{{ courseProgress >= 100 ? __('Actualizar') : __('Revisar estado') }}
					</button>
				</div>
			</div>
		</div>
	</div>
</template>
<script setup>
import { computed, inject, onMounted, ref } from 'vue'
import { Breadcrumbs, call, usePageMeta } from 'frappe-ui'
import { useRouter } from 'vue-router'
import { sessionStore } from '../../stores/session'
import { GraduationCap } from 'lucide-vue-next'

const courseTitle = ref(null)
const courseProgress = ref(0)
const { brand } = sessionStore()
const dayjs = inject('$dayjs')
const router = useRouter()

const props = defineProps({
	courseName: {
		type: String,
		required: true,
	},
})

onMounted(() => {
	fetchCertificationDetails()
})

const certificate = ref({ data: null })

const fetchCertificationDetails = () => {
	call('lms.lms.api.get_certification_details', {
		course: props.courseName,
	}).then((data) => {
		courseTitle.value = data.course_title
		courseProgress.value = Number(data.membership?.progress || 0)
		certificate.value.data = data.certificate || null
		if (!data.membership) {
			router.push({
				name: 'CourseDetail',
				params: { courseName: props.courseName },
			})
		} else if (
			data.paid_certificate &&
			!data.membership?.purchased_certificate &&
			!data.has_plus &&
			courseProgress.value >= 100
		) {
			router.push({
				name: 'Billing',
				params: { type: 'certificate', name: props.courseName },
			})
		} else {
			certificate.value.data = data.certificate || null
		}
	})
}

const openCertificate = (certificate) => {
	window.open(
		`/api/method/frappe.utils.print_format.download_pdf?doctype=LMS+Certificate&name=${
			certificate.name
		}&format=${encodeURIComponent(certificate.template)}`,
		'_blank'
	)
}

const breadcrumbs = computed(() => [
	{
		label: __('Courses'),
		route: { name: 'Courses' },
	},
	{
		label: courseTitle.value,
		route: { name: 'CourseDetail', params: { courseName: props.courseName } },
	},
	{
		label: __('Certification'),
	},
])

usePageMeta(() => {
	return {
		title: courseTitle.value,
		icon: brand.favicon,
	}
})
</script>

<style scoped>
.auto-cert-card {
	display: flex;
	gap: 16px;
	max-width: 760px;
	border: 1px solid rgba(10, 35, 81, 0.1);
	border-radius: 8px;
	background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
	padding: 22px;
	box-shadow: 0 8px 24px rgba(10, 35, 81, 0.06);
}

.auto-cert-icon {
	display: flex;
	align-items: center;
	justify-content: center;
	width: 48px;
	height: 48px;
	flex-shrink: 0;
	border-radius: 8px;
	background: #0a2351;
	color: white;
}

.auto-cert-button {
	border-radius: 8px;
	background: #0a2351;
	color: white;
	font-size: 0.875rem;
	font-weight: 600;
	padding: 0.5rem 0.85rem;
}

.auto-cert-button:hover {
	background: #12346f;
}

:root[data-theme='dark'] .auto-cert-card {
	border-color: rgba(255, 255, 255, 0.08);
	background: rgba(255, 255, 255, 0.03);
	box-shadow: none;
}

@media (max-width: 640px) {
	.auto-cert-card {
		flex-direction: column;
	}
}
</style>
