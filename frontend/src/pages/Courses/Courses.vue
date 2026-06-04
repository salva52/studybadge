<template>
	<div v-if="!isLoggedIn" class="courses-public-page">
		<nav class="courses-navbar">
			<div class="courses-navbar-inner">
				<a href="/" class="courses-brand">
					<img
						v-if="brand?.favicon"
						:src="brand.favicon"
						alt="StudyBadge"
						class="courses-brand-logo"
					/>
					<span class="courses-brand-name">StudyBadge</span>
				</a>

				<div class="courses-navbar-actions">
					<a href="/login" class="courses-nav-login">
						{{ __('Iniciar sesión') }}
					</a>

					<a href="/login#signup" class="courses-nav-cta">
						{{ __('Registrarse') }}
					</a>
				</div>

				<button
					class="courses-mobile-menu-button"
					type="button"
					:aria-expanded="mobileMenuOpen"
					aria-label="Abrir menú"
					@click="mobileMenuOpen = !mobileMenuOpen"
				>
					<Menu v-if="!mobileMenuOpen" class="size-5" />
					<X v-else class="size-5" />
				</button>
			</div>

			<Transition name="courses-menu-slide">
				<div v-if="mobileMenuOpen" class="courses-mobile-menu">
					<a href="/login" class="courses-mobile-link">
						{{ __('Iniciar sesión') }}
					</a>

					<a href="/login#signup" class="courses-mobile-cta">
						{{ __('Crear cuenta gratis') }}
					</a>
				</div>
			</Transition>
		</nav>

		<main class="courses-public-shell">
			<section class="courses-hero">
				<div class="courses-hero-content">
					<div class="courses-hero-copy">
						<div class="courses-eyebrow">
							<Sparkles class="size-4" />
							{{ __('Cursos con IA, práctica y certificados') }}
						</div>

						<h1 class="courses-hero-title">
							{{ __('Explora cursos para aprender habilidades digitales') }}
						</h1>

						<p class="courses-hero-subtitle">
							{{ __('Aprende IA, negocios, marketing, ventas y productividad con cursos cortos, TutorIA, actividades prácticas y certificados verificables.') }}
						</p>

						<div class="courses-hero-actions">
							<a href="/login#signup" class="courses-btn-light">
								{{ __('Crear cuenta gratis') }}
							</a>

							<a href="#catalogo" class="courses-btn-ghost">
								{{ __('Ver cursos') }}
							</a>
						</div>
					</div>

					<div class="courses-hero-card">
						<div class="courses-hero-card-top">
							<div>
								<p>{{ __('Catálogo StudyBadge') }}</p>
								<strong>{{ __('Aprende, practica y certifica') }}</strong>
							</div>

							<span class="courses-hero-badge">
								<Award class="size-4" />
								{{ __('Certificados') }}
							</span>
						</div>

						<div class="courses-hero-feature">
							<div class="courses-hero-feature-icon">
								<BookOpen class="size-5" />
							</div>

							<div>
								<strong>{{ __('Cursos cortos') }}</strong>
								<span>{{ __('Lecciones claras para avanzar sin perderte.') }}</span>
							</div>
						</div>

						<div class="courses-hero-feature">
							<div class="courses-hero-feature-icon gold">
								<Sparkles class="size-5" />
							</div>

							<div>
								<strong>{{ __('TutorIA') }}</strong>
								<span>{{ __('Pregunta, practica y pide ejemplos paso a paso.') }}</span>
							</div>
						</div>

						<div class="courses-hero-feature">
							<div class="courses-hero-feature-icon green">
								<CheckCircle2 class="size-5" />
							</div>

							<div>
								<strong>{{ __('Progreso verificable') }}</strong>
								<span>{{ __('Completa cursos y demuestra lo aprendido.') }}</span>
							</div>
						</div>
					</div>
				</div>
			</section>

			<section id="catalogo" class="courses-toolbar">
				<div class="courses-search-wrap">
					<Search class="courses-search-icon size-5" />

					<input
						v-model="title"
						type="text"
						class="courses-search-input"
						:placeholder="__('Buscar cursos, IA, ventas, marketing...')"
						@input="updateCourses()"
					/>
				</div>

				<div class="courses-chip-scroll">
					<button
						class="courses-chip"
						:class="{ active: !currentCategory }"
						type="button"
						@click="currentCategory = null; updateCourses()"
					>
						{{ __('Todos') }}
					</button>

					<button
						v-for="cat in categoryChips"
						:key="cat"
						class="courses-chip"
						:class="{ active: currentCategory === cat }"
						type="button"
						@click="selectCategory(cat)"
					>
						{{ cat }}
					</button>
				</div>
			</section>

			<section>
				<div v-if="courses.data?.length" class="courses-grid">
					<router-link
						v-for="course in courses.data"
						:key="course.name"
						:to="{ name: 'CourseDetail', params: { courseName: course.name } }"
						class="courses-card-link"
					>
						<CourseCard :course="course" />
					</router-link>
				</div>

				<div v-else-if="!courses.list.loading" class="courses-empty">
					<div class="courses-empty-icon">
						<BookOpen class="size-10" />
					</div>

					<h3>{{ __('No se encontraron cursos') }}</h3>
					<p>{{ __('Prueba con otra búsqueda o selecciona otra categoría.') }}</p>
				</div>

				<div v-else-if="courses.list.loading" class="courses-grid skeleton-grid">
					<div v-for="i in 6" :key="i" class="courses-card-skeleton">
						<div class="skeleton-img"></div>
						<div class="skeleton-content">
							<div class="skeleton-line title"></div>
							<div class="skeleton-line subtitle"></div>
							<div class="skeleton-line short"></div>
						</div>
					</div>
				</div>

				<div
					v-if="!courses.list.loading && courses.hasNextPage"
					class="courses-load-more"
				>
					<button class="courses-btn-outline" type="button" @click="courses.next()">
						{{ __('Cargar más cursos') }}
					</button>
				</div>
			</section>

			<section class="courses-register-banner">
				<div class="courses-register-left">
					<div class="courses-register-icon">
						<GraduationCap class="size-6" />
					</div>

					<div>
						<h4>{{ __('¿Listo para empezar?') }}</h4>
						<p>
							{{ __('Crea tu cuenta gratis, guarda tu progreso y accede a herramientas de aprendizaje con IA.') }}
						</p>
					</div>
				</div>

				<a href="/login#signup" class="courses-btn-primary">
					{{ __('Crear cuenta gratis') }}
				</a>
			</section>
		</main>

		<footer class="courses-footer">
			<p>
				© {{ new Date().getFullYear() }} StudyBadge.
				{{ __('Todos los derechos reservados.') }}
			</p>
		</footer>
	</div>

	<template v-else>
		<LayoutHeader>
			<template #left-header>
				<Breadcrumbs :items="breadcrumbs" />
			</template>

			<template #right-header>
				<Dropdown
					v-if="canCreateCourse()"
					placement="right"
					side="bottom"
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

		<div class="courses-auth-page">
			<section class="courses-auth-hero">
				<div class="courses-auth-hero-content">
					<div>
						<div class="courses-eyebrow">
							<Target class="size-4" />
							{{ __('Catálogo de cursos') }}
						</div>

						<h1 class="courses-auth-title">
							{{ __('Descubre tu próximo gran logro') }}
						</h1>

						<p class="courses-auth-subtitle">
							{{ __('Explora cursos prácticos, desarrolla nuevas habilidades y avanza con TutorIA, quizzes y certificados verificables.') }}
						</p>

						<div class="courses-auth-stats">
							<div class="courses-auth-stat">
								<BookOpen class="size-4" />
								<span>
									{{ courses.data?.length || 0 }}
									{{ __('cursos visibles') }}
								</span>
							</div>

							<div class="courses-auth-stat">
								<Award class="size-4" />
								<span>{{ __('Certificados disponibles') }}</span>
							</div>
						</div>
					</div>

					<div class="courses-auth-hero-icon">
						<BookOpen class="size-12" />
					</div>
				</div>
			</section>

			<section class="courses-auth-filters">
				<div class="courses-tabs-wrap">
					<TabButtons
						:buttons="courseTabs"
						v-model="currentTab"
						class="courses-tabs"
					/>
				</div>

				<div class="courses-auth-filter-grid">
					<div class="courses-auth-search">
						<Search class="courses-auth-search-icon size-4" />

						<FormControl
							v-model="title"
							:placeholder="__('Buscar curso...')"
							type="text"
							class="w-full courses-auth-search-control"
							@input="updateCourses()"
						/>
					</div>

					<div v-if="categories.length" class="courses-select-wrap">
						<Select
							v-model="currentCategory"
							:options="categories"
							:placeholder="__('Categoría')"
							@update:modelValue="updateCourses()"
						/>
					</div>

					<Tooltip :text="__('Mostrar solo cursos con certificado')">
						<label
							class="courses-cert-toggle"
							:class="{ active: certification }"
						>
							<input
								v-model="certification"
								type="checkbox"
								@change="updateCourses()"
							/>

							<span class="courses-cert-box">
								<CheckCircle2 class="size-4" />
							</span>

							<span>{{ __('Certificado') }}</span>
						</label>
					</Tooltip>
				</div>
			</section>

			<section>
				<div v-if="courses.data?.length" class="courses-grid auth">
					<router-link
						v-for="course in courses.data"
						:key="course.name"
						:to="{ name: 'CourseDetail', params: { courseName: course.name } }"
						class="courses-card-link"
					>
						<CourseCard :course="course" />
					</router-link>
				</div>

				<div v-else-if="!courses.list.loading" class="courses-empty auth">
					<div class="courses-empty-icon">
						<Search class="size-10" />
					</div>

					<h3>{{ __('No se encontraron cursos') }}</h3>
					<p>{{ __('Intenta con otros filtros de búsqueda.') }}</p>

					<button
						class="courses-btn-outline"
						type="button"
						@click="clearFilters"
					>
						{{ __('Limpiar filtros') }}
					</button>
				</div>

				<div v-else-if="courses.list.loading" class="courses-grid auth skeleton-grid">
					<div v-for="i in 6" :key="i" class="courses-card-skeleton">
						<div class="skeleton-img"></div>
						<div class="skeleton-content">
							<div class="skeleton-line title"></div>
							<div class="skeleton-line subtitle"></div>
							<div class="skeleton-line short"></div>
						</div>
					</div>
				</div>

				<div
					v-if="!courses.list.loading && courses.hasNextPage"
					class="courses-load-more"
				>
					<button class="courses-btn-outline" type="button" @click="courses.next()">
						{{ __('Cargar más') }}
					</button>
				</div>
			</section>
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
import {
	Award,
	BookOpen,
	CheckCircle2,
	ChevronDown,
	GraduationCap,
	Menu,
	Plus,
	Search,
	Sparkles,
	Target,
	X,
} from 'lucide-vue-next'
import { sessionStore } from '@/stores/session'
import { canCreateCourse } from '@/utils'
import CourseCard from '@/components/CourseCard.vue'
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
		label: __('Todas las categorías'),
		value: null,
	},
])

