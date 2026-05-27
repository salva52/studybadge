<template>
	<!-- ═══════════════════════════════════════════════════════════════
	     PUBLIC VIEW — Course catalog for unauthenticated users
	     ═══════════════════════════════════════════════════════════════ -->
	<div v-if="!isLoggedIn" class="sb-public-page">
		<!-- Top Navbar -->
		<nav class="sb-navbar">
			<div class="sb-navbar-inner">
				<div class="sb-navbar-brand">
					<img :src="brand.favicon" alt="StudyBadge" class="sb-navbar-logo" v-if="brand?.favicon" />
					<span class="sb-navbar-name">StudyBadge</span>
				</div>
				<div class="sb-navbar-links">
					<a href="/login" class="sb-nav-link sb-nav-login">Iniciar sesión</a>
					<a href="/login#signup" class="sb-nav-cta">Registrarse</a>
				</div>
				<button class="sb-mobile-menu-btn" @click="mobileMenuOpen = !mobileMenuOpen">
					<Menu v-if="!mobileMenuOpen" class="w-6 h-6" />
					<X v-else class="w-6 h-6" />
				</button>
			</div>
			<Transition name="sb-menu-slide">
				<div v-if="mobileMenuOpen" class="sb-mobile-menu">
					<a href="/login" class="sb-mobile-link">Iniciar sesión</a>
					<a href="/login#signup" class="sb-mobile-cta">Registrarse</a>
				</div>
			</Transition>
		</nav>

		<!-- Page Content -->
		<div class="sb-catalog">
			<!-- Compact Header -->
			<div class="sb-catalog-header">
				<h1 class="sb-catalog-title">Nuestros Cursos</h1>
				<p class="sb-catalog-desc">Elige un curso, inscríbete y empieza a aprender a tu ritmo. Todos incluyen actividades prácticas y certificado digital.</p>
			</div>

			<!-- Search Bar -->
			<div class="sb-search-bar">
				<Search class="sb-search-icon" />
				<input
					v-model="title"
					type="text"
					class="sb-search-input"
					:placeholder="__('Buscar IA, Excel, ventas, marketing...')"
					@input="updateCourses()"
				/>
			</div>

			<!-- Category Chips -->
			<div class="sb-chips">
				<button
					class="sb-chip"
					:class="{ 'sb-chip-active': !currentCategory }"
					@click="currentCategory = null; updateCourses()"
				>
					Todos
				</button>
				<button
					v-for="cat in categoryChips"
					:key="cat"
					class="sb-chip"
					:class="{ 'sb-chip-active': currentCategory === cat }"
					@click="selectCategory(cat)"
				>
					{{ cat }}
				</button>
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
			<div v-else-if="!courses.list.loading" class="sb-empty">
				<BookOpen class="w-12 h-12 mb-3" style="color: #cbd5e1;" />
				<p style="color: #64748b;">No se encontraron cursos.</p>
			</div>
			<div
				v-if="!courses.list.loading && courses.hasNextPage"
				class="flex justify-center mt-8"
			>
				<button class="sb-btn-outline" @click="courses.next()">
					{{ __('Cargar más cursos') }}
				</button>
			</div>

			<!-- Small Registration Banner -->
			<div class="sb-register-banner">
				<div class="sb-register-text">
					<GraduationCap class="w-5 h-5" style="color: #F5B301;" />
					<span>¿Listo para empezar? Regístrate gratis y accede a todos los cursos con certificado.</span>
				</div>
				<a href="/login#signup" class="sb-btn-primary">Crear cuenta gratis</a>
			</div>
		</div>

		<!-- Footer -->
		<footer class="sb-footer">
			<p>© {{ new Date().getFullYear() }} StudyBadge. Todos los derechos reservados.</p>
		</footer>
	</div>

	<!-- ═══════════════════════════════════════════════════════════════
	     AUTHENTICATED VIEW — Original dashboard for logged-in users
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
		<div class="bg-gray-50 dark:bg-gray-900 min-h-screen p-4 md:p-8 pb-12">
			<!-- Page Header / Hero -->
			<div class="mb-8 relative overflow-hidden rounded-xl bg-gray-900 p-8 md:p-12 text-white shadow-md">
				<div class="absolute top-0 right-0 -mr-20 -mt-20 w-72 h-72 rounded-full bg-white opacity-10 blur-3xl"></div>
				<div class="absolute bottom-0 left-10 w-48 h-48 rounded-full bg-white opacity-10 blur-2xl"></div>
				<div class="relative z-10 flex flex-col md:flex-row items-center gap-6">
					<div class="flex-1">
						<h1 class="text-3xl md:text-5xl font-extrabold mb-4 text-white">{{ __('¡Descubre tu próximo gran logro!') }}</h1>
						<p class="text-blue-100 dark:text-gray-300 text-lg max-w-xl leading-relaxed">{{ __('Explora nuestro catálogo de cursos, desarrolla nuevas habilidades y lleva tu carrera al siguiente nivel.') }}</p>
					</div>
					<div class="hidden md:flex items-center justify-center w-32 h-32 rounded-full bg-white/20 backdrop-blur-md border border-white/30 shadow-xl">
						<BookOpen class="w-16 h-16 text-white" />
					</div>
				</div>
			</div>

			<!-- Filters -->
			<div
				class="mb-8 flex flex-col justify-between space-y-4 lg:flex-row lg:items-center lg:space-y-0 bg-white dark:bg-gray-800 p-3 md:p-4 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700"
			>
				<TabButtons :buttons="courseTabs" v-model="currentTab" class="w-fit" />

				<div
					class="flex flex-col space-y-3 lg:flex-row lg:items-center lg:gap-x-3 lg:space-y-0"
				>
					<div class="grid grid-cols-2 gap-2">
						<FormControl
							v-model="title"
							:placeholder="__('Buscar')"
							type="text"
							class="w-full"
							@input="updateCourses()"
						/>
						<Select
							v-if="categories.length"
							v-model="currentCategory"
							:options="categories"
							:placeholder="__('Categoría')"
							@update:modelValue="updateCourses()"
						/>
					</div>

					<Tooltip :text="__('Mostrar solo cursos con certificado')">
						<FormControl
							type="checkbox"
							v-model="certification"
							:label="__('Certificación')"
							@change="updateCourses()"
						/>
					</Tooltip>
				</div>
			</div>
			<div
				v-if="courses.data?.length"
				class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3 2xl:grid-cols-4"
			>
				<router-link
					v-for="course in courses.data"
					:to="{ name: 'CourseDetail', params: { courseName: course.name } }"
				>
					<CourseCard :course="course" />
				</router-link>
			</div>
			<EmptyStateLayout v-else-if="!courses.list.loading" name="Courses" />
			<div
				v-if="!courses.list.loading && courses.hasNextPage"
				class="flex justify-center mt-5"
			>
				<Button @click="courses.next()">
					{{ __('Cargar Más') }}
				</Button>
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
/* ─── Public Page Shell ─── */
.sb-public-page {
	font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
	color: #1a1a2e;
	background: #F5F7FB;
	min-height: 100vh;
}

