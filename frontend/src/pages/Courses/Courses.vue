<template>
	<!-- ═══════════════════════════════════════════════════════════════
	     PUBLIC VIEW — Full marketing page for unauthenticated users
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
					<a href="#cursos" class="sb-nav-link">Cursos</a>
					<a href="#certificados" class="sb-nav-link">Certificados</a>
					<a href="#beneficios" class="sb-nav-link">Beneficios</a>
					<a href="/login" class="sb-nav-link sb-nav-login">Iniciar sesión</a>
					<a href="/login#signup" class="sb-nav-cta">Registrarse</a>
				</div>
				<!-- Mobile menu toggle -->
				<button class="sb-mobile-menu-btn" @click="mobileMenuOpen = !mobileMenuOpen">
					<Menu v-if="!mobileMenuOpen" class="w-6 h-6" />
					<X v-else class="w-6 h-6" />
				</button>
			</div>
			<!-- Mobile dropdown -->
			<Transition name="sb-menu-slide">
				<div v-if="mobileMenuOpen" class="sb-mobile-menu">
					<a href="#cursos" class="sb-mobile-link" @click="mobileMenuOpen = false">Cursos</a>
					<a href="#certificados" class="sb-mobile-link" @click="mobileMenuOpen = false">Certificados</a>
					<a href="#beneficios" class="sb-mobile-link" @click="mobileMenuOpen = false">Beneficios</a>
					<a href="/login" class="sb-mobile-link">Iniciar sesión</a>
					<a href="/login#signup" class="sb-mobile-cta">Registrarse</a>
				</div>
			</Transition>
		</nav>

		<!-- Hero Section -->
		<section class="sb-hero">
			<div class="sb-hero-bg-1"></div>
			<div class="sb-hero-bg-2"></div>
			<div class="sb-hero-content">
				<span class="sb-hero-badge">🎓 Plataforma de aprendizaje profesional</span>
				<h1 class="sb-hero-title">
					Aprende habilidades reales.<br/>
					<span class="sb-hero-gradient">Obtén certificados verificables.</span>
				</h1>
				<p class="sb-hero-subtitle">
					Explora cursos cortos, prácticos y diseñados para ayudarte a crecer profesionalmente, mejorar tu CV y avanzar a tu ritmo.
				</p>
				<div class="sb-hero-actions">
					<a href="#cursos" class="sb-btn-primary">Explorar cursos</a>
					<a href="#certificados" class="sb-btn-secondary">Ver certificados</a>
				</div>
				<!-- Feature pills -->
				<div class="sb-hero-pills">
					<div class="sb-pill"><GraduationCap class="w-4 h-4" /> Certificado incluido</div>
					<div class="sb-pill"><Sparkles class="w-4 h-4" /> TutorIA disponible</div>
					<div class="sb-pill"><Clock class="w-4 h-4" /> Curso corto</div>
					<div class="sb-pill"><FileCheck class="w-4 h-4" /> Proyecto final</div>
				</div>
			</div>
		</section>

		<!-- Category Chips -->
		<section class="sb-section" id="cursos">
			<div class="sb-section-inner">
				<h2 class="sb-section-title">Explora por categoría</h2>
				<div class="sb-chips">
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
			</div>
		</section>

		<!-- Search + Courses Grid -->
		<section class="sb-section sb-section-light">
			<div class="sb-section-inner">
				<!-- Search bar -->
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
					<BookOpen class="w-12 h-12 text-gray-300 mb-3" />
					<p class="text-gray-500">No se encontraron cursos.</p>
				</div>
				<div
					v-if="!courses.list.loading && courses.hasNextPage"
					class="flex justify-center mt-8"
				>
					<button class="sb-btn-outline" @click="courses.next()">
						{{ __('Cargar más cursos') }}
					</button>
				</div>
			</div>
		</section>

		<!-- Benefits Section -->
		<section class="sb-section" id="beneficios">
			<div class="sb-section-inner">
				<h2 class="sb-section-title">Todo lo que necesitas para aprender mejor</h2>
				<p class="sb-section-desc">Nuestra plataforma está diseñada para que aprendas de manera eficiente, práctica y motivadora.</p>
				<div class="sb-benefits-grid">
					<div class="sb-benefit-card">
						<div class="sb-benefit-icon sb-icon-blue"><BookOpen class="w-6 h-6" /></div>
						<h3>Cursos cortos y prácticos</h3>
						<p>Aprende lo esencial en módulos concisos, sin relleno innecesario.</p>
					</div>
					<div class="sb-benefit-card">
						<div class="sb-benefit-icon sb-icon-gold"><Award class="w-6 h-6" /></div>
						<h3>Certificados verificables</h3>
						<p>Cada certificado incluye un código QR y enlace único de validación.</p>
					</div>
					<div class="sb-benefit-card">
						<div class="sb-benefit-icon sb-icon-purple"><Sparkles class="w-6 h-6" /></div>
						<h3>TutorIA para resolver dudas</h3>
						<p>Un asistente con IA disponible 24/7 para guiarte en cada lección.</p>
					</div>
					<div class="sb-benefit-card">
						<div class="sb-benefit-icon sb-icon-green"><FileCheck class="w-6 h-6" /></div>
						<h3>Tareas, quizzes y proyectos</h3>
						<p>Pon en práctica lo aprendido con actividades evaluadas por IA.</p>
					</div>
					<div class="sb-benefit-card">
						<div class="sb-benefit-icon sb-icon-teal"><Clock class="w-6 h-6" /></div>
						<h3>Aprende a tu ritmo</h3>
						<p>Sin horarios fijos. Avanza cuando quieras, desde donde quieras.</p>
					</div>
					<div class="sb-benefit-card">
						<div class="sb-benefit-icon sb-icon-red"><Target class="w-6 h-6" /></div>
						<h3>Enfocado en habilidades reales</h3>
						<p>Contenido diseñado para el mundo real, no solo teoría.</p>
					</div>
				</div>
			</div>
		</section>

		<!-- Certificates Section -->
		<section class="sb-section sb-section-dark" id="certificados">
			<div class="sb-section-inner sb-cert-content">
				<div class="sb-cert-text">
					<h2 class="sb-section-title sb-title-white">Demuestra lo que sabes</h2>
					<p class="sb-cert-desc">
						Completa cursos, supera actividades y obtén certificados digitales que puedes compartir en tu CV, LinkedIn o portafolio. Cada certificado es verificable con un código QR único.
					</p>
					<a href="/login" class="sb-btn-gold">Obtener mi primer certificado</a>
				</div>
				<div class="sb-cert-visual">
					<div class="sb-cert-card">
						<Award class="w-16 h-16 text-amber-400" />
						<div class="sb-cert-card-text">
							<span class="sb-cert-label">Certificado Digital</span>
							<span class="sb-cert-sublabel">Verificable • Compartible • Profesional</span>
						</div>
					</div>
				</div>
			</div>
		</section>

		<!-- Final CTA -->
		<section class="sb-section sb-cta-section">
			<div class="sb-section-inner" style="text-align: center;">
				<h2 class="sb-cta-title">Empieza hoy con una habilidad nueva.</h2>
				<p class="sb-cta-desc">Únete a nuestra comunidad de estudiantes y transforma tu carrera profesional.</p>
				<a href="/login" class="sb-btn-primary sb-btn-lg">Explorar cursos</a>
			</div>
		</section>

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
/* ─── Design Tokens ─── */
:root {
	--sb-navy: #061B49;
	--sb-blue: #007BFF;
	--sb-gold: #F5B301;
	--sb-bg: #F5F7FB;
	--sb-text: #1a1a2e;
	--sb-text-muted: #64748b;
	--sb-radius: 12px;
}

