<template>
	<LayoutHeader>
		<template #left-header>
			<Breadcrumbs :items="breadcrumbs" />
		</template>
		<template #right-header>
			<router-link
				v-if="exercises.data?.length"
				class="hidden md:block"
				:to="{
					name: 'ProgrammingExerciseSubmissions',
				}"
			>
				<Button>
					<template #prefix>
						<ClipboardList class="size-4 stroke-1.5" />
					</template>
					{{ __('Ver todas las entregas') }}
				</Button>
			</router-link>
			<Button
				v-if="!readOnlyMode"
				variant="solid"
				@click="
					() => {
						exerciseID = 'new'
						showForm = true
					}
				"
			>
				<template #prefix>
					<Plus class="size-4 stroke-1.5" />
				</template>
				{{ __('Crear') }}
			</Button>
		</template>
	</LayoutHeader>
	<div class="flex min-h-0 flex-1 flex-col pt-5">
		<!-- Hero Header -->
		<div class="px-5 mb-6 flex items-center gap-4">
			<div class="flex items-center justify-center w-11 h-11 rounded-xl bg-gradient-to-br from-sb-primary/10 to-sb-medium/10 flex-shrink-0">
				<FeatherIcon name="code" class="w-5 h-5 text-sb-primary stroke-2" />
			</div>
			<div>
				<h1 class="text-xl font-bold text-sb-dark">{{ __('Ejercicios de Código') }}</h1>
				<p class="text-sm text-gray-500">{{ __('Desafía y evalúa las habilidades de programación') }}</p>
			</div>
		</div>

		<div
			class="mx-5 mb-5 p-4 bg-white rounded-2xl shadow-sb-soft border border-gray-100 flex flex-col justify-between gap-y-4 sm:flex-row sm:items-center"
		>
			<div class="text-lg font-semibold text-ink-gray-9">
				{{ __('{0} Ejercicios').format(exercises.data?.length) }}
			</div>
			<div class="flex flex-col gap-3 sm:gap-5 md:flex-row">
				<FormControl
					v-model="titleFilter"
					:placeholder="__('Buscar por título')"
					@input="updateList"
				/>
				<Select
					v-model="languageFilter"
					:options="languages"
					:placeholder="__('Lenguaje')"
					@update:modelValue="updateList"
				/>
			</div>
		</div>

		<ListView
			v-if="exercises.data?.length"
			:columns="columns"
			:rows="exercises.data"
			row-key="name"
			:options="{
				showTooltip: false,
				selectable: true,
				onRowClick: (row: any) => {
					if (readOnlyMode) return
					exerciseID = row.name
					showForm = true
				},
			}"
			class="flex-1 overflow-y-auto px-5"
		>
			<ListHeader
				class="mb-2 grid items-center rounded-none border-b bg-surface-white p-2"
			>
				<ListHeaderItem :item="item" v-for="item in columns">
					<template #prefix="{ item }">
						<FeatherIcon :name="item.icon?.toString()" class="h-4 w-4" />
					</template>
				</ListHeaderItem>
			</ListHeader>
			<ListRows>
				<ListRow
					:row="row"
					v-for="row in exercises.data"
					class="hover:bg-surface-gray-1"
				>
					<template #default="{ column, item }">
						<ListRowItem :item="row[column.key]" :align="column.align">
							<div
								v-if="column.key == 'modified'"
								class="text-sm text-ink-gray-5"
							>
								{{ dayjs(row[column.key]).format('MMM D, YYYY') }}
							</div>
							<div v-else>
								{{ row[column.key] }}
							</div>
						</ListRowItem>
					</template>
				</ListRow>
			</ListRows>
			<ListSelectBanner>
				<template #actions="{ unselectAll, selections }">
					<div class="flex gap-2">
						<Button
							variant="ghost"
							@click="showDeleteConfirmation(selections, unselectAll)"
						>
							<FeatherIcon name="trash-2" class="h-4 w-4 stroke-1.5" />
						</Button>
					</div>
				</template>
			</ListSelectBanner>
		</ListView>
		<div v-else class="flex flex-col items-center justify-center py-24 mx-5 bg-white rounded-2xl shadow-sb-soft border border-gray-100 mt-6">
			<div class="w-16 h-16 bg-sb-primary/10 rounded-full flex items-center justify-center mb-4">
				<FeatherIcon name="code" class="w-8 h-8 stroke-1.5 text-sb-primary" />
			</div>
			<p class="text-lg font-semibold text-sb-dark mb-2">
				{{ __('No se encontraron ejercicios de programación') }}
			</p>
			<p class="text-sm w-full md:w-1/2 text-center text-gray-500">
				{{ __('No hay ejercicios en este momento. ¡Crea el primero para empezar a desafiar a tus estudiantes!') }}
			</p>
		</div>
		<ListFooter
			v-model="pageLength"
			class="border-t px-3 py-2 sm:px-5"
			:options="{
				rowCount: exercises.data?.length,
				totalCount: totalExercises.data,
			}"
		>
			<template #right>
				<div class="flex items-center">
					<Button
						v-if="exercises.hasNextPage"
						:label="__('Cargar más')"
						@click="exercises.next()"
					/>
					<div v-if="exercises.hasNextPage" class="mx-3 h-[80%] border-l" />
					<div class="flex items-center gap-1 text-base text-ink-gray-5">
						<div>{{ exercises.data?.length || 0 }}</div>
						<div>{{ __('de') }}</div>
						<div>{{ totalExercises.data || 0 }}</div>
					</div>
				</div>
			</template>
		</ListFooter>
	</div>
	<ProgrammingExerciseForm
		v-model="showForm"
		v-model:exercises="exercises"
		:exerciseID="exerciseID"
		v-model:totalExercises="totalExercises"
	/>
