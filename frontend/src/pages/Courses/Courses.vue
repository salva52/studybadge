<template>
	<!-- ═══════════════════════════════════════════════════════════════
	     PUBLIC VIEW — Course catalog for unauthenticated users
	     ═══════════════════════════════════════════════════════════════ -->
	<div v-if="!isLoggedIn" class="c-public-page">
		<!-- Top Navbar -->
		<nav class="c-navbar">
			<div class="c-navbar-inner">
				<div class="c-navbar-brand">
					<img :src="brand.favicon" alt="StudyBadge" class="w-8 h-8" v-if="brand?.favicon" />
					<span class="c-navbar-name">StudyBadge</span>
				</div>
				<div class="c-navbar-links">
					<a href="/login" class="c-nav-login">{{ __('Iniciar sesión') }}</a>
					<a href="/login#signup" class="c-nav-cta">{{ __('Registrarse') }}</a>
				</div>
				<button class="c-mobile-menu-btn" @click="mobileMenuOpen = !mobileMenuOpen">
					<Menu v-if="!mobileMenuOpen" class="w-6 h-6" />
					<X v-else class="w-6 h-6" />
				</button>
			</div>
			<Transition name="c-menu-slide">
				<div v-if="mobileMenuOpen" class="c-mobile-menu">
					<a href="/login" class="c-mobile-link">{{ __('Iniciar sesión') }}</a>
					<a href="/login#signup" class="c-mobile-cta">{{ __('Registrarse') }}</a>
				</div>
			</Transition>
		</nav>

		<!-- Page Content -->
		<div class="c-catalog">
			<!-- Hero Section Public -->
			<div class="c-hero-banner relative overflow-hidden mb-10">
				<div class="c-hero-glow-1"></div>
				<div class="c-hero-glow-2"></div>
				<div class="c-hero-grid"></div>
				<div class="relative z-10 p-8 sm:p-12 text-center md:text-left flex flex-col md:flex-row items-center gap-8">
					<div class="flex-1">
						<div class="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-blue-500/10 border border-blue-400/20 text-blue-100 text-xs font-bold uppercase tracking-wider mb-4">
							<Sparkles class="size-3.5 text-amber-400" />
							{{ __('Aprende a tu ritmo') }}
						</div>
						<h1 class="text-3xl sm:text-4xl lg:text-5xl font-extrabold tracking-tight text-white leading-tight mb-4">
							{{ __('Explora nuestro catálogo') }}
						</h1>
						<p class="text-base sm:text-lg text-blue-100/80 max-w-2xl leading-relaxed">
							{{ __('Desarrolla nuevas habilidades con nuestros cursos. Todos incluyen actividades prácticas, tutor IA y certificado digital verificable.') }}
						</p>
					</div>
				</div>
			</div>

			<!-- Search and Filters -->
			<div class="c-filters-bar">
				<div class="relative flex-1 md:max-w-md">
					<Search class="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
					<input
						v-model="title"
						type="text"
						class="c-search-input"
						:placeholder="__('Buscar cursos...')"
						@input="updateCourses()"
					/>
				</div>
				<div class="c-chips">
					<button
						class="c-chip"
						:class="{ 'c-chip-active': !currentCategory }"
						@click="currentCategory = null; updateCourses()"
					>
						{{ __('Todos') }}
					</button>
					<button
						v-for="cat in categoryChips"
						:key="cat"
						class="c-chip"
						:class="{ 'c-chip-active': currentCategory === cat }"
						@click="selectCategory(cat)"
					>
						{{ cat }}
					</button>
				</div>
			</div>

			<!-- Courses Grid -->
			<div
				v-if="courses.data?.length"
				class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3 2xl:grid-cols-4 mt-8"
			>
				<router-link
					v-for="course in courses.data"
					:to="{ name: 'CourseDetail', params: { courseName: course.name } }"
				>
					<CourseCard :course="course" />
				</router-link>
			</div>
			<div v-else-if="!courses.list.loading" class="c-empty">
				<div class="c-empty-icon mb-4"><BookOpen class="size-10 text-gray-400" /></div>
				<p class="text-gray-500 font-medium">{{ __('No se encontraron cursos.') }}</p>
			</div>
			<div
				v-if="!courses.list.loading && courses.hasNextPage"
				class="flex justify-center mt-10"
			>
				<button class="c-btn-outline" @click="courses.next()">
					{{ __('Cargar más cursos') }}
				</button>
			</div>

			<!-- Small Registration Banner -->
			<div class="c-register-banner group mt-16">
				<div class="flex flex-col md:flex-row items-center justify-between gap-6 relative z-10">
					<div class="flex items-center gap-4">
						<div class="w-12 h-12 rounded-full bg-amber-100 flex items-center justify-center shrink-0">
							<GraduationCap class="w-6 h-6 text-amber-600" />
						</div>
						<div>
							<h4 class="text-lg font-bold text-gray-900 mb-1">{{ __('¿Listo para empezar?') }}</h4>
							<p class="text-sm text-gray-600">{{ __('Regístrate gratis y accede a todos los cursos con certificado.') }}</p>
						</div>
					</div>
					<a href="/login#signup" class="c-btn-primary shrink-0">{{ __('Crear cuenta gratis') }}</a>
				</div>
			</div>
		</div>

		<!-- Footer -->
		<footer class="c-footer">
			<p>© {{ new Date().getFullYear() }} StudyBadge. {{ __('Todos los derechos reservados.') }}</p>
		</footer>
	</div>

	<!-- ═══════════════════════════════════════════════════════════════
	     AUTHENTICATED VIEW — Dashboard for logged-in users
	     ═══════════════════════════════════════════════════════════════ -->
	<template v-else>
		<LayoutHeader>
			<template #left-header>
				<Breadcrumbs :items="breadcrumbs" />
			</template>
			<template #right-header>
				<Dropdown
					placement="right"
					side="bottom"
					v-if="canCreateCourse()"
					:options="courseMenu"
				>
					<template v-slot="{ open }">
						<Button variant="solid">
							<template #prefix>
								<Plus class="size-4 stroke-1.5" />
							</template>
							{{ __('Crear') }}
							<template #suffix>
								<ChevronDown
									:class="[
										'ms-1 size-4 transform stroke-1.5 transition-transform',
										open ? 'rotate-180' : '',
									]"
								/>
							</template>
						</Button>
					</template>
				</Dropdown>
			</template>
		</LayoutHeader>
		<div class="c-auth-page min-h-screen px-4 sm:px-6 pt-6 pb-12">
			<!-- Hero Section -->
			<div class="c-hero-banner relative overflow-hidden mb-8">
				<div class="c-hero-glow-1"></div>
				<div class="c-hero-glow-2"></div>
				<div class="c-hero-grid"></div>
				<div class="relative z-10 p-8 sm:p-10 flex flex-col md:flex-row items-center gap-8">
					<div class="flex-1">
						<div class="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-blue-500/10 border border-blue-400/20 text-blue-100 text-[11px] font-extrabold uppercase tracking-widest mb-4">
							<Target class="size-3.5 text-amber-400" />
							{{ __('Catálogo de Cursos') }}
						</div>
						<h1 class="text-3xl sm:text-4xl font-extrabold tracking-tight text-white leading-tight mb-3">
							{{ __('¡Descubre tu próximo gran logro!') }}
						</h1>
						<p class="text-base sm:text-lg text-blue-100/80 font-medium leading-relaxed max-w-2xl">
							{{ __('Explora nuestro catálogo, desarrolla nuevas habilidades y lleva tu carrera al siguiente nivel.') }}
						</p>
					</div>
					<div class="hidden md:flex items-center justify-center w-32 h-32 rounded-3xl bg-white/10 backdrop-blur-md border border-white/20 shadow-xl rotate-3 hover:rotate-6 transition-transform">
						<BookOpen class="w-14 h-14 text-white drop-shadow-md" />
					</div>
				</div>
			</div>

			<!-- Filters Bar -->
			<div class="c-filters-panel mb-8">
				<div class="flex flex-col lg:flex-row lg:items-center justify-between gap-5">
					<TabButtons :buttons="courseTabs" v-model="currentTab" class="w-fit" />

					<div class="flex flex-col sm:flex-row items-center gap-3">
						<div class="relative w-full sm:w-64">
							<Search class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400 z-10" />
							<FormControl
								v-model="title"
								:placeholder="__('Buscar curso...')"
								type="text"
								class="w-full c-auth-search"
								@input="updateCourses()"
							/>
						</div>
						<div class="w-full sm:w-48" v-if="categories.length">
							<Select
								v-model="currentCategory"
								:options="categories"
								:placeholder="__('Categoría')"
								@update:modelValue="updateCourses()"
							/>
						</div>
						<Tooltip :text="__('Mostrar solo cursos con certificado')">
							<label class="flex items-center gap-2 cursor-pointer bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 px-3 py-1.5 rounded-lg text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors">
								<input type="checkbox" v-model="certification" @change="updateCourses()" class="rounded border-gray-300 text-blue-600 focus:ring-blue-500" />
								<span>{{ __('Certificado') }}</span>
							</label>
						</Tooltip>
					</div>
				</div>
			</div>

			<!-- Courses Grid -->
			<div
				v-if="courses.data?.length"
				class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 2xl:grid-cols-4"
			>
				<router-link
					v-for="course in courses.data"
					:key="course.name"
					:to="{ name: 'CourseDetail', params: { courseName: course.name } }"
				>
					<CourseCard :course="course" />
				</router-link>
			</div>
			<div v-else-if="!courses.list.loading" class="flex flex-col items-center justify-center py-20 px-4 text-center">
				<div class="w-20 h-20 bg-gray-100 dark:bg-gray-800 rounded-full flex items-center justify-center mb-4">
					<Search class="w-10 h-10 text-gray-400 dark:text-gray-500" />
				</div>
				<h3 class="text-lg font-bold text-gray-900 dark:text-white mb-2">{{ __('No se encontraron cursos') }}</h3>
				<p class="text-gray-500 dark:text-gray-400">{{ __('Intenta con otros filtros de búsqueda.') }}</p>
			</div>
			
			<div
				v-if="!courses.list.loading && courses.hasNextPage"
				class="flex justify-center mt-10"
			>
				<button class="c-btn-outline" @click="courses.next()">
					{{ __('Cargar Más') }}
				</button>
			</div>
		</div>
		<NewCourseModal
			v-if="showCourseModal"
			v-model="showCourseModal"
			:courses="courses"
		/>

		<CourseImportModal
			v-if="showCourseImportModal"
			v-model="showCourseImportModal"
		/>
	</template>