const currentCategory = ref(null)
const title = ref('')
const certification = ref(false)
const filters = ref({})
const currentTab = ref('live')
const { brand, isLoggedIn } = sessionStore()
const router = useRouter()
const showCourseModal = ref(false)
const showCourseImportModal = ref(false)
const mobileMenuOpen = ref(false)

const categoryChips = [
	'IA',
	'Negocios',
	'Excel',
	'Power BI',
	'Marketing',
	'Ventas',
	'Emprendimiento',
	'Productividad',
]

const courses = createListResource({
	doctype: 'LMS Course',
	url: 'lms.lms.utils.get_courses',
	cache: ['courses', user.data?.name],
	pageLength: pageLength.value,
	start: start.value,
})

onMounted(() => {
	setFiltersFromQuery()
	updateCourses()
})

const setFiltersFromQuery = () => {
	const queries = new URLSearchParams(location.search)

	title.value = queries.get('title') || ''
	currentCategory.value = queries.get('category') || null
	certification.value =
		queries.get('certification') === 'true' ||
		queries.get('certification') === '1'

	if (queries.get('newCourse') === '1') {
		showCourseModal.value = true
	}
}

const selectCategory = (cat) => {
	currentCategory.value = currentCategory.value === cat ? null : cat
	updateCourses()
}