/* ─── Public Page Shell ─── */
.sb-public-page {
	font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
	color: var(--sb-text);
	background: var(--sb-bg);
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
	color: var(--sb-navy);
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
	color: var(--sb-text-muted);
	text-decoration: none;
	border-radius: 8px;
	transition: all 0.2s;
}
.sb-nav-link:hover {
	color: var(--sb-navy);
	background: rgba(0, 0, 0, 0.04);
}
.sb-nav-login {
	font-weight: 600;
	color: var(--sb-navy);
}
.sb-nav-cta {
	padding: 8px 20px;
	font-size: 14px;
	font-weight: 600;
	color: white;
	background: var(--sb-blue);
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
	color: var(--sb-navy);
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
	color: var(--sb-text-muted);
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
	background: var(--sb-blue);
	border-radius: 8px;
	text-decoration: none;
}
@media (max-width: 768px) {
	.sb-navbar-links { display: none; }
	.sb-mobile-menu-btn { display: block; }
	.sb-mobile-menu { display: flex; }
}

/* ─── Hero ─── */
.sb-hero {
	position: relative;
	overflow: hidden;
	padding: 80px 24px 100px;
	text-align: center;
	background: white;
}
.sb-hero-bg-1 {
	position: absolute;
	top: -120px;
	right: -80px;
	width: 500px;
	height: 500px;
	border-radius: 50%;
	background: radial-gradient(circle, rgba(0, 123, 255, 0.06) 0%, transparent 70%);
}
.sb-hero-bg-2 {
	position: absolute;
	bottom: -120px;
	left: -80px;
	width: 400px;
	height: 400px;
	border-radius: 50%;
	background: radial-gradient(circle, rgba(245, 179, 1, 0.06) 0%, transparent 70%);
}
.sb-hero-content {
	position: relative;
	z-index: 1;
	max-width: 800px;
	margin: 0 auto;
}
.sb-hero-badge {
	display: inline-block;
	font-size: 13px;
	font-weight: 600;
	color: var(--sb-blue);
	background: rgba(0, 123, 255, 0.08);
	border: 1px solid rgba(0, 123, 255, 0.15);
	border-radius: 100px;
	padding: 6px 18px;
	margin-bottom: 28px;
}
.sb-hero-title {
	font-size: clamp(32px, 5vw, 56px);
	font-weight: 800;
	color: var(--sb-navy);
	line-height: 1.15;
	letter-spacing: -0.03em;
	margin-bottom: 24px;
}
.sb-hero-gradient {
	background: linear-gradient(135deg, var(--sb-blue), #6366f1);
	-webkit-background-clip: text;
	-webkit-text-fill-color: transparent;
	background-clip: text;
}
.sb-hero-subtitle {
	font-size: 18px;
	line-height: 1.7;
	color: var(--sb-text-muted);
	max-width: 600px;
	margin: 0 auto 36px;
}
.sb-hero-actions {
	display: flex;
	align-items: center;
	justify-content: center;
	gap: 12px;
	flex-wrap: wrap;
	margin-bottom: 48px;
}
.sb-hero-pills {
	display: flex;
	align-items: center;
	justify-content: center;
	gap: 12px;
	flex-wrap: wrap;
}
.sb-pill {
	display: flex;
	align-items: center;
	gap: 6px;
	font-size: 13px;
	font-weight: 500;
	color: var(--sb-text-muted);
	background: var(--sb-bg);
	border: 1px solid rgba(0, 0, 0, 0.06);
	border-radius: 100px;
	padding: 8px 16px;
}

/* ─── Buttons ─── */
.sb-btn-primary {
	display: inline-block;
	padding: 14px 32px;
	font-size: 15px;
	font-weight: 600;
	color: white;
	background: var(--sb-blue);
	border-radius: 10px;
	text-decoration: none;
	transition: all 0.25s;
	border: none;
	cursor: pointer;
}
.sb-btn-primary:hover {
	background: #0069d9;
	transform: translateY(-2px);
	box-shadow: 0 8px 24px rgba(0, 123, 255, 0.25);
}
.sb-btn-lg {
	padding: 18px 40px;
	font-size: 17px;
}
.sb-btn-secondary {
	display: inline-block;
	padding: 14px 32px;
	font-size: 15px;
	font-weight: 600;
	color: var(--sb-navy);
	background: white;
	border: 1.5px solid rgba(0, 0, 0, 0.1);
	border-radius: 10px;
	text-decoration: none;
	transition: all 0.25s;
}
.sb-btn-secondary:hover {
	border-color: var(--sb-blue);
	color: var(--sb-blue);
	transform: translateY(-2px);
}
.sb-btn-outline {
	padding: 12px 28px;
	font-size: 14px;
	font-weight: 600;
	color: var(--sb-blue);
	background: white;
	border: 1.5px solid var(--sb-blue);
	border-radius: 10px;
	cursor: pointer;
	transition: all 0.2s;
}
.sb-btn-outline:hover {
	background: var(--sb-blue);
	color: white;
}
.sb-btn-gold {
	display: inline-block;
	padding: 14px 32px;
	font-size: 15px;
	font-weight: 600;
	color: var(--sb-navy);
	background: var(--sb-gold);
	border-radius: 10px;
	text-decoration: none;
	transition: all 0.25s;
}
.sb-btn-gold:hover {
	transform: translateY(-2px);
	box-shadow: 0 8px 24px rgba(245, 179, 1, 0.3);
}

/* ─── Sections ─── */
.sb-section {
	padding: 80px 24px;
}
.sb-section-light {
	background: white;
}
.sb-section-dark {
	background: var(--sb-navy);
}
.sb-section-inner {
	max-width: 1200px;
	margin: 0 auto;
}
.sb-section-title {
	font-size: clamp(24px, 3vw, 36px);
	font-weight: 800;
	color: var(--sb-navy);
	text-align: center;
	letter-spacing: -0.02em;
	margin-bottom: 12px;
}
.sb-title-white { color: white; }
.sb-section-desc {
	font-size: 16px;
	color: var(--sb-text-muted);
	text-align: center;
	max-width: 560px;
	margin: 0 auto 48px;
	line-height: 1.7;
}

/* ─── Category Chips ─── */
.sb-chips {
	display: flex;
	align-items: center;
	justify-content: center;
	gap: 10px;
	flex-wrap: wrap;
	margin-top: 24px;
}
.sb-chip {
	padding: 10px 22px;
	font-size: 14px;
	font-weight: 500;
	color: var(--sb-text-muted);
	background: white;
	border: 1.5px solid rgba(0, 0, 0, 0.08);
	border-radius: 100px;
	cursor: pointer;
	transition: all 0.2s;
}
.sb-chip:hover {
	border-color: var(--sb-blue);
	color: var(--sb-blue);
}
.sb-chip-active {
	background: var(--sb-blue);
	color: white !important;
	border-color: var(--sb-blue) !important;
}

/* ─── Search Bar ─── */
.sb-search-bar {
	position: relative;
	max-width: 640px;
	margin: 0 auto;
}
.sb-search-icon {
	position: absolute;
	left: 18px;
	top: 50%;
	transform: translateY(-50%);
	width: 20px;
	height: 20px;
	color: var(--sb-text-muted);
}
.sb-search-input {
	width: 100%;
	padding: 16px 20px 16px 52px;
	font-size: 16px;
	color: var(--sb-text);
	background: var(--sb-bg);
	border: 1.5px solid rgba(0, 0, 0, 0.08);
	border-radius: 14px;
	outline: none;
	transition: all 0.2s;
}
.sb-search-input:focus {
	border-color: var(--sb-blue);
	box-shadow: 0 0 0 4px rgba(0, 123, 255, 0.1);
}
.sb-search-input::placeholder {
	color: #94a3b8;
}

/* ─── Empty State ─── */
.sb-empty {
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	padding: 64px 0;
}

/* ─── Benefits Grid ─── */
.sb-benefits-grid {
	display: grid;
	grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
	gap: 24px;
}
.sb-benefit-card {
	background: white;
	border: 1px solid rgba(0, 0, 0, 0.06);
	border-radius: var(--sb-radius);
	padding: 32px 28px;
	transition: all 0.25s;
}
.sb-benefit-card:hover {
	transform: translateY(-4px);
	box-shadow: 0 12px 32px rgba(0, 0, 0, 0.08);
}
.sb-benefit-card h3 {
	font-size: 17px;
	font-weight: 700;
	color: var(--sb-navy);
	margin: 16px 0 8px;
}
.sb-benefit-card p {
	font-size: 14px;
	color: var(--sb-text-muted);
	line-height: 1.6;
	margin: 0;
}
.sb-benefit-icon {
	width: 48px;
	height: 48px;
	border-radius: 12px;
	display: flex;
	align-items: center;
	justify-content: center;
}
.sb-icon-blue { background: rgba(0, 123, 255, 0.1); color: var(--sb-blue); }
.sb-icon-gold { background: rgba(245, 179, 1, 0.12); color: #d4980b; }
.sb-icon-purple { background: rgba(99, 102, 241, 0.1); color: #6366f1; }
.sb-icon-green { background: rgba(16, 185, 129, 0.1); color: #10b981; }
.sb-icon-teal { background: rgba(20, 184, 166, 0.1); color: #14b8a6; }
.sb-icon-red { background: rgba(239, 68, 68, 0.1); color: #ef4444; }

/* ─── Certificates Section ─── */
.sb-cert-content {
	display: flex;
	align-items: center;
	gap: 64px;
	flex-wrap: wrap;
}
.sb-cert-text {
	flex: 1;
	min-width: 300px;
}
.sb-cert-text .sb-section-title {
	text-align: left;
}
.sb-cert-desc {
	font-size: 16px;
	color: rgba(255, 255, 255, 0.75);
	line-height: 1.8;
	margin: 16px 0 32px;
}
.sb-cert-visual {
	flex: 1;
	min-width: 300px;
	display: flex;
	justify-content: center;
}
.sb-cert-card {
	background: rgba(255, 255, 255, 0.08);
	backdrop-filter: blur(12px);
	border: 1px solid rgba(255, 255, 255, 0.12);
	border-radius: 20px;
	padding: 48px;
	display: flex;
	flex-direction: column;
	align-items: center;
	gap: 20px;
	text-align: center;
	transition: all 0.3s;
}
.sb-cert-card:hover {
	transform: translateY(-4px);
	background: rgba(255, 255, 255, 0.12);
}
.sb-cert-card-text {
	display: flex;
	flex-direction: column;
	gap: 4px;
}
.sb-cert-label {
	font-size: 20px;
	font-weight: 700;
	color: white;
}
.sb-cert-sublabel {
	font-size: 13px;
	color: rgba(255, 255, 255, 0.5);
}

/* ─── CTA Section ─── */
.sb-cta-section {
	background: white;
}
.sb-cta-title {
	font-size: clamp(28px, 4vw, 42px);
	font-weight: 800;
	color: var(--sb-navy);
	letter-spacing: -0.03em;
	margin-bottom: 16px;
}
.sb-cta-desc {
	font-size: 17px;
	color: var(--sb-text-muted);
	margin-bottom: 36px;
	line-height: 1.7;
}

/* ─── Footer ─── */
.sb-footer {
	text-align: center;
	padding: 32px 24px;
	font-size: 13px;
	color: var(--sb-text-muted);
	border-top: 1px solid rgba(0, 0, 0, 0.06);
	background: white;
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