/* ─── Navbar ─── */
.sb-navbar {
	position: sticky;
	top: 0;
	z-index: 100;
	background: rgba(255, 255, 255, 0.92);
	backdrop-filter: blur(16px);
	-webkit-backdrop-filter: blur(16px);
	border-bottom: 1px solid rgba(0, 0, 0, 0.06);
}
.sb-navbar-inner {
	max-width: 1280px;
	margin: 0 auto;
	padding: 0 24px;
	height: 64px;
	display: flex;
	align-items: center;
	justify-content: space-between;
}
.sb-navbar-brand {
	display: flex;
	align-items: center;
	gap: 10px;
}
.sb-navbar-logo {
	width: 32px;
	height: 32px;
}
.sb-navbar-name {
	font-size: 20px;
	font-weight: 800;
	color: #061B49;
	letter-spacing: -0.02em;
}
.sb-navbar-links {
	display: flex;
	align-items: center;
	gap: 8px;
}
.sb-nav-link {
	padding: 8px 14px;
	font-size: 14px;
	font-weight: 500;
	color: #64748b;
	text-decoration: none;
	border-radius: 8px;
	transition: all 0.2s;
}
.sb-nav-link:hover {
	color: #061B49;
	background: rgba(0, 0, 0, 0.04);
}
.sb-nav-login {
	font-weight: 600;
	color: #061B49;
}
.sb-nav-cta {
	padding: 8px 20px;
	font-size: 14px;
	font-weight: 600;
	color: white;
	background: #007BFF;
	border-radius: 8px;
	text-decoration: none;
	transition: all 0.2s;
}
.sb-nav-cta:hover {
	background: #0069d9;
	transform: translateY(-1px);
	box-shadow: 0 4px 12px rgba(0, 123, 255, 0.3);
}
.sb-mobile-menu-btn {
	display: none;
	background: none;
	border: none;
	cursor: pointer;
	color: #061B49;
}
.sb-mobile-menu {
	display: none;
	flex-direction: column;
	padding: 8px 24px 16px;
	border-top: 1px solid rgba(0, 0, 0, 0.06);
}
.sb-mobile-link {
	display: block;
	padding: 10px 0;
	font-size: 15px;
	color: #64748b;
	text-decoration: none;
	border-bottom: 1px solid rgba(0, 0, 0, 0.04);
}
.sb-mobile-cta {
	display: block;
	text-align: center;
	margin-top: 12px;
	padding: 12px;
	font-weight: 600;
	color: white;
	background: #007BFF;
	border-radius: 8px;
	text-decoration: none;
}
@media (max-width: 768px) {
	.sb-navbar-links { display: none; }
	.sb-mobile-menu-btn { display: block; }
	.sb-mobile-menu { display: flex; }
}

