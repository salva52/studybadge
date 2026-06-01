<template>
	<Button
		v-if="certification.data && certification.data.certificate"
		@click="downloadCertificate"
		class=""
	>
		<template #prefix>
			<GraduationCap class="size-4 stroke-1.5" />
		</template>
		<span class="hidden sm:inline">{{ __('Ver certificado') }}</span>
	</Button>
	<div
		v-else-if="
			certification.data &&
			certification.data.membership &&
			certification.data.paid_certificate &&
			user.data?.is_student
		"
	>
		<router-link
			v-if="
				certification.data.membership.progress >= 100 &&
				!certification.data.membership.purchased_certificate &&
				!certification.data.has_plus
			"
			:to="{
				name: 'Billing',
				params: {
					type: 'certificate',
					name: courseName,
				},
			}"
		>
			<Button>
				<template #prefix>
					<GraduationCap class="size-4 stroke-1.5" />
				</template>
				<span class="hidden sm:inline">{{ __('Comprar certificado') }}</span>
			</Button>
		</router-link>
		<router-link
			v-else-if="
				certification.data.membership.progress >= 100 &&
				(!certification.data.membership.certificate ||
					certification.data.has_plus)
			"
			:to="{
				name: 'CourseCertification',
				params: {
					courseName: courseName,
				},
			}"
		>
			<Button>
				<template #prefix>
					<GraduationCap class="size-4 stroke-1.5" />
				</template>
				<span class="hidden sm:inline">{{ __('Emitir certificado') }}</span>
			</Button>
		</router-link>
		<Button v-else variant="subtle" disabled>
			<template #prefix>
				<GraduationCap class="size-4 stroke-1.5" />
			</template>
			<span class="hidden sm:inline">{{ __('Completa el curso para certificarte') }}</span>
		</Button>
	</div>
</template>
<script setup>
import { Button, createResource } from 'frappe-ui'
import { inject } from 'vue'
import { GraduationCap } from 'lucide-vue-next'

const user = inject('$user')

const props = defineProps({
	courseName: {
		type: String,
		required: true,
	},
})

const certification = createResource({
	url: 'lms.lms.api.get_certification_details',
	makeParams(values) {
		return {
			course: props.courseName,
		}
	},
	auto: user.data ? true : false,
})

const downloadCertificate = () => {
	window.open(
		`/api/method/frappe.utils.print_format.download_pdf?doctype=LMS+Certificate&name=${
			certification.data.certificate.name
		}&format=${encodeURIComponent(certification.data.certificate.template)}`
	)
}
</script>