</template>

<script setup>
import {
	Breadcrumbs,
	Button,
	call,
	createListResource,
	Dropdown,
	FormControl,
	Select,
	TabButtons,
	Tooltip,
	usePageMeta,
} from 'frappe-ui'
import { computed, inject, onMounted, ref, watch } from 'vue'
import { ChevronDown, Plus, BookOpen, GraduationCap, Sparkles, Clock, FileCheck, Award, Target, Search, Menu, X } from 'lucide-vue-next'
import { sessionStore } from '@/stores/session'
import { canCreateCourse } from '@/utils'
import CourseCard from '@/components/CourseCard.vue'
import EmptyStateLayout from '@/components/Layouts/EmptyStateLayout.vue'
import LayoutHeader from '@/components/Layouts/LayoutHeader.vue'
import { useRouter } from 'vue-router'
import NewCourseModal from '@/pages/Courses/NewCourseModal.vue'
import CourseImportModal from '@/pages/Courses/CourseImportModal.vue'

const user = inject('$user')
const dayjs = inject('$dayjs')
const start = ref(0)
const pageLength = ref(30)
const categories = ref([
	{
		label: '',
		value: null,
	},
])
const currentCategory = ref(null)
const title = ref('')
const certification = ref(false)
const filters = ref({})
const currentTab = ref('live')
const { brand, isLoggedIn } = sessionStore()
const courseCount = ref(0)
const router = useRouter()
const showCourseModal = ref(false)
const showCourseImportModal = ref(false)
const mobileMenuOpen = ref(false)