/* ─── Catalog Layout ─── */
.sb-catalog {
	max-width: 1280px;
	margin: 0 auto;
	padding: 32px 24px 64px;
}

/* ─── Compact Header ─── */
.sb-catalog-header {
	margin-bottom: 32px;
}
.sb-catalog-title {
	font-size: 32px;
	font-weight: 800;
	color: #061B49;
	letter-spacing: -0.02em;
	margin-bottom: 8px;
}
.sb-catalog-desc {
	font-size: 16px;
	color: #64748b;
	line-height: 1.6;
	max-width: 600px;
}

/* ─── Search Bar ─── */
.sb-search-bar {
	position: relative;
	max-width: 480px;
	margin-bottom: 20px;
}
.sb-search-icon {
	position: absolute;
	left: 16px;
	top: 50%;
	transform: translateY(-50%);
	width: 18px;
	height: 18px;
	color: #94a3b8;
}
.sb-search-input {
	width: 100%;
	padding: 12px 16px 12px 46px;
	font-size: 15px;
	color: #1a1a2e;
	background: #ffffff;
	border: 1.5px solid rgba(0, 0, 0, 0.08);
	border-radius: 12px;
	outline: none;
	transition: all 0.2s;
}
.sb-search-input:focus {
	border-color: #007BFF;
	box-shadow: 0 0 0 4px rgba(0, 123, 255, 0.08);
}
.sb-search-input::placeholder {
	color: #94a3b8;
}

/* ─── Category Chips ─── */
.sb-chips {
	display: flex;
	align-items: center;
	gap: 8px;
	flex-wrap: wrap;
	margin-bottom: 8px;
}
.sb-chip {
	padding: 8px 18px;
	font-size: 13px;
	font-weight: 500;
	color: #64748b;
	background: #ffffff;
	border: 1.5px solid rgba(0, 0, 0, 0.08);
	border-radius: 100px;
	cursor: pointer;
	transition: all 0.2s;
}
.sb-chip:hover {
	border-color: #007BFF;
	color: #007BFF;
}
.sb-chip-active {
	background: #007BFF !important;
	color: #ffffff !important;
	border-color: #007BFF !important;
}

/* ─── Empty State ─── */
.sb-empty {
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	padding: 64px 0;
}

/* ─── Buttons ─── */
.sb-btn-primary {
	display: inline-block;
	padding: 12px 24px;
	font-size: 14px;
	font-weight: 600;
	color: #ffffff;
	background: #007BFF;
	border-radius: 10px;
	text-decoration: none;
	transition: all 0.2s;
	border: none;
	cursor: pointer;
	white-space: nowrap;
}
.sb-btn-primary:hover {
	background: #0069d9;
	transform: translateY(-1px);
	box-shadow: 0 4px 16px rgba(0, 123, 255, 0.25);
}
.sb-btn-outline {
	padding: 12px 28px;
	font-size: 14px;
	font-weight: 600;
	color: #007BFF;
	background: #ffffff;
	border: 1.5px solid #007BFF;
	border-radius: 10px;
	cursor: pointer;
	transition: all 0.2s;
}
.sb-btn-outline:hover {
	background: #007BFF;
	color: #ffffff;
}

/* ─── Registration Banner ─── */
.sb-register-banner {
	margin-top: 48px;
	padding: 24px 32px;
	background: #ffffff;
	border: 1.5px solid rgba(0, 123, 255, 0.12);
	border-radius: 14px;
	display: flex;
	align-items: center;
	justify-content: space-between;
	gap: 24px;
	flex-wrap: wrap;
}
.sb-register-text {
	display: flex;
	align-items: center;
	gap: 12px;
	font-size: 15px;
	font-weight: 500;
	color: #1a1a2e;
}

/* ─── Footer ─── */
.sb-footer {
	text-align: center;
	padding: 24px;
	font-size: 13px;
	color: #94a3b8;
	border-top: 1px solid rgba(0, 0, 0, 0.04);
}

/* ─── Transitions ─── */
.sb-menu-slide-enter-active,
.sb-menu-slide-leave-active {
	transition: all 0.2s ease;
}
.sb-menu-slide-enter-from,
.sb-menu-slide-leave-to {
	opacity: 0;
	transform: translateY(-8px);
}
</style>