</template>
<script setup lang="ts">
import { computed, getCurrentInstance, inject, onMounted, ref } from 'vue'
import type dayjsType from 'dayjs'
import {
	Breadcrumbs,
	Button,
	call,
	createResource,
	createListResource,
	FeatherIcon,
	FormControl,
	ListView,
	ListHeader,
	ListHeaderItem,
	ListRows,
	ListRow,
	ListRowItem,
	ListFooter,
	ListSelectBanner,
	toast,
	usePageMeta,
	Select,
} from 'frappe-ui'
import { ClipboardList, Plus } from 'lucide-vue-next'
import { sessionStore } from '@/stores/session'
import { useRouter } from 'vue-router'
import ProgrammingExerciseForm from '@/pages/ProgrammingExercises/ProgrammingExerciseForm.vue'
import LayoutHeader from '@/components/Layouts/LayoutHeader.vue'

const readOnlyMode = window.read_only_mode
const { brand } = sessionStore()
const showForm = ref<boolean>(false)
const exerciseID = ref<string>('new')
const user = inject<any>('$user')
const dayjs = inject<typeof dayjsType>('$dayjs')!
const titleFilter = ref<string>('')
const languageFilter = ref<string>('')
const router = useRouter()
const app = getCurrentInstance()
const { $dialog } = app?.appContext.config.globalProperties

onMounted(() => {
	validatePermissions()
})

const validatePermissions = () => {
	if (
		!user.data?.is_instructor &&
		!user.data?.is_moderator &&
		!user.data?.is_evaluator
	) {
		router.push({
			name: 'ProgrammingExerciseSubmissions',
		})
	}
}

const exercises = createListResource({
	doctype: 'LMS Programming Exercise',
	cache: ['programmingExercises'],
	fields: ['name', 'title', 'language', 'problem_statement', 'modified'],
	auto: true,
	orderBy: 'modified desc',
})

const updateList = () => {
	let filters = getFilters()
	exercises.update({
		filters: filters,
	})
	exercises.reload()
	totalExercises.update({
		filters: filters,
	})
	totalExercises.reload()
}

const getFilters = () => {
	let filters: any = {}
	if (titleFilter.value) {
		filters['title'] = ['like', `%${titleFilter.value}%`]
	}
	if (languageFilter.value && languageFilter.value.trim() !== '') {
		filters['language'] = languageFilter.value
	}
	return filters
}

const showDeleteConfirmation = (
	selections: Set<string>,
	unselectAll: () => void
) => {
	$dialog({
		title: __('Confirmar Acción'),
		message: __(
			'Eliminar estos ejercicios los borrará permanentemente del sistema, junto con todas las entregas asociadas. Esta acción es irreversible. ¿Estás seguro de que deseas continuar?'
		),
		actions: [
			{
				label: __('Eliminar'),
				theme: 'red',
				variant: 'solid',
				onClick(close: () => void) {
					deleteExercises(selections, unselectAll)
					close()
				},
			},
		],
	})
}

const deleteExercises = (selections: Set<string>, unselectAll: () => void) => {
	Array.from(selections).forEach(async (exerciseName) => {
		call('lms.lms.api.delete_programming_exercise', {
			exercise: exerciseName,
		})
			.then(() => {
				toast.success(__('Ejercicio eliminado correctamente'))
				updateList()
			})
			.catch((error: any) => {
				toast.error(__(error.message || error))
				console.error('Error deleting exercise:', error)
			})
	})
	unselectAll()
}

const pageLength = computed({
	get: () => exercises.pageLength,
	set: (value) => {
		exercises.update({ pageLength: value })
		exercises.reload()
	},
})

const totalExercises = createResource({
	url: 'frappe.client.get_count',
	params: {
		doctype: 'LMS Programming Exercise',
		filters: getFilters(),
	},
	auto: true,
	cache: ['programming_exercises_count', user.data?.name],
	onError(err: any) {
		toast.error(err.messages?.[0] || err)
		console.error(err)
	},
})

const languages = [
	{ label: ' ', value: ' ' },
	{ label: 'Python', value: 'Python' },
	{ label: 'JavaScript', value: 'JavaScript' },
]

const columns = computed(() => {
	return [
		{
			label: __('Título'),
			key: 'title',
			width: 1,
			icon: 'file-text',
		},
		{
			label: __('Lenguaje'),
			key: 'language',
			width: 1,
			align: 'left',
			icon: 'code',
		},
		{
			label: __('Actualizado el'),
			key: 'modified',
			width: 1,
			icon: 'clock',
			align: 'right',
		},
	]
})

usePageMeta(() => {
	return {
		title: __('Ejercicios de Código'),
		icon: brand.favicon,
	}
})

const breadcrumbs = computed(() => {
	return [
		{
			label: __('Ejercicios de Código'),
			route: { name: 'ProgrammingExercises' },
		},
	]
})
</script>
