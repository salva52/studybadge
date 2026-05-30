<template>
	<Dialog
		v-model="show"
		:options="{
			size: '3xl',
		}"
	>
		<template #body-header>
			<div class="flex items-center justify-between mb-6 pb-4 border-b border-surface-gray-2">
				<div>
					<div class="text-2xl font-bold leading-6 text-ink-gray-9">
						{{ __('Editar Perfil') }}
					</div>
					<div class="text-sm text-ink-gray-5 mt-2">
						Actualiza tu información personal y enlaces profesionales
					</div>
				</div>
				<div class="flex items-center gap-x-3">
					<Badge v-if="isDirty" theme="orange" class="animate-pulse">
						{{ __('Sin guardar') }}
					</Badge>
					<Button variant="solid" @click="saveProfile()" class="shadow-sm">
						{{ __('Guardar Cambios') }}
					</Button>
				</div>
			</div>
		</template>
		<template #body-content>
			<div class="text-base">
				<div class="grid grid-cols-2 gap-10">
					<div class="space-y-5">
						<div class="bg-surface-gray-1 p-5 rounded-xl border border-surface-gray-2">
							<Uploader
								v-model="profile.image"
								:label="__('Foto de Perfil')"
								:required="true"
								shape="circle"
							/>
						</div>

						<div class="grid grid-cols-2 gap-4">
							<FormControl
								v-model="profile.first_name"
								:label="__('Nombres')"
								:required="true"
							/>
							<FormControl
								v-model="profile.last_name"
								:label="__('Apellidos')"
								:required="true"
							/>
						</div>
						
						<FormControl v-model="profile.headline" :label="__('Titular Profesional')" placeholder="Ej. Desarrollador Frontend, Estudiante de Ingeniería..." />

						<div class="space-y-4 pt-2">
							<div class="text-sm font-semibold text-ink-gray-8 border-b border-surface-gray-2 pb-2">Redes Sociales</div>
							<FormControl
								v-model="profile.linkedin"
								:label="__('Perfil de LinkedIn')"
								placeholder="https://linkedin.com/in/usuario"
							/>
							<FormControl v-model="profile.github" :label="__('Usuario de GitHub')" placeholder="Ej. octocat" />
							<FormControl
								v-model="profile.twitter"
								:label="__('Usuario de X (Twitter)')"
								placeholder="Ej. usuario"
							/>
						</div>
					</div>
					<div class="space-y-5">
						<FormControl
							v-model="profile.open_to"
							type="select"
							:options="[
								{label: 'No especificar', value: ' '},
								{label: 'Buscando oportunidades', value: 'Work'},
								{label: 'Contratando talento', value: 'Hiring'}
							]"
							:label="__('Disponibilidad')"
						/>
						<FormControl
							v-if="hasRankingPrivacyField"
							v-model="profile.show_in_rankings"
							type="checkbox"
							:label="__('Mostrarme en rankings')"
							:description="
								__('Permite que tu perfil y monedas aparezcan en la tabla de rankings.')
							"
						/>
						<Link
							:label="__('Idioma Preferido')"
							v-model="profile.language"
							doctype="Language"
						/>
						<div class="pt-2">
							<div class="mb-1.5 text-sm font-medium text-ink-gray-7">
								{{ __('Acerca de ti (Biografía)') }}
							</div>
							<TextEditor
								:fixedMenu="true"
								@change="(val) => (profile.bio = val)"
								:content="profile.bio"
								:rows="15"
								editorClass="prose-sm py-2 px-2 min-h-[280px] border-outline-gray-2 hover:border-outline-gray-3 rounded-b-md bg-surface-gray-3"
							/>
						</div>
					</div>
				</div>
			</div>
		</template>
	</Dialog>
</template>
<script setup>
import {
	Badge,
	Button,
	createResource,
	Dialog,
	FormControl,
	TextEditor,
	toast,
} from 'frappe-ui'
import { computed, ref, reactive, watch } from 'vue'
import { sanitizeHTML } from '@/utils'
import Link from '@/components/Controls/Link.vue'

const show = defineModel()
const reloadProfile = defineModel('reloadProfile')
const hasLanguageChanged = ref(false)
const isDirty = ref(false)

const props = defineProps({
	profile: {
		type: Object,
		required: true,
	},
})

const profile = reactive({
	first_name: '',
	last_name: '',
	headline: '',
	bio: '',
	image: '',
	open_to: '',
	linkedin: '',
	github: '',
	twitter: '',
	show_in_rankings: true,
})

const updateProfile = createResource({
	url: 'frappe.client.set_value',
	makeParams(values) {
		let fieldname = {
			user_image: profile.image || null,
			...profile,
		}
		if (hasRankingPrivacyField.value) {
			fieldname.hide_from_rankings = profile.show_in_rankings ? 0 : 1
		}
		delete fieldname.image
		delete fieldname.show_in_rankings
		return {
			doctype: 'User',
			name: props.profile.data.name,
			fieldname,
		}
	},
	onSuccess(data) {
		props.profile.data = data
	},
})

const validateMandatoryFields = () => {
	let missingFields = []
	if (!profile.first_name) missingFields.push(__('First Name'))
	if (!profile.last_name) missingFields.push(__('Last Name'))
	if (!profile.image) missingFields.push(__('Profile Image'))
	if (missingFields.length) {
		toast.error(
			__('Please fill the mandatory fields: {0}').format(
				missingFields.join(', ')
			)
		)
		console.error('Missing mandatory fields:', missingFields)
	}
	return missingFields.length
}

const saveProfile = () => {
	let missingMandatoryFields = validateMandatoryFields()
	if (missingMandatoryFields) return
	profile.bio = sanitizeHTML(profile.bio)
	updateProfile.submit(
		{},
		{
			onSuccess() {
				show.value = false
				reloadProfile.value.reload()
				if (hasLanguageChanged.value) {
					hasLanguageChanged.value = false
					window.location.reload()
				}
			},
			onError(err) {
				toast.error(err.messages?.[0] || err)
			},
		}
	)
}

watch(
	() => profile,
	(newVal) => {
		if (!props.profile.data) return
		let keys = Object.keys(newVal).filter(
			(key) => !['image', 'show_in_rankings'].includes(key)
		)
		for (let key of keys) {
			if (newVal[key] !== props.profile.data[key]) {
				isDirty.value = true
				return
			}
		}
		if (profile.image !== props.profile.data.user_image) {
			isDirty.value = true
			return
		}
		if (
			hasRankingPrivacyField.value &&
			profile.show_in_rankings !== !props.profile.data.hide_from_rankings
		) {
			isDirty.value = true
			return
		}
		isDirty.value = false
	},
	{ deep: true }
)

watch(
	() => props.profile.data,
	(newVal) => {
		if (newVal) {
			profile.first_name = newVal.first_name
			profile.last_name = newVal.last_name
			profile.headline = newVal.headline
			profile.language = newVal.language
			profile.bio = newVal.bio
			profile.open_to = newVal.open_to
			profile.linkedin = newVal.linkedin
			profile.github = newVal.github
			profile.twitter = newVal.twitter
			profile.image = newVal.user_image
			profile.show_in_rankings = !newVal.hide_from_rankings
			isDirty.value = false
		}
	}
)

const hasRankingPrivacyField = computed(() => {
	return props.profile.data?.can_set_ranking_privacy
})

watch(
	() => profile.language,
	() => {
		if (profile.language !== props.profile.data.language) {
			hasLanguageChanged.value = true
		}
	}
)
</script>
