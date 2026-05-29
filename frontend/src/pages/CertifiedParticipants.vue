<template>
	<LayoutHeader>
		<template #left-header>
			<Breadcrumbs :items="breadcrumbs" />
		</template>
		<template #right-header>
			<router-link :to="{ name: 'Courses', query: { certification: true } }">
				<Button variant="solid" theme="indigo">
					<template #prefix>
						<GraduationCap class="size-4 stroke-1.5" />
					</template>
					{{ __('Obtener certificación') }}
				</Button>
			</router-link>
		</template>
	</LayoutHeader>
	<div class="mx-auto flex min-h-0 w-full flex-1 flex-col pb-8">
		<!-- Hero Header -->
		<div class="relative overflow-hidden bg-gradient-to-br from-[#092150] to-[#12336e] px-6 py-12 mb-6 shadow-md md:px-10">
			<div class="absolute inset-0 bg-[url('/assets/lms/images/grid-pattern.svg')] opacity-10"></div>
			<div class="relative z-10 max-w-4xl">
				<h1 class="text-3xl font-black text-white mb-2">{{ __('Miembros Certificados') }}</h1>
				<p class="text-indigo-200 text-base">{{ __('Descubre a los estudiantes que han demostrado su dominio y obtenido certificados oficiales en nuestros cursos.') }}</p>
			</div>
			<div class="absolute -right-10 -top-10 w-48 h-48 bg-indigo-500 rounded-full mix-blend-multiply filter blur-3xl opacity-50"></div>
			<div class="absolute -left-10 -bottom-10 w-48 h-48 bg-blue-500 rounded-full mix-blend-multiply filter blur-3xl opacity-50"></div>
		</div>

		<div class="mb-6 flex flex-col justify-between px-5 md:flex-row md:items-center gap-4">
			<div class="flex items-center gap-2 text-lg font-bold text-slate-800">
				<div class="flex h-8 min-w-[2rem] items-center justify-center rounded-full bg-indigo-100 px-3 text-sm font-black text-indigo-700">
					{{ memberCount }}
				</div>
				{{ __('Resultados') }}
			</div>
			<div
				class="flex flex-col space-y-4 md:flex-row md:items-center md:gap-x-4 md:space-y-0"
			>
				<div class="flex items-center gap-x-4">
					<FormControl
						v-model="nameFilter"
						:placeholder="__('Buscar por nombre')"
						type="text"
						class="min-w-40 lg:w-32 lg:min-w-0 xl:w-40"
						@input="updateParticipants()"
					/>
					<Select
						v-if="categories.data?.length"
						v-model="currentCategory"
						:options="categories.data"
						:placeholder="__('Categoría')"
						@update:modelValue="updateParticipants()"
					/>
				</div>
				<div class="flex items-center gap-x-4">
					<Checkbox
						v-model="openToWork"
						:label="__('Disponible para trabajar')"
						@change="updateParticipants()"
					/>
					<Checkbox
						v-model="hiring"
						:label="__('Contratando')"
						@change="updateParticipants()"
					/>
				</div>
			</div>
		</div>
		<div
			v-if="participants.data?.length"
			class="flex-1 overflow-y-auto px-5 pb-5"
		>
			<div class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-4">
				<div
					v-for="participant in participants.data"
					class="group flex cursor-pointer flex-col rounded-xl border border-slate-200 bg-white p-5 transition-all hover:-translate-y-1 hover:shadow-xl hover:shadow-indigo-500/10 hover:border-indigo-200 relative overflow-hidden"
					@click="
						router.push({
							name: 'ProfileAbout',
							params: { username: participant.username },
						})
					"
				>
					<div class="absolute top-0 right-0 w-24 h-24 bg-gradient-to-br from-indigo-50 to-white rounded-bl-full -z-10 transition-transform group-hover:scale-125"></div>
					<div class="flex items-center gap-x-4">
						<UserAvatar :user="participant" size="2xl" class="border-2 border-white shadow-sm ring-2 ring-indigo-50" />
						<div class="flex flex-col">
							<div class="line-clamp-1 font-bold text-slate-900 text-base group-hover:text-indigo-600 transition-colors">
								{{ participant.full_name }}
							</div>
							<div class="mb-4 line-clamp-1 text-sm font-medium text-slate-500 leading-5">
								{{
									participant.headline ||
									'Se unió ' + dayjs(participant.creation).fromNow()
								}}
							</div>
						</div>
					</div>
					<div class="mt-auto pt-4 border-t border-slate-100 flex items-center justify-between">
						<div class="flex items-center gap-x-1 text-indigo-600 font-semibold text-sm">
							<GraduationCap class="h-4 w-4 stroke-2" />
							<span>
								{{ participant.certificate_count }}
								{{
									participant.certificate_count > 1
										? __('certificados')
										: __('certificado')
								}}
							</span>
						</div>
						<div class="flex items-center gap-x-1 text-slate-400 text-xs font-medium">
							<Calendar class="h-3.5 w-3.5 stroke-1.5" />
							<span>{{
								dayjs(participant.issue_date).format('DD MMM YYYY')
							}}</span>
						</div>
					</div>
				</div>
			</div>
		</div>
		<div v-else class="flex min-h-0 flex-1 items-center justify-center px-5 py-16">
			<div class="text-center max-w-md mx-auto">
				<div class="mx-auto mb-6 flex h-24 w-24 items-center justify-center rounded-full bg-indigo-50 text-indigo-500 shadow-inner">
					<GraduationCap class="h-12 w-12 stroke-1.5" />
				</div>
				<h3 class="text-xl font-bold text-slate-900 mb-2">{{ __('Aún no hay miembros certificados') }}</h3>
				<p class="text-slate-500 mb-6">{{ __('Actualmente no hemos encontrado miembros con certificados. ¡Sigue aprendiendo y sé tú el primero en aparecer aquí!') }}</p>
			</div>
		</div>
		<ListFooter
			v-model="pageLength"
			class="border-t px-3 py-2 sm:px-5"
			:options="{
				rowCount: participants.data?.length,
				totalCount: memberCount,
				pageLengthOptions: [40, 80, 160],
			}"
		>
			<template #right>
				<div class="flex items-center">
					<Button
						v-if="participants.hasNextPage"
						:label="__('Cargar más')"
						@click="participants.next()"
					/>
					<div v-if="participants.hasNextPage" class="mx-3 h-[80%] border-l" />
					<div class="flex items-center gap-1 text-base text-ink-gray-5">
						<div>{{ participants.data?.length || 0 }}</div>
						<div>{{ __('de') }}</div>
						<div>{{ memberCount || 0 }}</div>
					</div>
				</div>
			</template>
		</ListFooter>
	</div>
