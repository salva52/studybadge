<template>
	<LayoutHeader>
		<template #left-header>
			<Breadcrumbs :items="breadcrumbs" />
		</template>
		<template #right-header>
			<router-link :to="{ name: 'Courses', query: { certification: true } }">
				<Button variant="solid" class="cm-btn-primary">
					<template #prefix>
						<GraduationCap class="size-4 stroke-1.5" />
					</template>
					{{ __('Obtener certificación') }}
				</Button>
			</router-link>
		</template>
	</LayoutHeader>

	<div class="cm-page mx-auto flex min-h-0 w-full flex-1 flex-col pb-12">
		<!-- ═══ HERO SECTION ═══ -->
		<div class="cm-hero relative overflow-hidden px-6 py-14 sm:py-20 mb-8">
			<div class="cm-hero-glow-1"></div>
			<div class="cm-hero-glow-2"></div>
			<div class="cm-hero-grid"></div>
			
			<div class="relative z-10 max-w-5xl mx-auto flex flex-col items-center text-center">
				<div class="cm-hero-icon-badge mb-6">
					<Award class="size-10 sm:size-12 text-amber-400 drop-shadow-md" />
				</div>
				<h1 class="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight text-white mb-5 leading-tight">
					{{ __('Miembros') }} <span class="text-transparent bg-clip-text bg-gradient-to-r from-amber-300 via-yellow-200 to-amber-400">{{ __('Certificados') }}</span>
				</h1>
				<p class="text-lg sm:text-xl text-blue-100/90 font-medium max-w-2xl leading-relaxed">
					{{ __('Descubre a los estudiantes que han demostrado su dominio y obtenido certificados oficiales en nuestros cursos.') }}
				</p>
			</div>
		</div>

		<!-- ═══ FILTERS ═══ -->
		<div class="mx-auto max-w-7xl w-full px-5">
			<div class="mb-8 flex flex-col justify-between gap-6 md:flex-row md:items-center">
				<div class="flex items-center gap-3 text-xl font-extrabold cm-text-primary">
					<div class="flex h-10 min-w-[2.5rem] items-center justify-center rounded-xl bg-blue-50 dark:bg-blue-900/30 px-3 text-base font-black text-blue-600 dark:text-blue-400 ring-1 ring-blue-100 dark:ring-blue-800">
						{{ memberCount }}
					</div>
					{{ __('Resultados') }}
				</div>
				<div class="flex flex-col space-y-4 md:flex-row md:items-center md:gap-x-4 md:space-y-0">
					<div class="flex items-center gap-x-4 w-full md:w-auto">
						<FormControl
							v-model="nameFilter"
							:placeholder="__('Buscar por nombre...')"
							type="text"
							class="w-full md:w-48 lg:w-64"
							@input="updateParticipants()"
						/>
						<Select
							v-if="categories.data?.length"
							v-model="currentCategory"
							:options="categories.data"
							:placeholder="__('Categoría')"
							class="w-full md:w-48"
							@update:modelValue="updateParticipants()"
						/>
					</div>
					<div class="flex items-center gap-x-6 bg-white dark:bg-gray-800 px-4 py-2 rounded-xl border cm-border shadow-sm">
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

			<!-- ═══ GRID ═══ -->
			<div v-if="participants.data?.length" class="flex-1 pb-5">
				<div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
					<div
						v-for="participant in participants.data"
						:key="participant.username"
						class="cm-card group relative flex cursor-pointer flex-col p-6"
						@click="
							router.push({
								name: 'ProfileAbout',
								params: { username: participant.username },
							})
						"
					>
						<div class="absolute top-0 right-0 w-32 h-32 bg-gradient-to-br from-amber-500/5 to-transparent rounded-bl-full -z-10 transition-transform duration-500 group-hover:scale-125"></div>
						
						<div class="flex items-start gap-x-4">
							<div class="relative shrink-0">
								<UserAvatar :user="participant" size="2xl" class="border-2 border-white dark:border-gray-800 shadow-md" />
								<div v-if="participant.certificate_count > 0" class="absolute -bottom-1 -right-1 bg-gradient-to-br from-amber-400 to-amber-600 text-white rounded-full p-1 shadow-sm ring-2 ring-white dark:ring-gray-800">
									<Award class="size-3.5" />
								</div>
							</div>
							<div class="flex flex-col min-w-0">
								<div class="line-clamp-1 font-extrabold cm-text-primary text-lg group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors mb-0.5">
									{{ participant.full_name }}
								</div>
								<div class="line-clamp-2 text-sm font-medium cm-text-muted leading-relaxed mb-4">
									{{
										participant.headline ||
										'Se unió ' + dayjs(participant.creation).fromNow()
									}}
								</div>
							</div>
						</div>

						<div class="mt-auto pt-4 border-t cm-border flex items-center justify-between">
							<div class="flex items-center gap-x-1.5 text-amber-600 dark:text-amber-500 font-bold text-sm bg-amber-50 dark:bg-amber-900/20 px-2 py-1 rounded-md">
								<GraduationCap class="size-4" />
								<span>
									{{ participant.certificate_count }}
									{{
										participant.certificate_count > 1
											? __('certs')
											: __('cert')
									}}
								</span>
							</div>
							<div class="flex items-center gap-x-1.5 cm-text-muted text-xs font-semibold">
								<Calendar class="size-3.5" />
								<span>{{
									dayjs(participant.issue_date).format('DD MMM YYYY')
								}}</span>
							</div>
						</div>
					</div>
				</div>
			</div>

			<!-- ═══ EMPTY STATE ═══ -->
			<div v-else class="cm-empty-state">
				<div class="cm-empty-icon mb-5">
					<GraduationCap class="size-12 text-amber-500/70" />
				</div>
				<h3 class="text-2xl font-extrabold cm-text-primary mb-3">{{ __('Aún no hay miembros certificados') }}</h3>
				<p class="cm-text-muted mb-8 max-w-lg mx-auto text-base leading-relaxed">
					{{ __('Actualmente no hemos encontrado miembros con certificados. ¡Sigue aprendiendo y sé tú el primero en aparecer aquí!') }}
				</p>
				<router-link :to="{ name: 'Courses', query: { certification: true } }" class="cm-btn-primary">
					<GraduationCap class="size-5" /> {{ __('Explorar cursos con certificado') }}
				</router-link>
			</div>

			<!-- ═══ PAGINATION ═══ -->
			<ListFooter
				v-model="pageLength"
				class="mt-8 border-t cm-border pt-4"
				:options="{
					rowCount: participants.data?.length,
					totalCount: memberCount,
					pageLengthOptions: [40, 80, 160],
				}"
			>
				<template #right>
					<div class="flex items-center">
						<button
							v-if="participants.hasNextPage"
							class="cm-btn-outline text-sm py-1.5 px-3 mr-3"
							@click="participants.next()"
						>
							{{ __('Cargar más') }}
						</button>
						<div v-if="participants.hasNextPage" class="mx-3 h-5 border-l cm-border" />
						<div class="flex items-center gap-1.5 text-sm font-semibold cm-text-muted bg-gray-50 dark:bg-gray-800/50 px-3 py-1.5 rounded-lg border cm-border">
							<span class="cm-text-primary">{{ participants.data?.length || 0 }}</span>
							<span>{{ __('de') }}</span>
							<span class="cm-text-primary">{{ memberCount || 0 }}</span>
						</div>
					</div>
				</template>
			</ListFooter>
		</div>
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
import { GraduationCap, Calendar, Award } from 'lucide-vue-next'
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
		data.unshift({ label: __(' Todas las categorías'), value: ' ' })
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
		...(currentCategory.value.trim(' ') && {
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

<style scoped>
/* ═══════════════════════════════════════
   TOKENS & THEME
   ═══════════════════════════════════════ */

.cm-page {
	background: var(--sb-bg);
}

.cm-border { border-color: rgba(6, 27, 73, 0.08); }
:root[data-theme="dark"] .cm-border { border-color: rgba(255, 255, 255, 0.08); }

.cm-text-primary { color: #111827; }
.cm-text-muted { color: #6b7280; }
:root[data-theme="dark"] .cm-text-primary { color: #f3f4f6; }
:root[data-theme="dark"] .cm-text-muted { color: #9ca3af; }

/* ═══════════════════════════════════════
   HERO
   ═══════════════════════════════════════ */

.cm-hero {
	background: linear-gradient(135deg, #061B49 0%, #0b2f73 40%, #0a2259 100%);
}

.cm-hero-glow-1 {
	position: absolute;
	top: -120px;
	right: -80px;
	width: 400px;
	height: 400px;
	background: radial-gradient(circle, rgba(59, 130, 246, 0.25), transparent 70%);
	border-radius: 50%;
	filter: blur(60px);
}

.cm-hero-glow-2 {
	position: absolute;
	bottom: -100px;
	left: -60px;
	width: 300px;
	height: 300px;
	background: radial-gradient(circle, rgba(245, 179, 1, 0.15), transparent 70%);
	border-radius: 50%;
	filter: blur(50px);
}

.cm-hero-grid {
	position: absolute;
	inset: 0;
	background-image:
		linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
		linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
	background-size: 48px 48px;
}

.cm-hero-icon-badge {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	padding: 1.25rem;
	border-radius: 1.25rem;
	background: rgba(255, 255, 255, 0.08);
	border: 1px solid rgba(255, 255, 255, 0.12);
	backdrop-filter: blur(12px);
	box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
}

/* ═══════════════════════════════════════
   CARDS
   ═══════════════════════════════════════ */

.cm-card {
	background: var(--sb-white);
	border: 1px solid rgba(6, 27, 73, 0.06);
	border-radius: 24px;
	box-shadow: 0 4px 6px -1px rgba(6, 27, 73, 0.03), 0 2px 4px -2px rgba(6, 27, 73, 0.02);
	transition: all 0.25s ease;
	z-index: 1;
}

.cm-card:hover {
	transform: translateY(-3px);
	box-shadow: 0 12px 24px -4px rgba(6, 27, 73, 0.08), 0 8px 12px -6px rgba(6, 27, 73, 0.06);
	border-color: rgba(13, 110, 253, 0.2);
}

:root[data-theme="dark"] .cm-card {
	border-color: rgba(255, 255, 255, 0.06);
	box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2), 0 2px 4px -2px rgba(0, 0, 0, 0.1);
}

:root[data-theme="dark"] .cm-card:hover {
	border-color: rgba(13, 110, 253, 0.4);
	box-shadow: 0 12px 24px -4px rgba(0, 0, 0, 0.4), 0 8px 12px -6px rgba(0, 0, 0, 0.2);
}

/* ═══════════════════════════════════════
   EMPTY STATE
   ═══════════════════════════════════════ */

.cm-empty-state {
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	padding: 60px 20px;
	text-align: center;
	background: var(--sb-white);
	border: 2px dashed rgba(6, 27, 73, 0.1);
	border-radius: 24px;
	margin-top: 20px;
}

:root[data-theme="dark"] .cm-empty-state {
	border-color: rgba(255, 255, 255, 0.1);
}

.cm-empty-icon {
	display: flex;
	align-items: center;
	justify-content: center;
	width: 96px;
	height: 96px;
	border-radius: 28px;
	background: rgba(245, 158, 11, 0.1);
}

:root[data-theme="dark"] .cm-empty-icon {
	background: rgba(245, 158, 11, 0.15);
}

/* ═══════════════════════════════════════
   BUTTONS
   ═══════════════════════════════════════ */

.cm-btn-primary {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	gap: 8px;
	padding: 10px 20px;
	border-radius: 12px;
	font-size: 14px;
	font-weight: 700;
	color: #fff !important;
	background: linear-gradient(135deg, #0d6efd, #0b5ed7) !important;
	border: none !important;
	cursor: pointer;
	transition: all 0.2s ease;
	box-shadow: 0 2px 8px rgba(13, 110, 253, 0.25) !important;
	text-decoration: none;
}

.cm-btn-primary:hover {
	transform: translateY(-1px);
	box-shadow: 0 4px 16px rgba(13, 110, 253, 0.35) !important;
}

.cm-btn-outline {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	gap: 8px;
	border-radius: 12px;
	font-weight: 700;
	color: #374151;
	background: transparent;
	border: 2px solid rgba(0, 0, 0, 0.08);
	cursor: pointer;
	transition: all 0.15s ease;
}

.cm-btn-outline:hover {
	background: rgba(0, 0, 0, 0.03);
	border-color: rgba(0, 0, 0, 0.15);
}

:root[data-theme="dark"] .cm-btn-outline {
	color: #d1d5db;
	border-color: rgba(255, 255, 255, 0.1);
}

:root[data-theme="dark"] .cm-btn-outline:hover {
	background: rgba(255, 255, 255, 0.05);
	border-color: rgba(255, 255, 255, 0.18);
}
</style>