const categoryChips = ['IA', 'Negocios', 'Excel', 'Power BI', 'Marketing', 'Ventas', 'Emprendimiento', 'Productividad']

const selectCategory = (cat) => {
	if (currentCategory.value === cat) {
		currentCategory.value = null
	} else {
		currentCategory.value = cat
	}
	updateCourses()
}

onMounted(() => {
	setFiltersFromQuery()
	updateCourses()
	getCourseCount()
})

const setFiltersFromQuery = () => {
	let queries = new URLSearchParams(location.search)
	title.value = queries.get('title') || ''
	currentCategory.value = queries.get('category') || null
	certification.value = queries.get('certification') || false
	if (queries.get('newCourse') == '1') {
		showCourseModal.value = true
	}
}

const courses = createListResource({
	doctype: 'LMS Course',
	url: 'lms.lms.utils.get_courses',
	cache: ['courses', user.data?.name],
	pageLength: pageLength.value,
	start: start.value,
})

const setCategories = (data) => {
	let allCategories = data.map((course) => course.category)
	allCategories = allCategories.filter(
		(category, index) => allCategories.indexOf(category) === index && category
	)
	if (categories.value.length <= allCategories.length) {
		updateCategories(data)
	}
}

const getCourseCount = () => {
	if (!user.data) return
	if (!user.data.is_moderator) return
	call('frappe.client.get_count', {
		doctype: 'LMS Course',
	}).then((data) => {
		courseCount.value = data
	})
}