</template>
<script setup>
import {
	Breadcrumbs,
	Button,
	call,
	createListResource,
	FormControl,
	ListFooter,
	Select,
	usePageMeta,
	Checkbox,
} from 'frappe-ui'
import { computed, inject, onMounted, ref } from 'vue'
import { GraduationCap, Calendar } from 'lucide-vue-next'
import { sessionStore } from '../stores/session'
import { useRouter } from 'vue-router'
import EmptyStateLayout from '@/components/Layouts/EmptyStateLayout.vue'
import UserAvatar from '@/components/UserAvatar.vue'
import LayoutHeader from '@/components/Layouts/LayoutHeader.vue'

const filters = ref({})
const currentCategory = ref('')
const nameFilter = ref('')
const openToWork = ref(false)
const hiring = ref(false)
const { brand } = sessionStore()
const memberCount = ref(0)
const dayjs = inject('$dayjs')
const user = inject('$user')
const router = useRouter()

onMounted(() => {
	if (!user.data) {
		router.push({ name: 'Courses' })
		return
	}
	setFiltersFromQuery()
	updateParticipants()
})

const participants = createListResource({
	doctype: 'LMS Certificate',
	url: 'lms.lms.api.get_certified_participants',
	start: 0,
	pageLength: 40,
	cache: ['certified_participants'],
})

const pageLength = computed({
	get: () => participants.pageLength,
	set: (value) => {
		participants.update({ pageLength: value })
		participants.reload()
	},
})

const getMemberCount = () => {
	call('lms.lms.api.get_count_of_certified_members', {
		filters: filters.value,
	}).then((data) => {
		memberCount.value = data
	})
}

const categories = createListResource({
	doctype: 'LMS Certificate',
	url: 'lms.lms.api.get_certification_categories',
	cache: ['certification_categories'],
	auto: user.data ? true : false,
	transform(data) {
		data.unshift({ label: __(' '), value: ' ' })
		return data
	},
})

const updateParticipants = () => {
	updateFilters()
	getMemberCount()
	setQueryParams()

	participants.update({
		filters: filters.value,
	})
	participants.reload()
}

const updateFilters = () => {
	filters.value = {
		...(currentCategory.value.trim('') && {
			category: currentCategory.value,
		}),
		...(nameFilter.value && {
			member_name: ['like', `%${nameFilter.value}%`],
		}),
		...(openToWork.value && {
			open_to_work: true,
		}),
		...(hiring.value && {
			hiring: true,
		}),
	}
}

const setQueryParams = () => {
	let queries = new URLSearchParams(location.search)
	let filterKeys = {
		category: currentCategory.value,
		name: nameFilter.value,
		'open-to-work': openToWork.value,
		hiring: hiring.value,
	}

	Object.keys(filterKeys).forEach((key) => {
		if (filterKeys[key] && hasValue(filterKeys[key])) {
			queries.set(key, filterKeys[key])
		} else {
			queries.delete(key)
		}
	})
	history.replaceState(
		{},
		'',
		`${location.pathname}${queries.size > 0 ? `?${queries.toString()}` : ''}`
	)
}

const hasValue = (value) => {
	if (typeof value === 'string') {
		return value.trim() !== ''
	}
	return true
}

const setFiltersFromQuery = () => {
	let queries = new URLSearchParams(location.search)
	nameFilter.value = queries.get('name') || ''
	currentCategory.value = queries.get('category') || ''
	openToWork.value = queries.get('open-to-opportunities') === 'true'
	hiring.value = queries.get('hiring') === 'true'
}

const breadcrumbs = computed(() => [
	{
		label: __('Miembros Certificados'),
		route: { name: 'CertifiedParticipants' },
	},
])

usePageMeta(() => {
	return {
		title: __('Miembros Certificados'),
		icon: brand.favicon,
	}
})
</script>
<style>
.headline {
	display: -webkit-box;
	-webkit-line-clamp: 1;
	-webkit-box-orient: vertical;
	text-overflow: ellipsis;
	width: 100%;
	overflow: hidden;
}
</style>
