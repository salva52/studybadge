<template>
	<header
		class="sticky top-0 z-10 flex items-center justify-between border-b bg-surface-white px-3 py-2.5 sm:px-5"
	>
		<Breadcrumbs class="h-7" :items="breadcrumbs" />
	</header>
	<div class="p-5">
		<div v-if="certificate.data && Object.keys(certificate.data).length">
			<div class="text-lg text-ink-gray-9 font-semibold mb-1">
				{{ __('Certification') }}
			</div>
			<div class="text-ink-gray-9 text-sm">
				{{
					__(
						'You are already certified for this course. Click on the card below to open your certificate.'
					)
				}}
			</div>
			<div
				class="border p-3 w-fit min-w-60 rounded-md space-y-2 hover:bg-surface-gray-1 cursor-pointer mt-5"
				@click="openCertificate(certificate.data)"
			>
				<div class="text-ink-gray-9 font-semibold">
					{{ courseTitle }}
				</div>
				<div class="text-sm text-ink-gray-7 font-medium">
					{{ __('Issued On') }}:
					{{ dayjs(certificate.data.issue_date).format('DD MMM YYYY') }}
				</div>
			</div>
		</div>
			<div v-else>
				<div
					v-if="hasPlusAccess"
					class="mb-4 rounded-md bg-surface-green-1 p-3 text-sm text-ink-green-3"
				>
					{{ __('Plus activo: puedes programar tu evaluacion de certificado.') }}
				</div>
				<UpcomingEvaluations v-if="courses.length" :courses="courses" />
			</div>
		</div>
</template>
<script setup>
import { computed, inject, onMounted, ref } from 'vue'
import { Breadcrumbs, call, createResource, usePageMeta } from 'frappe-ui'
import { useRouter } from 'vue-router'
import { sessionStore } from '../../stores/session'
import UpcomingEvaluations from '@/components/UpcomingEvaluations.vue'

const courseTitle = ref(null)
const evaluator = ref(null)
const hasPlusAccess = ref(false)
const { brand } = sessionStore()
const courses = ref([])
const user = inject('$user')
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
	fetchCourseDetails()
})

const certificate = createResource({
	url: 'frappe.client.get_value',
	params: {
		doctype: 'LMS Certificate',
		filters: {
			member: user.data?.name,
			course: props.courseName,
		},
		fieldname: ['name', 'template', 'issue_date'],
	},
	cache: [user.data?.name, props.courseName],
})

const fetchCertificationDetails = () => {
	call('lms.lms.api.get_certification_details', {
		course: props.courseName,
	}).then((data) => {
		const hasAccess =
			data.certificate ||
			!data.paid_certificate ||
			data.membership?.purchased_certificate ||
			data.has_plus
		hasPlusAccess.value = Boolean(data.has_plus)
		if (!data.membership) {
			router.push({
				name: 'CourseDetail',
				params: { courseName: props.courseName },
			})
		} else if (hasAccess) {
			certificate.reload()
		} else {
			router.push({
				name: 'Plus',
				query: { from: 'certificate', course: props.courseName },
			})
		}
	})
}

const fetchCourseDetails = () => {
	call('frappe.client.get_value', {
		doctype: 'LMS Course',
		filters: { name: props.courseName },
		fieldname: ['title', 'evaluator'],
	}).then((data) => {
		courseTitle.value = data.title
		evaluator.value = data.evaluator
		populateCourses()
	})
}

const populateCourses = () => {
	courses.value = [
		{
			course: props.courseName,
			title: courseTitle.value,
			evaluator: evaluator.value,
		},
	]
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