const updateCourses = () => {
	updateFilters()
	courses.update({
		filters: filters.value,
	})
	courses.reload().then((data) => {
		setCategories(data)
	})
}

const updateFilters = () => {
	updateCategoryFilter()
	updateTitleFilter()
	updateCertificationFilter()
	updateTabFilter()
	updateStudentFilter()
	setQueryParams()
}

const updateCategoryFilter = () => {
	if (currentCategory.value) {
		filters.value['category'] = currentCategory.value
	} else {
		delete filters.value['category']
	}
}

const updateTitleFilter = () => {
	if (title.value) {
		filters.value['title'] = ['like', `%${title.value}%`]
	} else {
		delete filters.value['title']
	}
}

const updateCertificationFilter = () => {
	if (certification.value) {
		filters.value['certification'] = 1
	} else {
		delete filters.value['certification']
	}
}

const updateTabFilter = () => {
	delete filters.value['live']
	delete filters.value['created']
	delete filters.value['published_on']
	delete filters.value['upcoming']

	if (currentTab.value == 'enrolled' && user.data?.is_student) {
		filters.value['enrolled'] = 1
		delete filters.value['published']
	} else {
		delete filters.value['published']
		delete filters.value['enrolled']

		if (currentTab.value == 'live') {
			filters.value['published'] = 1
			filters.value['upcoming'] = 0
			filters.value['live'] = 1
		} else if (currentTab.value == 'upcoming') {
			filters.value['upcoming'] = 1
		} else if (currentTab.value == 'new') {
			filters.value['published'] = 1
			filters.value['published_on'] = [
				'>=',
				dayjs().add(-3, 'month').format('YYYY-MM-DD'),
			]
		} else if (currentTab.value == 'created') {
			filters.value['created'] = 1
		} else if (currentTab.value == 'unpublished') {
			filters.value['published'] = 0
		}
	}
}

const updateStudentFilter = () => {
	if (!user.data || (user.data?.is_student && currentTab.value != 'enrolled')) {
		filters.value['published'] = 1
	}
}