const clearFilters = () => {
	title.value = ''
	currentCategory.value = null
	certification.value = false
	updateCourses()
}

const updateCourses = () => {
	updateFilters()

	courses.update({
		filters: filters.value,
	})

	courses.reload().then((data) => {
		setCategories(data || [])
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
		filters.value.category = currentCategory.value
	} else {
		delete filters.value.category
	}
}

const updateTitleFilter = () => {
	if (title.value) {
		filters.value.title = ['like', `%${title.value}%`]
	} else {
		delete filters.value.title
	}
}

const updateCertificationFilter = () => {
	if (certification.value) {
		filters.value.certification = 1
	} else {
		delete filters.value.certification
	}
}

const updateTabFilter = () => {
	delete filters.value.live
	delete filters.value.created
	delete filters.value.published_on
	delete filters.value.upcoming

	if (currentTab.value === 'enrolled' && user.data?.is_student) {
		filters.value.enrolled = 1
		delete filters.value.published
		return
	}

	delete filters.value.published
	delete filters.value.enrolled

	if (currentTab.value === 'live') {
		filters.value.published = 1
		filters.value.upcoming = 0
		filters.value.live = 1
	} else if (currentTab.value === 'upcoming') {
		filters.value.upcoming = 1
	} else if (currentTab.value === 'new') {
		filters.value.published = 1
		filters.value.published_on = [
			'>=',
			dayjs().add(-3, 'month').format('YYYY-MM-DD'),
		]
	} else if (currentTab.value === 'created') {
		filters.value.created = 1
	} else if (currentTab.value === 'unpublished') {
		filters.value.published = 0
	}
}

const updateStudentFilter = () => {
	if (!user.data || (user.data?.is_student && currentTab.value !== 'enrolled')) {
		filters.value.published = 1
	}
}

const setQueryParams = () => {
	const queries = new URLSearchParams(location.search)

	const filterKeys = {
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

	const queryString = queries.toString() ? `?${queries.toString()}` : ''
	history.replaceState({}, '', `${location.pathname}${queryString}`)
}

const setCategories = (data) => {
	const allCategories = data
		.map((course) => course.category)
		.filter((category, index, arr) => category && arr.indexOf(category) === index)

	allCategories.forEach((category) => {
		if (!categories.value.find((item) => item.value === category)) {
			categories.value.push({
				label: category,
				value: category,
			})
		}
	})
}

watch(currentTab, () => {
	updateCourses()
})

const courseTabs = computed(() => {
	const tabs = [
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
		tabs.push({ label: __('Sin publicar'), value: 'unpublished' })
	} else if (user.data) {
		tabs.push({ label: __('Inscritos'), value: 'enrolled' })
	}

	return tabs
})

const courseMenu = computed(() => [
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
])

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
.courses-public-page,
.courses-auth-page {
	--courses-primary: #0a2251;
	--courses-primary-hover: #12356f;
	--courses-primary-soft: #eaf1fb;
	--courses-primary-soft-2: #f4f8fd;
	--courses-gold: #f5b301;
	--courses-gold-soft: #fff7db;
	--courses-green: #16a34a;
	--courses-green-soft: #ecfdf3;
	--courses-bg: #f5f8fc;
	--courses-card: #ffffff;
	--courses-text: #0f172a;
	--courses-muted: #475569;
	--courses-soft: #64748b;
	--courses-border: #d7e2f0;
	--courses-border-strong: #b9cbe3;
	--courses-shadow-sm: 0 8px 22px rgba(10, 34, 81, 0.08);
	--courses-shadow-md: 0 18px 45px rgba(10, 34, 81, 0.13);
	--courses-shadow-lg: 0 28px 70px rgba(10, 34, 81, 0.2);

	background: var(--courses-bg);
	color: var(--courses-text);
}

:global(:root[data-theme='dark']) .courses-public-page,
:global(:root[data-theme='dark']) .courses-auth-page {
	--courses-bg: #07111f;
	--courses-card: #101a2b;
	--courses-text: #f8fafc;
	--courses-muted: #cbd5e1;
	--courses-soft: #94a3b8;
	--courses-border: rgba(255, 255, 255, 0.1);
	--courses-border-strong: rgba(255, 255, 255, 0.18);
	--courses-primary-soft: rgba(255, 255, 255, 0.06);
	--courses-primary-soft-2: rgba(255, 255, 255, 0.04);
	--courses-shadow-sm: 0 8px 22px rgba(0, 0, 0, 0.22);
	--courses-shadow-md: 0 18px 45px rgba(0, 0, 0, 0.28);
	--courses-shadow-lg: 0 28px 70px rgba(0, 0, 0, 0.34);
}

.courses-navbar {
	position: sticky;
	top: 0;
	z-index: 100;
	border-bottom: 1px solid var(--courses-border);
	background: rgba(255, 255, 255, 0.94);
	backdrop-filter: blur(16px);
}

:global(:root[data-theme='dark']) .courses-navbar {
	background: rgba(7, 17, 31, 0.92);
}

.courses-navbar-inner {
	display: flex;
	align-items: center;
	justify-content: space-between;
	gap: 1rem;
	width: min(1280px, calc(100% - 32px));
	min-height: 72px;
	margin: 0 auto;
}

.courses-brand {
	display: inline-flex;
	align-items: center;
	gap: 0.65rem;
	text-decoration: none;
}

.courses-brand-logo {
	width: 38px;
	height: 38px;
	border-radius: 12px;
	object-fit: contain;
	box-shadow: 0 8px 18px rgba(10, 34, 81, 0.14);
}

.courses-brand-name {
	color: var(--courses-primary);
	font-size: 1.25rem;
	font-weight: 950;
	letter-spacing: -0.04em;
}

:global(:root[data-theme='dark']) .courses-brand-name {
	color: #ffffff;
}

.courses-navbar-actions {
	display: flex;
	align-items: center;
	gap: 0.65rem;
}

.courses-nav-login,
.courses-nav-cta,
.courses-mobile-link,
.courses-mobile-cta {
	text-decoration: none;
}

.courses-nav-login {
	border-radius: 999px;
	padding: 0.65rem 0.95rem;
	color: var(--courses-primary);
	font-size: 0.9rem;
	font-weight: 850;
	transition: 0.18s ease;
}

.courses-nav-login:hover {
	background: var(--courses-primary-soft);
}

.courses-nav-cta {
	border-radius: 999px;
	background: var(--courses-primary);
	padding: 0.7rem 1rem;
	color: #ffffff;
	font-size: 0.9rem;
	font-weight: 900;
	box-shadow: 0 12px 24px rgba(10, 34, 81, 0.18);
	transition: 0.18s ease;
}

.courses-nav-cta:hover {
	background: var(--courses-primary-hover);
	transform: translateY(-1px);
}

.courses-mobile-menu-button {
	display: none;
	align-items: center;
	justify-content: center;
	width: 42px;
	height: 42px;
	border: 1px solid var(--courses-border);
	border-radius: 14px;
	background: var(--courses-card);
	color: var(--courses-primary);
	cursor: pointer;
}

.courses-mobile-menu {
	display: grid;
	gap: 0.7rem;
	width: min(1280px, calc(100% - 32px));
	margin: 0 auto;
	padding: 0 0 1rem;
}

.courses-mobile-link {
	border-radius: 14px;
	padding: 0.9rem;
	color: var(--courses-text);
	font-size: 0.95rem;
	font-weight: 800;
}

.courses-mobile-link:hover {
	background: var(--courses-primary-soft);
	color: var(--courses-primary);
}

.courses-mobile-cta {
	display: flex;
	align-items: center;
	justify-content: center;
	border-radius: 999px;
	background: var(--courses-primary);
	padding: 0.9rem 1rem;
	color: #ffffff;
	font-size: 0.95rem;
	font-weight: 900;
}

.courses-public-shell {
	width: min(1280px, calc(100% - 32px));
	margin: 0 auto;
	padding: 2rem 0 4rem;
}

.courses-hero {
	overflow: hidden;
	border-radius: 30px;
	background: var(--courses-primary);
	color: #ffffff;
	box-shadow: var(--courses-shadow-lg);
}

.courses-hero-content {
	display: grid;
	grid-template-columns: minmax(0, 1fr) 390px;
	gap: 2rem;
	align-items: center;
	padding: 2rem;
}

.courses-eyebrow {
	display: inline-flex;
	align-items: center;
	gap: 0.5rem;
	width: fit-content;
	margin-bottom: 1rem;
	border-radius: 999px;
	border: 1px solid rgba(255, 255, 255, 0.18);
	background: rgba(255, 255, 255, 0.1);
	padding: 0.45rem 0.75rem;
	color: rgba(255, 255, 255, 0.88);
	font-size: 0.72rem;
	font-weight: 950;
	letter-spacing: 0.06em;
	text-transform: uppercase;
}

.courses-hero-title,
.courses-auth-title {
	margin: 0;
	color: #ffffff;
	font-size: clamp(2.1rem, 5vw, 4.2rem);
	font-weight: 950;
	letter-spacing: -0.06em;
	line-height: 1.02;
}

.courses-hero-subtitle,
.courses-auth-subtitle {
	margin: 1rem 0 0;
	max-width: 680px;
	color: rgba(255, 255, 255, 0.78);
	font-size: 1rem;
	line-height: 1.75;
}

.courses-hero-actions {
	display: flex;
	flex-wrap: wrap;
	gap: 0.75rem;
	margin-top: 1.5rem;
}

.courses-btn-light,
.courses-btn-ghost,
.courses-btn-primary,
.courses-btn-outline {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	border-radius: 999px;
	font-size: 0.9rem;
	font-weight: 950;
	text-decoration: none;
	transition: 0.18s ease;
	white-space: nowrap;
}

.courses-btn-light {
	background: #ffffff;
	color: var(--courses-primary);
	padding: 0.85rem 1.15rem;
	box-shadow: 0 14px 28px rgba(0, 0, 0, 0.18);
}

.courses-btn-light:hover {
	background: #f8fbff;
	transform: translateY(-1px);
}

.courses-btn-ghost {
	border: 1px solid rgba(255, 255, 255, 0.28);
	background: rgba(255, 255, 255, 0.08);
	color: #ffffff;
	padding: 0.85rem 1.15rem;
}

.courses-btn-ghost:hover {
	background: rgba(255, 255, 255, 0.14);
	transform: translateY(-1px);
}

.courses-hero-card {
	border: 1px solid rgba(255, 255, 255, 0.18);
	border-radius: 26px;
	background: #ffffff;
	padding: 1.25rem;
	color: var(--courses-text);
	box-shadow: 0 24px 50px rgba(0, 0, 0, 0.22);
}

.courses-hero-card-top {
	display: flex;
	align-items: flex-start;
	justify-content: space-between;
	gap: 1rem;
	margin-bottom: 1rem;
	border-bottom: 1px solid var(--courses-border);
	padding-bottom: 1rem;
}

.courses-hero-card-top p {
	margin: 0;
	color: var(--courses-muted);
	font-size: 0.8rem;
	font-weight: 800;
}

.courses-hero-card-top strong {
	display: block;
	margin-top: 0.25rem;
	color: var(--courses-primary);
	font-size: 1.15rem;
	font-weight: 950;
	letter-spacing: -0.035em;
	line-height: 1.15;
}

.courses-hero-badge {
	display: inline-flex;
	align-items: center;
	gap: 0.35rem;
	border-radius: 999px;
	background: var(--courses-gold-soft);
	padding: 0.45rem 0.6rem;
	color: #8a5b00;
	font-size: 0.75rem;
	font-weight: 950;
	white-space: nowrap;
}

.courses-hero-feature {
	display: grid;
	grid-template-columns: 46px minmax(0, 1fr);
	gap: 0.8rem;
	align-items: center;
	border: 1px solid var(--courses-border);
	border-radius: 18px;
	background: var(--courses-primary-soft-2);
	padding: 0.85rem;
}

.courses-hero-feature + .courses-hero-feature {
	margin-top: 0.75rem;
}

.courses-hero-feature-icon {
	display: flex;
	align-items: center;
	justify-content: center;
	width: 46px;
	height: 46px;
	border-radius: 16px;
	background: var(--courses-primary);
	color: #ffffff;
}

.courses-hero-feature-icon.gold {
	background: var(--courses-gold);
	color: #3b2a00;
}

.courses-hero-feature-icon.green {
	background: var(--courses-green);
	color: #ffffff;
}

.courses-hero-feature strong {
	display: block;
	color: var(--courses-text);
	font-size: 0.9rem;
	font-weight: 950;
}

.courses-hero-feature span {
	display: block;
	margin-top: 0.18rem;
	color: var(--courses-muted);
	font-size: 0.8rem;
	line-height: 1.45;
}

.courses-toolbar {
	position: sticky;
	top: 72px;
	z-index: 20;
	display: grid;
	grid-template-columns: minmax(260px, 420px) minmax(0, 1fr);
	gap: 1rem;
	align-items: center;
	margin: 1.5rem 0;
	border: 1px solid var(--courses-border);
	border-radius: 24px;
	background: rgba(255, 255, 255, 0.92);
	padding: 1rem;
	box-shadow: var(--courses-shadow-sm);
	backdrop-filter: blur(14px);
}

:global(:root[data-theme='dark']) .courses-toolbar {
	background: rgba(16, 26, 43, 0.92);
}

.courses-search-wrap {
	position: relative;
	width: 100%;
}

.courses-search-icon {
	position: absolute;
	left: 1rem;
	top: 50%;
	transform: translateY(-50%);
	color: var(--courses-soft);
	pointer-events: none;
}

.courses-search-input {
	width: 100%;
	border: 1px solid var(--courses-border);
	border-radius: 999px;
	background: var(--courses-card);
	padding: 0.9rem 1rem 0.9rem 2.8rem;
	color: var(--courses-text);
	font-size: 0.95rem;
	font-weight: 700;
	outline: none;
	transition: 0.18s ease;
}

.courses-search-input:focus {
	border-color: var(--courses-primary);
	box-shadow: 0 0 0 4px rgba(10, 34, 81, 0.1);
}

.courses-search-input::placeholder {
	color: var(--courses-soft);
}

.courses-chip-scroll {
	display: flex;
	align-items: center;
	gap: 0.55rem;
	overflow-x: auto;
	padding-bottom: 0.15rem;
	scrollbar-width: none;
}

.courses-chip-scroll::-webkit-scrollbar {
	display: none;
}

.courses-chip {
	flex: 0 0 auto;
	border: 1px solid var(--courses-border);
	border-radius: 999px;
	background: var(--courses-card);
	padding: 0.75rem 1rem;
	color: var(--courses-muted);
	font-size: 0.85rem;
	font-weight: 850;
	cursor: pointer;
	transition: 0.18s ease;
}

.courses-chip:hover {
	border-color: var(--courses-primary);
	background: var(--courses-primary-soft);
	color: var(--courses-primary);
}

.courses-chip.active {
	border-color: var(--courses-primary);
	background: var(--courses-primary);
	color: #ffffff;
}

.courses-grid {
	display: grid;
	grid-template-columns: repeat(4, minmax(0, 1fr));
	gap: 1.25rem;
}

.courses-grid.auth {
	grid-template-columns: repeat(4, minmax(0, 1fr));
}

.courses-card-link {
	display: block;
	min-width: 0;
	text-decoration: none;
	transition: 0.18s ease;
}

.courses-card-link:hover {
	transform: translateY(-3px);
}

.courses-empty {
	display: flex;
	min-height: 320px;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	border: 1px dashed var(--courses-border-strong);
	border-radius: 28px;
	background: var(--courses-card);
	padding: 2rem;
	text-align: center;
	box-shadow: var(--courses-shadow-sm);
}

.courses-empty.auth {
	margin-top: 1rem;
}

.courses-empty-icon {
	display: flex;
	align-items: center;
	justify-content: center;
	width: 78px;
	height: 78px;
	border-radius: 24px;
	background: var(--courses-primary-soft);
	color: var(--courses-primary);
	margin-bottom: 1rem;
}

.courses-empty h3 {
	margin: 0;
	color: var(--courses-text);
	font-size: 1.15rem;
	font-weight: 950;
}

.courses-empty p {
	margin: 0.4rem 0 1.2rem;
	color: var(--courses-muted);
	font-size: 0.95rem;
	line-height: 1.6;
}

.courses-load-more {
	display: flex;
	justify-content: center;
	margin-top: 2rem;
}

.courses-btn-outline {
	border: 1px solid var(--courses-border-strong);
	background: var(--courses-card);
	color: var(--courses-primary);
	padding: 0.85rem 1.2rem;
	cursor: pointer;
}

.courses-btn-outline:hover {
	border-color: var(--courses-primary);
	background: var(--courses-primary-soft);
	transform: translateY(-1px);
}

.courses-btn-primary {
	background: var(--courses-primary);
	color: #ffffff;
	padding: 0.85rem 1.2rem;
	box-shadow: 0 12px 24px rgba(10, 34, 81, 0.18);
}

.courses-btn-primary:hover {
	background: var(--courses-primary-hover);
	transform: translateY(-1px);
}

.courses-register-banner {
	display: flex;
	align-items: center;
	justify-content: space-between;
	gap: 1.25rem;
	margin-top: 3rem;
	border: 1px solid var(--courses-border);
	border-radius: 28px;
	background: var(--courses-card);
	padding: 1.5rem;
	box-shadow: var(--courses-shadow-sm);
}

.courses-register-left {
	display: flex;
	align-items: center;
	gap: 1rem;
}

.courses-register-icon {
	display: flex;
	align-items: center;
	justify-content: center;
	width: 56px;
	height: 56px;
	border-radius: 20px;
	background: var(--courses-gold-soft);
	color: #8a5b00;
	flex: 0 0 auto;
}

.courses-register-banner h4 {
	margin: 0;
	color: var(--courses-text);
	font-size: 1.1rem;
	font-weight: 950;
}

.courses-register-banner p {
	margin: 0.25rem 0 0;
	color: var(--courses-muted);
	font-size: 0.9rem;
	line-height: 1.55;
}

.courses-footer {
	border-top: 1px solid var(--courses-border);
	padding: 2rem 1rem;
	text-align: center;
	color: var(--courses-muted);
	font-size: 0.85rem;
	font-weight: 700;
}

.courses-auth-page {
	min-height: 100vh;
	padding: 1.5rem 1.5rem 3rem;
}

.courses-auth-hero {
	overflow: hidden;
	border-radius: 30px;
	background: var(--courses-primary);
	color: #ffffff;
	box-shadow: var(--courses-shadow-lg);
}

.courses-auth-hero-content {
	display: grid;
	grid-template-columns: minmax(0, 1fr) 160px;
	gap: 1.5rem;
	align-items: center;
	padding: 2rem;
}

.courses-auth-title {
	font-size: clamp(2rem, 4vw, 3.4rem);
}

.courses-auth-stats {
	display: flex;
	flex-wrap: wrap;
	gap: 0.75rem;
	margin-top: 1.35rem;
}

.courses-auth-stat {
	display: inline-flex;
	align-items: center;
	gap: 0.45rem;
	border: 1px solid rgba(255, 255, 255, 0.16);
	border-radius: 999px;
	background: rgba(255, 255, 255, 0.08);
	padding: 0.5rem 0.75rem;
	color: rgba(255, 255, 255, 0.86);
	font-size: 0.8rem;
	font-weight: 850;
}

.courses-auth-stat svg {
	color: var(--courses-gold);
}

.courses-auth-hero-icon {
	display: flex;
	align-items: center;
	justify-content: center;
	width: 132px;
	height: 132px;
	border: 1px solid rgba(255, 255, 255, 0.18);
	border-radius: 32px;
	background: rgba(255, 255, 255, 0.1);
	color: #ffffff;
	transform: rotate(3deg);
}

.courses-auth-filters {
	position: sticky;
	top: 0.75rem;
	z-index: 20;
	display: flex;
	flex-direction: column;
	gap: 1rem;
	margin: 1.5rem 0;
	border: 1px solid var(--courses-border);
	border-radius: 24px;
	background: rgba(255, 255, 255, 0.92);
	padding: 1rem;
	box-shadow: var(--courses-shadow-sm);
	backdrop-filter: blur(14px);
}

:global(:root[data-theme='dark']) .courses-auth-filters {
	background: rgba(16, 26, 43, 0.92);
}

.courses-tabs-wrap {
	max-width: 100%;
	overflow-x: auto;
	padding-bottom: 0.15rem;
	scrollbar-width: none;
}

.courses-tabs-wrap::-webkit-scrollbar {
	display: none;
}

.courses-tabs {
	width: max-content;
}

.courses-auth-filter-grid {
	display: grid;
	grid-template-columns: minmax(220px, 1fr) 220px auto;
	gap: 0.75rem;
	align-items: center;
}

.courses-auth-search {
	position: relative;
	width: 100%;
}

.courses-auth-search-icon {
	position: absolute;
	left: 0.9rem;
	top: 50%;
	z-index: 2;
	transform: translateY(-50%);
	color: var(--courses-soft);
}

.courses-auth-search-control :deep(input) {
	border-radius: 999px;
	background: var(--courses-card);
	padding-left: 2.45rem;
}

.courses-select-wrap :deep(button),
.courses-select-wrap :deep(input) {
	border-radius: 999px;
}

.courses-cert-toggle {
	position: relative;
	display: inline-flex;
	align-items: center;
	justify-content: center;
	gap: 0.55rem;
	min-height: 38px;
	border: 1px solid var(--courses-border);
	border-radius: 999px;
	background: var(--courses-card);
	padding: 0.45rem 0.8rem;
	color: var(--courses-muted);
	font-size: 0.85rem;
	font-weight: 850;
	cursor: pointer;
	transition: 0.18s ease;
	white-space: nowrap;
}

.courses-cert-toggle:hover {
	border-color: var(--courses-primary);
	background: var(--courses-primary-soft);
	color: var(--courses-primary);
}

.courses-cert-toggle input {
	position: absolute;
	opacity: 0;
	pointer-events: none;
}

.courses-cert-box {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	color: var(--courses-soft);
}

.courses-cert-toggle.active {
	border-color: rgba(22, 163, 74, 0.35);
	background: var(--courses-green-soft);
	color: var(--courses-green);
}

.courses-cert-toggle.active .courses-cert-box {
	color: var(--courses-green);
}

.courses-menu-slide-enter-active,
.courses-menu-slide-leave-active {
	transition: all 0.2s ease;
}

.courses-menu-slide-enter-from,
.courses-menu-slide-leave-to {
	opacity: 0;
	transform: translateY(-8px);
}

@media (max-width: 1180px) {
	.courses-hero-content {
		grid-template-columns: 1fr;
	}

	.courses-hero-card {
		max-width: 620px;
	}

	.courses-grid,
	.courses-grid.auth {
		grid-template-columns: repeat(3, minmax(0, 1fr));
	}
}

@media (max-width: 900px) {
	.courses-auth-hero-content {
		grid-template-columns: 1fr;
	}

	.courses-auth-hero-icon {
		display: none;
	}

	.courses-grid,
	.courses-grid.auth {
		grid-template-columns: repeat(2, minmax(0, 1fr));
	}

	.courses-toolbar {
		grid-template-columns: 1fr;
		top: 72px;
	}

	.courses-auth-filter-grid {
		grid-template-columns: 1fr;
	}

	.courses-select-wrap {
		width: 100%;
	}
}

@media (max-width: 768px) {
	.courses-navbar-actions {
		display: none;
	}

	.courses-mobile-menu-button {
		display: flex;
	}
}

@media (max-width: 640px) {
	.courses-navbar-inner,
	.courses-public-shell {
		width: min(100% - 24px, 1280px);
	}

	.courses-public-shell {
		padding-top: 1rem;
	}

	.courses-hero,
	.courses-auth-hero,
	.courses-toolbar,
	.courses-auth-filters,
	.courses-register-banner,
	.courses-empty {
		border-radius: 22px;
	}

	.courses-hero-content,
	.courses-auth-hero-content {
		padding: 1.25rem;
	}

	.courses-hero-title,
	.courses-auth-title {
		font-size: clamp(2rem, 11vw, 2.8rem);
	}

	.courses-hero-subtitle,
	.courses-auth-subtitle {
		font-size: 0.95rem;
	}

	.courses-hero-actions {
		flex-direction: column;
	}

	.courses-btn-light,
	.courses-btn-ghost,
	.courses-btn-primary,
	.courses-btn-outline {
		width: 100%;
	}

	.courses-toolbar,
	.courses-auth-filters {
		position: static;
		padding: 0.85rem;
		margin: 1rem 0;
	}

	.courses-search-input {
		padding-block: 0.85rem;
		font-size: 0.9rem;
	}

	.courses-chip-scroll {
		margin-inline: -0.15rem;
		padding-inline: 0.15rem;
	}

	.courses-chip {
		padding: 0.65rem 0.85rem;
		font-size: 0.8rem;
	}

	.courses-grid,
	.courses-grid.auth {
		grid-template-columns: 1fr;
		gap: 1rem;
	}

	.courses-register-banner {
		align-items: stretch;
		flex-direction: column;
		padding: 1.15rem;
	}

	.courses-register-left {
		align-items: flex-start;
	}

	.courses-auth-page {
		padding: 1rem 1rem 2.5rem;
	}

	.courses-auth-stats {
		flex-direction: column;
		align-items: flex-start;
	}

	.courses-auth-stat {
		width: fit-content;
	}

	.courses-cert-toggle {
		width: 100%;
		justify-content: flex-start;
		padding: 0.75rem 0.9rem;
	}
}

/* Skeletons para Cursos */
.courses-card-skeleton {
	background: var(--courses-card);
	border-radius: 16px;
	overflow: hidden;
	box-shadow: var(--courses-shadow-sm);
}

.courses-card-skeleton .skeleton-img {
	width: 100%;
	height: 180px;
	background: var(--courses-border);
	animation: pulse 1.5s infinite;
}

.courses-card-skeleton .skeleton-content {
	padding: 1.5rem;
}

.courses-card-skeleton .skeleton-line {
	height: 12px;
	border-radius: 4px;
	background: var(--courses-border);
	animation: pulse 1.5s infinite;
	margin-bottom: 8px;
}

.courses-card-skeleton .skeleton-line.title {
	width: 80%;
	height: 18px;
	margin-bottom: 12px;
}

.courses-card-skeleton .skeleton-line.subtitle {
	width: 100%;
}

.courses-card-skeleton .skeleton-line.short {
	width: 40%;
}

@keyframes pulse {
	0% { opacity: 0.6; }
	50% { opacity: 0.3; }
	100% { opacity: 0.6; }
}
</style>