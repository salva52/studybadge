<template>
	<div class="min-h-screen">
		<!-- Search Header -->
		<div class="px-6 pt-10 pb-6 max-w-2xl mx-auto">
			<div class="text-center mb-8">
				<div class="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-gradient-to-br from-sb-primary/10 to-sb-medium/10 mb-4">
					<Search class="w-7 h-7 text-sb-primary" />
				</div>
				<h1 class="text-2xl font-bold text-sb-dark mb-2">{{ __('Buscar') }}</h1>
				<p class="text-sm text-gray-500">{{ __('Encuentra cursos, grupos, empleos y más') }}</p>
			</div>

			<!-- Search Input -->
			<div class="relative">
				<div class="flex items-center bg-white rounded-xl shadow-sb-card border border-gray-100 px-4 py-1 transition-all duration-300 focus-within:shadow-sb-card-hover focus-within:border-sb-primary/30">
					<Search class="w-5 h-5 text-gray-400 flex-shrink-0" />
					<input
						ref="searchInput"
						type="text"
						class="flex-1 bg-transparent border-none outline-none px-3 py-3 text-base text-sb-dark placeholder-gray-400 font-inter"
						:placeholder="__('Escribe una palabra clave y presiona Enter...')"
						autocomplete="off"
						:value="query"
						@input="updateQuery($event.target.value)"
						@keydown.enter="() => submit()"
					/>
					<button
						v-if="query"
						@click="clearSearch"
						class="p-1.5 rounded-lg hover:bg-gray-100 transition-colors duration-200"
					>
						<X class="w-4 h-4 text-gray-400" />
					</button>
				</div>
			</div>

			<!-- Status Text -->
			<div class="mt-4 text-center">
				<div v-if="query && searchResults.length" class="text-sm text-gray-500">
					<span class="font-semibold text-sb-primary">{{ searchResults.length }}</span>
					{{ searchResults.length === 1 ? __('resultado encontrado') : __('resultados encontrados') }}
				</div>
				<div v-else-if="queryChanged" class="text-sm text-gray-400 flex items-center justify-center gap-1.5">
					<span>{{ __('Presiona Enter para buscar') }}</span>
					<kbd class="px-1.5 py-0.5 text-xs bg-gray-100 text-gray-500 rounded font-mono">↵</kbd>
				</div>
				<div v-else-if="query && !searchResults.length" class="text-sm text-gray-400">
					{{ __('No se encontraron resultados') }}
				</div>
			</div>
		</div>

		<!-- Results -->
		<div class="max-w-2xl mx-auto px-6 pb-10">
			<div v-if="searchResults.length" class="space-y-3">
				<div
					v-for="(result, index) in searchResults"
					:key="index"
					@click="navigate(result)"
					class="group bg-white rounded-xl p-4 cursor-pointer border border-gray-100 transition-all duration-300 hover:shadow-sb-card-hover hover:border-sb-primary/20 hover:-translate-y-0.5"
				>
					<div class="flex gap-x-3.5 items-start">
						<Tooltip :text="result.author_info ? result.author_info.full_name : ''">
							<Avatar
								:label="(result.author_info ? result.author_info.full_name : '') || 'StudyBadge'"
								:image="result.author_info ? result.author_info.user_image : null"
								size="lg"
								class="flex-shrink-0 ring-2 ring-white shadow-sm"
							/>
						</Tooltip>
						<div class="flex-1 min-w-0">
							<div class="flex items-center gap-2 mb-1">
								<div
									class="font-semibold text-sb-dark group-hover:text-sb-primary transition-colors duration-200 truncate"
									v-html="result.title"
								></div>
								<span class="flex-shrink-0 px-2 py-0.5 text-xs font-medium rounded-full bg-sb-primary/8 text-sb-primary">
									{{ getDocTypeTitle(result.doctype) }}
								</span>
							</div>
							<div
								v-if="result.content"
								class="text-sm text-gray-500 leading-relaxed line-clamp-2"
								v-html="result.content"
							></div>
							<div
								v-if="result.published_on || result.start_date || result.creation || result.modified"
								class="text-xs text-gray-400 mt-1.5"
							>
								{{ dayjs(result.published_on || result.start_date || result.creation || result.modified).format('DD MMM YYYY') }}
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>
<script setup lang="ts">
import {
	Avatar,
	createResource,
	debounce,
	Tooltip,
	usePageMeta,
} from 'frappe-ui'
import { inject, onMounted, ref, watch } from 'vue'
import { Search, X } from 'lucide-vue-next'
import { sessionStore } from '@/stores/session'
import { useRouter, useRoute } from 'vue-router'

const query = ref('')
const searchInput = ref<HTMLInputElement | null>(null)
const searchResults = ref<Array<any>>([])
const { brand } = sessionStore()
const router = useRouter()
const route = useRoute()
const queryChanged = ref(false)
const dayjs = inject<any>('$dayjs')

onMounted(() => {
	if (router.currentRoute.value.query.q) {
		query.value = router.currentRoute.value.query.q as string
		submit()
	}
})

const updateQuery = (value: string) => {
	query.value = value
	router.replace({ query: value ? { q: value } : {} })
}

const submit = debounce(() => {
	if (query.value.length > 2) {
		search.reload()
	}
}, 500)

const search = createResource({
	url: 'lms.command_palette.search_sqlite',
	makeParams: () => ({
		query: query.value,
	}),
	onSuccess() {
		generateSearchResults()
	},
})

const generateSearchResults = () => {
	searchResults.value = []
	if (search.data) {
		queryChanged.value = false
		search.data.forEach((group: any) => {
			group.items.forEach((item: any) => {
				searchResults.value.push(item)
			})
		})
		sortResults()
	}
}

const sortResults = () => {
	searchResults.value.sort((a, b) => {
		const dateA = new Date(
			a.published_on || a.start_date || a.creation || a.modified
		).getTime()
		const dateB = new Date(
			b.published_on || b.start_date || b.creation || b.modified
		).getTime()
		return dateB - dateA
	})
}

const navigate = (result: any) => {
	if (result.doctype == 'LMS Course') {
		router.push({
			name: 'CourseDetail',
			params: {
				courseName: result.name,
			},
		})
	} else if (result.doctype == 'LMS Batch') {
		router.push({
			name: 'BatchDetail',
			params: {
				batchName: result.name,
			},
		})
	} else if (result.doctype == 'Job Opportunity') {
		router.push({
			name: 'JobDetail',
			params: {
				job: result.name,
			},
		})
	}
}

watch(query, () => {
	if (query.value && query.value != search.params?.query) {
		queryChanged.value = true
	} else if (!query.value) {
		queryChanged.value = false
		searchResults.value = []
	}
})

watch(
	() => route.query.q,
	(newQ) => {
		if (newQ && newQ !== query.value) {
			query.value = newQ as string
			submit()
		}
	}
)

const getDocTypeTitle = (doctype: string) => {
	if (doctype === 'LMS Course') {
		return __('Curso')
	} else if (doctype === 'LMS Batch') {
		return __('Grupo')
	} else if (doctype === 'Job Opportunity') {
		return __('Empleo')
	} else {
		return doctype
	}
}

const clearSearch = () => {
	query.value = ''
	updateQuery('')
}

usePageMeta(() => {
	return {
		title: __('Buscar'),
		icon: brand.favicon,
	}
})
</script>