const setQueryParams = () => {
	let queries = new URLSearchParams(location.search)
	let filterKeys = {
		title: title.value,
		category: currentCategory.value,
		certification: certification.value,
	}

	Object.keys(filterKeys).forEach((key) => {
		if (filterKeys[key]) {
			queries.set(key, filterKeys[key])
		} else {
			queries.delete(key)
		}
	})

	let queryString = ''
	if (queries.toString()) {
		queryString = `?${queries.toString()}`
	}

	history.replaceState({}, '', `${location.pathname}${queryString}`)
}

const updateCategories = (data) => {
	data.forEach((course) => {
		if (
			course.category &&
			!categories.value.find((category) => category.value === course.category)
		)
			categories.value.push({
				label: course.category,
				value: course.category,
			})
	})
}

watch(currentTab, () => {
	updateCourses()
})

const courseTabs = computed(() => {
	let tabs = [
		{
			label: __('Activos'),
			value: 'live',
		},
		{
			label: __('Nuevos'),
			value: 'new',
		},
		{
			label: __('Próximos'),
			value: 'upcoming',
		},
	]
	if (
		user.data?.is_moderator ||
		user.data?.is_instructor ||
		user.data?.is_evaluator
	) {
		tabs.push({ label: __('Destacados'), value: 'created' })
		tabs.push({ label: __('Sin Publicar'), value: 'unpublished' })
	} else if (user.data) {
		tabs.push({ label: __('Inscritos'), value: 'enrolled' })
	}
	return tabs
})

const courseMenu = computed(() => {
	return [
		{
			label: __('Nuevo Curso'),
			icon: 'book-open',
			onClick() {
				showCourseModal.value = true
			},
		},
		{
			label: __('Importar con Data Import'),
			icon: 'upload',
			onClick() {
				router.push({
					name: 'NewDataImport',
					params: { doctype: 'LMS Course' },
				})
			},
		},
		{
			label: __('Importar con ZIP'),
			icon: 'folder-plus',
			onClick() {
				showCourseImportModal.value = true
			},
		},
	]
})

const breadcrumbs = computed(() => [
	{
		label: __('Cursos'),
		route: { name: 'Courses' },
	},
])

usePageMeta(() => {
	return {
		title: __('Cursos'),
		icon: brand.favicon,
	}
})
</script>

<style scoped>
/* ═══════════════════════════════════════
   GLOBAL & SHARED
   ═══════════════════════════════════════ */

.c-btn-primary {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	padding: 10px 20px;
	font-size: 14px;
	font-weight: 700;
	color: #fff;
	background: linear-gradient(135deg, #0d6efd, #0b5ed7);
	border-radius: 12px;
	text-decoration: none;
	transition: all 0.2s ease;
	border: none;
	cursor: pointer;
	white-space: nowrap;
	box-shadow: 0 2px 8px rgba(13, 110, 253, 0.25);
}

.c-btn-primary:hover {
	transform: translateY(-1px);
	box-shadow: 0 4px 16px rgba(13, 110, 253, 0.35);
}

.c-btn-outline {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	padding: 10px 24px;
	font-size: 14px;
	font-weight: 700;
	color: #111827;
	background: transparent;
	border: 2px solid rgba(0, 0, 0, 0.1);
	border-radius: 12px;
	cursor: pointer;
	transition: all 0.2s ease;
}

.c-btn-outline:hover {
	background: rgba(0, 0, 0, 0.03);
	border-color: rgba(0, 0, 0, 0.2);
}

:root[data-theme="dark"] .c-btn-outline {
	color: #f3f4f6;
	border-color: rgba(255, 255, 255, 0.15);
}

:root[data-theme="dark"] .c-btn-outline:hover {
	background: rgba(255, 255, 255, 0.05);
	border-color: rgba(255, 255, 255, 0.25);
}

/* ═══════════════════════════════════════
   HERO BANNER (Used in both Public and Auth)
   ═══════════════════════════════════════ */

.c-hero-banner {
	background: linear-gradient(145deg, #061B49 0%, #0b2f73 40%, #0a2259 100%);
	border-radius: 24px;
	box-shadow: 0 4px 24px rgba(6, 27, 73, 0.15), 0 1px 3px rgba(6, 27, 73, 0.08);
}

:root[data-theme="dark"] .c-hero-banner {
	box-shadow: 0 4px 24px rgba(0, 0, 0, 0.4), 0 1px 3px rgba(0, 0, 0, 0.2);
}

.c-hero-glow-1 {
	position: absolute;
	top: -100px;
	right: -60px;
	width: 360px;
	height: 360px;
	background: radial-gradient(circle, rgba(59, 130, 246, 0.25), transparent 70%);
	border-radius: 50%;
	filter: blur(50px);
}

.c-hero-glow-2 {
	position: absolute;
	bottom: -80px;
	left: -40px;
	width: 260px;
	height: 260px;
	background: radial-gradient(circle, rgba(245, 179, 1, 0.15), transparent 70%);
	border-radius: 50%;
	filter: blur(40px);
}

.c-hero-grid {
	position: absolute;
	inset: 0;
	background-image:
		linear-gradient(rgba(255,255,255,0.025) 1px, transparent 1px),
		linear-gradient(90deg, rgba(255,255,255,0.025) 1px, transparent 1px);
	background-size: 40px 40px;
	border-radius: 24px;
}

/* ═══════════════════════════════════════
   AUTHENTICATED STYLES
   ═══════════════════════════════════════ */

.c-auth-page {
	background: var(--sb-bg);
}

.c-filters-panel {
	background: var(--sb-white);
	border: 1px solid rgba(6, 27, 73, 0.05);
	border-radius: 16px;
	padding: 16px;
	box-shadow: 0 1px 3px rgba(6, 27, 73, 0.03);
}

:root[data-theme="dark"] .c-filters-panel {
	border-color: rgba(255, 255, 255, 0.06);
	box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
}

.c-auth-search :deep(input) {
	padding-left: 2.25rem;
}

/* ═══════════════════════════════════════
   PUBLIC PAGE SPECIFIC
   ═══════════════════════════════════════ */

.c-public-page {
	font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
	color: #111827;
	background: #f5f7fb;
	min-height: 100vh;
}

/* Navbar */
.c-navbar {
	position: sticky;
	top: 0;
	z-index: 100;
	background: rgba(255, 255, 255, 0.92);
	backdrop-filter: blur(16px);
	border-bottom: 1px solid rgba(0, 0, 0, 0.06);
}

.c-navbar-inner {
	max-width: 1280px;
	margin: 0 auto;
	padding: 0 24px;
	height: 64px;
	display: flex;
	align-items: center;
	justify-content: space-between;
}

.c-navbar-brand {
	display: flex;
	align-items: center;
	gap: 10px;
}

.c-navbar-name {
	font-size: 20px;
	font-weight: 800;
	color: #061B49;
	letter-spacing: -0.02em;
}

.c-navbar-links {
	display: flex;
	align-items: center;
	gap: 12px;
}

.c-nav-login {
	padding: 8px 16px;
	font-size: 14px;
	font-weight: 700;
	color: #4b5563;
	text-decoration: none;
	border-radius: 10px;
	transition: all 0.2s;
}

.c-nav-login:hover {
	color: #061B49;
	background: rgba(0, 0, 0, 0.04);
}

.c-nav-cta {
	padding: 8px 20px;
	font-size: 14px;
	font-weight: 700;
	color: white;
	background: #111827;
	border-radius: 10px;
	text-decoration: none;
	transition: all 0.2s;
}

.c-nav-cta:hover {
	background: #000;
	transform: translateY(-1px);
	box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.c-mobile-menu-btn {
	display: none;
	background: none;
	border: none;
	cursor: pointer;
	color: #061B49;
}

.c-mobile-menu {
	display: none;
	flex-direction: column;
	padding: 8px 24px 16px;
	background: #fff;
	border-top: 1px solid rgba(0, 0, 0, 0.06);
}

.c-mobile-link {
	display: block;
	padding: 12px 0;
	font-size: 15px;
	font-weight: 600;
	color: #4b5563;
	text-decoration: none;
	border-bottom: 1px solid rgba(0, 0, 0, 0.04);
}

.c-mobile-cta {
	display: block;
	text-align: center;
	margin-top: 12px;
	padding: 12px;
	font-weight: 700;
	color: white;
	background: #111827;
	border-radius: 10px;
	text-decoration: none;
}

@media (max-width: 768px) {
	.c-navbar-links { display: none; }
	.c-mobile-menu-btn { display: block; }
	.c-mobile-menu { display: flex; }
}

/* Catalog Container */
.c-catalog {
	max-width: 1280px;
	margin: 0 auto;
	padding: 32px 24px 64px;
}

/* Search and Filters */
.c-filters-bar {
	display: flex;
	flex-direction: column;
	gap: 16px;
}

@media (min-width: 768px) {
	.c-filters-bar {
		flex-direction: row;
		align-items: center;
		justify-content: space-between;
	}
}

.c-search-input {
	width: 100%;
	padding: 12px 16px 12px 42px;
	font-size: 15px;
	font-weight: 500;
	color: #111827;
	background: #ffffff;
	border: 1px solid rgba(0, 0, 0, 0.1);
	border-radius: 14px;
	outline: none;
	transition: all 0.2s;
	box-shadow: 0 1px 3px rgba(0,0,0,0.02);
}

.c-search-input:focus {
	border-color: #3b82f6;
	box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1);
}

.c-search-input::placeholder {
	color: #9ca3af;
}

/* Chips */
.c-chips {
	display: flex;
	align-items: center;
	gap: 8px;
	flex-wrap: wrap;
}

.c-chip {
	padding: 8px 16px;
	font-size: 13px;
	font-weight: 600;
	color: #4b5563;
	background: #ffffff;
	border: 1px solid rgba(0, 0, 0, 0.1);
	border-radius: 100px;
	cursor: pointer;
	transition: all 0.2s ease;
	box-shadow: 0 1px 2px rgba(0,0,0,0.02);
}

.c-chip:hover {
	border-color: #d1d5db;
	background: #f9fafb;
}

.c-chip-active {
	background: #111827 !important;
	color: #ffffff !important;
	border-color: #111827 !important;
	box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
}

/* Empty State */
.c-empty {
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	padding: 80px 20px;
	text-align: center;
}

.c-empty-icon {
	width: 80px;
	height: 80px;
	border-radius: 24px;
	background: rgba(0,0,0,0.03);
	display: flex;
	align-items: center;
	justify-content: center;
}

/* Registration Banner */
.c-register-banner {
	padding: 32px;
	background: #ffffff;
	border: 1px solid rgba(0, 0, 0, 0.05);
	border-radius: 24px;
	box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
	position: relative;
	overflow: hidden;
}

.c-register-banner::before {
	content: '';
	position: absolute;
	top: 0;
	right: 0;
	bottom: 0;
	width: 30%;
	background: radial-gradient(circle at top right, rgba(245, 179, 1, 0.1), transparent);
	z-index: 0;
}

/* Footer */
.c-footer {
	text-align: center;
	padding: 32px 24px;
	font-size: 14px;
	font-weight: 500;
	color: #6b7280;
	border-top: 1px solid rgba(0, 0, 0, 0.05);
}

/* Transitions */
.c-menu-slide-enter-active,
.c-menu-slide-leave-active {
	transition: all 0.2s ease;
}
.c-menu-slide-enter-from,
.c-menu-slide-leave-to {
	opacity: 0;
	transform: translateY(-8px);
}
</style>
